"""Why does M3 under-predict overs? (STATUS next step 3)

python -m nhlpipe.backtest.m3totals collect   2025-26 per-game table -> data/backtest/m3eng/totals_games.csv
python -m nhlpipe.backtest.m3totals collect_past   2023-24 / 2024-25 per-game lambdas (no odds, no goalie term)
python -m nhlpipe.backtest.m3totals report    decomposition -> data/backtest/m3eng/totals_report.md

Per game (point-in-time, same code path as models.team_lambdas / the live M3):
lh, la with the goalie term and lh0, la0 without it, actual regulation and final
scores, and every Pinnacle half-goal total line at 1:50 PM (no-vig over prob).
"""
import gzip
import json
import sys
from datetime import date

import numpy as np
import pandas as pd

from .. import fair, models
from . import m3eng
from .features import Season

OUT = m3eng.OUT


def _no_goalie(r: dict) -> dict:
    r = dict(r)
    for s in ("home", "away"):
        r[f"{s}_goalie_gsax"] = None
    return r


def _reg(g):
    hs, as_ = g["home_score"], g["away_score"]
    ot = g["last_period"] in ("OT", "SO")
    return hs - (1 if ot and hs > as_ else 0), as_ - (1 if ot and as_ > hs else 0)


def collect() -> None:
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
        for g, srow in zip(sched, slate.to_dict("records")):
            lh, la = models.team_lambdas(pd.Series(srow), lp)
            lh0, la0 = models.team_lambdas(pd.Series(_no_goalie(srow)), lp)
            hr, ar = _reg(g)
            gk = f"{g['away']}@{g['home']}"
            base = {"date": ds, "game_id": g["game_id"], "game_key": gk, "lh": lh, "la": la, "lh0": lh0, "la0": la0,
                    "hr": hr, "ar": ar, "hs": g["home_score"], "as": g["away_score"], "last_period": g["last_period"],
                    "h_goalie_gp": srow.get("home_goalie_gp"), "a_goalie_gp": srow.get("away_goalie_gp"),
                    "lg_goals_pg": lp["goals_pg"], "calib": lp["calib"]}
            lines = [(k_l, books) for (k_gk, k_m, k_t, k_l), books in table.items()
                     if k_gk == gk and k_m == "total" and k_l is not None and not float(k_l).is_integer()]
            if not lines:
                rows.append({**base, "line": np.nan, "pin_over": np.nan})
            for k_l, _ in lines:
                c = {"market": "total", "team": None, "side": "yes", "line": k_l, "game_key": gk}
                fp, _src = fair.fair_prob(c, table)
                rows.append({**base, "line": k_l, "pin_over": fp})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "totals_games.csv", index=False)
    print(len(df), "rows,", df["game_id"].nunique(), "games")


def collect_past() -> None:
    out = []
    for season in ("20232024", "20242025"):
        g = m3eng.lambdas(season, m3eng.games_frame(season))
        g["season"] = season
        out.append(g[["season", "date", "game_id", "lh", "la", "hr", "ar", "tie", "total", "eng"]])
    pd.concat(out).to_csv(OUT / "totals_past.csv", index=False)
    print("ok")


# ---- analysis ----------------------------------------------------------------
Q = (models.P1E, models.P1T, models.P2E, models.P2C)
_K = np.arange(25)


def _eadd(lh, la, s):
    """Expected goals the pull phase adds, given regulation Poisson(lh*s), Poisson(la*s)."""
    from scipy.stats import poisson
    j = np.outer(poisson.pmf(_K, lh * s), poisson.pmf(_K, la * s))
    m = np.abs(_K[:, None] - _K[None, :])
    return j[m == 1].sum() * (Q[0] + Q[1]) + j[m == 2].sum() * (Q[2] + Q[3])


def mean_scale(lh, la):
    """Scale s so regulation goals incl. the pull phase average lh + la (what PULL_SCALE was meant to do)."""
    s = 1.0
    for _ in range(6):
        s = 1 - _eadd(lh, la, s) / (lh + la)
    return s


def _sim(df, lh, la, mode, seed=3):
    rng = np.random.default_rng(seed)
    out = []
    for r in df.itertuples():
        a, b = getattr(r, lh), getattr(r, la)
        s = {"old": 1.0, "live": models.PULL_SCALE, "meanfix": None}[mode]
        s = mean_scale(a, b) if s is None else s
        q = (0, 0, 0, 0) if mode == "old" else Q
        h, aa, hf, af, _ = m3eng.sim(a, b, (*q, s), rng)
        t = hf + af
        L = getattr(r, "line", np.nan)
        out.append({"pt": t.mean(), "preg": (h + aa).mean(), "po": (t > L).mean() if L == L else np.nan,
                    "o55": (t > 5.5).mean(), "o65": (t > 6.5).mean(), "hpl": (h - aa >= 2).mean(),
                    "apl": (aa - h >= 2).mean(), "tie": (h == aa).mean(), "s": s})
    return pd.DataFrame(out, index=df.index)


def report() -> None:
    from sklearn.linear_model import LogisticRegression
    ll = m3eng._ll
    lg = lambda x: np.log(np.clip(x, 1e-4, 1 - 1e-4) / (1 - np.clip(x, 1e-4, 1 - 1e-4)))  # noqa: E731
    d = pd.read_csv(OUT / "totals_games.csv")
    d["act"] = d["hs"] + d["as"]
    past = pd.read_csv(OUT / "totals_past.csv", dtype={"season": str})
    modes = {"old": "no pull (pre 11-03)", "live": "live (PULL_SCALE 0.93)", "meanfix": "mean-preserving scale"}
    md = ["# M3 totals bias: diagnosis", "",
          "Question (STATUS step 3): M3 put overs at ~43-45% in 2025-26 while 51% went over. Where does the gap come from?",
          "Code: `nhlpipe/backtest/m3totals.py` (collect, collect_past, report). Same point-in-time inputs and live M3 code.", "",
          "## Mean goals per game", "",
          "| Season | Model | Pred total | Actual | Pred reg. goals | Actual reg. | Scale s |", "|---|---|--:|--:|--:|--:|--:|"]
    sims = {}
    for sn, g in past.groupby("season"):
        for mo in modes:
            r = _sim(g, "lh", "la", mo)
            sims[(sn, mo)] = r
            md.append(f"| {sn[:4]}-{sn[6:]} | {modes[mo]} | {r.pt.mean():.2f} | {g.total.mean():.2f} | {r.preg.mean():.2f} | {(g.hr + g.ar).mean():.2f} | {r.s.mean():.3f} |")
    for lab, (lh, la) in (("", ("lh", "la")), (", no goalie term", ("lh0", "la0"))):
        for mo in modes:
            r = _sim(d, lh, la, mo)
            sims[("2025-26" + lab, mo)] = r
            md.append(f"| 2025-26{lab} | {modes[mo]} | {r.pt.mean():.2f} | {d.act.mean():.2f} | {r.preg.mean():.2f} | {(d.hr + d.ar).mean():.2f} | {r.s.mean():.3f} |")
    gt = ((d.lh0 + d.la0) - (d.lh + d.la)).mean()
    md += ["", f"Goalie term (2025-26 only; no goalie logs cached for earlier seasons) lowers expected goals by {gt:.3f}/game on average.", "",
           "## 2025-26 vs Pinnacle's main half-goal total at 1:50 PM", ""]
    m = d["line"].notna()
    dm, y = d[m], (d[m].act > d[m].line).astype(int)
    md += [f"{len(dm)} games (the other {(~m).sum()} had a whole-number main line). Pinnacle: avg P(over) {dm.pin_over.mean():.3f}, "
           f"log loss {ll(dm.pin_over, y):.4f}. Actual over rate {y.mean():.3f}.", "",
           "| Model | Goalie term | Avg P(over) | Log loss | Blend weight Pinnacle / M3 |", "|---|---|--:|--:|--:|"]
    for lab, key in (("yes", "2025-26"), ("no", "2025-26, no goalie term")):
        for mo in modes:
            po = sims[(key, mo)].loc[dm.index, "po"]
            X = np.column_stack([lg(dm.pin_over), lg(po)])
            lr = LogisticRegression(C=1e6, fit_intercept=False, max_iter=1000).fit(X, y)
            md.append(f"| {modes[mo]} | {lab} | {po.mean():.3f} | {ll(po, y):.4f} | {lr.coef_[0][0]:.2f} / {lr.coef_[0][1]:.2f} |")
    md += ["", "## Side effects of the scale fix on markets M3 does bet (log loss)", "",
           "| Season | Model | Home -1.5 | Away -1.5 | Goes to OT | Over 5.5 | Over 6.5 |", "|---|---|--:|--:|--:|--:|--:|"]
    for sn, g in list(past.groupby("season")) + [("2025-26", d.assign(tie=(d.hr == d.ar).astype(int), total=d.act))]:
        for mo in ("live", "meanfix"):
            r = sims[(sn if sn == "2025-26" else sn, mo)]
            md.append(f"| {sn[:4]}{'-' + sn[6:] if sn != '2025-26' else '-26'} | {modes[mo]} | {ll(r.hpl, g.hr - g.ar >= 2):.4f} | {ll(r.apl, g.ar - g.hr >= 2):.4f} | "
                      f"{ll(r.tie, g.tie):.4f} | {ll(r.o55, g.total > 5.5):.4f} | {ll(r.o65, g.total > 6.5):.4f} |")
    (OUT / "totals_report.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    {"collect": collect, "collect_past": collect_past, "report": report}[sys.argv[1]]()
