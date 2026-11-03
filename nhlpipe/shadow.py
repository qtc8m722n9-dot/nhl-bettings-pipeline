"""Shadow grading: every priced line, not just the bets.

python -m nhlpipe.shadow [YYYY-MM-DD ...]   (run by the morning grading job)
Writes data/shadow/<date>.csv: one row per candidate (Kalshi, Underdog/PrizePicks,
sportsbook SOG offers) with every model's probability at pick time, the fair
price at pick time, the closing prices, and the result. Bets are a small,
selected slice of this; the full board is what the combined model learns from
and what the flaw finder searches (no selection bias, ~20x more rows).
"""
import re
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from . import grade, results

ET = ZoneInfo("America/New_York")
DATA = Path(__file__).resolve().parent.parent / "data"
KEEP = ["cand_id", "game_key", "venue", "market", "team", "player", "line", "side", "price", "cost",
        "fair_prob", "fair_source", "model_raw", "model_prob", "sog_prob", "mu", "est_prob", "multiplier"]


def build_day(day: date) -> pd.DataFrame | None:
    cp = DATA / "picks" / f"{day}_candidates.csv.gz"
    if not cp.exists():
        return None
    res = results.fetch(day)
    if not res.get("all_final"):
        return None
    c = pd.read_csv(cp)
    c = c[[k for k in KEEP if k in c.columns]].drop_duplicates("cand_id")
    out = [grade.grade_leg(r, res) for r in c.to_dict("records")]
    c["result"] = [x[0] for x in out]
    c["detail"] = [x[1] for x in out]
    clp = DATA / "closing" / f"{day}.csv"
    if clp.exists():
        cl = pd.read_csv(clp)
        cols = [x for x in ("cand_id", "close_fair", "close_mid", "close_bid", "close_ask") if x in cl.columns]
        c = c.merge(cl[cols].drop_duplicates("cand_id"), on="cand_id", how="left")
    c["date"] = day.isoformat()
    c["y"] = c["result"].map({"win": 1, "loss": 0})
    path = DATA / "shadow" / f"{day}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    c.to_csv(path, index=False)
    print(f"{day}: shadow-graded {len(c)} lines {c['result'].value_counts().to_dict()}, "
          f"with close {c.get('close_fair', pd.Series(dtype=float)).notna().sum()} fair / {c.get('close_mid', pd.Series(dtype=float)).notna().sum()} Kalshi")
    return c


def main(argv: list[str]) -> None:
    days = [date.fromisoformat(a) for a in argv if re.fullmatch(r"\d{4}-\d{2}-\d{2}", a)]
    if not days:
        today = datetime.now(ET).date()
        have = {p.stem for p in (DATA / "shadow").glob("*.csv")}
        days = [date.fromisoformat(p.name[:10]) for p in sorted((DATA / "picks").glob("*_candidates.csv.gz"))
                if p.name[:10] not in have and date.fromisoformat(p.name[:10]) < today]
    for d in days:
        build_day(d)


if __name__ == "__main__":
    main(sys.argv[1:])
