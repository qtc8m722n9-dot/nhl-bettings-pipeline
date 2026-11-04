"""Bullseye: game-winner (moneyline) component for the combined model.

P(home team wins, OT/SO included) from pre-game factors, each one chosen because
published work or our own backtests say it moves win probability
(sources in data/bullseye/report.md):

  team strength   5v5 xG diff per game, non-5v5 xG diff per game (special teams,
                  4v4, 6v5), goals-minus-xG per game (finishing + team goaltending);
                  current-season games, recency-weighted, with last season's rating
                  (regressed) as a prior worth K games
  goalie          today's projected starter vs the team's usual goaltending
                  (shrunk GSAx per game; 0 when unknown)
  home ice        intercept (+ referee/last-change effects are inside it)
  rest            back-to-back for each side (road b2b is worse), 3-in-4 nights,
                  extra rest days
  travel          away team's time-zone shift since its last game (east/west),
                  km travelled since its last game
  lineup          share of the team's regular TOI missing from its last game
                  (live: injury list); proxy for injuries / scratches

All inputs are point-in-time: only games before the game date.
Coefficients are fit on past seasons only (data/bullseye/model.json).
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1] / "data" / "bullseye"

# arena (lat, lon, standard-time UTC offset)
ARENA = {
    "ANA": (33.81, -117.88, -8), "ARI": (33.43, -111.93, -7), "BOS": (42.37, -71.06, -5), "BUF": (42.88, -78.88, -5),
    "CAR": (35.80, -78.72, -5), "CBJ": (39.97, -83.01, -5), "CGY": (51.04, -114.05, -7), "CHI": (41.88, -87.67, -6),
    "COL": (39.75, -105.01, -7), "DAL": (32.79, -96.81, -6), "DET": (42.34, -83.06, -5), "EDM": (53.55, -113.50, -7),
    "FLA": (26.16, -80.33, -5), "LAK": (34.04, -118.27, -8), "MIN": (44.95, -93.10, -6), "MTL": (45.50, -73.57, -5),
    "NJD": (40.73, -74.17, -5), "NSH": (36.16, -86.78, -6), "NYI": (40.71, -73.73, -5), "NYR": (40.75, -73.99, -5),
    "OTT": (45.30, -75.93, -5), "PHI": (39.90, -75.17, -5), "PIT": (40.44, -79.99, -5), "SEA": (47.62, -122.35, -8),
    "SJS": (37.33, -121.90, -8), "STL": (38.63, -90.20, -6), "TBL": (27.94, -82.45, -5), "TOR": (43.64, -79.38, -5),
    "UTA": (40.77, -111.90, -7), "VAN": (49.28, -123.11, -8), "VGK": (36.10, -115.18, -8), "WPG": (49.89, -97.14, -6),
    "WSH": (38.90, -77.02, -5),
}
FEATURES = ["ev_xgd", "st_xgd", "fin", "goalie", "h_b2b", "a_b2b", "h_3in4", "a_3in4", "rest_diff",
            "a_tz_shift", "a_km", "lineup"]
GOALIE_PRIOR_GP = 25  # same shrinkage as M3


def _km(a, b):
    (la1, lo1, _), (la2, lo2, _) = ARENA[a], ARENA[b]
    p1, p2, dl = math.radians(la1), math.radians(la2), math.radians(lo2 - lo1)
    c = math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(dl)
    return 6371 * math.acos(max(-1.0, min(1.0, c)))


# ---- team ratings ---------------------------------------------------------------
def team_games(mp: pd.DataFrame) -> pd.DataFrame:
    """MoneyPuck team-game logs -> one row per team-game (regular season):
    ev_xgd, st_xgd (all minus 5v5), fin (all goals diff minus all xG diff)."""
    m = mp[(mp["gameId"] // 10000 % 100) == 2]
    p = m.pivot_table(index=["team", "season", "gameId", "gameDate"], columns="situation",
                      values=["xGoalsFor", "xGoalsAgainst", "goalsFor", "goalsAgainst"], aggfunc="sum")
    out = pd.DataFrame(index=p.index)
    xg_all = p[("xGoalsFor", "all")] - p[("xGoalsAgainst", "all")]
    xg_ev = p[("xGoalsFor", "5on5")] - p[("xGoalsAgainst", "5on5")]
    out["ev_xgd"] = xg_ev
    out["st_xgd"] = xg_all - xg_ev
    out["fin"] = (p[("goalsFor", "all")] - p[("goalsAgainst", "all")]) - xg_all
    return out.reset_index().sort_values(["team", "gameDate"])


def season_ratings(tg: pd.DataFrame) -> pd.DataFrame:
    """Full-season mean per team-season (used as next season's prior)."""
    return tg.groupby(["team", "season"])[["ev_xgd", "st_xgd", "fin"]].mean().reset_index()


def rating_asof(tg_team: pd.DataFrame, prior: dict, d_int: int, half_life: float, k: dict, regress: float) -> dict:
    """Recency-weighted current-season mean + regressed prior worth k[col] games."""
    g = tg_team[tg_team["gameDate"] < d_int]
    n = len(g)
    w = np.ones(n) if not half_life else 0.5 ** (np.arange(n)[::-1] / half_life)
    out = {}
    for c in ("ev_xgd", "st_xgd", "fin"):
        pr = prior.get(c, 0.0) * (1 - regress)
        s, ws = float((g[c].to_numpy() * w).sum()), float(w.sum())
        out[c] = (s + pr * k[c]) / (ws + k[c])
    out["gp"] = n
    return out


# ---- schedule factors -----------------------------------------------------------
def schedule_factors(sched: list[dict]) -> pd.DataFrame:
    """Per game: rest / b2b / 3-in-4 for each side; away travel since its last game."""
    games = sorted([g for g in sched], key=lambda g: (g["start_utc"] or g["date"], g["game_id"]))
    last = {}       # team -> (date, venue)
    hist = {}       # team -> list of dates
    rows = []
    for g in games:
        d = pd.Timestamp(g["date"])
        venue = g["home"]
        r = {"game_id": g["game_id"], "neutral": bool(g.get("neutral"))}
        for side in ("home", "away"):
            t = g[side]
            prev = last.get(t)
            rest = (d - prev[0]).days - 1 if prev else 3
            r[f"{side}_rest"] = min(rest, 3)
            r[f"{side}_b2b"] = int(prev is not None and rest == 0)
            recent = [x for x in hist.get(t, []) if (d - x).days <= 3]
            r[f"{side}_3in4"] = int(len(recent) >= 2)
            if side == "away":
                pv = prev[1] if prev else t
                ok = pv in ARENA and venue in ARENA
                r["a_km"] = _km(pv, venue) / 1000 if ok else 0.0
                r["a_tz_shift"] = (ARENA[venue][2] - ARENA[pv][2]) if ok else 0  # + = travelled east
        for side in ("home", "away"):
            t = g[side]
            last[t] = (d, venue)
            hist.setdefault(t, []).append(d)
        rows.append(r)
    return pd.DataFrame(rows)


# ---- lineup proxy ---------------------------------------------------------------
def lineup_missing(box: pd.DataFrame) -> pd.DataFrame:
    """box: playerId, teamAbbrev, gameId, gameDate, toi (sec), one row per skater-game.
    For each team-game G: TOI share (over the team's last 10 games) of 'regulars'
    (played >= 6 of the last 10) who did not play the team's previous game.
    Returned keyed by (team, next game date) semantics: value at G uses games before G."""
    out = []
    for team, b in box.groupby("teamAbbrev"):
        gids = b.drop_duplicates("gameId").sort_values("gameDate")[["gameId", "gameDate"]].to_numpy()
        per_game = {gid: set(x["playerId"]) for gid, x in b.groupby("gameId")}
        toi = b.pivot_table(index="gameId", columns="playerId", values="toi", aggfunc="sum").fillna(0)
        for i in range(len(gids)):
            gid, gd = gids[i]
            if i < 3:
                out.append({"team": team, "gameId": gid, "lineup": 0.0})
                continue
            prev = [x[0] for x in gids[max(0, i - 10):i]]
            t = toi.loc[prev]
            played = (t > 0).sum()
            regs = played[played >= min(6, len(prev) * 0.6)].index
            share = t[regs].sum() / t.to_numpy().sum()
            last_ids = per_game[prev[-1]]
            out.append({"team": team, "gameId": gid, "lineup": float(share[[p for p in regs if p not in last_ids]].sum())})
    return pd.DataFrame(out)


# ---- model ----------------------------------------------------------------------
def load_model() -> dict | None:
    p = ROOT / "model.json"
    return json.loads(p.read_text()) if p.exists() else None


def prob(feat: dict, model: dict) -> float:
    z = model["intercept"] + sum(model["coef"][f] * (feat.get(f) or 0.0) for f in model["coef"])
    return 1 / (1 + math.exp(-z))
