"""The 7 methods. Each returns up to 4 picks from tonight's candidates.

Pre-registered rules (do not change mid test period):
  - flat 1 unit per pick / entry
  - max 4 picks per method per night, max 2 per game
  - never both sides of the same market
  - minimum edge: 2.5% on game markets, 4% on player props
"""
import random

import pandas as pd

MAX_PICKS = 4
MAX_PER_GAME = 2
EDGE_GAME = 0.025
EDGE_PROP = 0.04
# Edges this large are almost always a model or data error, not a real price gap.
MAX_EDGE_GAME = 0.10
MAX_EDGE_PROP = 0.15
PROP_MARKETS = {"player_points", "player_goals", "player_sog"}
PICKEM_2_PAYOUT = 3.0  # Underdog / PrizePicks standard 2-pick power play


def _min_edge(market: str) -> float:
    return EDGE_PROP if market in PROP_MARKETS else EDGE_GAME


def _max_edge(market: str) -> float:
    return MAX_EDGE_PROP if market in PROP_MARKETS else MAX_EDGE_GAME


def _edge_ok(d: pd.DataFrame) -> pd.Series:
    return (d["edge"] >= d["market"].map(_min_edge)) & (d["edge"] <= d["market"].map(_max_edge))


def _market_key(r) -> str:
    return r["cand_id"].rsplit("|", 1)[0]


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
    """Four 2-pick entries from the best pick'em legs (sharp price or shots model)."""
    d = c[c["venue"].isin(["underdog", "prizepicks"])].copy()
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
        if len(legs) == MAX_PICKS * 2:
            break
    entries = []
    for i in range(0, len(legs) - 1, 2):
        a, b = legs[i], legs[i + 1]
        p = a["est_prob"] * b["est_prob"]
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
                "price": 1 / PICKEM_2_PAYOUT,
                "cost": 1 / PICKEM_2_PAYOUT,
                "american": 200,
                "est_prob": p,
                "est_source": f"{a['est_source']}+{b['est_source']}",
                "edge": p - 1 / PICKEM_2_PAYOUT,
                "legs": f"{a['cand_id']}||{b['cand_id']}",
            }
        )
    return pd.DataFrame(entries)


METHODS = {
    "B0_random": b0_random,
    "C1_chalk": c1_chalk,
    "M1_sharp_price": m1_sharp,
    "M2_goalie_news": m2_goalie,
    "M3_xg_model": m3_xg,
    "M4_shots_model": m4_shots,
    "M5_pickem_entries": m5_entries,
}
