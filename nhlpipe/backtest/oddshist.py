"""The Odds API historical endpoints, cached forever under data/backtest/odds/.

Every response is stored gzipped, keyed by (endpoint, snapshot time, markets,
bookmakers). A cached request is never sent again. Each paid call is logged
to data/backtest/odds/ledger.csv with the credits it cost, and a run stops
once it has spent MAX_CREDITS (env).

Cost (per The Odds API docs): historical odds = 10 x markets x regions,
where an explicit bookmaker list counts 1 region per 10 books; historical
events = 1.
"""
import gzip
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

from ..http import get
from ..odds_api import scrub

BASE = "https://api.the-odds-api.com/v4"
SPORT = "icehockey_nhl"
ROOT = Path(__file__).resolve().parents[2] / "data" / "backtest" / "odds"

# Sharp reference + main US books + pick'em / exchange if the archive has them (<= 10 = 1 region)
BOOKS = "pinnacle,draftkings,fanduel,betmgm,williamhill_us,betrivers,espnbet,underdog,prizepicks,kalshi"
FEATURED = ["h2h", "spreads", "totals"]
PROPS = ["player_shots_on_goal", "player_points"]

SPENT = {"credits": 0, "calls": 0, "cached": 0}
LAST_HEADERS: dict = {}


class BudgetExceeded(RuntimeError):
    pass


def _cap() -> int:
    try:
        return int(os.environ.get("MAX_CREDITS", "0") or 0)
    except ValueError:
        return 0


def cost_of(markets: list[str], books: str = BOOKS) -> int:
    regions = max(1, -(-len(books.split(",")) // 10))
    return 10 * len(markets) * regions


def _path(kind: str, iso: str, extra: str) -> Path:
    h = hashlib.sha1(extra.encode()).hexdigest()[:10]
    safe = iso.replace(":", "").replace("-", "")
    return ROOT / kind / iso[:10] / f"{safe}_{h}.json.gz"


def _ledger(row: dict) -> None:
    p = ROOT / "ledger.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    new = not p.exists()
    with p.open("a") as f:
        if new:
            f.write("pulled_utc,kind,date,detail,credits_last,remaining\n")
        f.write(",".join(str(row.get(k, "")) for k in ("pulled_utc", "kind", "date", "detail", "credits_last", "remaining")) + "\n")


def _fetch(kind: str, path: str, params: dict, iso: str, detail: str, est: int) -> dict:
    cache = _path(kind, iso, f"{path}|{json.dumps(params, sort_keys=True)}")
    if cache.exists():
        SPENT["cached"] += 1
        return json.loads(gzip.decompress(cache.read_bytes()))
    cap = _cap()
    if cap and SPENT["credits"] + est > cap:
        raise BudgetExceeded(f"credit cap {cap} reached (spent {SPENT['credits']})")
    key = os.environ.get("ODDS_API_KEY", "").strip()
    try:
        r = get(f"{BASE}{path}", params={**params, "apiKey": key, "dateFormat": "iso", "oddsFormat": "american"}, timeout=60)
    except requests.HTTPError as e:
        body = e.response.text[:300] if e.response is not None else ""
        code = getattr(e.response, "status_code", "?")
        if code == 422 or code == 404:  # e.g. no data for that event/time: cache the miss too
            data = {"error": code, "body": scrub(body)}
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(gzip.compress(json.dumps(data).encode()))
            return data
        raise RuntimeError(scrub(f"HTTP {code}: {body}")) from None
    used = int(r.headers.get("x-requests-last", est) or est)
    SPENT["credits"] += used
    SPENT["calls"] += 1
    LAST_HEADERS.update({k: r.headers.get(k) for k in ("x-requests-remaining", "x-requests-used", "x-requests-last")})
    data = r.json()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(gzip.compress(json.dumps(data).encode()))
    _ledger({
        "pulled_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "kind": kind, "date": iso, "detail": detail.replace(",", " "),
        "credits_last": used, "remaining": r.headers.get("x-requests-remaining"),
    })
    return data


def events(iso: str) -> dict:
    """Events listed at snapshot time `iso` (UTC, ...Z). 1 credit."""
    return _fetch("events", f"/historical/sports/{SPORT}/events", {"date": iso}, iso, "events", 1)


def featured(iso: str, markets: list[str] = FEATURED, books: str = BOOKS) -> dict:
    """All upcoming games' main markets at snapshot time `iso`."""
    return _fetch("featured", f"/historical/sports/{SPORT}/odds",
                  {"date": iso, "markets": ",".join(markets), "bookmakers": books}, iso, ",".join(markets),
                  cost_of(markets, books))


def event_odds(event_id: str, iso: str, markets: list[str] = PROPS, books: str = BOOKS) -> dict:
    """One game's (prop) markets at snapshot time `iso`."""
    return _fetch("event", f"/historical/sports/{SPORT}/events/{event_id}/odds",
                  {"date": iso, "markets": ",".join(markets), "bookmakers": books}, iso,
                  f"{event_id} {' '.join(markets)}", cost_of(markets, books))


def usage() -> dict:
    """Account usage from a free call (the sports list costs 0 credits)."""
    key = os.environ.get("ODDS_API_KEY", "").strip()
    r = get(f"{BASE}/sports", params={"apiKey": key})
    return {k: r.headers.get(k) for k in ("x-requests-remaining", "x-requests-used", "x-requests-last")}
