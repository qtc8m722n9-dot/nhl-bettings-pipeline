"""Every bet Evan could actually place tonight, priced where he'd place it.

Venues: Kalshi (game markets, player points) and Underdog / PrizePicks
(player shots on goal and points, via The Odds API). Sportsbooks are only
used as a reference for fair prices (see fair.py).

Each candidate row:
  cand_id, game_key (AWAY@HOME), venue, market, team, player, side, line,
  cost (prob you pay, incl. fees / payout breakeven), kalshi ticker/side.
"""
import re

import pandas as pd

from .names import norm
from .pull_odds import american_to_prob

MAX_KALSHI_SPREAD = 0.10  # skip markets where ask - bid > 10c (illiquid)

ALIASES = {
    "LAK": {"LA", "LAK"}, "NJD": {"NJ", "NJD"}, "SJS": {"SJ", "SJS"},
    "TBL": {"TB", "TBL"}, "VGK": {"VGK", "VEG", "VGS"}, "UTA": {"UTA", "UTAH"},
    "WSH": {"WSH", "WAS"}, "MTL": {"MTL", "MON"}, "CBJ": {"CBJ", "CLB"},
    "NSH": {"NSH", "NAS"}, "WPG": {"WPG", "WIN"},
}


def _codes(abbrev: str) -> set[str]:
    return ALIASES.get(abbrev, {abbrev})


def kalshi_fee(p: float) -> float:
    """Kalshi taker fee per contract ~ 0.07 * p * (1 - p) (rounded up per order)."""
    return 0.07 * p * (1 - p)


def _match_game(event_ticker: str, games: list[tuple[str, str]], day_code: str):
    try:
        body = event_ticker.split("-")[1]
    except IndexError:
        return None
    if not body.startswith(day_code):
        return None
    teams = body[len(day_code):]
    for away, home in games:
        for a in _codes(away):
            for h in _codes(home):
                if teams == a + h:
                    return away, home, {a: away, h: home}
    return None


def _kalshi_day_code(day) -> str:
    return day.strftime("%y%b%d").upper()  # 2026-10-30 -> 26OCT30


def kalshi(km: pd.DataFrame, slate: pd.DataFrame, day) -> list[dict]:
    games = list(zip(slate["away"], slate["home"]))
    code = _kalshi_day_code(day)
    out = []
    for m in km.itertuples(index=False):
        g = _match_game(str(m.event_ticker), games, code)
        if not g:
            continue
        away, home, codemap = g
        suffix = str(m.ticker).split("-")[-1]
        base = dict(game_key=f"{away}@{home}", venue="kalshi", ticker=m.ticker, team=None, player=None, line=None)
        s = m.series
        if s == "KXNHLGAME":
            team = codemap.get(suffix)
            if not team:
                continue
            base.update(market="ml", team=team)
        elif s == "KXNHLSPREAD":
            mm = re.match(r"([A-Z]+)(\d+)$", suffix)
            if not mm or mm.group(1) not in codemap:
                continue
            base.update(market="spread", team=codemap[mm.group(1)], line=int(mm.group(2)) - 0.5)
        elif s == "KXNHLTOTAL":
            base.update(market="total", line=int(suffix) - 0.5)
        elif s == "KXNHLTEAMTOTAL":
            mm = re.match(r"([A-Z]+)(\d+)$", suffix)
            if not mm or mm.group(1) not in codemap:
                continue
            base.update(market="team_total", team=codemap[mm.group(1)], line=int(mm.group(2)) - 0.5)
        elif s == "KXNHL1P":
            base.update(market="p1_result", team="TIE" if suffix == "TIE" else codemap.get(suffix))
            if not base["team"]:
                continue
        elif s == "KXNHL1PTOTAL":
            base.update(market="p1_total", line=int(suffix) - 0.5)
        elif s in ("KXNHLPTS", "KXNHLGOAL"):
            mm = re.match(r"^(.*): (\d+)\+", str(m.title))
            if not mm:
                continue
            base.update(
                market="player_points" if s == "KXNHLPTS" else "player_goals",
                player=mm.group(1).strip(),
                line=int(mm.group(2)) - 0.5,
            )
        else:
            continue
        # Two ways to play every Kalshi market: buy YES or buy NO.
        for side, ask, bid in (("yes", m.yes_ask, m.yes_bid), ("no", m.no_ask, m.no_bid)):
            if pd.isna(ask) or pd.isna(bid) or ask <= 0 or ask >= 1 or bid <= 0:
                continue
            if ask - bid > MAX_KALSHI_SPREAD:
                continue
            out.append(
                {
                    **base,
                    "side": side,  # yes = the title happens (over / team wins)
                    "price": float(ask),
                    "cost": float(ask) + kalshi_fee(float(ask)),
                    "american": None,
                }
            )
    return out


PICKEM_BOOKS = ("underdog", "prizepicks")
PICKEM_MARKETS = {"player_shots_on_goal": "player_sog", "player_points": "player_points"}


def pickem(odds: pd.DataFrame) -> list[dict]:
    o = odds[odds["book"].isin(PICKEM_BOOKS) & odds["market"].isin(PICKEM_MARKETS)]
    out = []
    for r in o.itertuples(index=False):
        p = american_to_prob(r.price_american)
        if p is None or pd.isna(r.point) or float(r.point).is_integer():
            continue  # whole-number lines can push; skip them
        out.append(
            {
                "game_key": f"{r.away}@{r.home}",
                "venue": r.book,
                "ticker": None,
                "market": PICKEM_MARKETS[r.market],
                "team": None,
                "player": r.player,
                "line": r.point,
                "side": "yes" if str(r.outcome).lower() == "over" else "no",
                "price": p,
                "cost": p,  # breakeven per pick at the 2-pick payout
                "american": r.price_american,
            }
        )
    return out


def describe(c: dict) -> str:
    m, side, line = c["market"], c["side"], c.get("line")
    ou = "Over" if side == "yes" else "Under"
    if m == "ml":
        return f"{c['team']} to win" if side == "yes" else f"{c['team']} NOT to win"
    if m == "spread":
        return f"{c['team']} -{line}" if side == "yes" else f"{c['team']} not to win by {line + 0.5:.0f}+"
    if m == "total":
        return f"Game {ou} {line}"
    if m == "team_total":
        return f"{c['team']} {ou} {line}"
    if m == "p1_result":
        who = "Tie" if c["team"] == "TIE" else f"{c['team']} win"
        return f"1st period {who}" + ("" if side == "yes" else " - NO")
    if m == "p1_total":
        return f"1st period {ou} {line}"
    stat = {"player_points": "points", "player_goals": "goals", "player_sog": "shots"}[m]
    return f"{c['player']} {ou} {line} {stat}"


def build(slate: pd.DataFrame, odds: pd.DataFrame, km: pd.DataFrame, day) -> pd.DataFrame:
    rows = kalshi(km, slate, day) if km is not None and not km.empty else []
    if odds is not None and not odds.empty:
        rows += pickem(odds)
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["player_key"] = df["player"].map(lambda p: norm(p) if isinstance(p, str) else None)
    df["selection"] = [describe(r) for r in df.to_dict("records")]
    def _who(r) -> str:
        # NaN is truthy, so test types explicitly (bug fixed 2026-10-30)
        if isinstance(r.get("team"), str):
            return r["team"]
        return r["player_key"] if isinstance(r.get("player_key"), str) else ""

    df["cand_id"] = [
        f"{r['venue']}|{r['game_key']}|{r['market']}|{_who(r)}|{r['line']}|{r['side']}"
        for r in df.to_dict("records")
    ]
    # keep the cheapest venue for identical bets
    return df.sort_values("cost").drop_duplicates("cand_id").reset_index(drop=True)
