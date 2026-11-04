"""Bullseye backtest (game-winner component).

python -m nhlpipe.backtest.bullseye_bt build    feature tables -> data/bullseye/games_<season>.csv
python -m nhlpipe.backtest.bullseye_bt market   2025-26 Pinnacle ML at 1:50 PM + M3 raw ML -> data/bullseye/market_2025.csv
python -m nhlpipe.backtest.bullseye_bt fit      tune on 2023-24 -> check 2024-25 -> refit both -> data/bullseye/model.json
python -m nhlpipe.backtest.bullseye_bt test     2025-26 out of sample vs Pinnacle and M3 -> data/bullseye/report.md

Protocol (written before the 2025-26 test was run):
  - hyperparameters (recency half-life, prior weight K, prior regression) chosen on
    2023-24 log loss only, confirmed on 2024-25;
  - coefficients refit on 2023-24 + 2024-25 and frozen in model.json;
  - the goalie term is not fit (no goalie logs cached before 2025-26): it enters in
    goal units with the ev_xgd coefficient, shrinkage GOALIE_PRIOR_GP as in M3;
  - 2025-26 is the test: log loss vs Pinnacle and M3, and the blend weight with
    Pinnacle (does Bullseye add information the market lacks?).
  - Shootout games have no winner in the cached past-season box scores: dropped
    from training (about 7%); kept in the 2025-26 test (scores there include SO).
"""
import gzip
import itertools
import json
import sys
from datetime import date

import numpy as np
import pandas as pd

from .. import bullseye as B
from ..shots2 import pull

OUT = B.ROOT
SEASONS = ["20232024", "20242025", "20252026"]


def _ll(p, y):
    p = np.clip(np.asarray(p, float), 1e-4, 1 - 1e-4)
    y = np.asarray(y, float)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def _results(season: str) -> pd.DataFrame:
    from .m3eng import games_frame
    g = games_frame(season)
    g["home_win"] = np.where(g["hg"] > g["ag"], 1, np.where(g["hg"] < g["ag"], 0, np.nan))  # nan = shootout
    return g[["game_id", "hg", "ag", "hr", "ar", "home_win"]]


def _box(season: str) -> pd.DataFrame:
    st = pull.load_stats(season)
    b = st[["playerId", "teamAbbrev", "gameId", "gameDate", "timeOnIcePerGame"]].rename(columns={"timeOnIcePerGame": "toi"})
    b["toi"] = pd.to_numeric(b["toi"], errors="coerce").fillna(0)
    return b[b["toi"] > 0]


def _goalie_terms(season: str, games: pd.DataFrame) -> dict:
    """2025-26 only: game_id -> starter shrunk GSAx/game minus team's usual (both sides, home - away)."""
    if season != "20252026":
        return {}
    from . import mpdata, nhldata
    from .features import Season
    recs = nhldata.load_range(nhldata.SEASON_START, nhldata.SEASON_END)
    gl = pd.read_csv(mpdata.ROOT / f"goalies_{mpdata.SEASON}.csv.gz")
    S = Season(recs, pd.DataFrame({"gameDate": [0]}), gl)
    gl = gl.dropna(subset=["gameDate"])
    gl["gsax"] = gl["xGoals"] - gl["goals"]
    out = {}
    for r in games.itertuples():
        d = date.fromisoformat(r.date)
        di = int(r.date.replace("-", ""))
        v = {}
        for side, team in (("h", r.home), ("a", r.away)):
            pid, _ = S.projected_starter(team, d)
            tg = gl[(gl["playerTeam"] == team) & (gl["gameDate"] < di)]
            team_term = tg["gsax"].sum() / (tg["gameId"].nunique() + B.GOALIE_PRIOR_GP) if len(tg) else 0.0
            if pid:
                gp, gsax = S.goalie_asof(pid, d)
                v[side] = gsax / (gp + B.GOALIE_PRIOR_GP) - team_term
            else:
                v[side] = 0.0
        out[r.game_id] = v["h"] - v["a"]
    return out


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mp = pd.read_csv(pull.ROOT / "mp_teams.csv.gz")
    tg = B.team_games(mp)
    pri = B.season_ratings(tg)
    for season in SEASONS:
        y = int(season[:4])
        sched = [g for g in pull.schedule(season, refresh=False)]
        sf = B.schedule_factors(sched)
        sch = pd.DataFrame(sched)[["game_id", "date", "home", "away"]].merge(sf, on="game_id")
        lm = B.lineup_missing(_box(season))
        sch = sch.merge(lm.rename(columns={"team": "home", "gameId": "game_id", "lineup": "h_lineup"}), on=["home", "game_id"], how="left")
        sch = sch.merge(lm.rename(columns={"team": "away", "gameId": "game_id", "lineup": "a_lineup"}), on=["away", "game_id"], how="left")
        sch = sch.merge(_results(season), on="game_id", how="inner")
        cur = tg[tg["season"] == y]
        prior = {t: r for t, r in pri[pri["season"] == y - 1].set_index("team").to_dict("index").items()}
        # raw per-game rows for every team before each date (ratings are recomputed per hyperparameter set at fit time)
        sch["d_int"] = sch["date"].str.replace("-", "").astype(int)
        sch["h_gp"] = [int(((cur["team"] == h) & (cur["gameDate"] < d)).sum()) for h, d in zip(sch["home"], sch["d_int"])]
        sch["a_gp"] = [int(((cur["team"] == a) & (cur["gameDate"] < d)).sum()) for a, d in zip(sch["away"], sch["d_int"])]
        gt = _goalie_terms(season, sch)
        sch["goalie"] = sch["game_id"].map(gt).fillna(0.0)
        sch["season"] = season
        sch.to_csv(OUT / f"games_{season}.csv", index=False)
        cur.to_csv(OUT / f"teamgames_{season}.csv", index=False)
        json.dump({t: {k: float(v) for k, v in r.items() if k in ("ev_xgd", "st_xgd", "fin")} for t, r in prior.items()},
                  open(OUT / f"prior_{season}.json", "w"))
        print(season, len(sch), "games; shootouts", int(sch["home_win"].isna().sum()), "; goalie terms", len(gt))


def features(season: str, hp: dict) -> pd.DataFrame:
    g = pd.read_csv(OUT / f"games_{season}.csv")
    tg = pd.read_csv(OUT / f"teamgames_{season}.csv")
    prior = json.load(open(OUT / f"prior_{season}.json"))
    by = {t: x.sort_values("gameDate") for t, x in tg.groupby("team")}
    k = {"ev_xgd": hp["k_ev"], "st_xgd": hp["k_st"], "fin": hp["k_fin"]}
    rows = []
    for r in g.itertuples():
        rh = B.rating_asof(by.get(r.home, tg.iloc[:0]), prior.get(r.home, {}), r.d_int, hp["hl"], k, hp["regress"])
        ra = B.rating_asof(by.get(r.away, tg.iloc[:0]), prior.get(r.away, {}), r.d_int, hp["hl"], k, hp["regress"])
        rows.append({"ev_xgd": rh["ev_xgd"] - ra["ev_xgd"], "st_xgd": rh["st_xgd"] - ra["st_xgd"], "fin": rh["fin"] - ra["fin"]})
    f = pd.concat([g.reset_index(drop=True), pd.DataFrame(rows)], axis=1)
    f["h_b2b"], f["a_b2b"] = f["home_b2b"], f["away_b2b"]
    f["h_3in4"], f["a_3in4"] = f["home_3in4"], f["away_3in4"]
    f["rest_diff"] = f["home_rest"] - f["away_rest"]
    f["lineup"] = f["h_lineup"].fillna(0) - f["a_lineup"].fillna(0)
    return f[~f["neutral"]]


FIT = [f for f in B.FEATURES if f != "goalie"]


def _fit(df: pd.DataFrame, C: float = 1.0):
    from sklearn.linear_model import LogisticRegression
    d = df.dropna(subset=["home_win"])
    X = d[FIT].to_numpy()
    sd = X.std(0)
    sd[sd == 0] = 1
    lr = LogisticRegression(C=C, max_iter=2000).fit(X / sd, d["home_win"])
    return {"intercept": float(lr.intercept_[0]), "coef": {f: float(c / s) for f, c, s in zip(FIT, lr.coef_[0], sd)}}


def _pred(df: pd.DataFrame, model: dict, goalie: bool = True) -> np.ndarray:
    z = model["intercept"] + sum(model["coef"][f] * df[f].to_numpy() for f in FIT)
    if goalie:
        z = z + model["coef"]["ev_xgd"] * df["goalie"].to_numpy()
    return 1 / (1 + np.exp(-z))


GRID = {"hl": [0, 40, 20], "k_ev": [10, 20, 40], "k_st": [10, 20, 40], "k_fin": [20, 40, 80], "regress": [0.33, 0.5]}


def fit() -> None:
    res = []
    cache = {}
    for vals in itertools.product(*GRID.values()):
        hp = dict(zip(GRID, vals))
        a = cache.setdefault(("23", json.dumps(hp)), features("20232024", hp))
        m = _fit(a)
        res.append({**hp, "ll_2324_in": _ll(_pred(a.dropna(subset=["home_win"]), m, False), a["home_win"].dropna())})
    # choose by in-sample-of-season fit with 10-fold CV would be cleaner; use time split inside 2023-24 instead:
    r = pd.DataFrame(res)
    best = []
    for _, row in r.sort_values("ll_2324_in").head(20).iterrows():
        hp = {k: row[k] for k in GRID}
        hp["hl"] = int(hp["hl"])
        a = features("20232024", hp).dropna(subset=["home_win"])
        tr, va = a[a["date"] < "2024-01-15"], a[a["date"] >= "2024-01-15"]
        best.append({**hp, "ll_split": _ll(_pred(va, _fit(tr), False), va["home_win"])})
    b = pd.DataFrame(best).sort_values("ll_split")
    hp = {k: b.iloc[0][k] for k in GRID}
    hp["hl"] = int(hp["hl"])
    a = features("20232024", hp)
    v = features("20242025", hp)
    m23 = _fit(a)
    vv = v.dropna(subset=["home_win"])
    chk = {"ll_2425_oos": _ll(_pred(vv, m23, False), vv["home_win"]),
           "ll_2425_home_rate_only": _ll(np.full(len(vv), a["home_win"].mean()), vv["home_win"])}
    model = _fit(pd.concat([a, v]))
    model.update({"hyper": hp, "check_2024_25": chk, "trained_on": ["2023-24", "2024-25"],
                  "goalie": "coef[ev_xgd] x (starter shrunk GSAx/g - team usual), not fit"})
    (OUT / "model.json").write_text(json.dumps(model, indent=1))
    print(b.head(5).to_string())
    print(json.dumps(model, indent=1))


def market() -> None:
    """2025-26 Pinnacle no-vig home ML at 1:50 PM and M3's raw home ML prob (same code path as models.BLEND fit)."""
    from .. import fair, models
    from . import mpdata, nhldata, oddshist
    from . import pipeline as P
    from .features import Season
    recs = nhldata.load_range(nhldata.SEASON_START, nhldata.SEASON_END)
    S = Season(recs, pd.read_csv(mpdata.ROOT / f"teams_{mpdata.SEASON}.csv.gz"),
               pd.read_csv(mpdata.ROOT / f"goalies_{mpdata.SEASON}.csv.gz"))
    rows = []
    for ds, rec in sorted(recs.items()):
        d = date.fromisoformat(ds)
        t = P.pick_dt(d)
        sched = [g for g in rec["games"] if P._utc(g["start_utc"]) > t and g["state"] in ("OFF", "FINAL")]
        cp = oddshist._path("featured", P._iso(t), f"/historical/sports/{oddshist.SPORT}/odds|" + json.dumps(
            {"bookmakers": oddshist.BOOKS, "date": P._iso(t), "markets": ",".join(oddshist.FEATURED)}, sort_keys=True))
        if not sched or not cp.exists():
            continue
        od = P.odds_frame([json.loads(gzip.decompress(cp.read_bytes()))], P.TMAP)
        table = fair.lookup_table(fair.devig(od[od["book"] == "pinnacle"]))
        slate, mp_t, _ = S.slate(d, sched)
        ok = not mp_t.empty and mp_t[mp_t["situation"] == "all"]["games_played"].min() >= 3
        lp = models.league_params(mp_t) if ok else None
        for i, (g, srow) in enumerate(zip(sched, slate.to_dict("records"))):
            gk = f"{g['away']}@{g['home']}"
            c = {"market": "ml", "team": g["home"], "side": "yes", "line": None, "game_key": gk}
            fp, _ = fair.fair_prob(c, table)
            m3 = None
            if ok:
                lh, la = models.team_lambdas(pd.Series(srow), lp)
                m3 = models.game_prob(c, models.simulate(lh, la, seed=i), g["home"], g["away"])
            rows.append({"game_id": g["game_id"], "date": ds, "pin": fp, "m3": m3,
                         "y": int(g["home_score"] > g["away_score"]), "last_period": g["last_period"]})
    pd.DataFrame(rows).to_csv(OUT / "market_2025.csv", index=False)
    print(len(rows))


def _lg(x):
    x = np.clip(np.asarray(x, float), 1e-4, 1 - 1e-4)
    return np.log(x / (1 - x))


def _lr(X, y, intercept=False):
    from sklearn.linear_model import LogisticRegression
    return LogisticRegression(C=1e6, fit_intercept=intercept, max_iter=2000).fit(X, y)


def _boot(df, fn, n=500, seed=1):
    """Percentile CI, resampling whole dates (games on one night share news / line moves)."""
    rng = np.random.default_rng(seed)
    days = df["date"].unique()
    groups = {d: x for d, x in df.groupby("date")}
    vals = []
    for _ in range(n):
        s = pd.concat([groups[d] for d in rng.choice(days, len(days))])
        vals.append(fn(s))
    return np.percentile(vals, [2.5, 97.5])


def test() -> None:
    model = json.loads((OUT / "model.json").read_text())
    hp = model["hyper"]
    f = features("20252026", hp)
    mk = pd.read_csv(OUT / "market_2025.csv")
    d = f.drop(columns=["home_win", "date"]).merge(mk, on="game_id").dropna(subset=["pin", "m3"]).reset_index(drop=True)
    d["bull"] = _pred(d, model, True)
    d["bull_ng"] = _pred(d, model, False)
    from .. import models
    w = models.BLEND["ml"]
    d["m3_blend"] = 1 / (1 + np.exp(-(w["a"] * _lg(d["pin"]) + w["b"] * _lg(d["m3"]))))
    y = d["y"].to_numpy()
    n = len(d)
    md = ["# Bullseye: game-winner component", "",
          f"2025-26 test: {n} games with a Pinnacle moneyline at 1:50 PM and an M3 price. Model frozen before this run "
          f"(trained on 2023-24 + 2024-25, `data/bullseye/model.json`). Lower log loss is better.", "",
          "## 1. Log loss, 2025-26 (out of sample)", "", "| Model | Log loss | vs Pinnacle (95% CI) |", "|---|--:|--:|"]
    base = _ll(d["pin"], y)
    for lab, col in (("Pinnacle no-vig", "pin"), ("Bullseye", "bull"), ("Bullseye without goalie term", "bull_ng"),
                     ("M3 raw", "m3"), ("M3 live blend (fit on this season)", "m3_blend")):
        if col == "pin":
            md.append(f"| {lab} | {base:.4f} | – |")
            continue
        ci = _boot(d, lambda s, c=col: _ll(s[c], s["y"]) - _ll(s["pin"], s["y"]))
        md.append(f"| {lab} | {_ll(d[col], y):.4f} | {_ll(d[col], y) - base:+.4f} ({ci[0]:+.4f}, {ci[1]:+.4f}) |")
    md.append(f"| Home-win rate only | {_ll(np.full(n, 0.527), y):.4f} | |")

    # 2. information test: weights in a logit blend (in-sample on 2025-26; a check, not a bet rule)
    md += ["", "## 2. Does Bullseye know something Pinnacle doesn't? (logit-blend weights, 2025-26)", "",
           "y ~ a·logit(Pinnacle) + b·logit(model). b clearly > 0 = the model adds information. CI by resampling nights.", "",
           "| Inputs | a (Pinnacle) | b (Bullseye) | c (M3) | b 95% CI |", "|---|--:|--:|--:|--:|"]
    for lab, cols in (("Pinnacle + Bullseye", ["pin", "bull"]), ("Pinnacle + M3", ["pin", "m3"]),
                      ("Pinnacle + Bullseye + M3", ["pin", "bull", "m3"])):
        X = np.column_stack([_lg(d[c]) for c in cols])
        co = _lr(X, y).coef_[0]
        ci = _boot(d, lambda s: _lr(np.column_stack([_lg(s[c]) for c in cols]), s["y"]).coef_[0][1]) if "bull" in cols else [np.nan, np.nan]
        b = co[cols.index("bull")] if "bull" in cols else np.nan
        c = co[cols.index("m3")] if "m3" in cols else np.nan
        md.append(f"| {lab} | {co[0]:.2f} | {b:.2f} | {c:.2f} | ({ci[0]:.2f}, {ci[1]:.2f}) |" if "bull" in cols else
                  f"| {lab} | {co[0]:.2f} | – | {c:.2f} | |")

    # 3. honest version: fit blend on Oct-Dec, judge on Jan-Apr
    tr, va = d[d["date"] < "2026-01-01"], d[d["date"] >= "2026-01-01"]
    md += ["", "## 3. Walk-forward: blend fit on Oct-Dec 2025, judged on Jan-Apr 2026", "",
           f"Train {len(tr)} games, test {len(va)} games.", "", "| Model | Log loss Jan-Apr | vs Pinnacle (95% CI) |", "|---|--:|--:|"]
    vb = _ll(va["pin"], va["y"])
    md.append(f"| Pinnacle | {vb:.4f} | – |")
    for lab, cols in (("Pinnacle + Bullseye", ["pin", "bull"]), ("Pinnacle + M3", ["pin", "m3"]),
                      ("Pinnacle + Bullseye + M3", ["pin", "bull", "m3"])):
        lr = _lr(np.column_stack([_lg(tr[c]) for c in cols]), tr["y"])
        va = va.assign(**{f"p_{lab}": lr.predict_proba(np.column_stack([_lg(va[c]) for c in cols]))[:, 1]})
        ci = _boot(va, lambda s, k=f"p_{lab}": _ll(s[k], s["y"]) - _ll(s["pin"], s["y"]))
        ws = ", ".join(f"{c} {x:.2f}" for c, x in zip(cols, lr.coef_[0]))
        md.append(f"| {lab} (weights {ws}) | {_ll(va[f'p_{lab}'], va['y']):.4f} | {_ll(va[f'p_{lab}'], va['y']) - vb:+.4f} ({ci[0]:+.4f}, {ci[1]:+.4f}) |")

    # 4. factor by factor: what does the market under-weight?
    md += ["", "## 4. Factor by factor against the market (2025-26)", "",
           "y ~ a·logit(Pinnacle) + intercept + g·factor (factor in its own units, home minus away where paired). "
           "g ≠ 0 means Pinnacle under- (same sign as Bullseye) or over-reacts to that factor. 12 tests: expect ~1 false hit at 95%.", "",
           "| Factor | Bullseye coef (2023-25) | g vs market | g 95% CI | Read |", "|---|--:|--:|--:|---|"]
    for fct in B.FEATURES:
        X = np.column_stack([_lg(d["pin"]), d[fct]])
        g = _lr(X, y, True).coef_[0][1]
        ci = _boot(d, lambda s: _lr(np.column_stack([_lg(s["pin"]), s[fct]]), s["y"], True).coef_[0][1], n=300)
        bc = model["coef"].get(fct, model["coef"]["ev_xgd"] if fct == "goalie" else np.nan)
        read = "market under-weights" if ci[0] > 0 and bc > 0 or ci[1] < 0 and bc < 0 else (
            "market over-weights" if ci[0] > 0 or ci[1] < 0 else "priced in / no signal")
        md.append(f"| {fct} | {bc:+.3f} | {g:+.3f} | ({ci[0]:+.3f}, {ci[1]:+.3f}) | {read} |")

    # 5. market calibration (favourite-longshot / home bias)
    lr = _lr(_lg(d["pin"]).reshape(-1, 1), y, True)
    md += ["", "## 5. Pinnacle moneyline calibration (2025-26)", "",
           f"y ~ intercept + a·logit(Pinnacle): a = {lr.coef_[0][0]:.2f}, intercept = {lr.intercept_[0]:+.3f} "
           f"(a = 1 and 0 = perfectly calibrated; a > 1 = favourites under-priced). Home teams won {y.mean():.3f}, "
           f"Pinnacle said {d['pin'].mean():.3f}.", ""]
    bins = pd.cut(d["pin"], [0, .35, .45, .55, .65, 1])
    md += ["| Pinnacle home prob | Games | Pinnacle avg | Bullseye avg | Actual |", "|---|--:|--:|--:|--:|"]
    for b_, g in d.groupby(bins, observed=True):
        md.append(f"| {b_} | {len(g)} | {g['pin'].mean():.3f} | {g['bull'].mean():.3f} | {g['y'].mean():.3f} |")
    d[["game_id", "date", "pin", "m3", "bull", "bull_ng", "y"] + B.FEATURES].to_csv(OUT / "test_2025.csv", index=False)
    (OUT / "report_results.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    {"build": build, "fit": fit, "market": market, "test": test}[sys.argv[1]]()
