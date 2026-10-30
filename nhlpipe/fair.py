"""Fair (no-vig) probabilities from sportsbooks.

Pinnacle is the reference. Where Pinnacle has no market, use the average of
de-vigged prices from at least two of DK / FD / MGM / ESPN ("consensus").
De-vig method: multiplicative (normalise each two-/three-way market to 1).
"""
import pandas as pd

from .names import norm

SHARP = "pinnacle"
CONSENSUS = ("draftkings", "fanduel", "betmgm", "espnbet")

# candidate market -> (sportsbook market key, selector)
BOOK_MARKET = {
    "ml": "h2h",
    "spread": "spreads",
    "total": "totals",
    "p1_total": "totals_p1",
    "p1_result": "h2h_p1",
    "player_points": "player_points",
    "player_sog": "player_shots_on_goal",
}


def devig(odds: pd.DataFrame) -> pd.DataFrame:
    o = odds[odds["book"].isin((SHARP,) + CONSENSUS)].copy()
    o = o[o["implied_prob"].notna()]
    o["player_key"] = o["player"].map(lambda p: norm(p) if isinstance(p, str) else "")
    o["abs_point"] = o["point"].abs()
    keys = ["book", "event_id", "market", "player_key"]
    o["grp_point"] = o["abs_point"].where(o["market"].isin(["spreads"]), o["point"])
    o["grp_point"] = o["grp_point"].fillna(-999)
    tot = o.groupby(keys + ["grp_point"])["implied_prob"].transform("sum")
    n = o.groupby(keys + ["grp_point"])["implied_prob"].transform("size")
    o = o[n >= 2]  # one-sided markets (e.g. anytime goal) can't be de-vigged
    o["fair"] = o["implied_prob"] / tot[n >= 2]
    # Books price the 1st-period winner 2-way (tie refunded) while Kalshi's is
    # 3-way. Only a 3-way book market (with a Draw) is comparable.
    p1 = o["market"] == "h2h_p1"
    if p1.any():
        has_draw = (
            o[p1].assign(d=o.loc[p1, "outcome"].str.lower().isin(["draw", "tie"]))
            .groupby(keys)["d"].transform("any")
        )
        o = o.drop(index=has_draw[~has_draw].index)
    return o


def _team_of(outcome: str, row) -> str | None:
    n = norm(outcome)
    if n == norm(row["home_name"]):
        return row["home"]
    if n == norm(row["away_name"]):
        return row["away"]
    if n in ("draw", "tie"):
        return "TIE"
    return None


def lookup_table(fair: pd.DataFrame) -> dict:
    """(game_key, cand market, team/player_key, line, 'yes') -> {source: prob}."""
    table: dict = {}
    inv = {v: k for k, v in BOOK_MARKET.items()}
    for r in fair.to_dict("records"):
        cm = inv.get(r["market"])
        if not cm:
            continue
        gk = f"{r['away']}@{r['home']}"
        if cm in ("ml", "p1_result"):
            t = _team_of(r["outcome"], r)
            if not t:
                continue
            key = (gk, cm, t, None)
        elif cm == "spread":
            t = _team_of(r["outcome"], r)
            if not t or r["point"] is None or r["point"] >= 0:
                continue  # we only need the "-1.5" side; NO = 1 - p
            key = (gk, cm, t, abs(r["point"]))
        elif cm in ("total", "p1_total"):
            if str(r["outcome"]).lower() != "over":
                continue
            key = (gk, cm, None, r["point"])
        else:  # player props
            if str(r["outcome"]).lower() != "over":
                continue
            key = (gk, cm, r["player_key"], r["point"])
        table.setdefault(key, {}).setdefault(r["book"], []).append(r["fair"])
    return table


def fair_prob(c: dict, table: dict) -> tuple[float | None, str | None]:
    m = c["market"]
    if m not in BOOK_MARKET:
        return None, None
    if m in ("ml", "p1_result"):
        key = (c["game_key"], m, c["team"], None)
    elif m == "spread":
        key = (c["game_key"], m, c["team"], c["line"])
    elif m in ("total", "p1_total"):
        key = (c["game_key"], m, None, c["line"])
    else:
        key = (c["game_key"], m, c["player_key"], c["line"])
    books = table.get(key)
    if not books:
        return None, None
    if SHARP in books:
        p, src = sum(books[SHARP]) / len(books[SHARP]), "pinnacle"
    else:
        vals = [sum(v) / len(v) for b, v in books.items() if b in CONSENSUS]
        if len(vals) < 2:
            return None, None
        p, src = sum(vals) / len(vals), "consensus"
    return (p if c["side"] == "yes" else 1 - p), src
