"""Official (undocumented) NHL API: schedule, standings.

Reference: https://github.com/Zmalski/NHL-API-Reference
"""
from datetime import date, timedelta

from .http import get_json
from .names import norm

BASE = "https://api-web.nhle.com/v1"


def _games_on(day: date) -> list[dict]:
    data = get_json(f"{BASE}/schedule/{day.isoformat()}")
    for wk in data.get("gameWeek", []):
        if wk.get("date") == day.isoformat():
            return wk.get("games", [])
    return []


def _team_label(t: dict) -> str:
    place = (t.get("placeName") or {}).get("default", "")
    common = (t.get("commonName") or {}).get("default", "")
    return f"{place} {common}".strip()


def schedule(day: date) -> list[dict]:
    """Regular-season and playoff games on `day`, with rest days for each team."""
    today = _games_on(day)
    yesterday = _games_on(day - timedelta(days=1))
    played_yday = {g["homeTeam"]["abbrev"] for g in yesterday} | {
        g["awayTeam"]["abbrev"] for g in yesterday
    }
    out = []
    for g in today:
        if g.get("gameType") not in (2, 3):  # 2 = regular season, 3 = playoffs
            continue
        h, a = g["homeTeam"], g["awayTeam"]
        out.append(
            {
                "game_id": g["id"],
                "start_utc": g.get("startTimeUTC"),
                "game_state": g.get("gameState"),
                "home": h["abbrev"],
                "away": a["abbrev"],
                "home_name": _team_label(h),
                "away_name": _team_label(a),
                "home_b2b": h["abbrev"] in played_yday,
                "away_b2b": a["abbrev"] in played_yday,
            }
        )
    return out


def team_name_map(games: list[dict], standings_rows: list[dict]) -> dict[str, str]:
    """normalised full name / nickname -> abbrev, for all 32 teams."""
    pairs = [(g[f"{s}_name"], g[s]) for g in games for s in ("home", "away")]
    pairs += [(r["name"], r["team"]) for r in standings_rows if r.get("name")]
    m = {}
    for name, abbrev in pairs:
        full = norm(name)
        if not full:
            continue
        m[full] = abbrev
        m[full.split(" ")[-1]] = abbrev  # nickname, e.g. 'canadiens'
    return m


def lookup_team(name: str | None, m: dict[str, str]) -> str | None:
    n = norm(name)
    if not n:
        return None
    return m.get(n) or m.get(n.split(" ")[-1])


def standings(day: date) -> list[dict]:
    data = get_json(f"{BASE}/standings/{day.isoformat()}")
    rows = []
    for t in data.get("standings", []):
        rows.append(
            {
                "team": t["teamAbbrev"]["default"],
                "name": (t.get("teamName") or {}).get("default", ""),
                "gp": t.get("gamesPlayed"),
                "w": t.get("wins"),
                "l": t.get("losses"),
                "otl": t.get("otLosses"),
                "pts": t.get("points"),
                "gf": t.get("goalFor"),
                "ga": t.get("goalAgainst"),
                "l10_w": t.get("l10Wins"),
                "l10_l": t.get("l10Losses"),
                "l10_otl": t.get("l10OtLosses"),
            }
        )
    return rows
