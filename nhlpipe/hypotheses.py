"""Pre-registered hypotheses, graded on the shadow board.

python -m nhlpipe.hypotheses     (run by the morning grading job after shadow grading)
Writes data/hypotheses.md.

A hypothesis is written down here, with its population, metric and decision rule,
BEFORE any game it is judged on has been played. Do not edit a registered spec;
add a new version with a new registration date instead.

H1 away back-to-back (registered 2026-11-05 ~16:10 ET, before that night's games; Evan approved)
  Lead: Bullseye research, 2025-26: when only the away team was on a back-to-back the home
  team won 60.6% vs Pinnacle 56.3% (254 games); Bullseye's 2023-25 fit (a_b2b +0.34) agrees.
  Population: every game from the 2026-11-05 slate on where the away team played the day
  before and the home team did not (slate flags at pick lock), with a pick-time fair moneyline.
  Primary metric: mean(home win - pick-time fair P(home win)), 95% bootstrap CI.
  Secondary: close move = mean(closing fair - pick-time fair) for the home side (does the
  market correct before puck drop?); paper ROI buying the home side on Kalshi at pick-time cost.
  Control: the same metrics on games where neither team is on a back-to-back.
  Decision: 2026-12-31 is an interim look only (expected ~60-90 games; a 4-pt effect is about
  0.8 SE there). Promote to a betting rule only if, at season end or once n >= 400, the primary
  CI lower bound is > 0 AND the gap over the control is positive. Otherwise it stays a
  combined-model input (a_b2b).
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
H1_START = "2026-11-05"
N_BOOT = 4000


def _home_rows(day: str) -> pd.DataFrame | None:
    """One row per game: pick-time fair, close fair and result for the HOME side, plus b2b flags."""
    sp, sl = DATA / "shadow" / f"{day}.csv", DATA / "slates" / f"{day}.csv"
    if not sp.exists() or not sl.exists():
        return None
    s = pd.read_csv(sp)
    s = s[(s["market"] == "ml") & s["fair_prob"].notna() & s["y"].notna()].copy()
    if s.empty:
        return None
    s["home"] = s["game_key"].str.split("@").str[1]
    # A row is "home wins" if it is home YES or away NO; otherwise flip it.
    is_home_side = (s["team"] == s["home"]) == (s["side"] == "yes")
    flip = lambda x: x.where(is_home_side, 1 - x)  # noqa: E731
    s["p_fair"] = flip(s["fair_prob"])
    s["p_close"] = flip(s["close_fair"]) if "close_fair" in s else np.nan
    s["home_win"] = flip(s["y"])
    # Kalshi cost of the home side at pick time: only rows that ARE the home side carry it.
    s["home_cost"] = s["cost"].where(is_home_side)
    g = s.groupby("game_key").agg(p_fair=("p_fair", "mean"), p_close=("p_close", "mean"),
                                  home_win=("home_win", "first"), home_cost=("home_cost", "min")).reset_index()
    sl = pd.read_csv(sl)
    sl["game_key"] = sl["away"] + "@" + sl["home"]
    g = g.merge(sl[["game_key", "home_b2b", "away_b2b"]], on="game_key", how="left")
    g["date"] = day
    return g


def _ci(x: np.ndarray, seed=11) -> tuple[float, float]:
    if len(x) < 5:
        return (np.nan, np.nan)
    rng = np.random.default_rng(seed)
    m = rng.choice(x, (N_BOOT, len(x))).mean(axis=1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def _summary(d: pd.DataFrame) -> dict:
    e = (d["home_win"] - d["p_fair"]).to_numpy()
    mv = (d["p_close"] - d["p_fair"]).dropna().to_numpy()
    b = d[d["home_cost"].notna()]
    roi = ((b["home_win"] / b["home_cost"]) - 1).mean() if len(b) else np.nan
    lo, hi = _ci(e)
    return {"n": len(d), "win": d["home_win"].mean(), "fair": d["p_fair"].mean(), "edge": e.mean() if len(e) else np.nan,
            "lo": lo, "hi": hi, "move": mv.mean() if len(mv) else np.nan, "n_move": len(mv),
            "roi": roi, "n_roi": len(b)}


def build() -> pd.DataFrame:
    days = sorted(p.stem for p in (DATA / "shadow").glob("*.csv") if p.stem >= H1_START)
    rows = [r for r in (_home_rows(d) for d in days) if r is not None]
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def report() -> str:
    g = build()
    pct = lambda x: "–" if pd.isna(x) else f"{100 * x:+.1f}"  # noqa: E731
    lines = ["# Pre-registered hypotheses", "",
             "Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. "
             "Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.", "",
             "## H1: away team on a back-to-back (registered 2026-11-05)", "",
             "Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; "
             "a verdict needs ~400 games.", ""]
    if g.empty:
        lines.append("No graded games yet.")
    else:
        bb = g["home_b2b"].astype(str).str.lower() == "true"
        ab = g["away_b2b"].astype(str).str.lower() == "true"
        groups = {"Only away on b2b (H1)": g[ab & ~bb], "Neither on b2b (control)": g[~ab & ~bb]}
        lines += ["| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |",
                  "|---|--:|--:|--:|--:|--:|--:|--:|"]
        for name, d in groups.items():
            if d.empty:
                lines.append(f"| {name} | 0 | – | – | – | – | – | – |")
                continue
            s = _summary(d)
            ci = "–" if pd.isna(s["lo"]) else f"{pct(s['lo'])} to {pct(s['hi'])}"
            lines.append(f"| {name} | {s['n']} | {100 * s['win']:.1f}% | {100 * s['fair']:.1f}% | {pct(s['edge'])} | {ci} | "
                         f"{pct(s['move'])} ({s['n_move']}) | {pct(s['roi'])}% ({s['n_roi']}) |")
        lines += ["", f"Games with a fair moneyline since {H1_START}: {len(g)}; dates {g['date'].min()} – {g['date'].max()}."]
    out = "\n".join(lines) + "\n"
    (DATA / "hypotheses.md").write_text(out)
    return out


if __name__ == "__main__":
    print(report())
