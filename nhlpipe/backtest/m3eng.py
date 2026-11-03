"""M3 game model: add a late-game pulled-goalie phase and test it on 2023-25 results.

python -m nhlpipe.backtest.m3eng          (offline: data/shots2 caches; no odds needed)

Current M3: independent Poisson regulation goals, tie -> OT/SO (+1 to the winner).
v2 adds, after regulation is simulated, the last-minutes goalie pull:
  one-goal game : leader scores into the empty net (q1e) or trailer ties it (q1t)
  two-goal game : leader scores into the empty net (q2e) or trailer cuts it to one (q2c)
and scales regulation scoring by s so the mean total still matches.
Fit (q1e, q1t, q2e, q2c, s) on 2023-24 games (regulation margin shares, ENG per game,
mean total); judge on 2024-25 by log loss of the puck line, totals and OT, old vs new.
Team strengths are M3's own point-in-time MoneyPuck inputs (no goalie term: no
goalie logs cached for those seasons).
"""
import itertools
from datetime import date, timedelta

import numpy as np
import pandas as pd

from .. import models
from ..shots2 import pull
from .features import Season

N = 6000
OUT = pull.ROOT.parent / "backtest" / "m3eng"


def games_frame(season: str) -> pd.DataFrame:
    st = pull.load_stats(season)
    for c in ("goals", "otGoals", "emptyNetGoals"):
        st[c] = pd.to_numeric(st[c], errors="coerce").fillna(0)
    t = st.groupby(["gameId", "teamAbbrev"])[["goals", "otGoals", "emptyNetGoals"]].sum().reset_index()
    sch = pd.DataFrame(pull.schedule(season))
    g = sch.merge(t.rename(columns={"teamAbbrev": "home", "goals": "hg", "otGoals": "hot", "emptyNetGoals": "heng"}),
                  left_on=["game_id", "home"], right_on=["gameId", "home"]) \
        .merge(t.rename(columns={"teamAbbrev": "away", "goals": "ag", "otGoals": "aot", "emptyNetGoals": "aeng"}),
               left_on=["game_id", "away"], right_on=["gameId", "away"])
    g["hr"], g["ar"] = g["hg"] - g["hot"], g["ag"] - g["aot"]  # regulation goals (shootout goals never in 'goals')
    g["tie"] = (g["hr"] == g["ar"]).astype(int)
    g["total"] = g["hr"] + g["ar"] + g["tie"]  # OT goal or shootout winner counts as one goal (book rules)
    g["eng"] = g["heng"] + g["aeng"]
    return g


def lambdas(season: str, g: pd.DataFrame) -> pd.DataFrame:
    mp = pd.read_csv(pull.ROOT / "mp_teams.csv.gz")
    mp = mp[mp["season"] == int(season[:4])]
    S = Season({}, mp, pd.DataFrame({"playerId": ["0"], "gameDate": [0], "xGoals": [0.0], "goals": [0]}))
    rows = []
    first = date.fromisoformat(g["date"].min()) + timedelta(days=10)  # need some games of stats
    for d, grp in g.groupby("date"):
        day = date.fromisoformat(d)
        if day < first:
            continue
        games = [{"game_id": r.game_id, "start_utc": r.start_utc, "home": r.home, "away": r.away,
                  "home_name": r.home, "away_name": r.away} for r in grp.itertuples()]
        slate, mp_t, _ = S.slate(day, games)
        if mp_t.empty or mp_t[mp_t["situation"] == "all"]["games_played"].min() < 3:
            continue
        lp = models.league_params(mp_t)
        for r in slate.to_dict("records"):
            lh, la = models.team_lambdas(pd.Series(r), lp)
            rows.append({"game_id": r["game_id"], "lh": lh, "la": la})
    return g.merge(pd.DataFrame(rows), on="game_id")


def sim(lh, la, prm, rng):
    q1e, q1t, q2e, q2c, s = prm
    h = rng.poisson(lh * s, N)
    a = rng.poisson(la * s, N)
    m = h - a
    u = rng.random(N)
    lead_h = m > 0
    one, two = np.abs(m) == 1, np.abs(m) == 2
    eng1, tie1 = one & (u < q1e), one & (u >= q1e) & (u < q1e + q1t)
    eng2, cut2 = two & (u < q2e), two & (u >= q2e) & (u < q2e + q2c)
    h = h + ((eng1 | eng2) & lead_h) + ((tie1 | cut2) & ~lead_h)
    a = a + ((eng1 | eng2) & ~lead_h) + ((tie1 | cut2) & lead_h)
    eng = (eng1 | eng2).astype(int)
    tie = h == a
    ot_home = rng.random(N) < models.OT_HOME_WIN
    return h, a, h + (tie & ot_home), a + (tie & ~ot_home), eng


OLD = (0.0, 0.0, 0.0, 0.0, 1.0)


def probs(g: pd.DataFrame, prm) -> pd.DataFrame:
    rng = np.random.default_rng(7)
    out = []
    for r in g.itertuples():
        h, a, hf, af, eng = sim(r.lh, r.la, prm, rng)
        m = h - a
        out.append({"game_id": r.game_id, "p_tie": (m == 0).mean(), "p_m1": (np.abs(m) == 1).mean(),
                    "p_m2": (np.abs(m) == 2).mean(), "p_home_pl": (hf - af >= 2).mean(), "p_away_pl": (af - hf >= 2).mean(),
                    "p_o55": (hf + af > 5.5).mean(), "p_o65": (hf + af > 6.5).mean(), "p_eng": eng.mean(),
                    "p_tot": (hf + af).mean()})
    return g.merge(pd.DataFrame(out), on="game_id")


def _ll(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def fit(g: pd.DataFrame):
    m = (g["hr"] - g["ar"]).abs()
    target = np.array([g["tie"].mean(), (m == 1).mean(), (m == 2).mean(), g["eng"].mean(), g["total"].mean()])
    sub = g.sample(min(len(g), 300), random_state=1)
    best, best_err = None, 1e9
    for q1e, q1t, q2e, q2c, s in itertools.product([0.25, 0.32, 0.40, 0.48], [0.10, 0.14, 0.18], [0.20, 0.30, 0.40],
                                                   [0.04, 0.08, 0.12], [0.90, 0.93, 0.96]):
        prm = (q1e, q1t, q2e, q2c, s)
        p = probs(sub, prm)
        pred = np.array([p["p_tie"].mean(), p["p_m1"].mean(), p["p_m2"].mean(), p["p_eng"].mean(), p["p_tot"].mean()])
        err = float(np.sum(((pred - target) / np.array([0.02, 0.02, 0.02, 0.05, 0.1])) ** 2))
        if err < best_err:
            best, best_err = prm, err
    return best, target


def run() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tr = lambdas("20232024", games_frame("20232024"))
    va = lambdas("20242025", games_frame("20242025"))
    prm, target = fit(tr)
    md = ["# M3 late-game goalie pull (empty-net) test", "",
          f"Fit on 2023-24 ({len(tr)} games): q1e={prm[0]}, q1t={prm[1]}, q2e={prm[2]}, q2c={prm[3]}, scoring scale s={prm[4]}", "",
          "| Season | Model | Reg. tie | 1-goal | 2-goal | ENG / game | Mean total |", "|---|---|--:|--:|--:|--:|--:|"]
    res = {}
    for name, g in (("2023-24 (fit)", tr), ("2024-25 (test)", va)):
        m = (g["hr"] - g["ar"]).abs()
        md.append(f"| {name} | actual | {g['tie'].mean():.3f} | {(m == 1).mean():.3f} | {(m == 2).mean():.3f} | {g['eng'].mean():.3f} | {g['total'].mean():.2f} |")
        for lab, p_ in (("M3 now", OLD), ("M3 + goalie pull", prm)):
            p = probs(g, p_)
            res[(name, lab)] = p
            md.append(f"| {name} | {lab} | {p['p_tie'].mean():.3f} | {p['p_m1'].mean():.3f} | {p['p_m2'].mean():.3f} | {p['p_eng'].mean():.3f} | {p['p_tot'].mean():.2f} |")
    md += ["", "Out-of-sample log loss on 2024-25 (lower is better):", "", "| Market | M3 now | M3 + goalie pull | Actual rate |", "|---|--:|--:|--:|"]
    va_old, va_new = res[("2024-25 (test)", "M3 now")], res[("2024-25 (test)", "M3 + goalie pull")]
    y = {"Home -1.5": (va_old["hr"] + va_old["tie"] * 0 - va_old["ar"] >= 2).astype(int),
         "Away -1.5": (va_old["ar"] - va_old["hr"] >= 2).astype(int),
         "Over 5.5": (va_old["total"] > 5.5).astype(int), "Over 6.5": (va_old["total"] > 6.5).astype(int),
         "Goes to OT": va_old["tie"]}
    cols = {"Home -1.5": "p_home_pl", "Away -1.5": "p_away_pl", "Over 5.5": "p_o55", "Over 6.5": "p_o65", "Goes to OT": "p_tie"}
    for k, yy in y.items():
        md.append(f"| {k} | {_ll(va_old[cols[k]], yy):.4f} | {_ll(va_new[cols[k]], yy):.4f} | {yy.mean():.3f} |")
    md += ["", "Note: puck-line outcomes use regulation goals; OT/shootout games are one-goal games, so -1.5 always loses there."]
    (OUT / "report.md").write_text("\n".join(md) + "\n")
    (OUT / "params.txt").write_text(",".join(map(str, prm)) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    run()


def market_test() -> None:
    """2025-26: M3 (now vs + goalie pull) against Pinnacle's 1:50 PM puck line / total, all games (cached odds)."""
    from .. import fair
    from . import nhldata, mpdata, oddshist
    from . import pipeline as P
    prm = tuple(float(x) for x in (OUT / "params.txt").read_text().strip().split(","))
    recs = nhldata.load_range(nhldata.SEASON_START, nhldata.SEASON_END)
    S = Season(recs, pd.read_csv(mpdata.ROOT / f"teams_{mpdata.SEASON}.csv.gz"),
               pd.read_csv(mpdata.ROOT / f"goalies_{mpdata.SEASON}.csv.gz"))
    rows = []
    for ds, rec in sorted(recs.items()):
        d = date.fromisoformat(ds)
        if d < date(2025, 10, 15):
            continue
        t = P.pick_dt(d)
        sched = [g for g in rec["games"] if P._utc(g["start_utc"]) > t and g["state"] in ("OFF", "FINAL")]
        if not sched:
            continue
        import gzip, json
        cp = oddshist._path("featured", P._iso(t), f"/historical/sports/{oddshist.SPORT}/odds|" + json.dumps(
            {"bookmakers": oddshist.BOOKS, "date": P._iso(t), "markets": ",".join(oddshist.FEATURED)}, sort_keys=True))
        if not cp.exists():
            continue
        od = P.odds_frame([json.loads(gzip.decompress(cp.read_bytes()))], P.TMAP)
        dv = fair.devig(od)
        pin = dv[dv["book"] == "pinnacle"]
        slate, mp_t, _ = S.slate(d, sched)
        if mp_t.empty or mp_t[mp_t["situation"] == "all"]["games_played"].min() < 3:
            continue
        lp = models.league_params(mp_t)
        for g, srow in zip(sched, slate.to_dict("records")):
            lh, la = models.team_lambdas(pd.Series(srow), lp)
            hr = g["home_score"] - (1 if g["last_period"] in ("OT", "SO") and g["home_score"] > g["away_score"] else 0)
            ar = g["away_score"] - (1 if g["last_period"] in ("OT", "SO") and g["away_score"] > g["home_score"] else 0)
            sims = {}
            for lab, p_ in (("old", OLD), ("new", prm)):
                h, a, hf, af, _ = sim(lh, la, p_, np.random.default_rng(g["game_id"] % 100000))
                sims[lab] = (hf, af)
            pg = pin[(pin["home"] == g["home"]) & (pin["away"] == g["away"])]
            for r in pg[pg["market"] == "spreads"].to_dict("records"):
                if r["point"] != -1.5:
                    continue
                team_home = P.norm(r["outcome"]) == P.norm(r["home_name"])
                y = int((hr - ar if team_home else ar - hr) >= 2)
                rec_ = {"market": "fav -1.5" , "pin": r["fair"], "y": y}
                for lab, (hf, af) in sims.items():
                    rec_[lab] = float(((hf - af) if team_home else (af - hf)).__ge__(2).mean())
                rows.append(rec_)
            for r in pg[(pg["market"] == "totals") & (pg["outcome"].str.lower() == "over")].to_dict("records"):
                tot = g["home_score"] + g["away_score"]
                if tot == r["point"]:
                    continue
                rec_ = {"market": f"over {r['point']}", "pin": r["fair"], "y": int(tot > r["point"])}
                for lab, (hf, af) in sims.items():
                    rec_[lab] = float(((hf + af) > r["point"]).mean())
                rows.append(rec_)
    df = pd.DataFrame(rows)
    df["mk"] = np.where(df["market"].str.startswith("over"), "totals", "puck line -1.5")
    md = ["", "## 2025-26 vs Pinnacle at 1:50 PM (all games; this season was already looked at, so treat as a check, not proof)", "",
          "| Market | n | M3 now | M3 + goalie pull | Pinnacle | Avg P: now / new / Pinnacle / actual |", "|---|--:|--:|--:|--:|--:|"]
    for mk, g in df.groupby("mk"):
        md.append(f"| {mk} | {len(g)} | {_ll(g['old'], g['y']):.4f} | {_ll(g['new'], g['y']):.4f} | {_ll(g['pin'], g['y']):.4f} | "
                  f"{g['old'].mean():.3f} / {g['new'].mean():.3f} / {g['pin'].mean():.3f} / {g['y'].mean():.3f} |")
    from sklearn.linear_model import LogisticRegression
    for mk, g in df.groupby("mk"):
        for lab in ("old", "new"):
            X = np.column_stack([np.log(g["pin"] / (1 - g["pin"])), np.log(np.clip(g[lab], 1e-3, 1 - 1e-3) / (1 - np.clip(g[lab], 1e-3, 1 - 1e-3)))])
            lr = LogisticRegression(C=1e6, max_iter=1000).fit(X, g["y"])
            md.append(f"- {mk}, {lab}: weight on Pinnacle {lr.coef_[0][0]:.2f}, on M3 {lr.coef_[0][1]:.2f} (M3 adds information only if clearly > 0)")
    with open(OUT / "report.md", "a") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md))


def blend_fit() -> None:
    """Fit models.BLEND on 2025-26: every Pinnacle ml / -1.5 / main total at 1:50 PM, live M3 code."""
    import gzip, json
    from sklearn.linear_model import LogisticRegression
    from .. import fair
    from . import nhldata, mpdata, oddshist
    from . import pipeline as P
    recs = nhldata.load_range(nhldata.SEASON_START, nhldata.SEASON_END)
    S = Season(recs, pd.read_csv(mpdata.ROOT / f"teams_{mpdata.SEASON}.csv.gz"),
               pd.read_csv(mpdata.ROOT / f"goalies_{mpdata.SEASON}.csv.gz"))
    rows = []
    for ds, rec in sorted(recs.items()):
        d = date.fromisoformat(ds)
        if d < date(2025, 10, 15):
            continue
        t = P.pick_dt(d)
        sched = [g for g in rec["games"] if P._utc(g["start_utc"]) > t and g["state"] in ("OFF", "FINAL")]
        cp = oddshist._path("featured", P._iso(t), f"/historical/sports/{oddshist.SPORT}/odds|" + json.dumps(
            {"bookmakers": oddshist.BOOKS, "date": P._iso(t), "markets": ",".join(oddshist.FEATURED)}, sort_keys=True))
        if not sched or not cp.exists():
            continue
        od = P.odds_frame([json.loads(gzip.decompress(cp.read_bytes()))], P.TMAP)
        table = fair.lookup_table(fair.devig(od[od["book"] == "pinnacle"]))
        slate, mp_t, _ = S.slate(d, sched)
        if mp_t.empty or mp_t[mp_t["situation"] == "all"]["games_played"].min() < 3:
            continue
        lp = models.league_params(mp_t)
        for i, (g, srow) in enumerate(zip(sched, slate.to_dict("records"))):
            lh, la = models.team_lambdas(pd.Series(srow), lp)
            sm = models.simulate(lh, la, seed=i)
            gk = f"{g['away']}@{g['home']}"
            hs, as_ = g["home_score"], g["away_score"]
            cands = [({"market": "ml", "team": g["home"], "side": "yes", "line": None, "game_key": gk}, int(hs > as_))]
            for team, opp_s, own_s in ((g["home"], as_, hs), (g["away"], hs, as_)):
                cands.append(({"market": "spread", "team": team, "side": "yes", "line": 1.5, "game_key": gk}, int(own_s - opp_s >= 2)))
            for (k_gk, k_m, k_t, k_l) in table:
                if k_gk == gk and k_m == "total" and k_l is not None and not float(k_l).is_integer():
                    cands.append(({"market": "total", "team": None, "side": "yes", "line": k_l, "game_key": gk}, int(hs + as_ > k_l)))
            for c, y in cands:
                fp, src = fair.fair_prob(c, table)
                mp_ = models.game_prob(c, sm, g["home"], g["away"])
                if fp is None or mp_ is None:
                    continue
                rows.append({"date": ds, "market": c["market"], "pin": fp, "m3": mp_, "y": y})
    df = pd.DataFrame(rows)
    lg = lambda x: np.log(np.clip(x, 1e-4, 1 - 1e-4) / (1 - np.clip(x, 1e-4, 1 - 1e-4)))  # noqa: E731
    out, md = {}, ["", "## Blend weights (2025-26 Pinnacle lines at 1:50 PM, M3 with goalie pull)", "",
                   "| Market | n | weight Pinnacle | weight M3 | log loss Pinnacle | M3 | blend (in-sample) |", "|---|--:|--:|--:|--:|--:|--:|"]
    for mk, g in df.groupby("market"):
        X = np.column_stack([lg(g["pin"]), lg(g["m3"])])
        lr = LogisticRegression(C=1e6, fit_intercept=False, max_iter=1000).fit(X, g["y"])
        a, b = float(lr.coef_[0][0]), float(lr.coef_[0][1])
        pb = 1 / (1 + np.exp(-(a * X[:, 0] + b * X[:, 1])))
        out[mk] = {"a": a, "b": b, "n": int(len(g))}
        md.append(f"| {mk} | {len(g)} | {a:.3f} | {b:.3f} | {_ll(g['pin'], g['y']):.4f} | {_ll(g['m3'], g['y']):.4f} | {_ll(pb, g['y']):.4f} |")
    (OUT / "blend.json").write_text(json.dumps(out, indent=1))
    df.to_csv(OUT / "blend_rows.csv", index=False)
    with open(OUT / "report.md", "a") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md))
