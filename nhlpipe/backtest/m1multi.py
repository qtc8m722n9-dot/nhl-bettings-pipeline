"""M1 sharp price at several snapshots per day (2025-26 archive).

python -m nhlpipe.backtest.cli m1multi START END [--props-late]

Snapshots (ET): 11:00, 13:50 (already cached), 16:30, 18:30. At each one, M1's
live rule runs on games starting at least 10 minutes later: power de-vigged
Pinnacle (else 2+ book consensus) vs every venue price, edge 2.5-10% on game
markets and 4-15% on props. A game can be bet once per day (first snapshot
where it qualifies). Game markets at every snapshot; player props at 13:50
(cached) and, with --props-late, also at 18:30.
Closing: Pinnacle ~2 min before each game (pulled only for bet games).
Writes data/backtest/m1multi/<date>.csv and data/backtest/m1multi/report.md
"""
from datetime import datetime, time, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .. import fair, grade, methods
from . import nhldata, oddshist
from . import pipeline as P
from .features import results_dict

OUT = P.OUT / "m1multi"
SNAPS = [time(11, 0), time(13, 50), time(16, 30), time(18, 30)]
LEAD = timedelta(minutes=10)


def _snap_dt(d, t):
    return datetime.combine(d, t, P.ET)


def run(start: str, end: str, *flags) -> None:
    props_late = "--props-late" in flags
    days = P._dates(start, end)
    recs = nhldata.load_range(nhldata.SEASON_START, days[-1])
    names = nhldata.rosters()
    grade._rosters.clear()
    for p in names.values():
        for t in p["teams"]:
            grade._rosters.setdefault(t, set()).add(P.norm(p["name"]))
    OUT.mkdir(parents=True, exist_ok=True)
    for d in days:
        rec = recs.get(d.isoformat())
        if not rec or not rec["games"]:
            continue
        res = results_dict(rec)
        bet_games, rows = set(), []
        for t in SNAPS:
            ts = _snap_dt(d, t)
            iso = P._iso(ts)
            try:
                feat = oddshist.featured(iso)
            except oddshist.BudgetExceeded as e:
                print(e)
                return _finish()
            evs = [e for e in (feat.get("data") or []) if P._utc(e["commence_time"]).astimezone(P.ET).date() == d
                   and P._utc(e["commence_time"]) > ts + LEAD]
            resp = [(feat, {e["id"] for e in evs})]
            if t == time(13, 50) or (props_late and t == time(18, 30)):
                for e in evs:
                    resp.append((oddshist.event_odds(e["id"], iso), {e["id"]}))
            od = P.odds_frame(resp, P.TMAP)
            if od.empty:
                continue
            gks = {f"{e_a}@{e_h}" for e_a, e_h in zip(od["away"], od["home"])} - bet_games
            c = P.candidates(od, gks)
            if c.empty:
                continue
            table = fair.lookup_table(fair.devig(od))
            fp = [fair.fair_prob(r, table) for r in c.to_dict("records")]
            c["fair_prob"], c["fair_source"] = [p for p, _ in fp], [s for _, s in fp]
            pk = methods.m1_sharp(c, d)
            if pk is None or pk.empty:
                continue
            for r in pk.to_dict("records"):
                if r["game_key"] in bet_games:
                    continue
                bet_games.add(r["game_key"])
                r["snapshot_et"] = t.strftime("%H:%M")
                rows.append(r)
        if not rows:
            continue
        b = pd.DataFrame(rows)
        # closing (Pinnacle, ~2 min before each bet game)
        close = []
        for r in b.to_dict("records"):
            ciso = P._iso(P._utc(r["commence_utc"]) - P.CLOSE_LEAD)
            if r["market"] in methods.PROP_MARKETS:
                close.append((oddshist.event_odds(r["event_id"], ciso), {r["event_id"]}))
            else:
                close.append((oddshist.featured(ciso), {r["event_id"]}))
        cod = P.odds_frame(close, P.TMAP)
        _, ptab = P._tables(cod)
        out = []
        for r in b.to_dict("records"):
            cp = fair.fair_prob(r, ptab)[0] if ptab else None
            result, detail = grade.grade_leg(r, res)
            profit = {"win": 1 / r["cost"] - 1, "loss": -1.0, "void": 0.0}.get(result)
            out.append({"date": d.isoformat(), "snapshot_et": r["snapshot_et"], "venue": r["venue"], "game_key": r["game_key"],
                        "market": r["market"], "selection": r["selection"], "cost": r["cost"], "fair_prob": r["fair_prob"],
                        "edge": r["edge"], "fair_source": r["fair_source"], "result": result, "profit": profit,
                        "close_pinnacle": cp, "clv": None if cp is None else cp - r["cost"], "detail": detail,
                        "cand_id": r["cand_id"]})
        pd.DataFrame(out).to_csv(OUT / f"{d}.csv", index=False)
        print(f"{d}: {len(out)} M1 bets {pd.DataFrame(out)['snapshot_et'].value_counts().to_dict()} credits {oddshist.SPENT}")
    _finish()


def _finish() -> None:
    files = sorted(OUT.glob("20*.csv"))
    if not files:
        print("no bets")
        return
    b = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    md = [f"# M1 sharp price, several snapshots a day ({b['date'].min()} – {b['date'].max()})", "",
          "| Snapshot (ET) | Bets | Game mkts | Props | Win % | Breakeven | ROI | Avg CLV vs Pinnacle close, pp | Beat close |",
          "|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for k, g in list(b.groupby("snapshot_et")) + [("all", b)]:
        s = g[g["result"].isin(["win", "loss"])]
        c = g.dropna(subset=["clv"])
        md.append(f"| {k} | {len(g)} | {(~g['market'].isin(methods.PROP_MARKETS)).sum()} | {g['market'].isin(methods.PROP_MARKETS).sum()} | "
                  f"{(s['result'] == 'win').mean():.1%} | {s['cost'].mean():.1%} | {s['profit'].mean():+.1%} | "
                  f"{c['clv'].mean() * 100:+.2f} (n={len(c)}) | {(c['clv'] > 0).mean():.0%} |")
    md += ["", f"Credits this run: {oddshist.SPENT}", ""]
    (OUT / "report.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
