"""Per-method scoreboard from data/graded/*.csv.

Usage: python -m nhlpipe.scoreboard
Writes data/scoreboard.md (readable on GitHub) and data/scoreboard.csv.
Windows: "Last 7 days" (7 slate dates ending on the latest graded date) and
"Season" (everything graded). Singles and parlays / pick'em entries are
scored separately.
"""
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from .methods import METHODS

ET = ZoneInfo("America/New_York")
DATA = Path(__file__).resolve().parent.parent / "data"
BUCKETS = {"single": "Singles", "parlay": "Parlays (3-leg) & pick'em entries (2-pick)"}
SETTLED = {"win", "loss"}


def load() -> pd.DataFrame:
    files = sorted((DATA / "graded").glob("*.csv"))
    if not files:
        return pd.DataFrame()
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def stats(d: pd.DataFrame) -> dict:
    s = d[d["result"].isin(SETTLED)]
    wins = int((s["result"] == "win").sum())
    bets = len(s)
    units = float(s["profit"].sum()) if bets else 0.0
    staked = float(s["stake"].sum()) if bets else 0.0
    clv_rows = d[d["result"].isin(SETTLED | {"void"})]  # CLV is pre-game: voids still count
    fair = clv_rows["fair_clv"].dropna()
    kal = clv_rows["kalshi_clv"].dropna()
    beat = clv_rows["beat_close"].dropna().astype(str).str.lower().map({"true": 1.0, "false": 0.0}).dropna()
    return {
        "bets": bets,
        "wins": wins,
        "losses": bets - wins,
        "voids": int((d["result"] == "void").sum()),
        "win_pct": wins / bets if bets else None,
        "units": units,
        "roi": units / staked if staked else None,
        "avg_fair_clv": float(fair.mean()) if len(fair) else None,
        "n_fair_clv": len(fair),
        "avg_kalshi_clv": float(kal.mean()) if len(kal) else None,
        "n_kalshi_clv": len(kal),
        "beat_close_pct": float(beat.mean()) if len(beat) else None,
        "n_beat_close": len(beat),
    }


def _pct(x, digits=0):
    return "–" if x is None else f"{x:.{digits}%}"


def _pp(x, n):
    return "–" if x is None else f"{x * 100:+.1f} ({n})"


def _beat(r: dict) -> str:
    return "–" if r["beat_close_pct"] is None else f"{r['beat_close_pct']:.0%} ({r['n_beat_close']})"


def _table(rows: list[dict]) -> list[str]:
    out = [
        "| Method | Bets | W-L | Win % | Units | ROI | Avg fair CLV, pp (n) | Avg Kalshi CLV, pp (n) | Beat close (n) | Void |",
        "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|",
    ]
    for r in rows:
        out.append(
            f"| {r['method']} | {r['bets']} | {r['wins']}-{r['losses']} | {_pct(r['win_pct'])} | "
            f"{r['units']:+.2f} | {_pct(r['roi'], 1)} | {_pp(r['avg_fair_clv'], r['n_fair_clv'])} | "
            f"{_pp(r['avg_kalshi_clv'], r['n_kalshi_clv'])} | "
            f"{_beat(r)} | "
            f"{r['voids']} |"
        )
    return out


def build() -> pd.DataFrame:
    df = load()
    md_path, csv_path = DATA / "scoreboard.md", DATA / "scoreboard.csv"
    if df.empty:
        md_path.write_text("# NHL paper-betting scoreboard\n\nNothing graded yet.\n")
        return df
    last = max(df["date"])
    windows = {
        f"Last 7 days ({last - timedelta(days=6):%b %d} – {last:%b %d})": df[df["date"] > last - timedelta(days=7)],
        f"Season ({min(df['date']):%b %d} – {last:%b %d}, {df['date'].nunique()} slates)": df,
    }
    methods = [m for m in METHODS if m in set(df["method"])] + sorted(set(df["method"]) - set(METHODS))
    rows, md = [], [
        "# NHL paper-betting scoreboard",
        "",
        f"Updated {datetime.now(ET):%Y-%m-%d %H:%M} ET · paper only, flat 1 unit per pick / parlay / entry · "
        "judged on CLV first, profit second.",
        "",
    ]
    for wname, wdf in windows.items():
        md += [f"## {wname}", ""]
        for bkey, bname in BUCKETS.items():
            bdf = wdf[wdf["bucket"] == bkey]
            if bdf.empty:
                continue
            trows = []
            for m in methods:
                mdf = bdf[bdf["method"] == m]
                if mdf.empty:
                    continue
                st = {"window": "last_7" if wname.startswith("Last") else "season", "bucket": bkey, "method": m, **stats(mdf)}
                rows.append(st)
                trows.append(st)
            md += [f"### {bname}", ""] + _table(trows) + [""]

    latest = df[df["date"] == last].sort_values(["method", "bucket", "pick_no"], ascending=[True, False, True])
    md += [f"## Latest slate: {last:%a %b %d}", "", "| Method | Pick | Cost | Result | Units | Fair CLV | Kalshi CLV | Detail |", "|---|---|--:|---|--:|--:|--:|---|"]
    for r in latest.to_dict("records"):
        res = r["result"] + (f" ({r['legs_result']})" if isinstance(r.get("legs_result"), str) else "")
        f = lambda x: "–" if pd.isna(x) else f"{x * 100:+.1f}"  # noqa: E731
        u = "–" if pd.isna(r["profit"]) else f"{r['profit']:+.2f}"
        md.append(f"| {r['method']} | {r['selection']} | {r['cost']:.3f} | {res} | {u} | {f(r['fair_clv'])} | {f(r['kalshi_clv'])} | {r['detail']} |")

    open_ = df[df["result"].isin(["pending", "error"])]
    md += [
        "",
        "## Notes",
        "- **Bets / W-L / Win % / Units / ROI** count settled bets only; voids (scratched player, push, postponed game) return the stake.",
        "- **Fair CLV** = sharp no-vig close (Pinnacle, else book consensus) − cost paid (incl. Kalshi fee). "
        "**Kalshi CLV** = Kalshi mid at listed start − price paid. Shown in percentage points; n = bets with a close.",
        "- **Beat close** uses fair CLV where a fair close exists, else Kalshi CLV.",
        "- Parlay / entry CLV uses the product of the legs' closing prices.",
        "- Small samples: a few weeks of bets say little about profit; CLV stabilises much sooner.",
    ]
    if len(open_):
        md.append(f"- **{len(open_)} pick(s) pending or ungraded**: "
                  + "; ".join(f"{r['date']} {r['method']} {r['selection']} ({r['detail']})" for r in open_.head(10).to_dict("records")))
    md_path.write_text("\n".join(md) + "\n")
    out = pd.DataFrame(rows)
    out.to_csv(csv_path, index=False)
    print(f"Wrote {md_path.relative_to(DATA.parent)} and {csv_path.relative_to(DATA.parent)}")
    return out


if __name__ == "__main__":
    build()
