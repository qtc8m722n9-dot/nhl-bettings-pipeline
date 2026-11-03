"""Flaw finder: why picks miss, per method, plus the one-model selection table.

python -m nhlpipe.diagnostics      (run by the morning grading job after the scoreboard)
Writes data/diagnostics.md

For every method (trial period, singles):
  calibration   predicted probability vs actual hit rate (methods that state one)
  slices        market, venue, side, price band, edge band: bets, win %, breakeven,
                units, average CLV -> where it loses and whether the loss is bad luck
                (CLV fine, results bad) or a real flaw (CLV bad too)
  flags         slices with >= MIN_N bets and CLV below -2 pp, or a calibration gap
                above 10 pp -> candidates to investigate / fix
  worst misses  confident picks that lost, with the box-score detail
Selection: CLV with a 95% interval (resampling whole slates), ROI, and the
pre-registered rule for narrowing to one model (see README).
"""
from datetime import date

import numpy as np
import pandas as pd

from .scoreboard import DATA, TRIAL_START

MIN_N = 15
CLV_FLAG = -0.02
CAL_FLAG = 0.10
RULE_MIN_BETS = 300
RULE_DATE = date(2026, 12, 31)


def load() -> pd.DataFrame:
    g = [pd.read_csv(f) for f in sorted((DATA / "graded").glob("*.csv"))]
    if not g:
        return pd.DataFrame()
    g = pd.concat(g, ignore_index=True)
    picks = [pd.read_csv(f) for f in sorted((DATA / "picks").glob("20??-??-??.csv"))]
    p = pd.concat(picks, ignore_index=True)[["date", "method", "pick_no", "side", "line", "est_prob", "edge"]]
    g = g.merge(p, on=["date", "method", "pick_no"], how="left")
    g["date"] = pd.to_datetime(g["date"]).dt.date
    g = g[g["date"] >= TRIAL_START]
    g["clv"] = g["fair_clv"].fillna(g["kalshi_clv"])
    g["won"] = (g["result"] == "win").astype(float)
    g.loc[~g["result"].isin(["win", "loss"]), "won"] = np.nan
    return g


def _boot(df, col, n=1000, seed=5):
    d = df.dropna(subset=[col])
    if len(d) < 10:
        return np.nan, np.nan
    by = [x[col].to_numpy() for _, x in d.groupby("date")]
    rng = np.random.default_rng(seed)
    sums, ns = np.array([b.sum() for b in by]), np.array([len(b) for b in by])
    idx = rng.integers(0, len(by), (n, len(by)))
    v = sums[idx].sum(1) / ns[idx].sum(1)
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def _f(x, pp=False, d=1):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "–"
    return f"{x * 100:+.{d}f}" if pp else f"{x:.{d}%}"


def _slice_table(df: pd.DataFrame, col: str) -> tuple[list[str], list[str]]:
    rows, flags = [], []
    for k, g in df.groupby(col, dropna=False):
        s = g[g["result"].isin(["win", "loss"])]
        if s.empty:
            continue
        clv = g["clv"].mean()
        rows.append(f"| {k} | {len(s)} | {_f(s['won'].mean())} | {_f(s['cost'].mean())} | {s['profit'].sum():+.2f} | {_f(clv, True)} |")
        if len(s) >= MIN_N and pd.notna(clv) and clv < CLV_FLAG and pd.notna(k):
            flags.append(f"{col} = {k}: {len(s)} bets, CLV {clv * 100:+.1f} pp, units {s['profit'].sum():+.2f}")
    return rows, flags


def build() -> None:
    g = load()
    out = DATA / "diagnostics.md"
    if g.empty:
        out.write_text("# Diagnostics\n\nNothing graded in the trial period yet.\n")
        return
    g["side_label"] = np.where(g["market"].isin(["total", "team_total", "p1_total", "player_sog", "player_points", "player_goals"]),
                               np.where(g["side"] == "yes", "over", "under"),
                               np.where(g["side"] == "yes", "yes / favourite side", "no / dog side"))
    g["price_band"] = pd.cut(g["cost"], [0, .35, .45, .55, .65, .75, 1], labels=["<35%", "35-45%", "45-55%", "55-65%", "65-75%", ">75%"])
    g["edge_band"] = pd.cut(g["edge"], [-1, .03, .05, .08, 1], labels=["<3%", "3-5%", "5-8%", ">8%"])
    md = ["# Diagnostics: where the methods miss", "",
          f"Trial period {TRIAL_START} – {max(g['date'])}. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, "
          "in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; "
          "bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts "
          "about half a spread behind.", ""]
    sel = []
    all_flags = []
    for m, d in g[g["bucket"] == "single"].groupby("method"):
        s = d[d["result"].isin(["win", "loss"])]
        lo, hi = _boot(d, "clv")
        rlo, rhi = _boot(s.assign(p=s["profit"]), "p")
        sel.append({"method": m, "bets": len(s), "clv": d["clv"].mean(), "clv_lo": lo, "clv_hi": hi,
                    "roi": s["profit"].mean() if len(s) else np.nan, "roi_lo": rlo, "roi_hi": rhi})
        md += [f"## {m}", ""]
        e = d.dropna(subset=["est_prob", "won"])
        if len(e) >= 5:
            md += ["Calibration (does the stated probability come true?):", "", "| Predicted | n | Avg predicted | Actual |", "|---|--:|--:|--:|"]
            for b, x in e.groupby(pd.cut(e["est_prob"], [0, .4, .5, .6, .7, .8, 1]), observed=True):
                md.append(f"| {b} | {len(x)} | {_f(x['est_prob'].mean())} | {_f(x['won'].mean())} |")
                if len(x) >= MIN_N and abs(x["est_prob"].mean() - x["won"].mean()) > CAL_FLAG:
                    all_flags.append(f"{m}: predicted {x['est_prob'].mean():.0%} in {b} but hit {x['won'].mean():.0%} ({len(x)} bets)")
            md.append("")
        for col, title in (("market", "By market"), ("venue", "By venue"), ("side_label", "By side"),
                           ("price_band", "By price paid"), ("edge_band", "By stated edge")):
            rows, flags = _slice_table(d, col)
            if rows:
                md += [f"{title}:", "", "| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |", "|---|--:|--:|--:|--:|--:|"] + rows + [""]
            all_flags += [f"{m}: {x}" for x in flags]
        miss = d[(d["result"] == "loss")].sort_values("est_prob", ascending=False).head(5)
        if len(miss) and miss["est_prob"].notna().any():
            md += ["Most confident misses:", "", "| Date | Pick | Stated P | Price | Detail |", "|---|---|--:|--:|---|"]
            md += [f"| {r.date} | {r.selection} | {_f(r.est_prob)} | {_f(r.cost)} | {r.detail} |" for r in miss.itertuples()]
            md.append("")
    md[4:4] = (["## Flags to investigate", ""] + ([f"- {x}" for x in all_flags] or ["- none yet (needs at least "
                f"{MIN_N} bets in a slice)"]) + [""])
    sdf = pd.DataFrame(sel).sort_values("clv_lo", ascending=False)
    md += ["## Narrowing to one model", "",
           f"Pre-registered rule: on {RULE_DATE} or once every live method has {RULE_MIN_BETS} settled singles, drop every method "
           "whose CLV 95% interval is entirely below 0; of the rest, keep the one with the highest lower CLV bound, "
           "using ROI only to break ties.", "",
           "| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |", "|---|--:|--:|--:|---|"]
    for r in sdf.to_dict("records"):
        status = "losing to the close" if pd.notna(r["clv_hi"]) and r["clv_hi"] < 0 else (
            "beating the close" if pd.notna(r["clv_lo"]) and r["clv_lo"] > 0 else "undecided")
        md.append(f"| {r['method']} | {r['bets']} | {_f(r['clv'], True, 2)} ({_f(r['clv_lo'], True)}, {_f(r['clv_hi'], True)}) | "
                  f"{_f(r['roi'])} ({_f(r['roi_lo'])}, {_f(r['roi_hi'])}) | {status} |")
    out.write_text("\n".join(md) + "\n")
    print(f"Wrote {out.relative_to(DATA.parent)}")


if __name__ == "__main__":
    build()
