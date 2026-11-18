"""Buy 2025-26 anytime-goalscorer prices at the 13:50 ET pick snapshot for H21 (Evan approved 2026-11-18).

Event ids come from the already-cached featured snapshots (no cost); each game's anytime-goal market costs 10 credits.
Run on GitHub Actions: Backtest (manual) -> task atg2526, args "2025-10-07 2026-04-16".
"""
from datetime import date

from ..backtest import nhldata, oddshist
from ..backtest.pipeline import _iso, _slate_events, pick_dt

MARKETS = ["player_goal_scorer_anytime"]


def pull(start: str, end: str) -> None:
    recs = nhldata.load_range(date.fromisoformat(start), date.fromisoformat(end))
    n = 0
    for ds in sorted(recs):
        if not recs[ds]["games"]:
            continue
        d = date.fromisoformat(ds)
        t = pick_dt(d)
        try:
            feat = oddshist.featured(_iso(t))  # cached by the 2025-26 backtest
            evs = _slate_events(feat, d, t)
            for ev in evs:
                oddshist.event_odds(ev["id"], _iso(t), markets=MARKETS)
            n += len(evs)
        except oddshist.BudgetExceeded as e:
            print(e)
            break
        print(f"{d}: {len(evs)} games  credits so far {oddshist.SPENT}", flush=True)
    print("events", n, "credits:", oddshist.SPENT, oddshist.LAST_HEADERS)
