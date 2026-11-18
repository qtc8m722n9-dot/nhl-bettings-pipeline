"""Live paper methods for H21 (docs/hypotheses_2026-11-18_goalscorers.md), from the 2026-11-19 pick lock.

  M8_scorer_price  Model P: Pinnacle team expected goals (total + moneyline) x the player's share
  M9_scorer_blind  Model B: never sees a price (frozen in data/patterns/scorer_B.json)
Both buy YES on Kalshi "player scores" (1+ goal) markets when model P(score) - Kalshi ask incl. fee >= 3 pts,
up to 2 per game; plus one 3-leg parlay from the best leg in each of the 3 best games.
"""
import json
from datetime import date

import numpy as np
import pandas as pd

from . import methods
from .names import norm
from .patterns import scorer
from .patterns.data import DATA, market_lines
from .shots2 import live as slive, pull as spull

EDGE, MAX_PER_GAME = 0.03, 2
PARAMS = DATA / "patterns" / "scorer_B.json"


def picks(day: date, slate: pd.DataFrame, odds: pd.DataFrame, cands: pd.DataFrame) -> pd.DataFrame:
    k = cands[(cands["venue"] == "kalshi") & (cands["market"] == "player_goals") & (cands["line"] == 0.5)
              & (cands["side"] == "yes") & cands["cost"].notna()].copy()
    if k.empty:
        return pd.DataFrame()
    k["key"] = k["player"].astype(str).map(lambda p: norm(p.split(" (#")[0]))
    k = k[~k.duplicated(["game_key", "key"], keep=False)]  # same-name skaters: skip
    seasons = list(dict.fromkeys(scorer.SEASONS[:-1] + [slive.season_of(day)]))
    hist = pd.concat([spull.load_stats(s) for s in seasons], ignore_index=True)
    hist = hist[hist["gameDate"] < day.isoformat()]
    games = [g for s in seasons for g in spull.schedule(s, refresh=False)]
    started = set(slate.loc[~slate["game_state"].isin(["FUT", "PRE"]), "game_id"]) if "game_state" in slate else set()
    tonight = [g for g in games if g["date"] == day.isoformat() and g["game_id"] not in started]
    rows = slive.tonight_rows(day, tonight, hist, set(zip(k["key"], k["game_key"])))
    if rows.empty:
        return pd.DataFrame()
    rows["goals"] = 0
    mp = pd.read_csv(DATA / "shots2" / "mp_teams.csv.gz")
    mp = mp[mp["gameDate"] < int(day.strftime("%Y%m%d"))]
    s = scorer.skater_frame(pd.concat([hist, rows], ignore_index=True), games, mp)
    s = s[s["date"] == day.isoformat()].copy()
    if s.empty:
        return pd.DataFrame()
    B = scorer.ModelB.from_json(json.loads(PARAMS.read_text()))
    s["p_B"] = B.prob(s)
    ml = market_lines(odds[pd.to_datetime(odds["commence_utc"]) > pd.Timestamp(odds["snapshot_et"].iloc[0])])
    lam = {}
    for r in ml.dropna(subset=["tot_line", "over_fair", "ml_home_fair"]).to_dict("records"):
        mu = scorer._total_mean(r["tot_line"], r["over_fair"])
        lh, la = scorer._split(mu, r["ml_home_fair"])
        lam[(f"{r['away']}@{r['home']}", r["home"])] = lh
        lam[(f"{r['away']}@{r['home']}", r["away"])] = la
    s["lam_team"] = [lam.get((g, t), np.nan) for g, t in zip(s["game_key"], s["teamAbbrev"])]
    s["p_P"] = 1 - np.exp(-s["lam_team"] * s["player_rate"] / s["team_rate"])
    m = k.merge(s[["game_key", "key", "p_B", "p_P"]], on=["game_key", "key"], how="inner")
    out = []
    for name, col in (("M8_scorer_price", "p_P"), ("M9_scorer_blind", "p_B")):
        d = m[m[col].notna()].copy()
        d["est_prob"] = d[col]
        d["est_source"] = "scorer_" + col[-1]
        d["edge"] = d["est_prob"] - d["cost"]
        d = d[d["edge"] >= EDGE].sort_values(["edge", "cand_id"], ascending=[False, True])
        singles = d.groupby("game_key", sort=False).head(MAX_PER_GAME)
        best = d.drop_duplicates("game_key").head(methods.PARLAY_LEGS)
        res = pd.concat([singles, methods.parlays(best)], ignore_index=True)
        if res.empty:
            continue
        res["method"] = name
        res["pick_no"] = range(1, len(res) + 1)
        out.append(res)
    pk = pd.concat(out, ignore_index=True) if out else pd.DataFrame()
    print(f"scorers: {len(s)} skaters, {len(m)} Kalshi markets matched, "
          + ", ".join(f"{n} {(pk['method'] == n).sum() if len(pk) else 0}" for n in ("M8_scorer_price", "M9_scorer_blind")))
    return pk
