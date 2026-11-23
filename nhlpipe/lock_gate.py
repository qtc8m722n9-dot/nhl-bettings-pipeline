"""Decide whether the early weekday pick-lock run should lock today's picks.

The weekday lock (cron 12:50 PM EST) usually starts 40-50 min late on GitHub, i.e. ~1:35-1:45 PM ET.
On weekdays with afternoon games (e.g. Black Friday 2026-11-27: three 1:00 PM starts) those games
would already be live at the lock and drop out of every method's slate. So picks.yml also runs an
early weekday lock (10:30 AM EST, same time as weekends); it only goes ahead when today's first game
starts before EARLY_CUTOFF ET. Otherwise it stops before pulling odds (no Odds API credits).
Added 2026-11-23 (weekly flaw review). Betting rules are unchanged; only the lock time on such days.

python -m nhlpipe.lock_gate EARLY|REGULAR [--force]  -> prints and writes run=true|false to $GITHUB_OUTPUT
"""
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from . import nhl_api

ET = ZoneInfo("America/New_York")
PICKS = Path(__file__).resolve().parent.parent / "data" / "picks"
EARLY_CUTOFF_H = 14.5  # first puck drop before 2:30 PM ET -> lock early


def first_start_et(games: list[dict]):
    ts = [pd.Timestamp(g["start_utc"]).tz_convert(ET) for g in games if g.get("start_utc")]
    return min(ts) if ts else None


def should_run(kind: str, games: list[dict], locked: bool = False, force: bool = False) -> tuple[bool, str]:
    if force:
        return True, "forced"
    if locked:
        return False, "already locked today (no odds pull)"
    if kind != "EARLY":
        return True, "regular lock"
    first = first_start_et(games)
    if first is None:
        return False, "no games today"
    h = first.hour + first.minute / 60
    if h < EARLY_CUTOFF_H:
        return True, f"first game {first:%H:%M} ET: lock early"
    return False, f"first game {first:%H:%M} ET: regular lock is early enough"


def main(argv: list[str]) -> None:
    kind = (argv[0] if argv else "REGULAR").upper()
    force = "--force" in argv
    today = datetime.now(ET).date()
    locked = (PICKS / f"{today.isoformat()}.csv").exists()
    games = nhl_api.schedule(today) if kind == "EARLY" and not locked and not force else []
    ok, why = should_run(kind, games, locked, force)
    print(f"{today} {kind}: run={ok} ({why})")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"run={'true' if ok else 'false'}\n")


if __name__ == "__main__":
    main(sys.argv[1:])
