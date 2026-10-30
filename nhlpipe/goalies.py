"""Projected/confirmed starting goalies from DailyFaceoff.

No API exists, so we read the page's embedded Next.js JSON. Parsing is
defensive: if the structure changes we save the raw JSON for debugging.
"""
import json
import re
from datetime import date

from .http import get

URL = "https://www.dailyfaceoff.com/starting-goalies/{d}"


def _next_data(html: str) -> dict:
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        raise ValueError("DailyFaceoff: __NEXT_DATA__ not found")
    return json.loads(m.group(1))


def _find_games(obj):
    """Find the list of dicts that carry home/away goalie names."""
    if isinstance(obj, list) and obj and isinstance(obj[0], dict):
        if any("homeGoalieName" in d or "home_goalie_name" in d for d in obj):
            return obj
    if isinstance(obj, dict):
        for v in obj.values():
            r = _find_games(v)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = _find_games(v)
            if r:
                return r
    return None


def _pick(d: dict, *keys):
    for k in keys:
        if d.get(k) not in (None, ""):
            return d[k]
    return None


def starters(day: date) -> tuple[list[dict], dict]:
    """Returns (rows, raw_json). Status is Confirmed / Likely / Unconfirmed."""
    raw = _next_data(get(URL.format(d=day.isoformat())).text)
    games = _find_games(raw) or []
    rows = []
    for g in games:
        for side in ("home", "away"):
            rows.append(
                {
                    "side": side,
                    "team_name": _pick(g, f"{side}TeamName", f"{side}_team_name"),
                    "goalie": _pick(g, f"{side}GoalieName", f"{side}_goalie_name"),
                    # DailyFaceoff leaves this blank until there is news.
                    "status": _pick(
                        g,
                        f"{side}NewsStrengthName",
                        f"{side}_news_strength_name",
                        f"{side}GoalieStatus",
                    )
                    or "Unconfirmed",
                    "updated": _pick(g, f"{side}NewsCreatedAt", "updatedAt", "date"),
                }
            )
    return rows, raw
