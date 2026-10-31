"""2025-26 NHL schedule, results and box scores, cached under data/backtest/nhl/.

One gzipped JSON per date with every regular-season game:
  game_id, start_utc, home/away (abbrev + full name), state, scores
  (official final: shootout winner +1), last_period, 1st-period goals,
  skaters [playerId, name, team, pos, goals, assists, points, sog, toi_sec],
  goalies [playerId, name, team, starter, toi_sec]
Full names come from each team's 2025-26 season roster (rosters.json).
Nothing here is used to make picks except data from dates strictly before
the pick date (see features.py); results are only read when grading.
"""
import gzip
import json
import re
from datetime import date, timedelta
from pathlib import Path

from ..http import get_json

BASE = "https://api-web.nhle.com/v1"
ROOT = Path(__file__).resolve().parents[2] / "data" / "backtest" / "nhl"
SEASON = "20252026"
SEASON_START, SEASON_END = date(2025, 10, 7), date(2026, 4, 16)
TEAMS = ["ANA", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LAK", "MIN",
         "MTL", "NJD", "NSH", "NYI", "NYR", "OTT", "PHI", "PIT", "SEA", "SJS", "STL", "TBL", "TOR", "UTA",
         "VAN", "VGK", "WPG", "WSH"]


def _rw(path: Path, obj=None):
    if obj is None:
        return json.loads(gzip.decompress(path.read_bytes()))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(json.dumps(obj, separators=(",", ":")).encode()))
    return obj


def rosters() -> dict[str, dict]:
    """playerId -> {name, team(s)} from every team's season roster."""
    path = ROOT / "rosters.json.gz"
    if path.exists():
        return _rw(path)
    out: dict[str, dict] = {}
    for t in TEAMS:
        d = get_json(f"{BASE}/roster/{t}/{SEASON}")
        for grp in ("forwards", "defensemen", "goalies"):
            for p in d.get(grp, []):
                pid = str(p["id"])
                rec = out.setdefault(pid, {"name": f"{p['firstName']['default']} {p['lastName']['default']}",
                                           "pos": p.get("positionCode"), "teams": []})
                rec["teams"].append(t)
    return _rw(path, out)


def _toi(s) -> int:
    try:
        m, sec = str(s).split(":")
        return int(m) * 60 + int(sec)
    except (ValueError, AttributeError):
        return 0


def _label(t: dict) -> str:
    return f"{(t.get('placeName') or {}).get('default', '')} {(t.get('commonName') or {}).get('default', '')}".strip()


def day(d: date, names: dict | None = None) -> dict:
    """Games on `d` (cached once all are final)."""
    path = ROOT / "days" / f"{d.isoformat()}.json.gz"
    if path.exists():
        cached = _rw(path)
        if cached.get("all_final"):
            return cached
    names = names if names is not None else rosters()
    sc = get_json(f"{BASE}/score/{d.isoformat()}")
    games = []
    for g in sc.get("games", []):
        if g.get("gameType") != 2:
            continue
        h, a = g["homeTeam"], g["awayTeam"]
        rec = {
            "game_id": g["id"], "start_utc": g.get("startTimeUTC"), "state": g.get("gameState"),
            "home": h["abbrev"], "away": a["abbrev"], "home_name": _label(h), "away_name": _label(a),
            "home_score": h.get("score"), "away_score": a.get("score"),
            "last_period": (g.get("gameOutcome") or {}).get("lastPeriodType"),
            "p1_home": sum(1 for x in g.get("goals", []) if x.get("period") == 1 and x.get("teamAbbrev") == h["abbrev"]),
            "p1_away": sum(1 for x in g.get("goals", []) if x.get("period") == 1 and x.get("teamAbbrev") == a["abbrev"]),
            "skaters": [], "goalies": [],
        }
        if rec["state"] in ("OFF", "FINAL"):
            box = get_json(f"{BASE}/gamecenter/{g['id']}/boxscore")
            for side, team in (("homeTeam", h["abbrev"]), ("awayTeam", a["abbrev"])):
                pg = box["playerByGameStats"][side]
                for grp in ("forwards", "defense"):
                    for p in pg.get(grp, []):
                        pid = str(p["playerId"])
                        rec["skaters"].append({
                            "pid": pid, "name": names.get(pid, {}).get("name", p["name"]["default"]),
                            "team": team, "pos": p.get("position"), "goals": p.get("goals", 0),
                            "assists": p.get("assists", 0), "points": p.get("points", 0), "sog": p.get("sog", 0),
                            "toi_sec": _toi(p.get("toi")),
                        })
                for p in pg.get("goalies", []):
                    pid = str(p["playerId"])
                    rec["goalies"].append({
                        "pid": pid, "name": names.get(pid, {}).get("name", p["name"]["default"]), "team": team,
                        "starter": bool(p.get("starter")), "toi_sec": _toi(p.get("toi")),
                    })
        games.append(rec)
    out = {"date": d.isoformat(), "all_final": all(x["state"] in ("OFF", "FINAL") for x in games), "games": games}
    return _rw(path, out)


def pull(start: date, end: date) -> None:
    names = rosters()
    d = start
    while d <= end:
        r = day(d, names)
        print(f"nhl {d}: {len(r['games'])} games")
        d += timedelta(days=1)
    fill_names(load_range(start, end, fix_names=False))


ABBREV = re.compile(r"^[A-Z]\. ")


def extra_names() -> dict[str, str]:
    p = ROOT / "extra_names.json.gz"
    return _rw(p) if p.exists() else {}


def fill_names(recs: dict) -> None:
    """Full names for players missing from the season rosters (one call each, cached)."""
    extra = extra_names()
    need = {s["pid"] for r in recs.values() for g in r["games"] for s in g["skaters"] + g["goalies"]
            if ABBREV.match(s["name"]) and s["pid"] not in extra}
    for pid in sorted(need):
        try:
            p = get_json(f"{BASE}/player/{pid}/landing")
            extra[pid] = f"{p['firstName']['default']} {p['lastName']['default']}"
        except Exception as e:  # noqa: BLE001
            print(f"player {pid}: {e}")
    if need:
        _rw(ROOT / "extra_names.json.gz", extra)
    print(f"full names filled for {len(need)} players")


def load_range(start: date, end: date, fix_names: bool = True) -> dict[str, dict]:
    """date -> day record, cached files only (no network)."""
    extra = extra_names() if fix_names else {}
    out = {}
    d = start
    while d <= end:
        p = ROOT / "days" / f"{d.isoformat()}.json.gz"
        if p.exists():
            rec = _rw(p)
            for g in rec["games"]:
                for s in g["skaters"] + g["goalies"]:
                    if s["pid"] in extra:
                        s["name"] = extra[s["pid"]]
            out[d.isoformat()] = rec
        d += timedelta(days=1)
    return out
