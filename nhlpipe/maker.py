"""Kalshi resting-order paper test (H20, docs/hypotheses_2026-11-17.md).

Question: if instead of buying at the ask (taker) we rest a bid one cent under Pinnacle's fair price
at the pick lock, how often does it fill, and are the fills still good bets?

For every Kalshi market side in the day's candidates with a Pinnacle fair price at the lock:
  bid   = fair - 1 cent, rounded down to the cent
  fill  = some 1-minute candle between the lock and the listed start traded or was offered
          STRICTLY through our bid (YES side: trade low or ask low <= bid - 0.01; NO side: the mirror on
          the YES bid / trade high). "Strictly through" means we'd be filled whatever our place in the queue.
  cost  = bid + maker fee (0.0175 x C x p x (1-p), rounded up per $100 paper order)
Compared with the taker cost the methods pay today (ask + taker fee, from the shadow board).

python -m nhlpipe.maker [YYYY-MM-DD ...]   (no dates: every graded date not done yet)
Writes data/maker/<date>.csv and data/maker.md. Run by the morning grading job (non-fatal).
"""
import math
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from . import kalshi

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "maker"
START = date(2026, 10, 31)
ORDER_USD = 100.0
TIME_BUDGET_S = 12 * 60  # never hold up the grading job; a long backfill finishes over several runs


def maker_fee(p: float) -> float:
    c = max(1, math.floor(ORDER_USD / p))
    return math.ceil(round(0.0175 * c * p * (1 - p) * 100, 6)) / 100 / c


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def candles(ticker: str, t0: int, t1: int) -> list[dict]:
    series = ticker.split("-")[0]
    params = {"start_ts": t0, "end_ts": t1, "period_interval": 1}
    for path in (f"/series/{series}/markets/{ticker}/candlesticks", f"/historical/markets/{ticker}/candlesticks"):
        try:
            c = kalshi.get_json(f"{kalshi.BASE}{path}", params).get("candlesticks", [])
        except Exception:  # noqa: BLE001
            continue
        if c:
            return c
    return []


def _fill(cs: list[dict], side: str, bid: float, t_start: int) -> int | None:
    """Minutes before start of the first candle that went strictly through our bid, else None."""
    for c in sorted(cs, key=lambda x: int(x.get("end_period_ts", 0))):
        end = int(c.get("end_period_ts", 0))
        if end > t_start:
            break
        pr, ya, yb = c.get("price") or {}, c.get("yes_ask") or {}, c.get("yes_bid") or {}
        if side == "yes":
            lows = [_f(pr.get("low_dollars")), _f(ya.get("low_dollars"))]
            if any(v is not None and v <= bid - 0.01 + 1e-9 for v in lows):
                return round((t_start - end) / 60)
        else:  # NO at `bid` = someone buying YES at 1 - bid or higher
            highs = [_f(pr.get("high_dollars")), _f(yb.get("high_dollars"))]
            if any(v is not None and v >= (1 - bid) + 0.01 - 1e-9 for v in highs):
                return round((t_start - end) / 60)
    return None


def day_rows(d: date) -> pd.DataFrame | None:
    ds = d.isoformat()
    cf, pk, sh, sl = (DATA / "picks" / f"{ds}_candidates.csv.gz", DATA / "picks" / f"{ds}.csv",
                      DATA / "shadow" / f"{ds}.csv", DATA / "slates" / f"{ds}.csv")
    if not all(p.exists() for p in (cf, pk, sh, sl)):
        return None
    c = pd.read_csv(cf)
    c = c[(c["venue"] == "kalshi") & c["fair_prob"].notna() & c["ticker"].notna()]
    if c.empty:
        return None
    lock = pd.Timestamp(pd.read_csv(pk)["created_et"].dropna().iloc[0]).tz_convert("UTC")
    slate = pd.read_csv(sl)
    slate["game_key"] = slate["away"] + "@" + slate["home"]
    start = dict(zip(slate["game_key"], pd.to_datetime(slate["start_utc"], utc=True)))
    s = pd.read_csv(sh).drop_duplicates("cand_id").set_index("cand_id")
    rows, cache = [], {}
    for r in c.to_dict("records"):
        st = start.get(r["game_key"])
        if st is None or r["cand_id"] not in s.index or pd.isna(s.loc[r["cand_id"], "y"]):
            continue
        t0, t1 = int(lock.timestamp()), int(st.timestamp())
        if t1 <= t0:
            continue
        if r["ticker"] not in cache:
            cache[r["ticker"]] = candles(r["ticker"], t0, t1)
        p = float(r["fair_prob"])
        bid = math.floor(round((p - 0.01) * 100, 6)) / 100
        if bid < 0.02 or bid > 0.97:
            continue
        mins = _fill(cache[r["ticker"]], r["side"], bid, t1)
        rows.append({"date": ds, "cand_id": r["cand_id"], "ticker": r["ticker"], "market": r["market"], "side": r["side"],
                     "fair_lock": p, "bid": bid, "filled": mins is not None, "fill_min_before": mins,
                     "maker_cost": bid + maker_fee(bid), "taker_cost": float(r["cost"]),
                     "y": s.loc[r["cand_id"], "y"], "close_fair": s.loc[r["cand_id"], "close_fair"] if "close_fair" in s else np.nan,
                     "n_candles": len(cache[r["ticker"]])})
    return pd.DataFrame(rows)


def report() -> str:
    fs = sorted(OUT.glob("*.csv"))
    if not fs:
        return ""
    d = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
    d = d[d["n_candles"] > 0]
    md = ["# Kalshi resting-order paper test (H20)", "",
          f"Updated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if "
          "the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.", "",
          "| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | "
          "Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |", "|---|--:|--:|--:|--:|--:|--:|--:|"]
    d["drift"] = d["close_fair"] - d["fair_lock"]
    groups = [("All", d)] + [(m, q) for m, q in d.groupby("market")]
    for name, q in groups:
        f = q[q["filled"]]
        nf = q[~q["filled"]]
        roi_m = (f["y"] / f["maker_cost"] - 1).mean() if len(f) else np.nan
        clv = (f["close_fair"] - f["maker_cost"]).mean()
        roi_t = (q["y"] / q["taker_cost"] - 1).mean()
        pts = lambda x: "–" if pd.isna(x) else f"{100 * x:+.1f}"  # noqa: E731
        md.append(f"| {name} | {len(q):,} | {q['filled'].mean():.0%} | {pts(roi_m)}% | {pts(clv)} | {pts(f['drift'].mean())} | "
                  f"{pts(nf['drift'].mean())} | {pts(roi_t)}% |")
    md += ["", "Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us "
           "(adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20)."]
    txt = "\n".join(md) + "\n"
    (DATA / "maker.md").write_text(txt)
    return txt


def main(argv: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if argv:
        days = [date.fromisoformat(a) for a in argv]
    else:
        days = sorted(date.fromisoformat(p.stem) for p in (DATA / "shadow").glob("*.csv"))
        days = [x for x in days if x >= START and not (OUT / f"{x.isoformat()}.csv").exists()]
    t_start = time.time()
    for d in days:
        if time.time() - t_start > TIME_BUDGET_S:
            print(f"time budget reached; {d} and later left for the next run")
            break
        r = day_rows(d)
        if r is None or r.empty:
            print(f"{d}: nothing")
            continue
        if (r["n_candles"] > 0).mean() < 0.5:  # Kalshi data not reachable: try again next run
            print(f"{d}: candles missing for most markets; not saved")
            continue
        r.to_csv(OUT / f"{d.isoformat()}.csv", index=False)
        print(f"{d}: {len(r)} market sides, fill rate {r['filled'].mean():.0%}, candles found for {(r['n_candles'] > 0).mean():.0%}")
    print(report())


if __name__ == "__main__":
    main(sys.argv[1:])
