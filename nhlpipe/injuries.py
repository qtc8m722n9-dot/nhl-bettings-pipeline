"""League-wide NHL injury list from ESPN's public site API (unofficial)."""
from .http import get_json

URL = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/injuries"


def injuries() -> list[dict]:
    data = get_json(URL)
    rows = []
    for team in data.get("injuries", []):
        tname = team.get("displayName")
        for inj in team.get("injuries", []):
            ath = inj.get("athlete") or {}
            pos = (ath.get("position") or {}).get("abbreviation")
            rows.append(
                {
                    "team_name": tname,
                    "player": ath.get("displayName"),
                    "position": pos,
                    "status": inj.get("status"),
                    "detail": inj.get("shortComment"),
                    "date": inj.get("date"),
                }
            )
    return rows
