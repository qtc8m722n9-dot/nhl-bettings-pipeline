"""Buy the 2024-25 season's pick-time prices for H10-H18 (Evan approved 2026-11-17, ~17k credits).

At 13:50 ET each game day: one featured snapshot (h2h + totals, all games, 20 credits) and one
SOG-props snapshot per game starting later that ET day (10 credits each). All through
backtest.oddshist: cached forever, logged in data/backtest/odds/ledger.csv, capped by MAX_CREDITS.
Run on GitHub Actions: Backtest (manual) -> task props2425, args "2024-10-04 2025-04-17".
"""
from datetime import date, timedelta

from ..backtest import oddshist
from ..backtest.pipeline import _iso, _slate_events, pick_dt
from ..shots2 import pull as spull

FEATURED = ["h2h", "totals"]
PROPS = ["player_shots_on_goal"]


def pull(start: str, end: str) -> None:
    days = sorted({g["date"] for g in spull.schedule("20242025", refresh=False)})
    days = [date.fromisoformat(d) for d in days if start <= d <= end]
    n_ev = 0
    for d in days:
        t = pick_dt(d)
        try:
            feat = oddshist.featured(_iso(t), markets=FEATURED)
            evs = _slate_events(feat, d, t)
            for ev in evs:
                oddshist.event_odds(ev["id"], _iso(t), markets=PROPS)
            n_ev += len(evs)
        except oddshist.BudgetExceeded as e:
            print(e)
            break
        print(f"{d}: {len(evs)} games  credits so far {oddshist.SPENT}", flush=True)
    print("events", n_ev, "credits:", oddshist.SPENT, oddshist.LAST_HEADERS)
