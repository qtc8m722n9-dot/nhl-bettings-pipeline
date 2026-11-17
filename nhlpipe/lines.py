"""DailyFaceoff line combinations (for hypothesis H3, docs/hypotheses_2026-11-17.md).

One page per team; the line-up is in the page's embedded Next.js JSON. Parsing is
defensive: every player dict found is flattened to its scalar fields, and if a page
yields nothing its JSON is saved for fixing the parser.
Writes data/raw/<date>/df_lines.csv (one row per player slot) via pull_daily.
"""
import json
import re

import pandas as pd

from .http import get

URL = "https://www.dailyfaceoff.com/teams/{slug}/line-combinations"
SLUGS = {
    "ANA": "anaheim-ducks", "BOS": "boston-bruins", "BUF": "buffalo-sabres", "CAR": "carolina-hurricanes",
    "CBJ": "columbus-blue-jackets", "CGY": "calgary-flames", "CHI": "chicago-blackhawks", "COL": "colorado-avalanche",
    "DAL": "dallas-stars", "DET": "detroit-red-wings", "EDM": "edmonton-oilers", "FLA": "florida-panthers",
    "LAK": "los-angeles-kings", "MIN": "minnesota-wild", "MTL": "montreal-canadiens", "NJD": "new-jersey-devils",
    "NSH": "nashville-predators", "NYI": "new-york-islanders", "NYR": "new-york-rangers", "OTT": "ottawa-senators",
    "PHI": "philadelphia-flyers", "PIT": "pittsburgh-penguins", "SEA": "seattle-kraken", "SJS": "san-jose-sharks",
    "STL": "st-louis-blues", "TBL": "tampa-bay-lightning", "TOR": "toronto-maple-leafs", "UTA": "utah-mammoth",
    "VAN": "vancouver-canucks", "VGK": "vegas-golden-knights", "WPG": "winnipeg-jets", "WSH": "washington-capitals",
}
NAME_KEYS = ("name", "playerName", "fullName")


def _next_data(html: str) -> dict:
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        raise ValueError("DailyFaceoff: __NEXT_DATA__ not found")
    return json.loads(m.group(1))


def _player_dicts(obj, path="") -> list[tuple[str, dict]]:
    """Every dict that looks like a player slot (has a name and a position/group field)."""
    out = []
    if isinstance(obj, dict):
        keys = set(obj)
        if keys & set(NAME_KEYS) and any(("position" in k.lower() or "group" in k.lower()) for k in keys):
            out.append((path, obj))
        for k, v in obj.items():
            out += _player_dicts(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += _player_dicts(v, f"{path}[{i}]")
    return out


def team_lines(team: str) -> tuple[list[dict], dict]:
    raw = _next_data(get(URL.format(slug=SLUGS[team])).text)
    pp = raw.get("props", {}).get("pageProps", raw)
    rows = []
    for path, d in _player_dicts(pp):
        r = {"team": team, "json_path": path}
        r.update({k: v for k, v in d.items() if isinstance(v, (str, int, float, bool)) or v is None})
        rows.append(r)
    updated = None
    for k in ("updatedAt", "lastUpdated", "date"):
        c = pp.get("combinations", {}) if isinstance(pp.get("combinations"), dict) else {}
        updated = updated or c.get(k) or pp.get(k)
    for r in rows:
        r["page_updated"] = updated
    return rows, pp


def all_lines(teams: list[str] | None = None) -> tuple[pd.DataFrame, dict]:
    """(one row per player slot for every team, {team: page JSON} for teams that parsed to nothing)."""
    rows, failed = [], {}
    for t in teams or sorted(SLUGS):
        try:
            r, pp = team_lines(t)
        except Exception as e:  # noqa: BLE001 - one team never kills the pull
            failed[t] = {"error": f"{type(e).__name__}: {e}"}
            continue
        if not r:
            failed[t] = pp
        rows += r
    return pd.DataFrame(rows), failed
