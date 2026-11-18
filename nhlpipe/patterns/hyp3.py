"""Tests of pre-registered H10-H18 (docs/hypotheses_2026-11-17.md): shots-model patterns and shot factors.
python -m nhlpipe.patterns.hyp3 -> data/patterns/sog2425.csv.gz, data/patterns/hypotheses_h10_h18.md

2024-25 (primary, fresh): Pinnacle SOG props + game lines bought 2026-11-17 (task props2425), shots model
refit on 2022-23 + 2023-24 only. 2025-26: lines.csv (model fit on 2023-25, out of sample). Live: frozen model.
"""
import json
from datetime import date, datetime, timezone

import numpy as np
import pandas as pd
from scipy import stats

from .. import fair
from ..backtest.pipeline import TMAP, odds_frame, pick_dt
from ..names import norm
from ..shots2 import features as sfeat, model as smodel, pull as spull
from .data import DATA, OUT, ODDS25, _load, _ts, market_lines
from .scan import _logit, bh

ALL = ["20222023", "20232024", "20242025", "20252026", "20262027"]


# ------------------------------------------------------------- 2024-25 ----
def lines_2425() -> pd.DataFrame:
    days = sorted({g["date"] for g in spull.schedule("20242025", refresh=False)})
    sog, gl = [], []
    for ds in days:
        d = date.fromisoformat(ds)
        t = pick_dt(d).astimezone(timezone.utc)
        fdir = [ODDS25 / "featured" / x for x in (ds, (d.fromordinal(d.toordinal() + 1)).isoformat())]
        ff = [f for dd in fdir for f in dd.glob("*.json.gz") if _ts(f) == t]
        ef = [f for dd in [ODDS25 / "event" / x for x in (ds, d.fromordinal(d.toordinal() + 1).isoformat())]
              for f in dd.glob("*.json.gz") if _ts(f) == t]
        if ff:
            od = odds_frame([_load(f) for f in ff], TMAP)
            if len(od):
                m = market_lines(od)
                m = m[pd.to_datetime(m["commence_utc"]).dt.tz_convert("America/New_York").dt.date == d]
                m["date"] = ds
                gl.append(m)
        if ef:
            od = odds_frame([_load(f) for f in ef], TMAP)
            od = od[(od["market"] == "player_shots_on_goal") & od["implied_prob"].notna()] if len(od) else od
            if len(od):
                dv = fair.devig(od)
                p = dv[(dv["book"] == "pinnacle") & (dv["outcome"] == "Over")]
                for r in p.to_dict("records"):
                    sog.append({"date": ds, "game_key": f"{r['away']}@{r['home']}", "key": norm(r["player"]),
                                "line": r["point"], "fair_over": r["fair"], "commence_utc": r["commence_utc"]})
    S = pd.DataFrame(sog).drop_duplicates(["date", "game_key", "key", "line"])
    G = pd.concat(gl, ignore_index=True) if gl else pd.DataFrame()
    return S, G


def frames_2425():
    """Skater features for 2024-25 + the out-of-sample model (fit on 2022-23 + 2023-24)."""
    hist = pd.concat([spull.load_stats(s) for s in ALL[:3]], ignore_index=True)
    games = [g for s in ALL[:3] for g in spull.schedule(s, refresh=False)]
    mp = pd.read_csv(DATA / "shots2" / "mp_teams.csv.gz")
    mp = mp[mp["gameDate"] < 20250801]
    s = sfeat.add_h2h(sfeat.build(hist, games, mp, date(2024, 10, 4)))
    s = s[(s["n_prior"] >= 1) & s["mu_base"].notna()].copy()
    yr = s["gameId"] // 1_000_000
    m = smodel.ShotsModel("glm").fit(s[yr.isin([2022, 2023])])
    t = s[yr == 2024].copy()
    t["mu"] = m.predict_mean(t)
    t["key"] = t["skaterFullName"].map(norm)
    t["game_key"] = t["opp"].where(t["home"] == 1, t["teamAbbrev"]) + "@" + t["teamAbbrev"].where(t["home"] == 1, t["opp"])
    t["date"] = t["date"].astype(str)
    t = t[~t.duplicated(["date", "game_key", "key"], keep=False)]
    return t, m


def build_2425() -> pd.DataFrame:
    S, G = lines_2425()
    t, m = frames_2425()
    P = S.merge(t, on=["date", "game_key", "key"], how="inner")
    P["y"] = np.where(P["shots"] > P["line"], 1.0, 0.0)
    P["p_model"] = m.p_over(P["mu"].to_numpy(), P["line"].to_numpy())
    P["D"] = (P["positionCode"] == "D").astype(float)
    if len(G):
        G["game_key"] = G["away"] + "@" + G["home"]
        P = P.merge(G[["date", "game_key", "home", "ml_home_fair", "tot_line", "over_fair"]].rename(columns={"home": "g_home"}),
                    on=["date", "game_key"], how="left")
        P["team_win_fair"] = np.where(P["teamAbbrev"] == P["g_home"], P["ml_home_fair"], 1 - P["ml_home_fair"])
    P["season"] = 2024
    keep = ["date", "game_key", "key", "line", "fair_over", "y", "season", "playerId", "teamAbbrev", "opp", "positionCode", "D",
            "mu", "p_model", "ev_toi", "pp_toi", "opp_b2b", "team_win_fair", "tot_line"]
    P = P[[c for c in keep if c in P.columns]]
    P.to_csv(OUT / "sog2425.csv.gz", index=False)
    return P


# ------------------------------------------------------- shared features ----
def player_extras() -> pd.DataFrame:
    """Per skater-game (all seasons): games this season before, missed team's previous game,
    opponent blocked shots and penalty minutes per game to date."""
    st = pd.concat([spull.load_stats(s) for s in ALL], ignore_index=True)
    st["season"] = st["gameId"] // 1_000_000
    st["d"] = pd.to_datetime(st["gameDate"]).dt.date
    st = st.sort_values(["playerId", "d", "gameId"])
    st["gp_season"] = st.groupby(["playerId", "season"]).cumcount()
    st["prev_d"] = st.groupby(["playerId", "season"])["d"].shift(1)
    tg = st[["teamAbbrev", "gameId", "d", "season", "opponentTeamAbbrev"]].drop_duplicates(["teamAbbrev", "gameId"]).sort_values(["teamAbbrev", "d"])
    tg["team_prev_d"] = tg.groupby(["teamAbbrev", "season"])["d"].shift(1)
    st = st.merge(tg[["teamAbbrev", "gameId", "team_prev_d"]], on=["teamAbbrev", "gameId"], how="left")
    st["returning"] = ((st["gp_season"] > 0) & st["team_prev_d"].notna() & (st["prev_d"] < st["team_prev_d"])).astype(float)
    # team per-game blocks and PIM, then season-to-date per game BEFORE each game (prev season if < 10 games)
    team = st.groupby(["teamAbbrev", "gameId", "d", "season"])[["blockedShots", "penaltyMinutes"]].sum().reset_index().sort_values(["teamAbbrev", "d"])
    g = team.groupby(["teamAbbrev", "season"])
    n = g.cumcount()
    for c, name in (("blockedShots", "blk_pg"), ("penaltyMinutes", "pim_pg")):
        cur = (g[c].cumsum() - team[c]) / n.replace(0, np.nan)
        prev = team.groupby(["teamAbbrev", "season"])[c].mean().rename("p").reset_index()
        prev["season"] += 1
        tmp = team[["teamAbbrev", "season"]].merge(prev, on=["teamAbbrev", "season"], how="left")["p"].to_numpy()
        team[name] = np.where(n >= 10, cur, tmp)
    opp = team[["teamAbbrev", "gameId", "blk_pg", "pim_pg"]].rename(columns={"teamAbbrev": "opp_team", "blk_pg": "opp_blk_pg", "pim_pg": "opp_pim_pg"})
    st = st.merge(opp, left_on=["opponentTeamAbbrev", "gameId"], right_on=["opp_team", "gameId"], how="left")
    st["date"] = st["d"].astype(str)
    return st[["playerId", "date", "gp_season", "returning", "opp_blk_pg", "opp_pim_pg"]].drop_duplicates(["playerId", "date"])


# ---------------------------------------------------------------- tests ----
def logit_fit(y, off, X, cl):
    """Logistic with offset; sandwich SE clustered by game. Returns (beta, z)."""
    X = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(X.shape[1])
    for _ in range(60):
        mu = 1 / (1 + np.exp(-(off + X @ b)))
        H = X.T @ (X * (mu * (1 - mu))[:, None])
        step = np.linalg.solve(H, X.T @ (y - mu))
        b += step
        if np.abs(step).max() < 1e-9:
            break
    mu = 1 / (1 + np.exp(-(off + X @ b)))
    U = pd.DataFrame(X * (y - mu)[:, None]).groupby(np.asarray(cl)).sum().to_numpy()
    Hi = np.linalg.inv(X.T @ (X * (mu * (1 - mu))[:, None]))
    V = Hi @ (U.T @ U) @ Hi
    return b[1:], b[1:] / np.sqrt(np.diag(V)[1:])


def edge(q):
    r = q["y"] - q["fair_over"]
    v = max(float((q["fair_over"] * (1 - q["fair_over"])).sum()), float((r.groupby(q["gid"]).sum() ** 2).sum()))
    return r.mean(), r.sum() / np.sqrt(v) if v > 0 else np.nan


def run():
    p25 = build_2425()
    sog = pd.read_csv(OUT / "sog.csv.gz")
    sog = sog.rename(columns={"close_over": "close_over"})
    A = pd.concat([p25, sog], ignore_index=True, sort=False)
    A["date"] = A["date"].astype(str)
    A = A.merge(player_extras(), on=["playerId", "date"], how="left")
    A["gid"] = A["date"] + A["game_key"]
    A = A.dropna(subset=["y", "fair_over", "p_model"])
    A["dm"] = _logit(A["p_model"]) - _logit(A["fair_over"])
    A["off"] = _logit(A["fair_over"])
    A["sample"] = A["season"].map({2024: "2024-25 (fresh)", 2025: "2025-26", 2026: "2026-27 live"})
    # cut points for "top third" from 2024-25 (feature distribution only, no outcomes)
    base = A[A["season"] == 2024]
    toi_cut, pp_cut = base["ev_toi"].quantile(2 / 3), base["pp_toi"].quantile(2 / 3)
    A["top_toi"] = (A["ev_toi"] > toi_cut).astype(float)
    A["top_pp"] = (A["pp_toi"] > pp_cut).astype(float)
    A["closeness"] = 1 - (2 * A["team_win_fair"] - 1).abs()
    A["quiet"] = ((A["close_over"] - A["fair_over"]).abs() < 0.005).astype(float).where(A["close_over"].notna())
    A["heavy_fav_star"] = ((A["team_win_fair"] >= 0.67) & (A["top_toi"] == 1)).astype(float).where(A["team_win_fair"].notna())

    tests = {
        "H10": ("Model sharpens with games played", "interaction dm x log(1+gp)", +1,
                lambda q: logit_fit(q["y"].to_numpy(), q["off"].to_numpy(),
                                    np.column_stack([q["dm"], q["dm"] * np.log1p(q["gp_season"])]), q["gid"])[1][1],
                lambda q: q["gp_season"].notna()),
        "H11": ("Model beats quiet lines", "interaction dm x quiet", +1,
                lambda q: logit_fit(q["y"].to_numpy(), q["off"].to_numpy(),
                                    np.column_stack([q["dm"], q["quiet"], q["dm"] * q["quiet"]]), q["gid"])[1][2],
                lambda q: q["quiet"].notna()),
        "H12": ("Tired opponent", "opp_b2b = 1", +1, lambda q: edge(q[q["opp_b2b"] == 1])[1], lambda q: q["opp_b2b"].notna()),
        "H13": ("Game script", "trend on team win fair", -1, lambda q: _trend(q, "team_win_fair"), lambda q: q["team_win_fair"].notna()),
        "H14": ("Returning from absence", "missed team's last game = 1", -1, lambda q: edge(q[q["returning"] == 1])[1],
                lambda q: q["returning"].notna()),
        "H15": ("Opponent shot blocking", "trend on opponent blocks/game", -1, lambda q: _trend(q, "opp_blk_pg"),
                lambda q: q["opp_blk_pg"].notna()),
        "H16": ("Overtime chance (top-TOI players)", "trend on closeness", +1, lambda q: _trend(q, "closeness"),
                lambda q: (q["top_toi"] == 1) & q["closeness"].notna()),
        "H17": ("Blowout benching", "heavy-favourite top-TOI = 1", -1, lambda q: edge(q[q["heavy_fav_star"] == 1])[1],
                lambda q: q["heavy_fav_star"].notna()),
        "H18": ("Power-play opportunities (top-PP players)", "trend on opponent PIM/game", +1, lambda q: _trend(q, "opp_pim_pg"),
                lambda q: (q["top_pp"] == 1) & q["opp_pim_pg"].notna()),
    }
    rows = []
    for hid, (name, metric, sign, fn, mask) in tests.items():
        r = {"id": hid, "name": name, "metric": metric, "pred": "+" if sign > 0 else "-"}
        for s in ("2024-25 (fresh)", "2025-26", "2026-27 live"):
            q = A[(A["sample"] == s)]
            q = q[mask(q).fillna(False).to_numpy(bool)]
            try:
                z = fn(q) if len(q) >= 50 else np.nan
            except Exception:  # noqa: BLE001
                z = np.nan
            r[f"n {s}"], r[f"z {s}"] = len(q), z
        rows.append(r)
    R = pd.DataFrame(rows)
    prim = np.where(R["id"] == "H11", R["z 2025-26"], R["z 2024-25 (fresh)"])
    sgn = np.where(R["pred"] == "+", 1, -1)
    R["p_primary"] = stats.norm.sf(prim * sgn)
    R["bh"] = bh(R["p_primary"].to_numpy())
    support = np.where(R["id"] == "H11", R["z 2026-27 live"], R["z 2025-26"])
    R["passes"] = R["bh"] & (np.sign(support) == sgn)
    return R, A


def _trend(q, col):
    x = q[col].to_numpy(float)
    xs = (x - np.nanmean(x)) / np.nanstd(x)
    return logit_fit(q["y"].to_numpy(), q["off"].to_numpy(), xs[:, None], q["gid"])[1][0]


def slices(A) -> list[str]:
    """Descriptive edges (pts) for the flags, per sample."""
    out = ["| Slice | Sample | Lines | Over edge vs Pinnacle, pts | z |", "|---|---|--:|--:|--:|"]
    defs = {"Opponent on a back-to-back": lambda q: q["opp_b2b"] == 1,
            "Returning from absence": lambda q: q["returning"] == 1,
            "Star on a heavy favourite (67%+)": lambda q: q["heavy_fav_star"] == 1,
            "Big underdog's players (team win < 35%)": lambda q: q["team_win_fair"] < 0.35,
            "Model says over by 5+ pts, player has 20+ games": lambda q: (q["p_model"] - q["fair_over"] > 0.05) & (q["gp_season"] >= 20),
            "Model says over by 5+ pts, player has < 20 games": lambda q: (q["p_model"] - q["fair_over"] > 0.05) & (q["gp_season"] < 20),
            "Model says under by 5+ pts, player has 20+ games": lambda q: (q["fair_over"] - q["p_model"] > 0.05) & (q["gp_season"] >= 20),
            "Model says under by 5+ pts, player has < 20 games": lambda q: (q["fair_over"] - q["p_model"] > 0.05) & (q["gp_season"] < 20)}
    for name, m in defs.items():
        for s in ("2024-25 (fresh)", "2025-26", "2026-27 live"):
            q = A[A["sample"] == s]
            q = q[m(q).fillna(False).to_numpy(bool)]
            if len(q) < 20:
                continue
            e, z = edge(q)
            if "under" in name:
                e, z = -e, -z
                lab = name + " (shown as UNDER edge)"
            else:
                lab = name
            out.append(f"| {lab} | {s} | {len(q):,} | {100 * e:+.1f} | {z:+.2f} |")
    return out


def main() -> str:
    R, A = run()
    md = ["# H10-H18: shots model patterns and shot factors", "",
          f"Run {date.today().isoformat()} by `python -m nhlpipe.patterns.hyp3`. Specs in `docs/hypotheses_2026-11-17.md`, "
          "committed before the 2024-25 data was bought. Residual = SOG over hit - Pinnacle no-vig fair at pick time. "
          "Primary sample = 2024-25 (never looked at; H11 uses 2025-26 because 2024-25 has no closing prices). "
          "z is in the direction of the prediction's sign; pass = survives Benjamini-Hochberg (q 0.10) over the 9 "
          "and the supporting season has the same sign.", "",
          "| ID | Pattern | Metric | Predicted sign | z 2024-25 (n) | z 2025-26 (n) | z live (n) | Primary p (one-sided) | Passes |",
          "|---|---|---|---|--:|--:|--:|--:|---|"]
    for r in R.to_dict("records"):
        f = lambda s: "–" if pd.isna(r[f"z {s}"]) else f"{r[f'z {s}']:+.2f} ({int(r[f'n {s}']):,})"  # noqa: E731
        md.append(f"| {r['id']} | {r['name']} | {r['metric']} | {r['pred']} | {f('2024-25 (fresh)')} | {f('2025-26')} | "
                  f"{f('2026-27 live')} | {r['p_primary']:.3f} | {'YES' if r['passes'] else 'no'} |")
    md += ["", "## Slices (descriptive)", "", *slices(A), "",
           f"2024-25 sample: {int((A['season'] == 2024).sum()):,} Pinnacle SOG lines matched to skaters "
           f"({A.loc[A['season'] == 2024, 'date'].min()} - {A.loc[A['season'] == 2024, 'date'].max()}).", ""]
    txt = "\n".join(md) + "\n"
    (OUT / "hypotheses_h10_h18.md").write_text(txt)
    return txt


if __name__ == "__main__":
    print(main())
