"""Entry point for the "Backtest (manual)" workflow.

python -m nhlpipe.backtest.cli <task> [args]
  audit                 Part-1 audit pulls (ESPN box scores, historical Pinnacle at 10-30 closing times, key check)
  probe                 small coverage probe (MoneyPuck game-by-game, archive books/markets)
  pull START END        cache NHL results, MoneyPuck game logs and historical odds for a date range
  run START END         build point-in-time picks, grade, write data/backtest/results/
  report                summarise everything run so far
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

from ..http import get, get_json
from . import oddshist

ROOT = Path(__file__).resolve().parents[2] / "data"
AUDIT = ROOT / "backtest" / "audit"


def _save(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1) if not isinstance(obj, str) else obj)


def audit() -> None:
    print("key check:", oddshist.usage())
    # 1) independent results source: ESPN
    sb = get_json("https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard", {"dates": "20261030"})
    _save(AUDIT / "espn" / "scoreboard_20261030.json", sb)
    for ev in sb.get("events", []):
        summ = get_json("https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/summary", {"event": ev["id"]})
        _save(AUDIT / "espn" / f"summary_{ev['id']}.json", summ)
        print("espn", ev["id"], ev.get("shortName"))
    # 2) historical Pinnacle/consensus at each 10-30 live closing capture time
    close = pd.read_csv(ROOT / "closing" / "2026-10-30.csv")
    times = close.groupby("game_key")["captured_et"].max()
    for gk, et in times.items():
        if not isinstance(et, str):
            continue
        t = datetime.fromisoformat(et).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        evs = oddshist.events(t).get("data", [])
        print(gk, t, len(evs), "events")
        for ev in evs:
            name = f"{ev['away_team']} @ {ev['home_team']}"
            away_ab, home_ab = gk.split("@")
            if not (home_ab_match(ev["home_team"], home_ab)):
                continue
            d = oddshist.event_odds(ev["id"], t, ["h2h", "spreads", "totals", "player_points", "player_shots_on_goal"],
                                    "pinnacle,draftkings,fanduel,betmgm,espnbet")
            print("  ", name, "snapshot", d.get("timestamp"), "books", [b["key"] for b in d.get("data", {}).get("bookmakers", [])])
    print("credits:", oddshist.SPENT, oddshist.LAST_HEADERS)


NICK = {"VGK": "golden knights", "FLA": "panthers", "CGY": "flames"}


def home_ab_match(home_name: str, ab: str) -> bool:
    return NICK.get(ab, "~").lower() in home_name.lower()


def probe() -> None:
    out = AUDIT.parent / "probe"
    # MoneyPuck game-by-game
    for url, name in (
        ("https://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/teams/ANA.csv", "mp_team_ANA"),
        ("https://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/goalies/8481692.csv", "mp_goalie_8481692"),
        ("https://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/skaters/8478402.csv", "mp_skater_8478402"),
    ):
        try:
            txt = get(url, timeout=60).text
            lines = txt.splitlines()
            _save(out / f"{name}_head.csv", "\n".join(lines[:1] + [l for l in lines[1:] if ",2025," in l][:6]))
            print(name, "rows", len(lines), "cols", lines[0][:300])
        except Exception as e:  # noqa: BLE001
            print(name, "FAILED", e)
    # archive coverage on one mid-season afternoon (EST: 13:50 ET = 18:50Z)
    t = "2025-12-02T18:50:00Z"
    evs = oddshist.events(t)
    print("events at", t, evs.get("timestamp"), len(evs.get("data", [])))
    feat = oddshist.featured(t)
    cov = {}
    for ev in feat.get("data", []):
        for b in ev.get("bookmakers", []):
            for m in b.get("markets", []):
                cov.setdefault(m["key"], set()).add(b["key"])
    print("featured snapshot", feat.get("timestamp"), {k: sorted(v) for k, v in cov.items()})
    today = [e for e in evs.get("data", []) if e["commence_time"][:10] in ("2025-12-02", "2025-12-03")]
    if today:
        d = oddshist.event_odds(today[0]["id"], t)
        cov = {}
        for b in d.get("data", {}).get("bookmakers", []):
            for m in b.get("markets", []):
                cov.setdefault(m["key"], {})[b["key"]] = len(m["outcomes"])
        print("props snapshot", d.get("timestamp"), today[0]["home_team"], cov)
    print("credits:", oddshist.SPENT, oddshist.LAST_HEADERS)


def season_schedule() -> None:
    """Whole 2025-26 regular-season schedule (free NHL API), for the credit estimate."""
    from .nhldata import ROOT as NHL, SEASON_END, SEASON_START
    games, d = {}, SEASON_START
    while d <= SEASON_END:
        for wk in get_json(f"https://api-web.nhle.com/v1/schedule/{d.isoformat()}").get("gameWeek", []):
            for g in wk.get("games", []):
                if g.get("gameType") == 2:
                    games[g["id"]] = {"date": wk["date"], "start_utc": g["startTimeUTC"],
                                      "home": g["homeTeam"]["abbrev"], "away": g["awayTeam"]["abbrev"]}
        d += timedelta(days=7)
    _save(NHL / "season_schedule.json", list(games.values()))
    print(f"{len(games)} regular-season games")


def main(argv: list[str]) -> None:
    task, args = argv[0], argv[1:]
    if task == "audit":
        audit()
    elif task == "probe":
        probe()
    elif task == "schedule":
        season_schedule()
    elif task == "spot":
        from .audit_check import fetch_spot
        fetch_spot(*map(int, args))
    elif task in ("pull", "run", "report"):
        from . import pipeline
        getattr(pipeline, task)(*args)
    else:
        raise SystemExit(f"unknown task {task}")


if __name__ == "__main__":
    main(sys.argv[1:])
