"""Grade locked paper picks from final NHL results.

Usage: python -m nhlpipe.grade [YYYY-MM-DD ...] [--no-backfill]
  no dates: grade every past date in data/picks/ that isn't fully graded yet
Reads:  data/picks/<date>.csv (+ _candidates.csv.gz for parlay / entry legs)
        data/closing/<date>.csv, data/results/<date>.json (fetched if missing)
Writes: data/graded/<date>.csv, then rebuilds data/scoreboard.md / .csv

Settlement rules (paper, flat 1 unit per pick / parlay / entry):
  game markets   final score as the NHL records it: OT counts, a shootout
                 adds 1 goal for the winner (same as Kalshi's rules)
  1st period     1st-period goals only
  player props   boxscore goals / points / shots (regulation + OT, never
                 shootout); a player who doesn't dress or logs no ice time
                 -> void
  singles        win pays 1/cost - 1 (cost includes Kalshi fees; for pick'em
                 legs it is the per-pick breakeven), loss -1, void 0
  3-leg parlays  void legs drop out and the parlay is repriced on the rest;
                 all legs void -> void
  2-pick entries both hit -> +2 (3x payout); any miss -> -1; any void leg ->
                 whole entry refunded (both apps refund a 2-pick that loses a leg)
  postponed / cancelled game -> void
CLV per pick:
  fair CLV   = close_fair - cost   (parlays/entries: product of leg closes - cost)
  Kalshi CLV = close_mid  - price  (Kalshi only; parlays only if every leg is Kalshi)
  beat close = fair CLV > 0 where a fair close exists, else Kalshi CLV > 0
"""
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from . import closing, results, scoreboard
from .methods import PICKEM_2_PAYOUT, split_legs
from .names import norm

ET = ZoneInfo("America/New_York")
DATA = Path(__file__).resolve().parent.parent / "data"
VOID_STATES = {"PPD", "CNCL", "SUSP"}
STAT = {"player_goals": "goals", "player_points": "points", "player_sog": "sog"}

GRADED_COLS = [
    "date", "method", "pick_no", "bucket", "venue", "game_key", "market", "selection",
    "price", "cost", "stake", "result", "profit", "legs_result",
    "close_fair", "fair_clv", "close_mid", "kalshi_clv", "beat_close", "detail", "cand_id",
]

_rosters: dict[str, set[str]] = {}


def _num(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(x) else x


def _find_player(name: str, g: dict) -> dict | None:
    players = g["players"]
    n = norm(name)
    if n in players:
        return players[n]
    parts = n.split(" ")
    if len(parts) < 2:
        return None
    first, last = parts[0], " ".join(parts[1:])
    hits = [p for k, p in players.items() if k.endswith(" " + last) and k[:1] == first[:1]]
    return hits[0] if len(hits) == 1 else None


def _on_roster(name: str, g: dict) -> bool:
    n = norm(name)
    for t in (g["home"], g["away"]):
        if t not in _rosters:
            _rosters[t] = results.roster_names(t)
        if n in _rosters[t]:
            return True
    return False


def grade_leg(c: dict, res: dict) -> tuple[str, str]:
    """One bet -> ('win' | 'loss' | 'void' | 'pending' | 'error', detail)."""
    g = res["games"].get(c["game_key"])
    if g is None:
        return "error", "game not found in NHL results"
    if g["state"] in VOID_STATES:
        return "void", f"game {g['state']}"
    if not g["final"]:
        return "pending", f"game state {g['state']}"
    m, line = c["market"], _num(c.get("line"))
    team = c.get("team") if isinstance(c.get("team"), str) else None
    score = {g["home"]: g["home_score"], g["away"]: g["away_score"]}
    p1 = {g["home"]: g["p1_home"], g["away"]: g["p1_away"]}
    opp = {g["home"]: g["away"], g["away"]: g["home"]}
    fs = f"{g['away']} {g['away_score']}-{g['home_score']} {g['home']}" + (f" ({g['last_period']})" if g["last_period"] != "REG" else "")
    if m == "ml":
        val, detail = score[team] > score[opp[team]], fs
    elif m == "spread":
        val, detail = score[team] - score[opp[team]], fs
    elif m == "total":
        val, detail = score[g["home"]] + score[g["away"]], fs
    elif m == "team_total":
        val, detail = score[team], fs
    elif m == "p1_result":
        detail = f"1P {g['away']} {g['p1_away']}-{g['p1_home']} {g['home']}"
        val = p1[g["home"]] == p1[g["away"]] if team == "TIE" else p1[team] > p1[opp[team]]
    elif m == "p1_total":
        val, detail = g["p1_home"] + g["p1_away"], f"1P {g['p1_away']}-{g['p1_home']}"
    elif m in STAT:
        name = c.get("player")
        p = _find_player(str(name), g)
        if p is None:
            if _on_roster(str(name), g):
                return "void", f"{name} did not dress"
            return "error", f"{name} not matched to boxscore"
        if p["toi_sec"] == 0:
            return "void", f"{name} no ice time"
        val, detail = p[STAT[m]], f"{p['name']} {p[STAT[m]]} {STAT[m]}"
    else:
        return "error", f"unknown market {m}"
    if isinstance(val, bool):
        happened = val
    else:
        if line is None:
            return "error", "no line"
        if val == line:
            return "void", detail + " (push)"
        happened = val > line
    won = happened if c["side"] == "yes" else not happened
    return ("win" if won else "loss"), detail


def _prod(xs):
    out = 1.0
    for x in xs:
        if x is None:
            return None
        out *= x
    return out


def grade_day(day: date, backfill: bool = True) -> pd.DataFrame | None:
    pp = DATA / "picks" / f"{day.isoformat()}.csv"
    if not pp.exists():
        return None
    picks = pd.read_csv(pp)
    cands = pd.read_csv(DATA / "picks" / f"{day.isoformat()}_candidates.csv.gz").set_index("cand_id")
    res = results.fetch(day)
    if backfill and res.get("all_final"):
        try:
            closing.backfill(day)
        except Exception as e:  # noqa: BLE001
            print(f"Kalshi backfill failed: {e}")
    cp = DATA / "closing" / f"{day.isoformat()}.csv"
    close = pd.read_csv(cp).set_index("cand_id") if cp.exists() else pd.DataFrame()

    def cl(cid: str, col: str):
        return _num(close.at[cid, col]) if (len(close) and cid in close.index and col in close) else None

    def leg(cid: str) -> dict:
        if cid in cands.index:
            return {"cand_id": cid, **cands.loc[cid].to_dict()}
        return {"cand_id": cid, "market": "?"}

    out = []
    for r in picks.to_dict("records"):
        cid = r["cand_id"]
        stake = _num(r.get("stake")) or 1.0
        cost, price = _num(r["cost"]), _num(r["price"])
        rec = {k: r.get(k) for k in ("date", "method", "pick_no", "venue", "game_key", "market", "selection", "cand_id")}
        rec.update(price=price, cost=cost, stake=stake)
        if cid.startswith(("parlay|", "entry|")):
            legs = [leg(x) for x in split_legs(r["legs"])]
            graded = [grade_leg(lg, res) for lg in legs]
            res_list = [x[0] for x in graded]
            rec["bucket"] = "parlay"
            rec["legs_result"] = ",".join({"win": "W", "loss": "L", "void": "V", "pending": "P", "error": "E"}[x] for x in res_list)
            rec["detail"] = " | ".join(d for _, d in graded)
            entry = cid.startswith("entry|")
            if "error" in res_list:
                result = "error"
            elif "pending" in res_list:
                result = "pending"
            elif entry and "void" in res_list:
                result = "void"
            elif "loss" in res_list:
                result = "loss"
            elif all(x == "void" for x in res_list):
                result = "void"
            else:
                result = "win"
            if result == "win":
                if entry:
                    profit = stake * (PICKEM_2_PAYOUT - 1)
                else:
                    eff = _prod([_num(lg.get("cost")) for lg, x in zip(legs, res_list) if x == "win"])
                    profit = stake * (1 / eff - 1) if eff else None
            else:
                profit = {"loss": -stake, "void": 0.0}.get(result)
            fair_close = _prod([cl(lg["cand_id"], "close_fair") for lg in legs])
            rec["close_fair"] = fair_close
            rec["fair_clv"] = None if fair_close is None or cost is None else fair_close - cost
            if all(lg.get("venue") == "kalshi" for lg in legs):
                mid = _prod([cl(lg["cand_id"], "close_mid") for lg in legs])
                px = _prod([_num(lg.get("price")) for lg in legs])
                rec["close_mid"] = mid
                rec["kalshi_clv"] = None if mid is None or px is None else mid - px
        else:
            rec["bucket"] = "single"
            result, rec["detail"] = grade_leg(r, res)
            profit = {"win": stake * (1 / cost - 1) if cost else None, "loss": -stake, "void": 0.0}.get(result)
            rec["close_fair"] = cl(cid, "close_fair")
            rec["fair_clv"] = None if rec["close_fair"] is None or cost is None else rec["close_fair"] - cost
            if r["venue"] == "kalshi":
                rec["close_mid"] = cl(cid, "close_mid")
                rec["kalshi_clv"] = None if rec["close_mid"] is None or price is None else rec["close_mid"] - price
        rec["result"], rec["profit"] = result, profit
        fc, kc = rec.get("fair_clv"), rec.get("kalshi_clv")
        rec["beat_close"] = (fc > 0) if fc is not None else ((kc > 0) if kc is not None else None)
        out.append(rec)

    df = pd.DataFrame(out)
    for col in GRADED_COLS:
        if col not in df:
            df[col] = None
    df = df[GRADED_COLS]
    path = DATA / "graded" / f"{day.isoformat()}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    n = df["result"].value_counts().to_dict()
    print(f"{day}: graded {len(df)} picks {n}  units {df['profit'].sum():+.2f}")
    return df


def _needs_grading(day: date) -> bool:
    path = DATA / "graded" / f"{day.isoformat()}.csv"
    if not path.exists():
        return True
    g = pd.read_csv(path)
    return g["result"].isin(["pending", "error"]).any()


def pick_dates() -> list[date]:
    out = []
    for p in (DATA / "picks").glob("*.csv"):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.csv", p.name):
            out.append(date.fromisoformat(p.stem))
    return sorted(out)


def main(argv: list[str]) -> None:
    today = datetime.now(ET).date()
    days = [date.fromisoformat(a) for a in argv if re.fullmatch(r"\d{4}-\d{2}-\d{2}", a)]
    if not days:
        days = [d for d in pick_dates() if d < today and _needs_grading(d)]
    if not days:
        print("Nothing new to grade.")
    for d in days:
        grade_day(d, backfill="--no-backfill" not in argv)
    scoreboard.build()


if __name__ == "__main__":
    main(sys.argv[1:])
