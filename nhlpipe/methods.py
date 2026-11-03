"""The 7 methods.

Pre-registered rules (do not change mid test period). Updated 2026-10-30,
before the trial period started, to collect data faster:
  - flat 1 unit per pick / parlay / entry
  - singles: every bet that clears the edge bar, max 1 per game (cap 16)
    (B0 random and C1 chalk: one per game, so they stay fair baselines)
  - parlays: each method also builds up to 2 three-leg parlays from its
    top singles, every leg from a different game; tracked separately
  - M5: up to 6 two-pick pick'em entries
  - never both sides of the same market
  - minimum edge: 2.5% on game markets, 4% on player props

Amendments 2026-11-03 (pricing / rule fixes, applied from that slate on):
  - fair prices de-vigged with the power method (was multiplicative)
  - Underdog picks priced at its real payout (3.5x standard 2-pick x the pick's
    multiplier); PrizePicks at 3x; PrizePicks demons/goblins skipped
  - M5: Underdog only, and an entry's two picks come from different games
  - Kalshi fee rounded up per (nominal $100) order; Kalshi DNP/postponed bets
    graded at Kalshi's fair-price settlement instead of void
  - new method M6 shots model v2 (nhlpipe/shots2/live.py)
"""
import random
import re

import pandas as pd

MAX_PICKS = 16
MAX_PER_GAME = 1
MAX_ENTRIES = 6
PARLAY_LEGS = 3
MAX_PARLAYS = 2
EDGE_GAME = 0.025
EDGE_PROP = 0.04
# Edges this large are almost always a model or data error, not a real price gap.
MAX_EDGE_GAME = 0.10
MAX_EDGE_PROP = 0.15
PROP_MARKETS = {"player_points", "player_goals", "player_sog"}
PICKEM_2_PAYOUT = 3.0  # Underdog / PrizePicks standard 2-pick power play


_LEG_SPLIT = re.compile(r"\|\|(?=[a-z0-9_]+\|[A-Z]+@[A-Z]+\|)")


def split_legs(s) -> list[str]:
    """Split a parlay/entry 'legs' string on '||'.

    A leg id can itself contain '||' (empty team/player slot, e.g. game totals:
    'kalshi|BUF@LAK|total||8.5|no'), so only split where the next leg starts
    ('venue|AWAY@HOME|'). Fixed 2026-11-01.
    """
    return _LEG_SPLIT.split(str(s)) if isinstance(s, str) and s else []


def _min_edge(market: str) -> float:
    return EDGE_PROP if market in PROP_MARKETS else EDGE_GAME


def _max_edge(market: str) -> float:
    return MAX_EDGE_PROP if market in PROP_MARKETS else MAX_EDGE_GAME


def _edge_ok(d: pd.DataFrame) -> pd.Series:
    return (d["edge"] >= d["market"].map(_min_edge)) & (d["edge"] <= d["market"].map(_max_edge))


def _market_key(r) -> str:
    """Same bet regardless of venue or side (no both sides, no duplicates across apps)."""
    return r["cand_id"].split("|", 1)[1].rsplit("|", 1)[0]


def _take(df: pd.DataFrame, order_col: str, ascending=False) -> pd.DataFrame:
    picked, per_game, used = [], {}, set()
    for r in df.sort_values(order_col, ascending=ascending).to_dict("records"):
        mk = _market_key(r)
        if mk in used or per_game.get(r["game_key"], 0) >= MAX_PER_GAME:
            continue
        picked.append(r)
        used.add(mk)
        per_game[r["game_key"]] = per_game.get(r["game_key"], 0) + 1
        if len(picked) == MAX_PICKS:
            break
    return pd.DataFrame(picked)


def _value(df: pd.DataFrame, prob_col: str, src_col: str | None = None) -> pd.DataFrame:
    d = df[df[prob_col].notna()].copy()
    d["est_prob"] = d[prob_col]
    d["est_source"] = d[src_col] if src_col else prob_col
    d["edge"] = d["est_prob"] - d["cost"]
    d = d[_edge_ok(d)]
    return _take(d, "edge")


def b0_random(c: pd.DataFrame, day) -> pd.DataFrame:
    d = c[(c["cost"] >= 0.20) & (c["cost"] <= 0.85)].copy()
    d["rand"] = [random.Random(f"{day}|{i}").random() for i in d["cand_id"]]
    d["est_prob"], d["est_source"], d["edge"] = None, "random", None
    return _take(d, "rand")


def c1_chalk(c: pd.DataFrame, day) -> pd.DataFrame:
    d = c[(c["venue"] == "kalshi") & (c["cost"] >= 0.55) & (c["cost"] <= 0.85)].copy()
    d["est_prob"], d["est_source"], d["edge"] = None, "chalk", None
    return _take(d, "price")


def m1_sharp(c: pd.DataFrame, day) -> pd.DataFrame:
    return _value(c, "fair_prob", "fair_source")


def m2_goalie(c: pd.DataFrame, day, backup_games: set[str]) -> pd.DataFrame:
    d = c[c["game_key"].isin(backup_games) & ~c["market"].isin(PROP_MARKETS)]
    return _value(d, "model_prob")


def m3_xg(c: pd.DataFrame, day) -> pd.DataFrame:
    d = c[~c["market"].isin(PROP_MARKETS)]
    return _value(d, "model_prob")


def m4_shots(c: pd.DataFrame, day) -> pd.DataFrame:
    d = c[c["market"] == "player_sog"]
    return _value(d, "sog_prob")


def m5_entries(c: pd.DataFrame, day) -> pd.DataFrame:
    """Up to 6 two-pick entries from the best pick'em legs (sharp price or shots model)."""
    # Amended 2026-11-03: Underdog only (PrizePicks left Canada on 2026-04-03; Underdog
    # reprices same-game picks), and the two picks of an entry come from different games.
    d = c[c["venue"] == "underdog"].copy()
    d["est_prob"] = d["fair_prob"].fillna(d["sog_prob"])
    d["est_source"] = d["fair_source"].where(d["fair_prob"].notna(), "sog_model")
    d = d[d["est_prob"].notna()]
    d["edge"] = d["est_prob"] - d["cost"]
    d = d[_edge_ok(d)]
    if d.empty:
        return pd.DataFrame()
    venue = d["venue"].value_counts().idxmax()  # an entry must be on one app
    legs, seen_players = [], set()
    for r in d[d["venue"] == venue].sort_values("edge", ascending=False).to_dict("records"):
        if r["player_key"] in seen_players:
            continue
        legs.append(r)
        seen_players.add(r["player_key"])
        if len(legs) == MAX_ENTRIES * 2:
            break
    entries, pairs, used = [], [], set()
    for i, a in enumerate(legs):  # best remaining leg + best remaining leg from another game
        if i in used:
            continue
        j = next((j for j in range(i + 1, len(legs)) if j not in used and legs[j]["game_key"] != a["game_key"]), None)
        if j is None:
            continue
        used |= {i, j}
        pairs.append((a, legs[j]))
    for a, b in pairs:
        p = a["est_prob"] * b["est_prob"]
        payout = (1 / a["cost"]) * (1 / b["cost"])  # Underdog: product of pick multipliers; PrizePicks: 3x
        entries.append(
            {
                "cand_id": f"entry|{a['cand_id']}||{b['cand_id']}",
                "game_key": f"{a['game_key']} + {b['game_key']}",
                "venue": venue,
                "market": "pickem_2",
                "selection": f"{a['selection']}  +  {b['selection']}",
                "side": "yes",
                "line": None,
                "team": None,
                "player": f"{a['player']} | {b['player']}",
                "ticker": None,
                "price": 1 / payout,
                "cost": 1 / payout,
                "american": round((payout - 1) * 100),
                "est_prob": p,
                "est_source": f"{a['est_source']}+{b['est_source']}",
                "edge": p - 1 / payout,
                "legs": f"{a['cand_id']}||{b['cand_id']}",
            }
        )
    return pd.DataFrame(entries)


def parlays(singles: pd.DataFrame) -> pd.DataFrame:
    """Up to 2 three-leg parlays from a method's singles, in the method's own order.

    Singles are already one per game, so legs never share a game. Priced as
    the product of leg prices (what a combo / pick'em pays, roughly)."""
    if singles is None or len(singles) < PARLAY_LEGS:
        return pd.DataFrame()
    rows = singles.to_dict("records")
    out = []
    for k in range(MAX_PARLAYS):
        legs = rows[k * PARLAY_LEGS:(k + 1) * PARLAY_LEGS]
        if len(legs) < PARLAY_LEGS:
            break
        cost = 1.0
        est = 1.0
        for leg in legs:
            cost *= leg["cost"]
            est = None if est is None or leg.get("est_prob") is None or pd.isna(leg.get("est_prob")) else est * leg["est_prob"]
        venues = {leg["venue"] for leg in legs}
        out.append(
            {
                "cand_id": "parlay|" + "||".join(leg["cand_id"] for leg in legs),
                "game_key": " + ".join(leg["game_key"] for leg in legs),
                "venue": venues.pop() if len(venues) == 1 else "mixed",
                "market": f"parlay_{PARLAY_LEGS}",
                "selection": "  +  ".join(leg["selection"] for leg in legs),
                "side": "yes",
                "line": None, "team": None, "ticker": None,
                "player": None,
                "price": cost,
                "cost": cost,
                "american": round((1 / cost - 1) * 100),
                "est_prob": est,
                "est_source": "product_of_legs",
                "edge": None if est is None else est - cost,
                "legs": "||".join(leg["cand_id"] for leg in legs),
            }
        )
    return pd.DataFrame(out)


METHODS = {
    "B0_random": b0_random,
    "C1_chalk": c1_chalk,
    "M1_sharp_price": m1_sharp,
    "M2_goalie_news": m2_goalie,
    "M3_xg_model": m3_xg,
    "M4_shots_model": m4_shots,
    "M5_pickem_entries": m5_entries,
}
