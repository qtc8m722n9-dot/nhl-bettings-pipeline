"""Observed-vs-expected pattern scan. Research only: it places no bets and changes no method.

Idea (Evan, 2026-11-17): the market's fair price is the expected value; compare what
actually happened in a slice of games to what the price said, and test whether the
gap is bigger than chance.

Rules, fixed in this file BEFORE the scan was first run (2026-11-17):
  expected   Pinnacle no-vig probability at pick time (power de-vig, as live)
  observed   the result (books' settlement: OT/SO count, shootout +1 goal; total pushes dropped)
  markets    games: total over, home win, favourite -1.5; props: SOG over, points over
  samples    DISCOVERY 2025-10-15..2026-01-31 (patterns are searched only here)
             HOLDOUT   2026-02-01..2026-04-16 (untouched until the candidates were fixed)
             LIVE      2026-27 pick-lock prices (2026-10-30 on)
  tests      per slice: z = (observed hits - expected hits) / sqrt(sum p(1-p))
               props: variance clustered by game (max of binomial and clustered)
             per feature: slices = discovery terciles (cut points fixed from discovery) or
               flag = 1; plus a trend test: logistic y ~ offset(logit p) + a + b*x, Wald z on b
             chi-square across a feature's slices = goodness of fit of observed vs expected
             pairs: extreme-tercile corners of a fixed shortlist of features (and flags)
  multiple   Benjamini-Hochberg at q = 0.10 over every discovery test (all markets together)
  candidates BH survivors, plus the 10 largest |z| per market as "leads" (labelled as such)
  holds up   holdout: same direction, one-sided p < 0.05; then BH over the candidates' holdout
             p-values at q = 0.10. Live is reported, not used to select (too small).
  bettable   also needs a positive holdout ROI at Pinnacle's own price (with its margin)
  pre-specified (no search, no multiple-testing penalty): evan_under (data.derive), tested
             on all of 2025-26 and live.
python -m nhlpipe.patterns.scan  -> data/patterns/report.md, tests.csv
"""
import math
from datetime import date

import numpy as np
import pandas as pd
from scipy import stats

from .data import OUT

DISC_END, HOLD_END = date(2026, 1, 31), date(2026, 4, 16)
Q = 0.10
N_LEADS = 10

GAME_TOTAL = [
    "sum_gf_pg", "sum_ga_pg", "sum_xgf_pg", "sum_xga_pg", "sum_sf_pg", "sum_sa_pg", "sum_finish_pg", "sum_save_pg",
    "sum_l10_gf_pg", "sum_l10_ga_pg", "sum_pen_for_pg", "sum_pp_xgf60", "sum_pk_xga60", "sum_goalie_gsax_pg",
    "sum_goalie_gsax", "xg_total_minus_line", "g_total_minus_line", "home_ga_pg_pct", "away_ga_pg_pct",
    "home_goalie_gsax_pg", "away_goalie_gsax_pg", "over_fair", "fav_fair", "tot_line", "season_gp", "start_hour_et",
    "home_rest", "away_rest", "home_tz_shift", "away_tz_shift", "away_road_trip",
    "both_goalies_hot", "both_goalies_cold", "both_def_top_third", "both_def_bottom_third", "both_off_top_third",
    "any_backup", "home_backup", "away_backup", "away_b2b_only", "home_b2b_only", "both_b2b", "line_55", "line_65",
    "line_whole", "early_start", "weekend", "division_game", "conference_game",
]
GAME_ML = [
    "diff_xg_pct", "diff_ev_xg_pct", "diff_gd_pg", "diff_finish_pg", "diff_save_pg", "diff_goalie_gsax_pg",
    "diff_l10_xg_pct", "diff_rest", "diff_prev_xg_pct", "diff_pp_xgf60", "home_finish_pg", "away_finish_pg",
    "home_save_pg", "away_save_pg", "home_goalie_gsax_pg", "away_goalie_gsax_pg", "ml_home_fair", "tot_line",
    "season_gp", "start_hour_et", "away_tz_shift", "away_road_trip", "home_rest", "away_rest", "home_momentum",
    "away_momentum", "home_backup", "away_backup", "away_b2b_only", "home_b2b_only", "both_b2b", "home_fav",
    "early_start", "weekend", "division_game", "conference_game",
]
GAME_PL = [
    "fav_fair_pl", "pl_fav_home", "fav_xg_edge", "fav_gd_edge", "fav_finish_pg", "dog_finish_pg", "fav_goalie_gsax_pg",
    "dog_goalie_gsax_pg", "fav_b2b", "dog_b2b", "dog_backup", "fav_backup", "tot_line", "over_fair", "season_gp",
    "dog_pk_xga60", "fav_pp_xgf60", "division_game", "early_start",
]
SOG = [
    "D", "line", "mu_base", "base_minus_line", "mu_minus_line", "model_minus_fair", "ev_toi", "pp_toi", "toi_jump",
    "pp_jump", "on_net", "ev_att60", "oz_start", "home", "b2b", "opp_b2b", "rest_days", "tz_shift", "road_trip",
    "opp_sa_ratio", "team_ca_ratio", "xg_edge", "opp_pen_ratio", "missing_toi", "traded", "h2h_resid", "n_prior",
    "fair_over", "team_win_fair", "game_over_fair", "tot_line", "opp_goalie_gsax_pg", "opp_ga_pct", "opp_sa_pg",
]
POINTS = [
    "D", "line", "points_std", "pts_minus_line", "pts_l10", "goals_std", "assists_std", "ppPoints_std", "shots_std",
    "toi_std", "pp_toi_std", "gp_std", "home", "fair_over", "team_win_fair", "tot_line", "game_over_fair", "opp_ga_pct",
    "opp_goalie_gsax_pg", "team_implied_goals",
]
PAIRS = {
    "total": ["sum_ga_pg", "sum_gf_pg", "sum_goalie_gsax_pg", "xg_total_minus_line", "sum_finish_pg", "over_fair",
              "both_goalies_hot", "any_backup", "both_b2b", "line_55"],
    "home": ["diff_xg_pct", "diff_finish_pg", "diff_goalie_gsax_pg", "ml_home_fair", "away_b2b_only", "home_b2b_only",
             "away_backup", "home_backup", "diff_rest"],
}
FAMILIES = {
    # name: (table, outcome, expected, features, cluster, side labels (if y=1, if y=0), ROI price columns)
    "total": ("games", "y_over", "over_fair", GAME_TOTAL, None, ("over", "under"), ("pin_over_imp", "pin_under_imp", "best_over_imp", "best_under_imp")),
    "home": ("games", "y_home", "ml_home_fair", GAME_ML, None, ("home", "away"), ("pin_home_imp", "pin_away_imp", "best_home_imp", "best_away_imp")),
    "pl_fav": ("games", "y_pl_fav", "pl_fav_fair", GAME_PL, None, ("fav -1.5", "dog +1.5"), ("pin_pl_imp", None, None, None)),
    "sog": ("sog", "y", "fair_over", SOG, "gid", ("over", "under"), (None, None, None, None)),
    "points": ("points", "y", "fair_over", POINTS, "gid", ("over", "under"), ("pin_over_imp", None, "best_over_imp", "best_under_imp")),
}
CLOSE = {"total": "close_over_fair", "home": "close_home_fair", "sog": "close_over", "points": "close_over"}


# ------------------------------------------------------------ prepare ----
def load() -> dict[str, pd.DataFrame]:
    g = pd.read_csv(OUT / "games.csv.gz").copy()
    for s in ("home", "away"):
        g[f"{s}_momentum"] = g[f"{s}_l10_xg_pct"] - g[f"{s}_xg_pct"]
    fh = g["pl_fav_home"] == 1
    pick = lambda h, a: np.where(fh, g[h], g[a])  # noqa: E731
    g["fav_fair_pl"] = np.where(fh, g["ml_home_fair"], 1 - g["ml_home_fair"])
    g["fav_xg_edge"] = np.where(fh, g["diff_xg_pct"], -g["diff_xg_pct"])
    g["fav_gd_edge"] = np.where(fh, g["diff_gd_pg"], -g["diff_gd_pg"])
    for name, (h, a) in {"fav_finish_pg": ("home_finish_pg", "away_finish_pg"), "dog_finish_pg": ("away_finish_pg", "home_finish_pg"),
                         "fav_goalie_gsax_pg": ("home_goalie_gsax_pg", "away_goalie_gsax_pg"),
                         "dog_goalie_gsax_pg": ("away_goalie_gsax_pg", "home_goalie_gsax_pg"),
                         "fav_b2b": ("home_b2b", "away_b2b"), "dog_b2b": ("away_b2b", "home_b2b"),
                         "fav_backup": ("home_backup", "away_backup"), "dog_backup": ("away_backup", "home_backup"),
                         "dog_pk_xga60": ("away_pk_xga60", "home_pk_xga60"), "fav_pp_xgf60": ("home_pp_xgf60", "away_pp_xgf60")}.items():
        g[name] = pick(h, a)
    g.loc[g["pl_fav"].isna(), [c for c in GAME_PL if c not in ("tot_line", "over_fair", "season_gp", "division_game", "early_start")]] = np.nan
    out = {"games": g.copy()}
    for k in ("sog", "points"):
        p = pd.read_csv(OUT / f"{k}.csv.gz")
        p["gid"] = p["date"].astype(str) + p["game_key"]
        out[k] = p
    for k, d in out.items():
        d["date"] = pd.to_datetime(d["date"]).dt.date
        d["split"] = np.where(d["season"] == 2026, "live", np.where(d["date"] <= DISC_END, "discovery", "holdout"))
    return out


# --------------------------------------------------------------- tests ----
def _z(y: np.ndarray, p: np.ndarray, cl: np.ndarray | None) -> tuple[float, float, float]:
    """(edge = mean(y - p), z, sd of the edge) with a binomial (and, for props, clustered) variance."""
    r = y - p
    v = float(np.sum(p * (1 - p)))
    if cl is not None:
        s = pd.Series(r).groupby(cl).sum().to_numpy()
        v = max(v, float(np.sum(s ** 2)))
    n = len(y)
    if n == 0 or v <= 0:
        return np.nan, np.nan, np.nan
    return r.mean(), r.sum() / math.sqrt(v), math.sqrt(v) / n


def _logit(p):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return np.log(p / (1 - p))


def trend(y, p, x, cl=None) -> tuple[float, float]:
    """Logistic y ~ offset(logit p) + a + b*x (x standardised); returns (b, z) with sandwich SE."""
    ok = ~(np.isnan(x) | np.isnan(y) | np.isnan(p))
    y, p, x = y[ok], p[ok], x[ok]
    if len(y) < 30 or np.std(x) == 0:
        return np.nan, np.nan
    xs = (x - x.mean()) / x.std()
    X = np.column_stack([np.ones_like(xs), xs])
    off = _logit(p)
    beta = np.zeros(2)
    for _ in range(50):
        mu = 1 / (1 + np.exp(-(off + X @ beta)))
        W = mu * (1 - mu)
        H = X.T @ (X * W[:, None])
        step = np.linalg.solve(H, X.T @ (y - mu))
        beta += step
        if np.abs(step).max() < 1e-8:
            break
    mu = 1 / (1 + np.exp(-(off + X @ beta)))
    U = X * (y - mu)[:, None]
    if cl is not None:
        U = pd.DataFrame(U).groupby(np.asarray(cl)[ok]).sum().to_numpy()
    Hi = np.linalg.inv(X.T @ (X * (mu * (1 - mu))[:, None]))
    V = Hi @ (U.T @ U) @ Hi
    return float(beta[1]), float(beta[1] / math.sqrt(V[1, 1]))


def _is_flag(s: pd.Series) -> bool:
    v = s.dropna().unique()
    return len(v) <= 2 and set(v) <= {0.0, 1.0}


def slices(disc: pd.DataFrame, feats: list[str]) -> list[tuple[str, str, callable]]:
    """(feature label, slice label, mask function) with cut points fixed from discovery."""
    out = []
    for f in feats:
        if f not in disc or disc[f].notna().sum() < 50:
            continue
        s = disc[f]
        if _is_flag(s):
            out.append((f, f"{f} = 1", lambda d, f=f: d[f] == 1))
            continue
        lo, hi = s.quantile([1 / 3, 2 / 3])
        if lo == hi:
            out.append((f, f"{f} > {lo:.3g}", lambda d, f=f, lo=lo: d[f] > lo))
            continue
        out += [(f, f"{f} low (<= {lo:.3g})", lambda d, f=f, lo=lo: d[f] <= lo),
                (f, f"{f} mid", lambda d, f=f, lo=lo, hi=hi: (d[f] > lo) & (d[f] <= hi)),
                (f, f"{f} high (> {hi:.3g})", lambda d, f=f, hi=hi: d[f] > hi)]
    return out


def pair_slices(disc: pd.DataFrame, feats: list[str]) -> list[tuple[str, str, callable]]:
    ends = {}
    for f in feats:
        if f not in disc:
            continue
        s = disc[f]
        if _is_flag(s):
            ends[f] = [(f"{f}=1", lambda d, f=f: d[f] == 1)]
        else:
            lo, hi = s.quantile([1 / 3, 2 / 3])
            ends[f] = [(f"{f} low", lambda d, f=f, lo=lo: d[f] <= lo), (f"{f} high", lambda d, f=f, hi=hi: d[f] > hi)]
    out, fs = [], list(ends)
    for i in range(len(fs)):
        for j in range(i + 1, len(fs)):
            for la, ma in ends[fs[i]]:
                for lb, mb in ends[fs[j]]:
                    out.append((f"{fs[i]} x {fs[j]}", f"{la} & {lb}", lambda d, ma=ma, mb=mb: ma(d) & mb(d)))
    return out


def evaluate(d: pd.DataFrame, mask, y: str, p: str, cl: str | None) -> dict:
    m = mask(d).fillna(False).to_numpy(bool) if hasattr(mask(d), "fillna") else mask(d)
    q = d[m & d[y].notna().to_numpy() & d[p].notna().to_numpy()]
    if len(q) == 0:
        return {"n": 0, "obs": np.nan, "exp": np.nan, "edge": np.nan, "z": np.nan, "se": np.nan}
    e, z, se = _z(q[y].to_numpy(float), q[p].to_numpy(float), q[cl].to_numpy() if cl else None)
    return {"n": len(q), "obs": q[y].mean(), "exp": q[p].mean(), "edge": e, "z": z, "se": se}


def roi(d: pd.DataFrame, mask, fam: str, direction: int) -> tuple[float, float, int]:
    """Flat-stake ROI betting the slice's direction at Pinnacle's price and at the best US-book price."""
    _, y, _, _, _, _, cols = FAMILIES[fam]
    pin_yes, pin_no, best_yes, best_no = cols
    m = mask(d).fillna(False).to_numpy(bool)
    q = d[m & d[y].notna().to_numpy()]
    if q.empty or pin_yes is None:
        return np.nan, np.nan, 0
    won = q[y] if direction > 0 else 1 - q[y]
    pin = q[pin_yes] if direction > 0 else (q[pin_no] if pin_no else np.nan)
    best = q[best_yes] if (direction > 0 and best_yes) else (q[best_no] if best_no else pd.Series(np.nan, index=q.index))
    r_pin = (won / pin - 1).mean() if isinstance(pin, pd.Series) else np.nan
    r_best = (won / best - 1).dropna().mean() if best is not None else np.nan
    return float(r_pin), float(r_best), len(q)


def bh(p: np.ndarray, q: float = Q) -> np.ndarray:
    p = np.asarray(p, float)
    ok = ~np.isnan(p)
    out = np.zeros(len(p), bool)
    ps = p[ok]
    order = np.argsort(ps)
    m = len(ps)
    passed = ps[order] <= q * (np.arange(1, m + 1) / m)
    if passed.any():
        k = np.max(np.where(passed)[0])
        sel = np.zeros(m, bool)
        sel[order[: k + 1]] = True
        out[np.where(ok)[0]] = sel
    return out


# ---------------------------------------------------------------- run -----
def run() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    T = load()
    rows, trends = [], []
    for fam, (tab, y, p, feats, cl, _, _) in FAMILIES.items():
        d = T[tab]
        disc = d[d["split"] == "discovery"]
        sl = slices(disc, feats) + (pair_slices(disc, PAIRS[fam]) if fam in PAIRS else [])
        for feat, lab, mask in sl:
            r = {"family": fam, "feature": feat, "slice": lab, "kind": "pair" if " x " in feat else "single", "mask": mask}
            for sp in ("discovery", "holdout", "live"):
                e = evaluate(d[d["split"] == sp], mask, y, p, cl)
                r.update({f"{sp}_{k}": v for k, v in e.items()})
            rows.append(r)
        for f in feats:
            if f not in d:
                continue
            t = {"family": fam, "feature": f}
            for sp in ("discovery", "holdout", "live"):
                q = d[(d["split"] == sp) & d[y].notna() & d[p].notna()]
                b, z = trend(q[y].to_numpy(float), q[p].to_numpy(float), q[f].to_numpy(float), q[cl].to_numpy() if cl else None)
                t[f"{sp}_b"], t[f"{sp}_z"] = b, z
            trends.append(t)
    R, TR = pd.DataFrame(rows), pd.DataFrame(trends)
    R["discovery_p"] = 2 * stats.norm.sf(np.abs(R["discovery_z"]))
    TR["discovery_p"] = 2 * stats.norm.sf(np.abs(TR["discovery_z"]))
    allp = np.concatenate([R["discovery_p"].to_numpy(), TR["discovery_p"].to_numpy()])
    sig = bh(allp)
    R["bh_disc"], TR["bh_disc"] = sig[: len(R)], sig[len(R):]
    R["n_tests_total"] = int(np.sum(~np.isnan(allp)))
    # candidates: BH survivors + top leads per family (slices with >= 40 discovery games / lines)
    R["candidate"] = ""
    R.loc[R["bh_disc"], "candidate"] = "BH"
    for fam in FAMILIES:
        ok = (R["family"] == fam) & (R["discovery_n"] >= 40) & (R["candidate"] == "")
        top = R[ok].assign(a=R["discovery_z"].abs()).sort_values("a", ascending=False).head(N_LEADS).index
        R.loc[top, "candidate"] = "lead"
    C = R[R["candidate"] != ""].copy()
    C["dir"] = np.sign(C["discovery_edge"])
    C["holdout_p1"] = stats.norm.sf(C["holdout_z"] * C["dir"])
    C["live_p1"] = stats.norm.sf(C["live_z"] * C["dir"])
    C["holdout_bh"] = bh(C["holdout_p1"].to_numpy())
    # ROI and close drift for candidates
    for i, r in C.iterrows():
        tab = FAMILIES[r["family"]][0]
        d = T[tab]
        for sp in ("discovery", "holdout", "live"):
            ds = d[d["split"] == sp]
            a, b, _ = roi(ds, r["mask"], r["family"], int(r["dir"]))
            C.loc[i, f"{sp}_roi_pin"], C.loc[i, f"{sp}_roi_best"] = a, b
            cc = CLOSE.get(r["family"])
            if cc and cc in ds:
                m = r["mask"](ds).fillna(False).to_numpy(bool)
                q = ds[m]
                drift = (q[cc] - q[FAMILIES[r["family"]][2]]).dropna()
                C.loc[i, f"{sp}_drift"] = drift.mean() * r["dir"] if len(drift) else np.nan
                C.loc[i, f"{sp}_n_close"] = len(drift)
    C["holds_up"] = (C["holdout_p1"] < 0.05) & C["holdout_bh"] & (C["holdout_n"] > 0)
    C["bettable"] = C["holds_up"] & (C["holdout_roi_pin"] > 0)
    extra = {"T": T}
    return R, TR, C, extra


# ------------------------------------------------------------ extras ------
def calibration(T: dict) -> list[str]:
    out = []
    for fam, (tab, y, p, _, cl, labels, _) in FAMILIES.items():
        d = T[tab]
        out += [f"**{fam}** (expected = {p}; 'over/home/fav' side):", "",
                "| Sample | n | Hit rate | Expected | Edge, pts | z | Chi-square by price band (df) | p |", "|---|--:|--:|--:|--:|--:|--:|--:|"]
        for sp in ("discovery", "holdout", "live"):
            q = d[(d["split"] == sp) & d[y].notna() & d[p].notna()]
            if q.empty:
                continue
            e, z, _ = _z(q[y].to_numpy(float), q[p].to_numpy(float), q[cl].to_numpy() if cl else None)
            bands = pd.cut(q[p], [0, .2, .3, .4, .45, .5, .55, .6, .7, .8, 1])
            chi, k = 0.0, 0
            for _, b in q.groupby(bands, observed=True):
                if len(b) < 10:
                    continue
                v = (b[p] * (1 - b[p])).sum()
                chi += (b[y].sum() - b[p].sum()) ** 2 / v
                k += 1
            pv = stats.chi2.sf(chi, k) if k else np.nan
            out.append(f"| {sp} | {len(q):,} | {q[y].mean():.1%} | {q[p].mean():.1%} | {100 * e:+.1f} | {z:+.2f} | {chi:.1f} ({k}) | {pv:.2f} |")
        out.append("")
    return out


def goals_distribution(T: dict) -> list[str]:
    """Is the total-goals distribution what the market's own number implies? (Poisson check)"""
    g = T["games"]
    g = g[g["tot_line"].notna() & g["over_fair"].notna() & (g["tot_line"] % 1 == 0.5)].copy()
    lam = []
    for line, p in zip(g["tot_line"], g["over_fair"]):
        lo, hi = 0.5, 15.0
        for _ in range(60):
            m = (lo + hi) / 2
            if stats.poisson.sf(math.floor(line), m) < p:
                lo = m
            else:
                hi = m
        lam.append((lo + hi) / 2)
    g["lam"] = lam
    ks = list(range(0, 11))
    obs = [(g["total"] == k).sum() for k in ks] + [(g["total"] >= 11).sum()]
    exp = [stats.poisson.pmf(k, g["lam"]).sum() for k in ks] + [stats.poisson.sf(10, g["lam"]).sum()]
    chi = sum((o - e) ** 2 / e for o, e in zip(obs, exp) if e > 0)
    resid = g["total"] - g["lam"]
    out = ["Each game's Poisson mean is solved from Pinnacle's line and over price (half-goal lines only, "
           f"n = {len(g):,}, all seasons). Chi-square goodness of fit of the goal counts: {chi:.1f} on {len(obs) - 1} df, "
           f"p = {stats.chi2.sf(chi, len(obs) - 1):.3f}. Mean actual {g['total'].mean():.2f} vs implied {g['lam'].mean():.2f}; "
           f"variance of (actual - implied) {resid.var():.2f} vs Poisson {g['lam'].mean():.2f} "
           f"(ratio {resid.var() / g['lam'].mean():.2f}; > 1 = more blowouts and shutouts than a Poisson market assumes).", "",
           "| Goals | Games | Implied by price |", "|--:|--:|--:|"]
    out += [f"| {k if k < 11 else '11+'} | {o} | {e:.1f} |" for k, o, e in zip(ks + [11], obs, exp)]
    return out


def z_normality(R: pd.DataFrame, TR: pd.DataFrame) -> list[str]:
    z = TR["discovery_z"].dropna().to_numpy()
    zs = R.loc[R["kind"] == "single", "discovery_z"].dropna().to_numpy()
    ks = stats.kstest(z, "norm")
    sw = stats.shapiro(z) if 3 <= len(z) <= 5000 else None
    out = [f"If every feature were noise, the trend z-scores would look like draws from a standard normal. "
           f"Trend tests: {len(z)}; |z| > 1.96: {np.mean(np.abs(z) > 1.96):.1%} (5% expected under pure noise); "
           f"|z| > 2.58: {np.mean(np.abs(z) > 2.58):.1%} (1% expected); largest |z| {np.abs(z).max():.2f}. "
           f"Kolmogorov-Smirnov vs N(0,1): D = {ks.statistic:.3f}, p = {ks.pvalue:.3f}"
           + (f"; Shapiro-Wilk normality p = {sw.pvalue:.3f}" if sw else "") + ". "
           f"Single-feature slices: {len(zs)}; |z| > 1.96: {np.mean(np.abs(zs) > 1.96):.1%} (slices of one feature overlap, "
           "so this is a rough guide).", "", "Per market:", "", "| Market | Trend tests | Share with abs(z) > 1.96 | KS p (vs normal) |", "|---|--:|--:|--:|"]
    for fam, q in TR.groupby("family"):
        zz = q["discovery_z"].dropna().to_numpy()
        out.append(f"| {fam} | {len(zz)} | {np.mean(np.abs(zz) > 1.96):.0%} | {stats.kstest(zz, 'norm').pvalue:.2f} |")
    return out


def evan(T: dict) -> list[str]:
    g = T["games"]
    out = ["Pre-specified before the scan: both teams in the league's best third for goals against per game "
           "(as of the morning of the game) AND both projected starters with GSAx >= 0 -> the under hits more often than "
           "Pinnacle's price says. Tested on all of 2025-26 (no search was involved, so no multiple-testing penalty) and live.", "",
           "| Version | Sample | Games | Under hit | Under expected | Edge, pts (95% CI) | z | ROI at Pinnacle | ROI best US book | Close move toward under, pts |",
           "|---|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
    versions = {
        "Evan's rule (both D top third + both goalies GSAx >= 0)": lambda d: d["evan_under"] == 1,
        "Both D top third (goalies any)": lambda d: d["both_def_top_third"] == 1,
        "Both goalies GSAx >= 0 (defence any)": lambda d: (d["home_goalie_gsax"] >= 0) & (d["away_goalie_gsax"] >= 0),
        "Both D top half + both goalies GSAx >= 0": lambda d: (d["home_ga_pg_pct"] <= .5) & (d["away_ga_pg_pct"] <= .5)
        & (d["home_goalie_gsax"] >= 0) & (d["away_goalie_gsax"] >= 0),
        "Combined GA/g in lowest third (discovery cut)": None,
    }
    disc = g[g["split"] == "discovery"]
    cut = disc["sum_ga_pg"].quantile(1 / 3)
    versions["Combined GA/g in lowest third (discovery cut)"] = lambda d: d["sum_ga_pg"] <= cut
    for name, m in versions.items():
        for sp, d in (("2025-26 (all)", g[g["season"] == 2025]), ("2026-27 live", g[g["season"] == 2026])):
            q = d[m(d).fillna(False) & d["y_over"].notna() & d["over_fair"].notna()]
            if q.empty:
                out.append(f"| {name} | {sp} | 0 | – | – | – | – | – | – | – |")
                continue
            yu, pu = 1 - q["y_over"].to_numpy(float), 1 - q["over_fair"].to_numpy(float)
            e, z, se = _z(yu, pu, None)
            r_pin = ((1 - q["y_over"]) / q["pin_under_imp"] - 1).mean()
            r_best = ((1 - q["y_over"]) / q["best_under_imp"] - 1).dropna().mean()
            dr = (q["over_fair"] - q["close_over_fair"]).dropna() if "close_over_fair" in q else pd.Series(dtype=float)
            drs = f"{100 * dr.mean():+.1f} (n={len(dr)})" if len(dr) else "–"
            out.append(f"| {name} | {sp} | {len(q)} | {yu.mean():.1%} | {pu.mean():.1%} | {100 * e:+.1f} ({100 * (e - 1.96 * se):+.1f}, {100 * (e + 1.96 * se):+.1f}) | "
                       f"{z:+.2f} | {r_pin:+.1%} | {r_best:+.1%} | {drs} |")
    mn = g[(g["home"] == "MTL") & (g["away"] == "NYR") | (g["home"] == "NYR") & (g["away"] == "MTL")]
    if len(mn):
        out += ["", "MTL-NYR games in the data:", "", "| Date | Game | Line | Pinnacle P(under) | Goals | Evan's rule flag | Both D top third | Goalies GSAx (home, away) |", "|---|---|--:|--:|--:|--:|--:|---|"]
        for r in mn.sort_values("date").to_dict("records"):
            out.append(f"| {r['date']} | {r['away']}@{r['home']} | {r['tot_line']} | {1 - r['over_fair']:.1%} | {r['total']} | "
                       f"{int(r['evan_under'])} | {int(r['both_def_top_third'])} | {r['home_goalie_gsax']:+.1f}, {r['away_goalie_gsax']:+.1f} |")
    return out


def consistent(C: pd.DataFrame) -> list[str]:
    """Candidates whose edge kept the same sign in all three samples (descriptive, not a test)."""
    q = C[(C["holdout_n"] > 0) & (C["live_n"] > 0)
          & (C["holdout_edge"] * C["dir"] > 0) & (C["live_edge"] * C["dir"] > 0)]
    out = ["Same direction in discovery, holdout AND live (by chance alone about 1 in 4 candidates would do this):", "",
           "| Market | Slice | Side | Edge disc / hold / live, pts | Lines or games disc / hold / live |", "|---|---|---|---|---|"]
    for r in q.to_dict("records"):
        side = FAMILIES[r["family"]][5][0 if r["dir"] > 0 else 1]
        out.append(f"| {r['family']} | {r['slice']} | {side} | {100 * r['discovery_edge'] * r['dir']:+.1f} / "
                   f"{100 * r['holdout_edge'] * r['dir']:+.1f} / {100 * r['live_edge'] * r['dir']:+.1f} | "
                   f"{r['discovery_n']} / {r['holdout_n']} / {r['live_n']} |")
    out += ["", f"{len(q)} of {len(C)} candidates."]
    return out


def model_by_month(T: dict) -> list[str]:
    """Does the shots model add information beyond Pinnacle, and when in the season?"""
    G = T["sog"].copy()
    G["mon"] = pd.to_datetime(G["date"]).dt.to_period("M").astype(str)
    out = ["Trend test of the outcome on (shots model probability - Pinnacle fair), after Pinnacle's price, by month. "
           "2025-26 uses the model fit on 2023-25 only (out of sample); 2026-27 uses the frozen live model. "
           "z > 2 = the model's disagreement with Pinnacle came true more than chance.", "",
           "| Month | Lines | z |", "|---|--:|--:|"]
    for m, q in G.groupby("mon"):
        q = q.dropna(subset=["y", "fair_over", "model_minus_fair"])
        _, z = trend(q["y"].to_numpy(float), q["fair_over"].to_numpy(float), q["model_minus_fair"].to_numpy(float), q["gid"].to_numpy())
        out.append(f"| {m} | {len(q):,} | {_f(z)} |")
    return out


def points_d(T: dict) -> list[str]:
    P = T["points"]
    out = ["| Sample | Line | Position | Lines | Hit | Pinnacle fair | Edge, pts | Best US-book cost | ROI best US book |",
           "|---|--:|---|--:|--:|--:|--:|--:|--:|"]
    for (sp, line, d), q in P.groupby(["split", "line", "D"]):
        if len(q) < 30:
            continue
        b = q["best_over_imp"].dropna()
        roi_b = ((q["y"] / q["best_over_imp"]) - 1).dropna().mean() if len(b) else np.nan
        out.append(f"| {sp} | {line} | {'D' if d == 1 else 'F'} | {len(q):,} | {q['y'].mean():.1%} | {q['fair_over'].mean():.1%} | "
                   f"{100 * (q['y'].mean() - q['fair_over'].mean()):+.1f} | {b.mean():.1%} | {_f(roi_b, pct=True)} |"
                   if len(b) else
                   f"| {sp} | {line} | {'D' if d == 1 else 'F'} | {len(q):,} | {q['y'].mean():.1%} | {q['fair_over'].mean():.1%} | "
                   f"{100 * (q['y'].mean() - q['fair_over'].mean()):+.1f} | – | – |")
    return out


# ------------------------------------------------------------- report -----
def _f(x, pct=False, pts=False, d=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "–"
    if pts:
        return f"{100 * x:+.1f}"
    if pct:
        return f"{x:+.1%}"
    return f"{x:+.{d}f}"


def report() -> str:
    R, TR, C, X = run()
    T = X["T"]
    R.drop(columns=["mask"]).to_csv(OUT / "tests.csv", index=False)
    TR.to_csv(OUT / "trends.csv", index=False)
    C.drop(columns=["mask"]).to_csv(OUT / "candidates.csv", index=False)
    g = T["games"]
    cov = []
    for k, d in T.items():
        for sp in ("discovery", "holdout", "live"):
            q = d[d["split"] == sp]
            cov.append(f"| {k} | {sp} | {len(q):,} | {q['date'].min() if len(q) else '–'} – {q['date'].max() if len(q) else '–'} |")
    n_tests = int(R["n_tests_total"].iloc[0])
    nb = int(R["bh_disc"].sum() + TR["bh_disc"].sum())
    md = ["# Pattern scan: observed vs expected", "",
          f"Built {date.today().isoformat()} by `python -m nhlpipe.patterns.scan`. Research only: no bets, no method changed. "
          "Rules are in the docstring of `nhlpipe/patterns/scan.py` and were fixed before the first run.", "",
          "**How to read it.** *Expected* = Pinnacle's no-vig chance at pick time. *Edge* = actual hit rate minus expected, "
          "in percentage points. *z* = how many standard errors the edge is from zero (|z| ≈ 2 is the usual 5% bar for ONE test; "
          "with hundreds of tests, several will pass that bar by luck, which is what the Benjamini-Hochberg (BH) correction and the "
          "untouched holdout are for). A pattern only counts if it was found in DISCOVERY and then showed up again in the HOLDOUT. "
          "To make money an edge must also beat the bookmaker's margin, roughly 2 to 2.5 points on game lines and more on props.", "",
          "## 1. Data", "", "| Table | Sample | Rows | Dates |", "|---|---|--:|---|", *cov, "",
          f"Discovery tests run: **{n_tests:,}** (slices + trend tests, all markets). Expected false positives at p < 0.05 by luck alone: ~{0.05 * n_tests:.0f}. "
          f"Discovery tests surviving BH at q = {Q}: **{nb}**.", "",
          "## 2. Is the market itself biased? (calibration, no features)", "", *calibration(T),
          "## 3. Evan's under rule (pre-specified)", "", *evan(T), "",
          "## 4. Is there more signal than chance? (normality check of the z-scores)", "", *z_normality(R, TR), ""]
    # candidates table
    md += ["## 5. Candidates from discovery and whether they held up", "",
           "Sorted by discovery |z|. Direction = the side the slice beat its price on. Holdout p is one-sided in that direction. "
           "'Holds up' = holdout p < 0.05 and survives BH across all candidates. Drift = average move of Pinnacle's price toward the "
           "pattern between pick time and the close (positive = the market later agreed).", "",
           "| Market | Slice | Why picked | Side | Disc n | Disc edge | Disc z | Hold n | Hold edge | Hold p | Live n | Live edge | Hold ROI Pinnacle | Hold drift | Holds up |",
           "|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|"]
    C = C.assign(a=C["discovery_z"].abs()).sort_values(["family", "a"], ascending=[True, False])
    for r in C.to_dict("records"):
        side = FAMILIES[r["family"]][5][0 if r["dir"] > 0 else 1]
        md.append(f"| {r['family']} | {r['slice']} | {r['candidate']} | {side} | {r['discovery_n']} | {_f(r['discovery_edge'], pts=True)} | "
                  f"{_f(r['discovery_z'])} | {r['holdout_n']} | {_f(r['holdout_edge'] * r['dir'], pts=True) if r['holdout_n'] else '–'} | "
                  f"{r['holdout_p1']:.3f} | {r['live_n']} | {_f(r['live_edge'] * r['dir'], pts=True) if r['live_n'] else '–'} | "
                  f"{_f(r.get('holdout_roi_pin'), pct=True)} | {_f(r.get('holdout_drift'), pts=True)} | {'YES' if r['holds_up'] else 'no'} |")
    md += ["", "Holdout and live edges are shown in the candidate's direction (positive = it kept working).", ""]
    # strongest trends
    md += ["## 6. Strongest trend tests (does the gap grow with the feature?)", "",
           "b = change in log-odds per 1 standard deviation of the feature, after the market price. Top 8 per market by discovery |z|.", "",
           "| Market | Feature | Disc z | Holdout z (same sign = kept) | Live z | BH (disc) |", "|---|---|--:|--:|--:|---|"]
    for fam, q in TR.assign(a=TR["discovery_z"].abs()).sort_values("a", ascending=False).groupby("family", sort=False):
        for r in q.head(8).to_dict("records"):
            md.append(f"| {fam} | {r['feature']} | {_f(r['discovery_z'])} | {_f(r['holdout_z'])} | {_f(r['live_z'])} | {'yes' if r['bh_disc'] else ''} |")
    md += ["", "## 7. Goals distribution vs the market's implied Poisson", "", *goals_distribution(T), "",
           "Odd totals (5, 7, 9) are far more common than even ones (4, 6, 8) because a game tied after regulation "
           "always gets one more goal (overtime or the shootout's +1). That is why a plain Poisson fails, and why a "
           "whole-number line such as 6.0 pushes less often than a naive model expects. Pinnacle's main-line prices "
           "already reflect it (section 2 shows no total bias), so it is a modelling fact, not an edge.", "",
           "## 8. Patterns that kept the same direction everywhere", "", *consistent(C), "",
           "## 9. Shots model (M6 signal) by month", "", *model_by_month(T), "",
           "## 10. Player points overs by position and line (price check)", "",
           "Best US-book cost exists for 2025-26 only (live props come from the shadow board).", "", *points_d(T), "",
           "## 11. Limits", "",
           "- 2025-26 starters are projected by a rule (right 83% of the time); live uses DailyFaceoff. A wrong starter blurs goalie patterns.",
           "- Injuries and line changes are not in the 2025-26 archive, so they can't be scanned yet.",
           "- Live 2026-27 is small (a few hundred games), so a live miss is weak evidence either way.",
           "- Closing prices for 2025-26 exist only where a snapshot was cached within 30 minutes of the start.",
           "- Prop slices cluster by game; patterns among lines of the same game are not independent.", ""]
    txt = "\n".join(md) + "\n"
    (OUT / "report.md").write_text(txt)
    return txt


if __name__ == "__main__":
    print(report())
