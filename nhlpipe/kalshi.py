"""Kalshi public market data (no key needed for reading prices).

We discover NHL series by ticker/title rather than hard-coding tickers,
then pull every open market in them. Prices are contract cost in dollars
(0-1), i.e. directly an implied probability before fees.
"""
from .http import get_json

BASE = "https://api.elections.kalshi.com/trade-api/v2"


def _paged(path: str, key: str, params: dict, max_pages: int = 20) -> list[dict]:
    out, cursor = [], None
    for _ in range(max_pages):
        p = dict(params)
        if cursor:
            p["cursor"] = cursor
        d = get_json(f"{BASE}{path}", p)
        out += d.get(key, [])
        cursor = d.get("cursor")
        if not cursor:
            break
    return out


def nhl_series() -> list[dict]:
    series = _paged("/series", "series", {"category": "Sports"}, max_pages=10)
    if not series:  # category filter unsupported -> pull all
        series = _paged("/series", "series", {}, max_pages=30)
    keep = []
    for s in series:
        text = f"{s.get('ticker', '')} {s.get('title', '')}".upper()
        if "NHL" in text or "HOCKEY" in text or "STANLEY CUP" in text:
            keep.append({"ticker": s.get("ticker"), "title": s.get("title")})
    return keep


# Single-game series (found 2026-10-30). Futures/awards are skipped.
GAME_SERIES = [
    "KXNHLGAME",       # moneyline
    "KXNHLSPREAD",     # puck line
    "KXNHLTOTAL",      # game total
    "KXNHLTEAMTOTAL",  # team total
    "KXNHL1P", "KXNHL1PTOTAL", "KXNHL1PSPREAD", "KXNHL1PBTTS",  # first period
    "KXNHLGOAL", "KXNHLANYGOAL", "KXNHLFIRSTGOAL",               # goalscorer
    "KXNHLPTS", "KXNHLAST",                                      # points, assists
    "KXNHLSAVES", "KXNHLSAVE",                                   # goalie saves
    "KXNHLOT",                                                   # goes to OT
]


def _price(m: dict, side: str) -> float | None:
    """Dollar price for 'yes_bid'/'yes_ask'; handles old cents fields too."""
    v = m.get(f"{side}_dollars")
    if v not in (None, ""):
        return float(v)
    v = m.get(side)
    return None if v in (None, "") else float(v) / 100.0


def open_markets(series_tickers: list[str]) -> list[dict]:
    rows = []
    for t in series_tickers:
        for m in _paged("/markets", "markets", {"series_ticker": t, "status": "open", "limit": 1000}):
            rows.append(
                {
                    "source": "kalshi",
                    "book": "kalshi",
                    "series": t,
                    "event_ticker": m.get("event_ticker"),
                    "ticker": m.get("ticker"),
                    "title": m.get("title"),
                    "yes_sub_title": m.get("yes_sub_title"),
                    "close_time": m.get("close_time"),
                    "yes_bid": _price(m, "yes_bid"),
                    "yes_ask": _price(m, "yes_ask"),
                    "no_bid": _price(m, "no_bid"),
                    "no_ask": _price(m, "no_ask"),
                    "last_price": _price(m, "last_price"),
                    "volume": m.get("volume_fp", m.get("volume")),
                    "open_interest": m.get("open_interest_fp", m.get("open_interest")),
                }
            )
    return rows
