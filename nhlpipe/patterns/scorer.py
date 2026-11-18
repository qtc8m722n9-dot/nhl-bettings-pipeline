"""H21: goalscorer models, price-driven (P) vs price-blind (B). Spec: docs/hypotheses_2026-11-18_goalscorers.md.

python -m nhlpipe.patterns.scorer -> data/patterns/scorer_rows.csv.gz, data/patterns/goalscorers.md
No API calls: 2025-26 anytime-goal prices come from the cache filled by the atg2526 task.
"""
import glob
import json
import math
from datetime import date, timedelta, timezone

import numpy as np
import pandas as pd
from scipy import stats

from .. import fair
from ..backtest.pipeline import TMAP, odds_frame, pick_dt
from ..names import norm
from ..shots2 import features as sfeat, pull as spull
from .data import DATA, ODDS25, OUT, US_BOOKS, _load, _ts, team_asof

SEASONS = ["20222023", "20232024", "20242025", "20252026", "20262027"]
CUTOFF = date(2025, 10, 1)          # league priors in the shots features: games before 2025-26 only
SH_PRIOR = 223                      # shots of position-average shooting % added (research: half-signal point)
TEAM_PRIOR_GP = 10
FACTORS = ["ev_toi", "pp_toi", "D", "home", "b2b", "opp_b2b", "opp_xga_pg", "opp_save_pg", "team_xgf_pg",
           "opp_pen_ratio", "log_n_prior"]
EDGE = 0.03


# --------------------------------------------------------------- frame ----
def skater_frame(hist: pd.DataFrame | None = None, games: list | None = None, mp: pd.DataFrame | None = None) -> pd.DataFrame:
    """Point-in-time scorer features. Defaults: every cached season. Live passes today's placeholder rows in `hist`."""
    hist = hist if hist is not None else pd.concat([spull.load_stats(s) for s in SEASONS], ignore_index=True)
    games = games if games is not None else [g for s in SEASONS for g in spull.schedule(s, refresh=False)]
    mp = mp if mp is not None else pd.read_csv(DATA / "shots2" / "mp_teams.csv.gz")
    s = sfeat.build(hist, games, mp, CUTOFF)
    s = s[(s["n_prior"] >= 1) & s["mu_base"].notna()].copy()
    s["season"] = s["gameId"] // 1_000_000
    s["D"] = (s["positionCode"] == "D").astype(float)
    s["log_n_prior"] = np.log1p(s["n_prior"].clip(upper=300))
    # shooting %: this season before the game + all of last season, shrunk to the position rate
    s = s.sort_values(["playerId", "date", "gameId"])
    g = s.groupby(["playerId", "season"])
    s["g_cur"] = g["goals"].cumsum() - s["goals"]
    s["s_cur"] = g["shots"].cumsum() - s["shots"]
    tot = s.groupby(["playerId", "season"])[["goals", "shots"]].sum().reset_index()
    tot["season"] += 1
    s = s.merge(tot.rename(columns={"goals": "g_prev", "shots": "s_prev"}), on=["playerId", "season"], how="left")
    s[["g_prev", "s_prev"]] = s[["g_prev", "s_prev"]].fillna(0)
    lg = s.groupby(["season", "D"])[["goals", "shots"]].sum()
    lg = (lg["goals"] / lg["shots"]).rename("lg_sh").reset_index()
    lg["season"] += 1  # use the previous season's league rate (known in advance)
    s = s.merge(lg, on=["season", "D"], how="left")
    s["lg_sh"] = s["lg_sh"].fillna(s.groupby("D")["lg_sh"].transform("mean")).fillna(0.09)
    s["sh_pct"] = (s["g_cur"] + s["g_prev"] + SH_PRIOR * s["lg_sh"]) / (s["s_cur"] + s["s_prev"] + SH_PRIOR)
    s["player_rate"] = s["mu_base"].clip(lower=0.05) * s["sh_pct"]
    # team context, season to date before the game
    ta = team_asof(mp, list(s["date"]))
    ta = ta[["team", "date", "gp", "gf", "gf_pg", "xgf_pg", "xga_pg", "save_pg"]]
    lgf = ta.groupby("date").apply(lambda q: q["gf"].sum() / q["gp"].sum()).rename("lg_gf").reset_index()
    ta = ta.merge(lgf, on="date")
    ta["team_rate"] = (ta["gf"] + TEAM_PRIOR_GP * ta["lg_gf"]) / (ta["gp"] + TEAM_PRIOR_GP)
    s = s.merge(ta[["team", "date", "team_rate", "xgf_pg"]].rename(columns={"team": "teamAbbrev", "xgf_pg": "team_xgf_pg"}),
                on=["teamAbbrev", "date"], how="left")
    s = s.merge(ta[["team", "date", "xga_pg", "save_pg"]].rename(columns={"team": "opp", "xga_pg": "opp_xga_pg", "save_pg": "opp_save_pg"}),
                on=["opp", "date"], how="left")
    s["y"] = (s["goals"] >= 1).astype(float)
    s["key"] = s["skaterFullName"].map(norm)
    s["game_key"] = s["opp"].where(s["home"] == 1, s["teamAbbrev"]) + "@" + s["teamAbbrev"].where(s["home"] == 1, s["opp"])
    s["date"] = s["date"].astype(str)
    s = s[~s.duplicated(["date", "game_key", "key"], keep=False)]
    keep = ["date", "season", "gameId", "game_key", "key", "playerId", "skaterFullName", "teamAbbrev", "opp", "home",
            "goals", "y", "mu_base", "sh_pct", "player_rate", "team_rate", "n_prior"] + FACTORS
    return s[[c for c in dict.fromkeys(keep)]].dropna(subset=["team_rate", "opp_xga_pg"])


# ------------------------------------------------------------ model B ----
def poisson_fit(X, y, off, ridge=1e-4):
    Xc = np.column_stack([np.ones(len(X)), X])
    b = np.zeros(Xc.shape[1])
    b[0] = math.log(y.mean() / np.exp(off).mean())
    for _ in range(50):
        mu = np.exp(off + Xc @ b)
        H = Xc.T @ (Xc * mu[:, None]) + ridge * np.eye(len(b))
        step = np.linalg.solve(H, Xc.T @ (y - mu) - ridge * b)
        b += step
        if np.abs(step).max() < 1e-9:
            break
    se = np.sqrt(np.diag(np.linalg.inv(Xc.T @ (Xc * np.exp(off + Xc @ b)[:, None]))))
    return b, se


class ModelB:
    def fit(self, tr: pd.DataFrame, factors=FACTORS):
        self.f = list(factors)
        X = tr[self.f].to_numpy(float)
        self.m, self.sd = np.nanmean(X, 0), np.nanstd(X, 0)
        self.sd[self.sd == 0] = 1
        Z = np.nan_to_num((X - self.m) / self.sd)
        self.b, self.se = poisson_fit(Z, tr["goals"].to_numpy(float), np.log(tr["player_rate"].to_numpy()))
        return self

    def to_json(self) -> dict:
        return {"factors": self.f, "mean": self.m.tolist(), "sd": self.sd.tolist(), "b": self.b.tolist()}

    @classmethod
    def from_json(cls, j: dict) -> "ModelB":
        m = cls()
        m.f, m.m, m.sd, m.b = j["factors"], np.array(j["mean"]), np.array(j["sd"]), np.array(j["b"])
        return m

    def prob(self, d: pd.DataFrame) -> np.ndarray:
        Z = np.nan_to_num((d[self.f].to_numpy(float) - self.m) / self.sd)
        lam = np.exp(np.log(d["player_rate"].to_numpy()) + self.b[0] + Z @ self.b[1:])
        return 1 - np.exp(-lam)


# ------------------------------------------------------------ model P ----
def _total_mean(line: float, p_over: float) -> float:
    lo, hi = 1.0, 15.0
    for _ in range(60):
        m = (lo + hi) / 2
        over = stats.poisson.sf(math.floor(line), m)
        under = stats.poisson.cdf(math.ceil(line) - 1, m)
        q = over / (over + under)
        lo, hi = (m, hi) if q < p_over else (lo, m)
    return (lo + hi) / 2


def _split(mu: float, p_home: float) -> tuple[float, float]:
    k = np.arange(0, 16)
    lo, hi = 0.05, 0.95
    for _ in range(50):
        s = (lo + hi) / 2
        ph, pa = stats.poisson.pmf(k, mu * s), stats.poisson.pmf(k, mu * (1 - s))
        j = np.outer(ph, pa)
        q = np.tril(j, -1).sum() + 0.5 * np.trace(j)
        lo, hi = (s, hi) if q < p_home else (lo, s)
    s = (lo + hi) / 2
    return mu * s, mu * (1 - s)


def team_lambdas() -> pd.DataFrame:
    g = pd.read_csv(OUT / "games.csv.gz")
    g = g[g["tot_line"].notna() & g["over_fair"].notna() & g["ml_home_fair"].notna()]
    rows = []
    for r in g.to_dict("records"):
        mu = _total_mean(r["tot_line"], r["over_fair"])
        lh, la = _split(mu, r["ml_home_fair"])
        rows.append({"date": str(r["date"]), "game_key": f"{r['away']}@{r['home']}", "home_team": r["home"], "lam_home": lh, "lam_away": la})
    return pd.DataFrame(rows)


# -------------------------------------------------------------- prices ----
def _atg_rows(od: pd.DataFrame) -> list[dict]:
    a = od[(od["market"] == "player_goal_scorer_anytime") & od["implied_prob"].notna()].copy()
    if a.empty:
        return []
    a["player"] = a["player"].fillna("")
    pin = a[a["book"] == "pinnacle"]
    pv = pin.pivot_table(index=["event_id", "player", "home", "away"], columns="outcome", values="implied_prob", aggfunc="first")
    out = []
    us = a[a["book"].isin(US_BOOKS) & (a["outcome"] == "Yes")].groupby(["event_id", "player"])["implied_prob"].min()
    for (eid, pl, h, aw), r in pv.iterrows():
        if pd.isna(r.get("Yes")) or pd.isna(r.get("No")):
            continue
        f = fair.power_fair(pd.Series([r["Yes"], r["No"]])).iloc[0]
        out.append({"game_key": f"{aw}@{h}", "key": norm(pl), "pin_fair": f, "pin_yes_imp": r["Yes"],
                    "best_yes": us.get((eid, pl), np.nan)})
    return out


def prices_2526() -> pd.DataFrame:
    rows = []
    for dd in sorted((ODDS25 / "event").iterdir()):
        d = date.fromisoformat(dd.name)
        if not (date(2025, 10, 1) <= d <= date(2026, 4, 30)):
            continue
        t = pick_dt(d).astimezone(timezone.utc)
        fs = [f for f in dd.glob("*.json.gz") if _ts(f) == t]
        if not fs:
            continue
        od = odds_frame([_load(f) for f in fs], TMAP)
        if od.empty or "player_goal_scorer_anytime" not in set(od["market"]):
            continue
        for r in _atg_rows(od):
            rows.append({**r, "date": d.isoformat()})
    d = pd.DataFrame(rows)
    return d.drop_duplicates(["date", "game_key", "key"]) if len(d) else pd.DataFrame(columns=["date", "game_key", "key"])


def prices_live() -> pd.DataFrame:
    rows = []
    for od_dir in sorted((DATA / "odds").iterdir()):
        pk = DATA / "picks" / f"{od_dir.name}.csv"
        if not pk.exists():
            continue
        snap = str(int(pd.read_csv(pk)["odds_snapshot"].dropna().iloc[0])).zfill(4)
        f = od_dir / snap / "odds_long.csv"
        if not f.exists():
            continue
        od = pd.read_csv(f)
        lock = pd.Timestamp(od["snapshot_et"].iloc[0])
        od = od[pd.to_datetime(od["commence_utc"]) > lock]
        for r in _atg_rows(od):
            rows.append({**r, "date": od_dir.name})
        sh = DATA / "shadow" / f"{od_dir.name}.csv"
        if sh.exists():
            s = pd.read_csv(sh)
            k = s[(s["venue"] == "kalshi") & (s["market"] == "player_goals") & (s["line"] == 0.5) & (s["side"] == "yes")]
            for x in k.to_dict("records"):
                rows.append({"date": od_dir.name, "game_key": x["game_key"], "key": norm(str(x["player"])),
                             "kalshi_cost": x["cost"], "_k": 1})
    d = pd.DataFrame(rows)
    a = d[d.get("_k").isna()].drop(columns="_k") if "_k" in d else d
    k = d[d["_k"] == 1][["date", "game_key", "key", "kalshi_cost"]].drop_duplicates(["date", "game_key", "key"]) if "_k" in d else None
    a = a.drop(columns=[c for c in ["kalshi_cost"] if c in a]).drop_duplicates(["date", "game_key", "key"])
    if k is not None:
        a = a.merge(k, on=["date", "game_key", "key"], how="outer")
    return a


# ---------------------------------------------------------------- eval ----
def _ll(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def _edge_z(q: pd.DataFrame) -> tuple[float, float]:
    r = q["y"] - q["pin_fair"]
    v = max(float((q["pin_fair"] * (1 - q["pin_fair"])).sum()), float((r.groupby(q["gid"]).sum() ** 2).sum()))
    return float(r.mean()), float(r.sum() / math.sqrt(v)) if v > 0 else np.nan


def run() -> str:
    S = skater_frame()
    tr = S[S["season"].isin([2022, 2023, 2024])]
    B = ModelB().fit(tr)
    (OUT / "scorer_B.json").write_text(json.dumps({"fit": "2022-23..2024-25 skater-games", "frozen": date.today().isoformat(), **B.to_json()}))
    lam = team_lambdas()
    E = S[S["season"].isin([2025, 2026])].merge(lam, on=["date", "game_key"], how="inner")
    E["lam_team"] = np.where(E["teamAbbrev"] == E["home_team"], E["lam_home"], E["lam_away"])
    E["p_P"] = 1 - np.exp(-E["lam_team"] * E["player_rate"] / E["team_rate"])
    E["p_B"] = B.prob(E)
    pr = pd.concat([prices_2526(), prices_live()], ignore_index=True, sort=False)
    E = E.merge(pr, on=["date", "game_key", "key"], how="left")
    E["gid"] = E["date"] + E["game_key"]
    E["sample"] = np.where(E["season"] == 2025, "2025-26", "2026-27 live")
    E.to_csv(OUT / "scorer_rows.csv.gz", index=False)

    md = ["# H21 Goalscorer models: price-driven (P) vs price-blind (B)", "",
          f"Run {date.today().isoformat()} by `python -m nhlpipe.patterns.scorer`. Spec: `docs/hypotheses_2026-11-18_goalscorers.md` "
          "(committed before the data was bought or looked at). P(score) = chance of at least one goal.", "",
          "**Model P** uses Pinnacle's game total and moneyline for each team's expected goals, times the player's share. "
          "**Model B** never sees a betting price: shots-rate x shooting % baseline plus game factors, fitted on 2022-23 to 2024-25.", "",
          "## 1. Accuracy on the same player-games (log loss, lower = better)", "",
          "| Sample | Player-games | Pinnacle no-vig | Model P | Model B | Actual scoring rate | Avg Pinnacle | Avg P | Avg B |",
          "|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for sp, q in E[E["pin_fair"].notna()].groupby("sample"):
        y = q["y"].to_numpy()
        md.append(f"| {sp} | {len(q):,} | {_ll(q['pin_fair'], y).mean():.4f} | {_ll(q['p_P'], y).mean():.4f} | {_ll(q['p_B'], y).mean():.4f} | "
                  f"{y.mean():.1%} | {q['pin_fair'].mean():.1%} | {q['p_P'].mean():.1%} | {q['p_B'].mean():.1%} |")
    allq = E.groupby("sample")
    md += ["", "Without the price filter (every skater-game the models can score, 2025-26 and live):", "",
           "| Sample | Player-games | Model P | Model B |", "|---|--:|--:|--:|"]
    for sp, q in allq:
        md.append(f"| {sp} | {len(q):,} | {_ll(q['p_P'], q['y']).mean():.4f} | {_ll(q['p_B'], q['y']).mean():.4f} |")
    # calibration
    md += ["", "## 2. Calibration (2025-26 + live, priced player-games)", "", "| Predicted band | Model P n / actual | Model B n / actual | Pinnacle n / actual |", "|---|--:|--:|--:|"]
    Q = E[E["pin_fair"].notna()]
    bands = [0, .1, .15, .2, .25, .3, .35, .45, 1]
    for lo, hi in zip(bands[:-1], bands[1:]):
        cells = []
        for col in ("p_P", "p_B", "pin_fair"):
            q = Q[(Q[col] > lo) & (Q[col] <= hi)]
            cells.append(f"{len(q):,} / {q['y'].mean():.1%}" if len(q) else "–")
        md.append(f"| {lo:.0%}-{hi:.0%} | {cells[0]} | {cells[1]} | {cells[2]} |")
    # single legs
    md += ["", "## 3. Single legs: model P(score) at least 3 pts above the price (YES)", "",
           "| Model | Sample | Venue | Legs | Hit | Avg cost | ROI | Edge vs Pinnacle fair, pts (z) |", "|---|---|---|--:|--:|--:|--:|--:|"]
    prim = {}
    for col, name in (("p_P", "Model P"), ("p_B", "Model B")):
        for sp, q in E.groupby("sample"):
            for venue, cost in (("best US book", "best_yes"), ("Kalshi (ask + fee)", "kalshi_cost")):
                if cost not in q:
                    continue
                L = q[q[cost].notna() & (q[col] - q[cost] >= EDGE)]
                if len(L) < 5:
                    continue
                roi = (L["y"] / L[cost] - 1).mean()
                Lf = L[L["pin_fair"].notna()]
                e, z = _edge_z(Lf) if len(Lf) >= 5 else (np.nan, np.nan)
                if sp == "2025-26" and venue == "best US book":
                    prim[name] = (e, z, len(Lf))
                md.append(f"| {name} | {sp} | {venue} | {len(L):,} | {L['y'].mean():.1%} | {L[cost].mean():.1%} | {roi:+.1%} | "
                          + ("–" if pd.isna(e) else f"{100 * e:+.1f} ({z:+.2f})") + " |")
    md += ["", "Primary comparison (pre-registered): edge vs Pinnacle fair of each model's single legs on 2025-26, one-sided p:", ""]
    for name, (e, z, n) in prim.items():
        md.append(f"- {name}: {100 * e:+.2f} pts over {n:,} legs, z {z:+.2f}, p = {stats.norm.sf(z):.3f} -> "
                  f"{'beats Pinnacle' if stats.norm.sf(z) < 0.05 else 'does not beat Pinnacle'}")
    # parlays
    md += ["", "## 4. Paper parlays: each night the 3 biggest-edge legs from different games (best US-book price)", "",
           "| Model | Sample | Nights | Hit (all 3) | Avg payout (x stake) | ROI |", "|---|---|--:|--:|--:|--:|"]
    for col, name in (("p_P", "Model P"), ("p_B", "Model B")):
        for sp, q in E.groupby("sample"):
            L = q[q["best_yes"].notna()].assign(edge=q[col] - q["best_yes"])
            L = L[L["edge"] >= EDGE].sort_values("edge", ascending=False).drop_duplicates(["date", "game_key"])
            nights = [x.head(3) for _, x in L.groupby("date") if len(x) >= 3]
            if not nights:
                continue
            hit = np.array([x["y"].prod() for x in nights])
            pay = np.array([1 / x["best_yes"].prod() for x in nights])
            md.append(f"| {name} | {sp} | {len(nights)} | {hit.mean():.1%} | {pay.mean():.1f} | {(hit * pay - 1).mean():+.1%} |")
    # model B factors
    md += ["", "## 5. Model B: which factors matter", "",
           "Coefficient = change in log scoring rate per 1 standard deviation (beyond the shots x shooting % baseline), fit 2022-25. "
           "Drop = how much worse 2025-26 log loss gets when the factor is removed and the model refit (x 10,000; bigger = more important).", "",
           "| Factor | Coefficient | SE | Drop |", "|---|--:|--:|--:|"]
    ev = E[E["sample"] == "2025-26"]
    base = _ll(B.prob(ev), ev["y"]).mean()
    for i, f in enumerate(FACTORS):
        Bf = ModelB().fit(tr, [x for x in FACTORS if x != f])
        drop = _ll(Bf.prob(ev), ev["y"]).mean() - base
        md.append(f"| {f} | {B.b[i + 1]:+.3f} | {B.se[i + 1]:.3f} | {1e4 * drop:+.1f} |")
    md.append(f"| (intercept vs baseline) | {B.b[0]:+.3f} | {B.se[0]:.3f} | |")
    txt = "\n".join(md) + "\n"
    (OUT / "goalscorers.md").write_text(txt)
    return txt


if __name__ == "__main__":
    print(run())
