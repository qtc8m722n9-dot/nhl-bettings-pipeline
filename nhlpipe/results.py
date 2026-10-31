"""Final results from the NHL API, cached per date for grading.

Usage: python -m nhlpipe.results YYYY-MM-DD
Writes data/results/<date>.json:
  games[game_key] = {
    game_id, state, final (bool), last_period (REG / OT / SO),
    home, away, home_score, away_score,   # official final, shootout winner +1
    p1_home, p1_away,                     # 1st-period goals
    players: {norm full name: {team, goals, assists, points, sog, toi}},
  }
Player stats come from the boxscore (regulation + OT; shootout goals never
count). Only skaters who dressed appear; a scratched player is absent.
"""
import json
import sys
from datetime import date
from pathlib import Path

from .http import get_json
from .names import norm

BASE = "https://api-web.nhle.com/v1"
DATA = Path(__file__).resolve().parent.parent / "data"
FINAL_STATES = {"OFF", "FINAL"}


def _toi_sec(toi: str | None) -> int:
    try:
        m, s = str(toi).split(":")
        return int(m) * 60 + int(s)
    except (ValueError, AttributeError):
        return 0


def _game(g: dict) -> dict:
    home, away = g["homeTeam"]["abbrev"], g["awayTeam"]["abbrev"]
    rec = {
        "game_id": g["id"],
        "state": g.get("gameState"),
        "final": g.get("gameState") in FINAL_STATES,
        "start_utc": g.get("startTimeUTC"),
        "last_period": (g.get("gameOutcome") or {}).get("lastPeriodType"),
        "home": home,
        "away": away,
        "home_score": g["homeTeam"].get("score"),
        "away_score": g["awayTeam"].get("score"),
        "p1_home": sum(1 for x in g.get("goals", []) if x.get("period") == 1 and x.get("teamAbbrev") == home),
        "p1_away": sum(1 for x in g.get("goals", []) if x.get("period") == 1 and x.get("teamAbbrev") == away),
        "players": {},
    }
    if not rec["final"]:
        return rec
    box = get_json(f"{BASE}/gamecenter/{g['id']}/boxscore")
    pbp = get_json(f"{BASE}/gamecenter/{g['id']}/play-by-play")
    team_ids = {box["homeTeam"]["id"]: home, box["awayTeam"]["id"]: away}
    full = {
        r["playerId"]: (f"{r['firstName']['default']} {r['lastName']['default']}", team_ids.get(r.get("teamId")))
        for r in pbp.get("rosterSpots", [])
    }
    for side, team in (("homeTeam", home), ("awayTeam", away)):
        for grp in ("forwards", "defense"):
            for p in box["playerByGameStats"][side].get(grp, []):
                name = full.get(p["playerId"], (p["name"]["default"], team))[0]
                rec["players"][norm(name)] = {
                    "name": name,
                    "team": team,
                    "goals": p.get("goals", 0),
                    "assists": p.get("assists", 0),
                    "points": p.get("points", 0),
                    "sog": p.get("sog", 0),
                    "toi_sec": _toi_sec(p.get("toi")),
                }
    return rec


def roster_names(team: str) -> set[str]:
    """Current roster, to tell a scratch (on roster, didn't dress) from a name mismatch."""
    try:
        d = get_json(f"{BASE}/roster/{team}/current")
    except Exception:  # noqa: BLE001
        return set()
    out = set()
    for grp in ("forwards", "defensemen", "goalies"):
        for p in d.get(grp, []):
            out.add(norm(f"{p['firstName']['default']} {p['lastName']['default']}"))
    return out


def fetch(day: date, refresh: bool = False) -> dict:
    """Results for `day`. Cached once every game is final."""
    path = DATA / "results" / f"{day.isoformat()}.json"
    if path.exists() and not refresh:
        cached = json.loads(path.read_text())
        if cached.get("all_final"):
            return cached
    data = get_json(f"{BASE}/score/{day.isoformat()}")
    games = {}
    for g in data.get("games", []):
        if g.get("gameType") not in (2, 3):
            continue
        rec = _game(g)
        games[f"{rec['away']}@{rec['home']}"] = rec
    out = {"date": day.isoformat(), "all_final": bool(games) and all(g["final"] for g in games.values()), "games": games}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    d = date.fromisoformat(sys.argv[1])
    r = fetch(d, refresh=True)
    for gk, g in r["games"].items():
        print(f"{gk:10s} {g['state']:5s} {g['away_score']}-{g['home_score']} ({g['last_period']})  1P {g['p1_away']}-{g['p1_home']}  players {len(g['players'])}")
