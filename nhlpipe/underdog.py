"""Underdog Pick'em NHL lines (fallback probe).

Underdog has no public API. This reads the same public JSON its web app
loads, once per run, only to record lines for paper testing. If The Odds
API carries Underdog, that source is preferred and this can be removed.
"""
from .http import get_json

URL = "https://api.underdogfantasy.com/beta/v5/over_under_lines"


def nhl_lines() -> list[dict]:
    d = get_json(URL)
    games = {g["id"]: g for g in d.get("games", [])}
    players = {p["id"]: p for p in d.get("players", [])}
    appearances = {a["id"]: a for a in d.get("appearances", [])}
    rows = []
    for line in d.get("over_under_lines", []):
        ou = line.get("over_under") or {}
        stat = (ou.get("appearance_stat") or {})
        app = appearances.get(stat.get("appearance_id"), {})
        player = players.get(app.get("player_id"), {})
        game = games.get(app.get("match_id"), {})
        sport = (player.get("sport_id") or game.get("sport_id") or "").upper()
        if sport != "NHL":
            continue
        for opt in line.get("options", []):
            rows.append(
                {
                    "source": "underdog",
                    "book": "underdog",
                    "game_title": game.get("title") or game.get("abbreviated_title"),
                    "scheduled_at": game.get("scheduled_at"),
                    "player": f"{player.get('first_name', '')} {player.get('last_name', '')}".strip(),
                    "stat": stat.get("display_stat") or stat.get("stat"),
                    "line": line.get("stat_value"),
                    "choice": opt.get("choice"),  # higher / lower
                    "payout_multiplier": opt.get("payout_multiplier"),
                    "american_price": opt.get("american_price"),
                    "status": line.get("status"),
                }
            )
    return rows
