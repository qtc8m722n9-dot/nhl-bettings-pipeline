"""Closing-price capture for closing line value (CLV).

Live capture (python -m nhlpipe.closing), run by the "Closing prices"
workflow ~25 min before each :00 / :30 start slot. For each game with locked
picks, the job sleeps until ~TARGET_MIN minutes before the listed start and
then records, for every picked bet (and every parlay / pick'em leg):
  close_bid / close_ask / close_mid   Kalshi quote now (Kalshi bets only)
  close_fair, close_fair_source       sharp no-vig probability now
                                      (Pinnacle, else book consensus)
A game is snapshotted once FINAL_MIN or less before start (one Odds API call
per game), so credits aren't spent twice. A late or dropped GitHub cron run
can still miss a game; the fair close is then missing for it.

Backfill (python -m nhlpipe.closing --backfill YYYY-MM-DD), run by the
morning grading job, makes the close exact no matter when (or whether) the
live snapshot ran:
  Kalshi: close_bid/ask/mid from the last 1-minute candle at or before the
          listed start
  fair:   close_fair from The Odds API historical archive, last snapshot
          ~2 min before the listed start (fair_close_from = archive)

CLV (computed at grading):
  fair CLV   = close_fair - cost at pick time   (main yardstick)
  Kalshi CLV = close_mid  - price at pick time  (Kalshi only)

Usage: python -m nhlpipe.closing [--plan] [--all]
       python -m nhlpipe.closing --backfill YYYY-MM-DD
Writes data/closing/<date>.csv
"""
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from . import fair, kalshi, nhl_api, odds_api
from .pull_odds import american_to_prob

ET = ZoneInfo("America/New_York")
DATA = Path(__file__).resolve().parent.parent / "data"
TARGET_MIN = 10    # aim for the final snapshot this many minutes before listed start
FINAL_MIN = 12     # a snapshot this close (or closer) to start is final
HORIZON_MIN = 30   # sleep-and-wait for games starting within this many minutes
MAX_RUN_MIN = 40   # never keep one Actions job alive longer than this (billed minutes)
CLOSE_BOOKS = "pinnacle,draftkings,fanduel,betmgm,espnbet"


def _picked_cands(picks: pd.DataFrame) -> set[str]:
    ids = set(picks["cand_id"].dropna())
    for legs in picks["legs"].dropna():
        ids |= set(str(legs).split("||"))
    return {i for i in ids if not i.startswith(("entry|", "parlay|"))}


def _starts(slate: pd.DataFrame) -> dict[str, datetime]:
    out = {}
    for r in slate.to_dict("records"):
        try:
            out[f"{r['away']}@{r['home']}"] = datetime.fromisoformat(str(r["start_utc"]).replace("Z", "+00:00"))
        except ValueError:
            pass
    return out


def _load_day(day: date):
    pp = DATA / "picks" / f"{day.isoformat()}.csv"
    if not pp.exists():
        return None
    picks = pd.read_csv(pp)
    cands = pd.read_csv(DATA / "picks" / f"{day.isoformat()}_candidates.csv.gz")
    slate = pd.read_csv(DATA / "slates" / f"{day.isoformat()}.csv")
    wanted = cands[cands["cand_id"].isin(_picked_cands(picks))]
    return wanted, _starts(slate)


def _closing_path(day: date) -> Path:
    return DATA / "closing" / f"{day.isoformat()}.csv"


def _save(day: date, new: pd.DataFrame) -> pd.DataFrame:
    path = _closing_path(day)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = pd.read_csv(path)
        new = pd.concat([old[~old["cand_id"].isin(new["cand_id"])], new], ignore_index=True)
    new.to_csv(path, index=False)
    return new


def _final_games(day: date) -> set[str]:
    """Games that already have a snapshot taken FINAL_MIN or less before start."""
    path = _closing_path(day)
    if not path.exists():
        return set()
    c = pd.read_csv(path)
    if "min_before_start" not in c:
        return set()
    return set(c.loc[c["min_before_start"].between(0, FINAL_MIN), "game_key"])


def _capture(day: date, todo: pd.DataFrame, starts: dict, games: set[str]) -> None:
    now = datetime.now(timezone.utc)
    stand = nhl_api.standings(day)
    tmap = nhl_api.team_name_map([], stand)
    rows = []
    try:
        events = odds_api.events()
    except Exception as e:  # noqa: BLE001
        print(odds_api.scrub(f"events failed: {e}"))
        events = []
    for ev in events:
        away = nhl_api.lookup_team(ev.get("away_team"), tmap)
        home = nhl_api.lookup_team(ev.get("home_team"), tmap)
        gk = f"{away}@{home}"
        if gk not in games:
            continue
        need = sorted({fair.BOOK_MARKET[m] for m in todo[todo["game_key"] == gk]["market"] if m in fair.BOOK_MARKET})
        if not need:
            continue
        try:
            data, errs = odds_api.event_odds(ev["id"], need, bookmakers=CLOSE_BOOKS)
        except Exception as e:  # noqa: BLE001
            print(odds_api.scrub(f"odds failed for {gk}: {e}"))
            continue
        if errs:
            print("rejected:", list(errs))
        rows += odds_api.flatten(data, now.astimezone(ET).isoformat(timespec="seconds")) if data else []
    table = {}
    if rows:
        od = pd.DataFrame(rows)
        od["home"] = od["home_name"].map(lambda n: nhl_api.lookup_team(n, tmap))
        od["away"] = od["away_name"].map(lambda n: nhl_api.lookup_team(n, tmap))
        od["implied_prob"] = od["price_american"].map(american_to_prob)
        table = fair.lookup_table(fair.devig(od))

    out = []
    for c in todo[todo["game_key"].isin(games)].to_dict("records"):
        rec = {
            "cand_id": c["cand_id"],
            "game_key": c["game_key"],
            "captured_et": now.astimezone(ET).isoformat(timespec="seconds"),
            "min_before_start": round((starts[c["game_key"]] - now).total_seconds() / 60, 1),
        }
        if c["venue"] == "kalshi" and isinstance(c.get("ticker"), str):
            try:
                q = kalshi.market_quote(c["ticker"])
                bid, ask = q[f"{c['side']}_bid"], q[f"{c['side']}_ask"]
                rec.update(close_bid=bid, close_ask=ask, close_mid=(bid + ask) / 2 if bid is not None and ask is not None else None)
                rec["kalshi_close_source"] = "live"
            except Exception as e:  # noqa: BLE001
                rec["note"] = f"kalshi: {e}"[:120]
        p, src = fair.fair_prob(c, table) if table else (None, None)
        rec.update(close_fair=p, close_fair_source=src)
        out.append(rec)
    if out:
        new = _save(day, pd.DataFrame(out))
        print(new.tail(len(out)).to_string(index=False))
    print("odds api:", odds_api.USAGE)


def run(plan: bool = False, all_games: bool = False) -> None:
    """Sleep until ~TARGET_MIN before each due game, snapshot it, repeat; exit when nothing is near."""
    t0 = datetime.now(timezone.utc)
    day = t0.astimezone(ET).date()
    loaded = _load_day(day)
    if loaded is None:
        print(f"No picks for {day}; nothing to close.")
        return
    wanted, starts = loaded
    picked_games = set(wanted["game_key"])
    if all_games:  # test mode: snapshot every not-yet-started picked game now
        games = {g for g in picked_games if g in starts and starts[g] > t0}
        print(f"--all: snapshotting {sorted(games)}")
        if games and not plan:
            _capture(day, wanted, starts, games)
        return
    while True:
        now = datetime.now(timezone.utc)
        done = _final_games(day)
        mins = {
            g: (starts[g] - now).total_seconds() / 60
            for g in picked_games - done if g in starts and starts[g] > now
        }
        due = {g for g, m in mins.items() if m <= FINAL_MIN}
        soon = {g: m for g, m in mins.items() if FINAL_MIN < m <= HORIZON_MIN}
        print(f"{now.astimezone(ET):%H:%M:%S} ET  due now: {sorted(due) or '-'}  "
              f"next: {', '.join(f'{g} in {m:.0f}m' for g, m in sorted(soon.items(), key=lambda x: x[1])) or '-'}")
        if due:
            if plan:
                print("  (plan only: would snapshot now)")
                return
            _capture(day, wanted, starts, due)
            continue
        if not soon:
            return
        wake = min(starts[g] for g in soon) - timedelta(minutes=TARGET_MIN)
        if (wake - t0).total_seconds() / 60 > MAX_RUN_MIN:
            print("  next snapshot is past this job's time budget; leaving it to the next run")
            return
        wait = max(0.0, (wake - now).total_seconds())
        print(f"  sleeping {wait / 60:.1f} min until {wake.astimezone(ET):%H:%M} ET")
        if plan:
            return
        time.sleep(wait)


# --- exact Kalshi close from 1-minute candles ---------------------------------
def _candle_quote(ticker: str, start: datetime) -> tuple[float, float, int] | None:
    """(yes_bid, yes_ask, minutes before start) from the last candle ending at or before `start`."""
    series = ticker.split("-")[0]
    st = int(start.timestamp())
    params = {"start_ts": st - 45 * 60, "end_ts": st, "period_interval": 1}
    candles = []
    for path in (f"/series/{series}/markets/{ticker}/candlesticks", f"/historical/markets/{ticker}/candlesticks"):
        try:
            candles = kalshi.get_json(f"{kalshi.BASE}{path}", params).get("candlesticks", [])
        except Exception:  # noqa: BLE001
            continue
        if candles:
            break
    best = None
    for c in candles:
        end = int(c.get("end_period_ts", 0))
        bid = (c.get("yes_bid") or {}).get("close_dollars")
        ask = (c.get("yes_ask") or {}).get("close_dollars")
        if end <= st and bid not in (None, "") and ask not in (None, ""):
            if best is None or end > best[2]:
                best = (float(bid), float(ask), end)
    if best is None:
        return None
    return best[0], best[1], round((st - best[2]) / 60)


def backfill(day: date) -> None:
    """Morning backfill: exact Kalshi closes (candles) and archived sharp closes."""
    backfill_kalshi(day)
    try:
        backfill_fair(day)
    except Exception as e:  # noqa: BLE001
        print(odds_api.scrub(f"fair backfill failed: {e}"))


# --- sharp close from The Odds API historical archive ---------------------------
# GitHub often starts scheduled runs late or skips them, so the live snapshot can
# miss a game. The archive has every game's odds at 5-minute snapshots, so the
# morning job reads the last snapshot ~ARCHIVE_LEAD before the listed start.
# Cost: 1 credit (events) + 10 per market per game; responses cached forever.
ARCHIVE_LEAD = timedelta(minutes=2)
HIST = "https://api.the-odds-api.com/v4/historical/sports/icehockey_nhl"


def _hist(path: str, params: dict, cache: Path) -> dict:
    import gzip
    import json
    import os

    from .http import get
    if cache.exists():
        return json.loads(gzip.decompress(cache.read_bytes()))
    key = os.environ.get("ODDS_API_KEY", "").strip()
    r = get(f"{HIST}{path}", params={**params, "apiKey": key, "dateFormat": "iso", "oddsFormat": "american"}, timeout=60)
    data = r.json()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(gzip.compress(json.dumps(data).encode()))
    odds_api.USAGE.update({k: r.headers.get(k) for k in ("x-requests-remaining", "x-requests-used", "x-requests-last")})
    return data


def backfill_fair(day: date) -> None:
    loaded = _load_day(day)
    if loaded is None:
        return
    wanted, starts = loaded
    path = _closing_path(day)
    old = pd.read_csv(path) if path.exists() else pd.DataFrame(columns=["cand_id"])
    done = set(old.loc[old["fair_close_from"] == "archive", "cand_id"]) if "fair_close_from" in old else set()
    todo = wanted[wanted["market"].isin(list(fair.BOOK_MARKET)) & ~wanted["cand_id"].isin(done)]
    if todo.empty:
        print(f"{day}: archived sharp closes already in place")
        return
    tmap = nhl_api.team_name_map([], nhl_api.standings(day))
    raw = DATA / "closing" / "archive" / day.isoformat()
    out = []
    for gk, grp in todo.groupby("game_key"):
        start = starts.get(gk)
        if start is None:
            continue
        iso = (start - ARCHIVE_LEAD).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        evs = _hist("/events", {"date": iso}, raw / f"events_{iso.replace(':', '')}.json.gz").get("data", [])
        ev = next((e for e in evs if f"{nhl_api.lookup_team(e['away_team'], tmap)}@{nhl_api.lookup_team(e['home_team'], tmap)}" == gk), None)
        if ev is None:
            print(f"{gk}: not in archive at {iso}")
            continue
        need = sorted({fair.BOOK_MARKET[m] for m in grp["market"]})
        d = _hist(f"/events/{ev['id']}/odds", {"date": iso, "markets": ",".join(need), "bookmakers": CLOSE_BOOKS},
                  raw / f"{gk.replace('@', '_at_')}_{'_'.join(need)}.json.gz")
        snap = d.get("timestamp")
        rows = odds_api.flatten(d.get("data") or {}, snap)
        table = {}
        if rows:
            od = pd.DataFrame(rows)
            od["home"] = od["home_name"].map(lambda n: nhl_api.lookup_team(n, tmap))
            od["away"] = od["away_name"].map(lambda n: nhl_api.lookup_team(n, tmap))
            od["implied_prob"] = od["price_american"].map(american_to_prob)
            table = fair.lookup_table(fair.devig(od))
        mins = round((start - datetime.fromisoformat(snap.replace("Z", "+00:00"))).total_seconds() / 60, 1) if snap else None
        for c in grp.to_dict("records"):
            p, src = fair.fair_prob(c, table) if table else (None, None)
            prev = old[old["cand_id"] == c["cand_id"]]
            rec = prev.iloc[0].to_dict() if len(prev) else {"cand_id": c["cand_id"], "game_key": gk}
            if p is not None:
                rec.update(close_fair=p, close_fair_source=src)
            rec.update(fair_close_from="archive" if p is not None else rec.get("fair_close_from", "none"),
                       fair_close_snapshot=snap, fair_close_min_before=mins)
            out.append(rec)
    if out:
        _save(day, pd.DataFrame(out))
    n = sum(1 for r in out if r.get("fair_close_from") == "archive")
    print(f"{day}: archived sharp closes for {n} bet(s), odds api {odds_api.USAGE}")


def backfill_kalshi(day: date) -> None:
    loaded = _load_day(day)
    if loaded is None:
        print(f"No picks for {day}.")
        return
    wanted, starts = loaded
    path = _closing_path(day)
    old = pd.read_csv(path) if path.exists() else pd.DataFrame(columns=["cand_id"])
    done = set(old.loc[old["kalshi_close_source"] == "candle", "cand_id"]) if "kalshi_close_source" in old else set()
    out = []
    k = wanted[(wanted["venue"] == "kalshi") & wanted["ticker"].notna() & ~wanted["cand_id"].isin(done)]
    for c in k.to_dict("records"):
        start = starts.get(c["game_key"])
        if start is None:
            continue
        q = _candle_quote(c["ticker"], start)
        if q is None:
            print(f"no candle: {c['ticker']}")
            continue
        yb, ya, mb = q
        bid, ask = (yb, ya) if c["side"] == "yes" else (round(1 - ya, 4), round(1 - yb, 4))
        prev = old[old["cand_id"] == c["cand_id"]]
        rec = prev.iloc[0].to_dict() if len(prev) else {"cand_id": c["cand_id"], "game_key": c["game_key"]}
        rec.update(close_bid=bid, close_ask=ask, close_mid=(bid + ask) / 2,
                   kalshi_close_source="candle", kalshi_close_min_before=mb)
        out.append(rec)
    if out:
        _save(day, pd.DataFrame(out))
    print(f"{day}: Kalshi candle closes for {len(out)} bet(s)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--backfill" in a:
        backfill(date.fromisoformat(a[a.index("--backfill") + 1]))
    else:
        # --plan: print what would happen, no API calls. --all: snapshot every
        # not-yet-started picked game now (test mode).
        run(plan="--plan" in a or "--dry" in a, all_games="--all" in a)
