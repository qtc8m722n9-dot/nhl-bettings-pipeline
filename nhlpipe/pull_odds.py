"""Odds snapshot for today's NHL slate.

Usage: python -m nhlpipe.pull_odds [main|full] [--probe]
  main   moneyline / puck line / totals for all upcoming games (3 credits)
  full   main + first-period and player props for today's games
         (~6 credits per game)
  --probe  one-off check of which exchange / pick'em books The Odds API covers

Writes data/odds/<date>/<HHMM>/{odds_long.csv, kalshi.csv, underdog.csv, status.json}
Each source fails independently.
"""
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from . import kalshi, nhl_api, odds_api, underdog

ET = ZoneInfo("America/New_York")
ROOT = Path(__file__).resolve().parent.parent / "data" / "odds"


def american_to_prob(a) -> float | None:
    try:
        a = float(a)
    except (TypeError, ValueError):
        return None
    return 100 / (a + 100) if a > 0 else -a / (-a + 100)


def _try(status: dict, name: str, fn):
    try:
        res = fn()
        status[name] = "ok"
        return res
    except Exception as e:  # noqa: BLE001
        status[name] = odds_api.scrub(f"FAILED: {type(e).__name__}: {e}")
        print(odds_api.scrub(traceback.format_exc()))
        return None


def _is_today(iso_utc: str, today) -> bool:
    try:
        t = datetime.fromisoformat(iso_utc.replace("Z", "+00:00")).astimezone(ET)
    except (AttributeError, ValueError):
        return False
    return t.date() == today


def run(mode: str = "main", probe: bool = False) -> None:
    now = datetime.now(ET)
    snap = now.isoformat(timespec="seconds")
    out = ROOT / now.date().isoformat() / now.strftime("%H%M")
    out.mkdir(parents=True, exist_ok=True)
    status: dict = {"snapshot_et": snap, "mode": mode}

    # team-name -> abbrev map (free NHL API call)
    stand = _try(status, "standings", lambda: nhl_api.standings(now.date())) or []
    tmap = nhl_api.team_name_map([], stand)

    rows: list[dict] = []

    # --- sportsbooks via The Odds API --------------------------------------
    main = _try(status, "odds_main", odds_api.main_odds) or []
    for ev in main:
        rows += odds_api.flatten(ev, snap)

    if mode == "full":
        todays = [ev for ev in main if _is_today(ev.get("commence_time", ""), now.date())]
        status["games_today"] = len(todays)
        errs = {}
        for ev in todays:
            res = _try(status, f"event_{ev['id']}", lambda ev=ev: odds_api.event_odds(ev["id"], odds_api.EVENT_MARKETS))
            if res:
                data, e = res
                errs.update(e)
                if data:
                    rows += odds_api.flatten(data, snap)
        if errs:
            status["rejected_markets"] = {k: v[:160] for k, v in errs.items()}

    if probe and main:
        ev = sorted(main, key=lambda e: e.get("commence_time", ""))[0]
        coverage = {}
        for book in odds_api.PROBE_BOOKS:
            res = _try(
                status,
                f"probe_{book}",
                lambda book=book: odds_api.event_odds(ev["id"], ["h2h", "player_shots_on_goal", "player_points"], bookmakers=book),
            )
            data = res[0] if res else {}
            mk = sorted({m["key"] for b in data.get("bookmakers", []) for m in b.get("markets", [])})
            coverage[book] = mk or "none"
            if data:
                rows += odds_api.flatten(data, snap)
        status["probe_coverage"] = coverage
        status["probe_event"] = f"{ev.get('away_team')} @ {ev.get('home_team')}"

    status["odds_api_usage"] = dict(odds_api.USAGE)

    df = pd.DataFrame(rows)
    if not df.empty:
        df["home"] = df["home_name"].map(lambda n: nhl_api.lookup_team(n, tmap))
        df["away"] = df["away_name"].map(lambda n: nhl_api.lookup_team(n, tmap))
        df["implied_prob"] = df["price_american"].map(american_to_prob)
        df.to_csv(out / "odds_long.csv", index=False)
        status["odds_rows"] = len(df)
        status["books_seen"] = sorted(df["book"].unique().tolist())
        status["markets_seen"] = sorted(df["market"].unique().tolist())

    # --- Kalshi (public, no key) ------------------------------------------
    series = _try(status, "kalshi_series", kalshi.nhl_series) or []
    status["kalshi_nhl_series"] = [s["ticker"] for s in series]
    if series:
        km = _try(status, "kalshi_markets", lambda: kalshi.open_markets([s["ticker"] for s in series])) or []
        if km:
            pd.DataFrame(km).assign(snapshot_et=snap).to_csv(out / "kalshi.csv", index=False)
        status["kalshi_markets"] = len(km)

    # --- Underdog fallback probe ------------------------------------------
    ud = _try(status, "underdog", underdog.nhl_lines)
    if ud is not None:
        status["underdog_nhl_lines"] = len(ud)
        if ud:
            pd.DataFrame(ud).assign(snapshot_et=snap).to_csv(out / "underdog.csv", index=False)

    (out / "status.json").write_text(json.dumps(status, indent=1))
    print(json.dumps(status, indent=1))


if __name__ == "__main__":
    args = sys.argv[1:]
    run(mode=next((a for a in args if a in ("main", "full")), "main"), probe="--probe" in args)
