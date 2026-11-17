"""Tests of pre-registered H7-H9 (docs/hypotheses_2026-11-17.md). No API calls.
python -m nhlpipe.patterns.hyp2 -> data/patterns/hypotheses_h7_h9.md

Deviation from the H8 text, stated before running: MoneyPuck logs have no separate 5-on-3 situation,
so team PP time per game = (sum of the team's skaters' PP time) / 5, from the same NHL stats source.
"""
from datetime import date

import numpy as np
import pandas as pd
from scipy import stats

from .data import DATA, OUT
from .scan import _z, load, trend
from ..shots2 import pull as spull

SEASONS = ["20242025", "20252026", "20262027"]


def _stats() -> pd.DataFrame:
    st = pd.concat([spull.load_stats(s) for s in SEASONS], ignore_index=True)
    st["season"] = st["gameId"] // 1_000_000
    st["date"] = pd.to_datetime(st["gameDate"]).dt.date
    return st


# ------------------------------------------------------------------ H7 ----
def pull_proxy(dates) -> pd.DataFrame:
    st = _stats()
    eng = st.groupby(["gameId", "teamAbbrev", "opponentTeamAbbrev"])["emptyNetGoals"].sum().reset_index()
    eng = eng.rename(columns={"teamAbbrev": "scorer", "opponentTeamAbbrev": "team", "emptyNetGoals": "eng_against"})
    m = pd.read_csv(DATA / "shots2" / "mp_teams.csv.gz")
    a = m[m["situation"] == "all"][["gameId", "team", "season", "gameDate", "goalsFor", "goalsAgainst"]].copy()
    a["d"] = pd.to_datetime(a["gameDate"].astype(str)).dt.date
    a = a.merge(eng[["gameId", "team", "eng_against"]], on=["gameId", "team"], how="left").fillna({"eng_against": 0})
    a["reg_loss"] = (a["goalsFor"] < a["goalsAgainst"]).astype(int)  # MP 'all' excludes the shootout goal; OT losses are 1-goal
    out = []
    for D in sorted(set(dates)):
        S = D.year if D.month >= 8 else D.year - 1
        w = a[(a["season"] == S - 1) | ((a["season"] == S) & (a["d"] < D))]
        g = w.groupby("team")[["eng_against", "reg_loss"]].sum()
        lg = g["eng_against"].sum() / g["reg_loss"].sum()
        g["pull_proxy"] = (g["eng_against"] + 20 * lg) / (g["reg_loss"] + 20)
        g = g.reset_index()
        g["date"] = D
        out.append(g[["team", "date", "pull_proxy"]])
    return pd.concat(out, ignore_index=True)


def h7(T) -> list[str]:
    g = T["games"].copy()
    g = g[g["pl_fav"].notna() & g["y_pl_fav"].notna() & g["pl_fav_fair"].notna()]
    g["dog"] = np.where(g["pl_fav"] == g["home"], g["away"], g["home"])
    pp = pull_proxy(list(g["date"]))
    g = g.merge(pp.rename(columns={"team": "dog", "pull_proxy": "dog_pull"}), on=["dog", "date"], how="left")
    out = ["Pull proxy = empty-net goals a team conceded per regulation loss (previous + current season before the game, "
           "shrunk to the league rate with 20 losses). Higher = its coach pulls earlier or more often.", "",
           "| Sample | Games | Primary: trend z, fav -1.5 on the underdog's pull proxy | Fav -1.5 edge, top third, pts (z) | "
           "Fav -1.5 edge, bottom third, pts (z) | Secondary: trend z, over |", "|---|--:|--:|--:|--:|--:|"]
    lo, hi = g.loc[g["split"] == "discovery", "dog_pull"].quantile([1 / 3, 2 / 3])
    res = {}
    for sp in ("discovery", "holdout", "live"):
        q = g[g["split"] == sp].dropna(subset=["dog_pull"])
        _, z = trend(q["y_pl_fav"].to_numpy(float), q["pl_fav_fair"].to_numpy(float), q["dog_pull"].to_numpy(float))
        o = q.dropna(subset=["y_over", "over_fair"])
        _, zo = trend(o["y_over"].to_numpy(float), o["over_fair"].to_numpy(float), o["dog_pull"].to_numpy(float))
        a, b = q[q["dog_pull"] > hi], q[q["dog_pull"] <= lo]
        ea, eb = _z(a["y_pl_fav"].to_numpy(float), a["pl_fav_fair"].to_numpy(float), None), _z(b["y_pl_fav"].to_numpy(float), b["pl_fav_fair"].to_numpy(float), None)
        res[sp] = z
        out.append(f"| {sp} | {len(q)} | {z:+.2f} | {100 * ea[0]:+.1f} ({ea[1]:+.2f}) | {100 * eb[0]:+.1f} ({eb[1]:+.2f}) | {zo:+.2f} |")
    p = stats.norm.sf(res["holdout"])
    out += ["", f"Rule: discovery z > 0 and holdout one-sided p < 0.05. Holdout p = {p:.3f} -> "
            f"**{'PASSES' if res['discovery'] > 0 and p < 0.05 else 'does not pass'}**.", "",
            "Highest pull proxies now: " + ", ".join(f"{r.team} {r.pull_proxy:.2f}" for r in
                                                       pp[pp['date'] == pp['date'].max()].sort_values('pull_proxy', ascending=False).head(5).itertuples()) +
            "; lowest: " + ", ".join(f"{r.team} {r.pull_proxy:.2f}" for r in
                                      pp[pp['date'] == pp['date'].max()].sort_values('pull_proxy').head(5).itertuples()) + "."]
    return out


# ---------------------------------------------------------- H8 and H9 ----
def player_features() -> pd.DataFrame:
    st = _stats().sort_values(["playerId", "date", "gameId"]).reset_index(drop=True)
    team_pp = st.groupby(["gameId", "teamAbbrev"])["ppTimeOnIce"].sum().rename("team_pp_sec") / 5
    st = st.merge(team_pp.reset_index(), on=["gameId", "teamAbbrev"], how="left")
    st["pp_share"] = np.where(st["team_pp_sec"] > 0, st["ppTimeOnIce"] / st["team_pp_sec"], np.nan)
    g = st.groupby(["playerId", "season"])
    # H8: last 3 games vs the 17 before them (strictly earlier games)
    s1 = g["pp_share"].shift(1)
    st["_s"] = s1
    gg = st.groupby(["playerId", "season"])["_s"]
    last3 = gg.transform(lambda x: x.rolling(3, min_periods=3).mean())
    prev17 = gg.transform(lambda x: x.shift(3).rolling(17, min_periods=8).mean())
    st["pp_shift"] = last3 - prev17
    # H9: finishing luck per game, season to date
    st["g_cum"] = g["goals"].cumsum() - st["goals"]
    st["s_cum"] = g["shots"].cumsum() - st["shots"]
    st["gp_cum"] = g.cumcount()
    prev = st.groupby(["playerId", "season"])[["goals", "shots"]].sum().reset_index()
    prev["season"] += 1
    prev = prev.rename(columns={"goals": "pg", "shots": "ps"})
    st = st.merge(prev, on=["playerId", "season"], how="left").fillna({"pg": 0, "ps": 0})
    st["D"] = (st["positionCode"] == "D").astype(int)
    lg = st.groupby(["season", "D"])[["goals", "shots"]].sum()
    lg = (lg["goals"] / lg["shots"]).rename("lg_sh").reset_index()
    st = st.merge(lg, on=["season", "D"], how="left")
    st["exp_sh"] = (st["pg"] + 223 * st["lg_sh"]) / (st["ps"] + 223)
    st["finish_luck"] = np.where(st["gp_cum"] > 0, (st["g_cum"] - st["s_cum"] * st["exp_sh"]) / st["gp_cum"], np.nan)
    return st[["playerId", "date", "pp_shift", "finish_luck"]]


def _trend_rows(P, col, label, mask=None) -> tuple[list[str], dict]:
    rows, res = [], {}
    for sp in ("discovery", "holdout", "live"):
        q = P[(P["split"] == sp)].dropna(subset=["y", "fair_over", col])
        if mask is not None:
            q = q[mask(q)]
        _, z = trend(q["y"].to_numpy(float), q["fair_over"].to_numpy(float), q[col].to_numpy(float), q["gid"].to_numpy())
        res[sp] = z
        rows.append(f"| {label} | {sp} | {len(q):,} | {z:+.2f} |")
    return rows, res


def h8_h9(T) -> tuple[list[str], list[str]]:
    F = player_features()
    P = T["points"].merge(F, on=["playerId", "date"], how="left")
    S = T["sog"].merge(F, on=["playerId", "date"], how="left")
    h8 = ["PP share = player PP time / team PP time; shift = last 3 games minus the 17 before. Positive z = overs beat the price "
          "after a promotion.", "", "| Test | Sample | Lines | Trend z |", "|---|---|--:|--:|"]
    r, res = _trend_rows(P, "pp_shift", "Primary: points overs")
    h8 += r
    r, _ = _trend_rows(S, "pp_shift", "Secondary: SOG overs")
    h8 += r
    r, _ = _trend_rows(P, "pp_shift", "Secondary: defencemen points overs", lambda q: q["D"] == 1)
    h8 += r
    p = stats.norm.sf(res["holdout"])
    h8 += ["", f"Rule: discovery z > 0 and holdout one-sided p < 0.05. Holdout p = {p:.3f} -> "
           f"**{'PASSES' if res['discovery'] > 0 and p < 0.05 else 'does not pass'}**.", ""]
    # big promotions as a slice (descriptive)
    for sp in ("discovery", "holdout", "live"):
        q = P[(P["split"] == sp) & (P["pp_shift"] >= 0.15)]
        e = _z(q["y"].to_numpy(float), q["fair_over"].to_numpy(float), q["gid"].to_numpy())
        h8.append(f"- {sp}: players whose PP share rose 15+ points: {len(q)} points lines, over edge {100 * e[0]:+.1f} pts (z {e[1]:+.2f}).")
    h9 = ["Finishing luck = goals above (shots x expected shooting %) per game, season to date. Negative z = hot finishers' "
          "points overs lose to the price, as predicted.", "", "| Test | Sample | Lines | Trend z |", "|---|---|--:|--:|"]
    r, res = _trend_rows(P, "finish_luck", "Primary: points overs")
    h9 += r
    p = stats.norm.cdf(res["holdout"])
    h9 += ["", f"Rule: discovery z < 0 and holdout one-sided p < 0.05 (negative direction). Holdout p = {p:.3f} -> "
           f"**{'PASSES' if res['discovery'] < 0 and p < 0.05 else 'does not pass'}**.", ""]
    lo, hi = P.loc[P["split"] == "discovery", "finish_luck"].quantile([0.1, 0.9])
    for sp in ("discovery", "holdout", "live"):
        q = P[(P["split"] == sp)]
        a, b = q[q["finish_luck"] > hi], q[q["finish_luck"] < lo]
        ea = _z(a["y"].to_numpy(float), a["fair_over"].to_numpy(float), a["gid"].to_numpy())
        eb = _z(b["y"].to_numpy(float), b["fair_over"].to_numpy(float), b["gid"].to_numpy())
        h9.append(f"- {sp}: luckiest 10% over edge {100 * ea[0]:+.1f} pts (z {ea[1]:+.2f}, n {len(a)}); "
                  f"unluckiest 10% {100 * eb[0]:+.1f} pts (z {eb[1]:+.2f}, n {len(b)}).")
    return h8, h9


def main() -> str:
    T = load()
    h8, h9 = h8_h9(T)
    md = ["# Hypotheses H7-H9: results", "",
          f"Run {date.today().isoformat()} by `python -m nhlpipe.patterns.hyp2`. Specs in `docs/hypotheses_2026-11-17.md`, "
          "committed before this ran. Splits: discovery Oct-Jan 2025-26, holdout Feb-Apr 2026, live 2026-27.", "",
          "## H7 Trailing coach's goalie-pull aggressiveness -> favourite -1.5", "", *h7(T), "",
          "## H8 Power-play role change -> points (and SOG) overs", "", *h8, "",
          "## H9 Shooting-luck regression in points props", "", *h9, ""]
    txt = "\n".join(md) + "\n"
    (OUT / "hypotheses_h7_h9.md").write_text(txt)
    return txt


if __name__ == "__main__":
    print(main())
