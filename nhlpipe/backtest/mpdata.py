"""MoneyPuck game-by-game logs for 2025-26 (data courtesy of MoneyPuck.com),
cached under data/backtest/mp/. Pulled once, filtered to season 2025.

teams_2025.csv.gz    one row per team-game-situation (same columns as the
                     season-summary teams.csv, one game at a time)
goalies_2025.csv.gz  one row per goalie-game, situation 'all'
Features only ever aggregate rows with gameDate < the pick date.
"""
import io
from pathlib import Path

import pandas as pd

from ..http import get
from ..names import mp_team
from .nhldata import TEAMS

BASE = "https://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular"
ROOT = Path(__file__).resolve().parents[2] / "data" / "backtest" / "mp"
SEASON = 2025
MP_CODES = {"NJD": "N.J", "SJS": "S.J", "TBL": "T.B", "LAK": "L.A"}
TEAM_COLS = ["team", "season", "gameId", "playerTeam", "opposingTeam", "home_or_away", "gameDate", "situation",
             "iceTime", "xGoalsFor", "xGoalsAgainst", "goalsFor", "goalsAgainst", "shotsOnGoalFor",
             "shotsOnGoalAgainst"]


def _csv(url: str) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(get(url, timeout=90).text))


def pull_teams(refresh: bool = False) -> pd.DataFrame:
    path = ROOT / f"teams_{SEASON}.csv.gz"
    if path.exists() and not refresh:
        return pd.read_csv(path)
    frames = []
    for t in TEAMS:
        df = None
        for code in (t, MP_CODES.get(t, t)):
            try:
                df = _csv(f"{BASE}/teams/{code}.csv")
                break
            except Exception as e:  # noqa: BLE001
                print(f"MoneyPuck team {code}: {e}")
        if df is None:
            raise RuntimeError(f"no MoneyPuck game log for {t}")
        df = df.loc[:, ~df.columns.duplicated()]
        df = df[df["season"] == SEASON]
        frames.append(df[[c for c in TEAM_COLS if c in df.columns]])
    out = pd.concat(frames, ignore_index=True)
    for c in ("team", "playerTeam", "opposingTeam"):
        out[c] = out[c].map(mp_team)
    ROOT.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, index=False, compression="gzip")
    return out


def pull_goalies(goalie_ids: list[str], refresh: bool = False) -> pd.DataFrame:
    """Adds any goalie not cached yet (one request per new goalie)."""
    path = ROOT / f"goalies_{SEASON}.csv.gz"
    have = pd.read_csv(path) if path.exists() and not refresh else pd.DataFrame(columns=["playerId"])
    known = set(have["playerId"].astype(str)) | set(_missing_ids())
    new = []
    for pid in sorted(set(map(str, goalie_ids)) - known):
        try:
            df = _csv(f"{BASE}/goalies/{pid}.csv")
        except Exception as e:  # noqa: BLE001
            print(f"MoneyPuck goalie {pid}: {e}")
            _note_missing(pid)
            continue
        df = df[(df["season"] == SEASON) & (df["situation"] == "all")]
        if df.empty:
            _note_missing(pid)
            continue
        new.append(df[["playerId", "name", "gameId", "playerTeam", "gameDate", "icetime", "xGoals", "goals"]])
    if new:
        have = pd.concat([have] + new, ignore_index=True)
        have["playerTeam"] = have["playerTeam"].map(mp_team)
        ROOT.mkdir(parents=True, exist_ok=True)
        have.to_csv(path, index=False, compression="gzip")
    return have


def _missing_ids() -> list[str]:
    p = ROOT / "goalies_missing.txt"
    return p.read_text().split() if p.exists() else []


def _note_missing(pid: str) -> None:
    p = ROOT / "goalies_missing.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(f"{pid}\n")
