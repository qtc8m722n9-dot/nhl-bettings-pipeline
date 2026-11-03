"""Free game-level data for the shots model v2, cached under data/shots2/.

  nhlstats/<season>/<report>/<from>_<to>.json.gz   NHL stats API per-player-game
      reports: summary (shots), timeonice (EV/PP/SH TOI, shifts), realtime
      (shot attempts, missed, blocked-against, hits), powerplay (PP shots),
      puckPossessions (zone starts)
  schedule/<season>.json.gz                       every regular-season game
                                                  (start time, teams)
  mp_teams.csv.gz                                 MoneyPuck team-game logs
                                                  (situations), seasons >= 2022
Nothing here costs Odds API credits. Completed weeks are never re-pulled;
the current week is refreshed.

python -m nhlpipe.shots2.pull 20222023 20232024 20242025 20252026
"""
import gzip
import io
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

from ..http import get, get_json

ROOT = Path(__file__).resolve().parents[2] / "data" / "shots2"
STATS = "https://api.nhle.com/stats/rest/en/skater"
REPORTS = ["summary", "timeonice", "realtime", "powerplay"]
THREADS = 6
SORT = '[{"property":"gameDate","direction":"ASC"},{"property":"playerId","direction":"ASC"}]'


def _rw(path: Path, obj=None):
    if obj is None:
        return json.loads(gzip.decompress(path.read_bytes()))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(json.dumps(obj, separators=(",", ":")).encode()))
    return obj


def schedule(season: str, refresh: bool = True) -> list[dict]:
    path = ROOT / "schedule" / f"{season}.json.gz"
    done = path.exists() and (_rw(path).get("complete") or not refresh)
    if done:
        return _rw(path)["games"]
    y = int(season[:4])
    d, end = date(y, 9, 25), date(y + 1, 4, 30)
    games = {}
    while d <= end:
        for wk in get_json(f"https://api-web.nhle.com/v1/schedule/{d.isoformat()}").get("gameWeek", []):
            for g in wk.get("games", []):
                if g.get("gameType") == 2 and str(g.get("season")) == season:
                    games[g["id"]] = {"game_id": g["id"], "date": wk["date"], "start_utc": g.get("startTimeUTC"),
                                      "home": g["homeTeam"]["abbrev"], "away": g["awayTeam"]["abbrev"],
                                      "state": g.get("gameState"), "neutral": bool(g.get("neutralSite"))}
        d += timedelta(days=7)
    gl = sorted(games.values(), key=lambda g: (g["start_utc"] or "", g["game_id"]))
    complete = bool(gl) and all(g["state"] in ("OFF", "FINAL") for g in gl)
    _rw(path, {"season": season, "complete": complete, "games": gl})
    return gl


def _report(season: str, rep: str, d: date) -> list[dict]:
    """One day of one report, 100 rows a page (big pages time out on this API)."""
    import time
    exp = f"gameTypeId=2 and seasonId={season} and gameDate='{d}'"
    rows, start = [], 0
    while True:
        for attempt in range(6):
            try:
                resp = get_json(f"{STATS}/{rep}", {"isAggregate": "false", "isGame": "true", "start": start, "limit": 100,
                                                   "sort": SORT, "cayenneExp": exp})
                break
            except Exception as e:  # noqa: BLE001  (522s and resets: back off and retry)
                if attempt == 5:
                    raise
                time.sleep(5 * (attempt + 1))
        page = resp.get("data", [])
        rows += page
        start += len(page)
        if not page or start >= resp.get("total", 0):
            return rows


def pull_stats(season: str) -> None:
    from concurrent.futures import ThreadPoolExecutor
    games = schedule(season)
    if not games:
        return
    today = datetime.now(timezone.utc).date()
    days = sorted({date.fromisoformat(g["date"]) for g in games if date.fromisoformat(g["date"]) < today})
    jobs = []
    for d in days:
        for rep in REPORTS:
            path = ROOT / "nhlstats" / season / rep / f"{d}.json.gz"
            if path.exists() and d < today - timedelta(days=2):
                continue
            jobs.append((d, rep, path))

    def one(job):
        d, rep, path = job
        _rw(path, _report(season, rep, d))
        return d

    with ThreadPoolExecutor(THREADS) as ex:
        for i, d in enumerate(ex.map(one, jobs)):
            if i % 100 == 0:
                print(f"{season}: {i}/{len(jobs)} day-reports ({d})", flush=True)
    print(f"{season}: done, {len(jobs)} day-reports pulled", flush=True)


def pull_mp_teams(min_season: int = 2022) -> None:
    path = ROOT / "mp_teams.csv.gz"
    txt = get("https://moneypuck.com/moneypuck/playerData/careers/gameByGame/all_teams.csv", timeout=300).text
    df = pd.read_csv(io.StringIO(txt), low_memory=False)
    df = df.loc[:, ~df.columns.duplicated()]
    keep = ["team", "season", "gameId", "playerTeam", "opposingTeam", "home_or_away", "gameDate", "situation",
            "iceTime", "xGoalsFor", "xGoalsAgainst", "goalsFor", "goalsAgainst", "shotsOnGoalFor",
            "shotsOnGoalAgainst", "shotAttemptsFor", "shotAttemptsAgainst", "unblockedShotAttemptsFor",
            "unblockedShotAttemptsAgainst", "penaltiesFor", "penaltiesAgainst"]
    df = df[df["season"] >= min_season][[c for c in keep if c in df.columns]]
    ROOT.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, compression="gzip")
    print("mp teams rows", len(df), "seasons", sorted(df["season"].unique()))


def load_stats(season: str) -> pd.DataFrame:
    """One row per player-game with all reports merged."""
    frames = {}
    for rep in REPORTS:
        rows = [r for f in sorted((ROOT / "nhlstats" / season / rep).glob("*.json.gz")) for r in _rw(f)]
        frames[rep] = pd.DataFrame(rows).drop_duplicates(["gameId", "playerId"])
    key = ["gameId", "playerId"]
    out = frames["summary"]
    for rep in REPORTS[1:]:
        f = frames[rep]
        cols = key + [c for c in f.columns if c not in out.columns]
        out = out.merge(f[cols], on=key, how="left")
    return out


if __name__ == "__main__":
    seasons = [a for a in sys.argv[1:] if a.isdigit()]
    for s in seasons:
        pull_stats(s)
    if "--no-mp" not in sys.argv:
        pull_mp_teams()
