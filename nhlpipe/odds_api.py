"""The Odds API (v4) client for NHL.

Credit cost = (#markets) x (#regions, where every 10 bookmakers count as 1).
We pass an explicit bookmaker list (<=10) so each market costs 1 credit.
"""
import os

import requests

from .http import get

BASE = "https://api.the-odds-api.com/v4/sports/icehockey_nhl"

# Pinnacle = sharp reference (has main lines AND most props).
# DK/FD/MGM/ESPN = consensus for props. Underdog/PrizePicks/Kalshi = where
# Evan would actually play. Max 10 books = 1 credit per market.
BOOKS = "pinnacle,draftkings,fanduel,betmgm,williamhill_us,betrivers,espnbet,underdog,prizepicks,kalshi"
# Coverage confirmed 2026-10-30: kalshi=h2h, underdog/prizepicks=points+SOG.
PROBE_BOOKS = ["kalshi", "underdog", "prizepicks"]

MAIN_MARKETS = ["h2h", "spreads", "totals"]
EVENT_MARKETS = [
    "h2h_p1",
    "totals_p1",
    "player_shots_on_goal",
    "player_total_saves",
    "player_points",
    "player_goal_scorer_anytime",
]

USAGE: dict = {}


def _key() -> str:
    k = os.environ.get("ODDS_API_KEY", "").strip()
    if not k:
        raise RuntimeError("ODDS_API_KEY is not set")
    return k


def scrub(msg: str) -> str:
    """Never let the key leak into logs or committed files."""
    k = os.environ.get("ODDS_API_KEY", "").strip()
    return msg.replace(k, "***") if k else msg


def _call(path: str, params: dict) -> list | dict:
    params = {**params, "apiKey": _key(), "oddsFormat": "american", "dateFormat": "iso"}
    try:
        r = get(f"{BASE}{path}", params=params)
    except requests.HTTPError as e:
        body = e.response.text[:300] if e.response is not None else ""
        raise RuntimeError(scrub(f"HTTP {getattr(e.response, 'status_code', '?')}: {body}")) from None
    for h in ("x-requests-remaining", "x-requests-used", "x-requests-last"):
        if h in r.headers:
            USAGE[h] = r.headers[h]
    return r.json()


def events() -> list[dict]:
    """Upcoming events (free: costs 0 credits)."""
    return _call("/events", {})


def main_odds(bookmakers: str = BOOKS) -> list[dict]:
    return _call("/odds", {"markets": ",".join(MAIN_MARKETS), "bookmakers": bookmakers})


def event_odds(event_id: str, markets: list[str], bookmakers: str = BOOKS) -> tuple[dict, dict]:
    """Returns (data, errors). If a market key is rejected, retry markets one at a time."""
    try:
        return _call(f"/events/{event_id}/odds", {"markets": ",".join(markets), "bookmakers": bookmakers}), {}
    except RuntimeError as e:
        if len(markets) == 1:
            return {}, {markets[0]: str(e)}
    merged: dict = {}
    errors: dict = {}
    for m in markets:
        try:
            d = _call(f"/events/{event_id}/odds", {"markets": m, "bookmakers": bookmakers})
        except RuntimeError as e:
            errors[m] = str(e)
            continue
        if not merged:
            merged = d
        else:
            have = {b["key"]: b for b in merged.get("bookmakers", [])}
            for b in d.get("bookmakers", []):
                if b["key"] in have:
                    have[b["key"]]["markets"] += b["markets"]
                else:
                    merged.setdefault("bookmakers", []).append(b)
    return merged, errors


def flatten(event: dict, snapshot: str) -> list[dict]:
    """One row per (book, market, outcome)."""
    rows = []
    for b in event.get("bookmakers", []):
        for m in b.get("markets", []):
            for o in m.get("outcomes", []):
                rows.append(
                    {
                        "snapshot_et": snapshot,
                        "source": "odds_api",
                        "event_id": event.get("id"),
                        "commence_utc": event.get("commence_time"),
                        "home_name": event.get("home_team"),
                        "away_name": event.get("away_team"),
                        "book": b.get("key"),
                        "book_updated": m.get("last_update") or b.get("last_update"),
                        "market": m.get("key"),
                        "outcome": o.get("name"),
                        "player": o.get("description"),
                        "point": o.get("point"),
                        "price_american": o.get("price"),
                    }
                )
    return rows
