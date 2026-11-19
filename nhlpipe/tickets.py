"""H22 (docs/hypotheses_2026-11-19_tickets.md): 6-leg ticket test - leg quality vs ticket count. Paper only.

  T1_tickets_fair   as many 6-leg tickets as the night allows from legs priced AT OR BETTER than Pinnacle's
                    no-vig fair (fair 55-65%), best edge first
  T2_tickets_all20  20 six-leg tickets from ALL priced 55-65% legs (any price), random order (seeded by date)
Both: no leg used twice, one leg per game within a ticket, the same bet at several venues counts once (cheapest
price kept), PrizePicks excluded. Ticket price = product of leg prices; 1 unit per ticket.
"""
from datetime import date

import numpy as np
import pandas as pd

LEGS, FAIR_LO, FAIR_HI, T2_TICKETS = 6, 0.55, 0.65, 20


def _pool(c: pd.DataFrame) -> pd.DataFrame:
    p = c[c["fair_prob"].between(FAIR_LO, FAIR_HI) & c["cost"].notna() & (c["venue"] != "prizepicks")].copy()
    p["who"] = p["player_key"].fillna(p["team"]).fillna("")
    p = p.sort_values("cost").drop_duplicates(["game_key", "market", "who", "line", "side"])
    p["edge_fair"] = p["fair_prob"] - p["cost"]
    return p


def _tickets(legs: pd.DataFrame, max_tickets: int) -> list[list[dict]]:
    rows, out = legs.to_dict("records"), []
    used = set()
    while len(out) < max_tickets:
        t, games = [], set()
        for i, r in enumerate(rows):
            if i in used or r["game_key"] in games:
                continue
            t.append(i)
            games.add(r["game_key"])
            if len(t) == LEGS:
                break
        if len(t) < LEGS:
            break
        used |= set(t)
        out.append([rows[i] for i in t])
    return out


def _row(legs: list[dict]) -> dict:
    cost = float(np.prod([lg["cost"] for lg in legs]))
    fair = float(np.prod([lg["fair_prob"] for lg in legs]))
    venues = {lg["venue"] for lg in legs}
    return {"cand_id": "parlay|" + "||".join(lg["cand_id"] for lg in legs), "game_key": " + ".join(lg["game_key"] for lg in legs),
            "venue": venues.pop() if len(venues) == 1 else "mixed", "market": f"parlay_{LEGS}",
            "selection": "  +  ".join(lg["selection"] for lg in legs), "side": "yes", "line": None, "team": None,
            "ticker": None, "player": None, "price": cost, "cost": cost, "american": round((1 / cost - 1) * 100),
            "est_prob": fair, "est_source": "product_of_pinnacle_fair", "edge": fair - cost,
            "legs": "||".join(lg["cand_id"] for lg in legs)}


def picks(day: date, c: pd.DataFrame) -> pd.DataFrame:
    p = _pool(c)
    if p.empty:
        return pd.DataFrame()
    a = p[p["edge_fair"] >= 0].sort_values(["edge_fair", "cand_id"], ascending=[False, True])
    b = p.sample(frac=1, random_state=int(day.strftime("%Y%m%d")))
    out = []
    for name, legs, n in (("T1_tickets_fair", a, 10 ** 6), ("T2_tickets_all20", b, T2_TICKETS)):
        t = pd.DataFrame([_row(x) for x in _tickets(legs, n)])
        if len(t):
            t["method"] = name
            t["pick_no"] = range(1, len(t) + 1)
            out.append(t)
    pk = pd.concat(out, ignore_index=True) if out else pd.DataFrame()
    print(f"tickets: pool {len(p)} legs ({len(a)} at/better than fair); "
          + ", ".join(f"{n} {(pk['method'] == n).sum() if len(pk) else 0}" for n in ("T1_tickets_fair", "T2_tickets_all20")))
    return pk
