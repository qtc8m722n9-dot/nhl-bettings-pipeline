"""Closing-price capture for closing line value (CLV).

Runs every ~15 min during game hours. For each game with locked picks that
starts within WINDOW_MIN minutes, it records, for every picked bet (and
every leg of a pick'em entry):
  close_bid / close_ask / close_mid   the venue's price now (Kalshi only)
  close_fair, close_fair_source       sharp no-vig probability now
                                      (Pinnacle, else book consensus)
Later snapshots overwrite earlier ones, so the stored value is the last one
taken before puck drop.

CLV (computed at grading):
  fair CLV  = close_fair - cost at pick time   (main yardstick)
  venue CLV = close_mid  - price at pick time  (Kalshi only)

Usage: python -m nhlpipe.closing [--dry]
Writes data/closing/<date>.csv
"""
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from . import fair, kalshi, nhl_api, odds_api
from .pull_odds import american_to_prob

ET = ZoneInfo("America/New_York")
DATA = Path(__file__).resolve().parent.parent / "data"
WINDOW_MIN = 40
CLOSE_BOOKS = "pinnacle,draftkings,fanduel,betmgm,espnbet"


def _picked_cands(picks: pd.DataFrame) -> set[str]:
    ids = set(picks["cand_id"].dropna())
    for legs in picks["legs"].dropna():
        ids |= set(str(legs).split("||"))
    return {i for i in ids if not i.startswith("entry|")}


def _starts(slate: pd.DataFrame) -> dict[str, datetime]:
    out = {}
    for r in slate.to_dict("records"):
        try:
            out[f"{r['away']}@{r['home']}"] = datetime.fromisoformat(str(r["start_utc"]).replace("Z", "+00:00"))
        except ValueError:
            pass
    return out


def run(dry: bool = False) -> None:
    now = datetime.now(timezone.utc)
    day = now.astimezone(ET).date()
    pp = DATA / "picks" / f"{day.isoformat()}.csv"
    if not pp.exists():
        print(f"No picks for {day}; nothing to close.")
        return
    picks = pd.read_csv(pp)
    cands = pd.read_csv(DATA / "picks" / f"{day.isoformat()}_candidates.csv.gz")
    slate = pd.read_csv(DATA / "slates" / f"{day.isoformat()}.csv")
    starts = _starts(slate)

    wanted = cands[cands["cand_id"].isin(_picked_cands(picks))]
    due = {
        gk for gk, t in starts.items()
        if 0 < (t - now).total_seconds() / 60 <= WINDOW_MIN
    }
    todo = wanted[wanted["game_key"].isin(due)]
    print(f"{now.astimezone(ET):%H:%M} ET  games due: {sorted(due) or 'none'}  bets to close: {len(todo)}")
    if todo.empty or dry:
        return

    # --- sharp fair prices for due games ------------------------------------
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
        if gk not in due:
            continue
        need = sorted({fair.BOOK_MARKET[m] for m in todo[todo["game_key"] == gk]["market"] if m in fair.BOOK_MARKET})
        if not need:
            continue
        data, errs = odds_api.event_odds(ev["id"], need, bookmakers=CLOSE_BOOKS)
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

    # --- per bet ---------------------------------------------------------------
    out = []
    for c in todo.to_dict("records"):
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
            except Exception as e:  # noqa: BLE001
                rec["note"] = f"kalshi: {e}"[:120]
        p, src = fair.fair_prob(c, table) if table else (None, None)
        rec.update(close_fair=p, close_fair_source=src)
        out.append(rec)

    path = DATA / "closing" / f"{day.isoformat()}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    new = pd.DataFrame(out)
    if path.exists():
        old = pd.read_csv(path)
        new = pd.concat([old[~old["cand_id"].isin(new["cand_id"])], new], ignore_index=True)
    new.to_csv(path, index=False)
    print(new.tail(len(out)).to_string(index=False))
    print("odds api:", odds_api.USAGE)


if __name__ == "__main__":
    run(dry="--dry" in sys.argv)
