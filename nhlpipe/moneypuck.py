"""MoneyPuck season-summary CSVs (data courtesy of MoneyPuck.com).

Free for non-commercial use with credit. We download the published CSVs once
per run; we do not scrape beyond the download files.
"""
import io
from datetime import date

import pandas as pd

from .http import get
from .names import mp_team

BASE = "https://moneypuck.com/moneypuck/playerData/seasonSummary"


def season_year(day: date) -> int:
    """MoneyPuck labels a season by its starting year: 2026-27 -> 2026."""
    return day.year if day.month >= 8 else day.year - 1


def _csv(kind: str, day: date) -> pd.DataFrame:
    url = f"{BASE}/{season_year(day)}/regular/{kind}.csv"
    df = pd.read_csv(io.StringIO(get(url, timeout=60).text))
    df = df.loc[:, ~df.columns.duplicated()]  # teams.csv repeats 'team'
    if "team" in df.columns:
        df["team"] = df["team"].map(mp_team)
    return df


def teams(day: date) -> pd.DataFrame:
    return _csv("teams", day)


def goalies(day: date) -> pd.DataFrame:
    return _csv("goalies", day)


def skaters(day: date) -> pd.DataFrame:
    return _csv("skaters", day)


def team_features(df: pd.DataFrame) -> pd.DataFrame:
    """One row per team: 5v5 xG share and per-60 rates, PP/PK xG rates."""
    out = {}
    for sit, tag in (("5on5", "ev"), ("5on4", "pp"), ("4on5", "pk"), ("all", "all")):
        s = df[df["situation"] == sit].set_index("team")
        mins = s["iceTime"] / 60.0
        out[f"{tag}_xgf60"] = s["xGoalsFor"] / mins * 60
        out[f"{tag}_xga60"] = s["xGoalsAgainst"] / mins * 60
        if tag == "ev":
            out["ev_xg_pct"] = s["xGoalsPercentage"]
            out["ev_gf60"] = s["goalsFor"] / mins * 60
            out["ev_ga60"] = s["goalsAgainst"] / mins * 60
        if tag == "all":
            out["gp"] = s["games_played"]
            out["sog_for_pg"] = s["shotsOnGoalFor"] / s["games_played"]
            out["sog_against_pg"] = s["shotsOnGoalAgainst"] / s["games_played"]
    return pd.DataFrame(out).reset_index().rename(columns={"index": "team"})


def goalie_features(df: pd.DataFrame) -> pd.DataFrame:
    s = df[df["situation"] == "all"].copy()
    s["gsax"] = s["xGoals"] - s["goals"]
    s["gsax_per60"] = s["gsax"] / (s["icetime"] / 3600.0)
    return s[["playerId", "name", "team", "games_played", "icetime", "gsax", "gsax_per60"]]
