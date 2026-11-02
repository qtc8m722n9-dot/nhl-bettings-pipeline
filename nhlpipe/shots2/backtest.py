"""Shots model v2: train on past seasons, test on 2025-26 against the market.

python -m nhlpipe.shots2.backtest            (offline: uses data/shots2 + data/backtest caches)

Stages (all strictly date-ordered, no future data):
  1. validation   fit on 2023-24, score 2024-25 (choose GLM vs boosted, check calibration)
  2. test         fit on 2023-24 + 2024-25, predict every 2025-26 skater-game
  3. grading      a) every skater-game: NB log score vs the old M4 (Poisson) mean
                  b) every Pinnacle-priced SOG line at pick time: log loss of model,
                     Pinnacle pick-time and Pinnacle close; encompassing regression
                     outcome ~ logit(Pinnacle) + logit(model)
                  c) bets: blend weights fit on Oct-Dec 2025, frozen, bets graded Jan-Apr 2026
                     (and the pure model over the whole season, for comparison)
Writes data/shots2/report.md, data/shots2/bets.csv, data/shots2/lines.csv
"""
import gzip
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from ..backtest import oddshist
from ..backtest import pipeline as BP
from ..names import norm
from . import features, model, pull

ROOT = pull.ROOT
SEASONS = ["20222023", "20232024", "20242025", "20252026"]
TEST_START, SPLIT, TEST_END = date(2025, 10, 15), date(2026, 1, 1), date(2026, 4, 16)
EDGE_MIN, EDGE_MAX, MAX_PER_GAME = 0.03, 0.12, 3
PICKEM = {"underdog", "prizepicks"}


# ------------------------------------------------------------------ data ----
def load() -> pd.DataFrame:
    stats = pd.concat([pull.load_stats(s) for s in SEASONS], ignore_index=True)
    games = [g for s in SEASONS for g in pull.schedule(s)]
    mp = pd.read_csv(ROOT / "mp_teams.csv.gz")
    s = features.build(stats, games, mp, TEST_START)
    s = features.add_h2h(s, "mu_base")
    s["season"] = s["gameId"] // 1_000_000
    s["key"] = s["skaterFullName"].map(norm)
    sch = pd.DataFrame(games)[["game_id", "home", "away"]].rename(columns={"game_id": "gameId"})
    s = s.merge(sch, on="gameId", how="left")
    s["game_key"] = s["away"] + "@" + s["home"]
    return s


def _cached(kind: str, path: str, params: dict, iso: str) -> dict | None:
    p = oddshist._path(kind, iso, f"{path}|{json.dumps(params, sort_keys=True)}")
    return json.loads(gzip.decompress(p.read_bytes())) if p.exists() else None


def sog_lines() -> pd.DataFrame:
    """Every archived SOG price at the 13:50 pick snapshot (+ Pinnacle close where cached)."""
    rows = []
    d = TEST_START
    while d <= TEST_END:
        t = BP.pick_dt(d)
        iso = BP._iso(t)
        feat = _cached("featured", f"/historical/sports/{oddshist.SPORT}/odds",
                       {"bookmakers": oddshist.BOOKS, "date": iso, "markets": ",".join(oddshist.FEATURED)}, iso)
        if feat:
            for ev in BP._slate_events(feat, d, t):
                pick = _cached("event", f"/historical/sports/{oddshist.SPORT}/events/{ev['id']}/odds",
                               {"bookmakers": oddshist.BOOKS, "date": iso, "markets": ",".join(oddshist.PROPS)}, iso)
                ciso = BP._iso(BP._utc(ev["commence_time"]) - BP.CLOSE_LEAD)
                close = _cached("event", f"/historical/sports/{oddshist.SPORT}/events/{ev['id']}/odds",
                                {"bookmakers": oddshist.BOOKS, "date": ciso, "markets": ",".join(oddshist.PROPS)}, ciso)
                gk = f"{BP.TMAP.get(norm(ev['away_team']))}@{BP.TMAP.get(norm(ev['home_team']))}"
                for snap, resp in (("pick", pick), ("close", close)):
                    data = (resp or {}).get("data") or {}
                    for b in data.get("bookmakers", []):
                        for m in b.get("markets", []):
                            if m["key"] != "player_shots_on_goal":
                                continue
                            for o in m["outcomes"]:
                                rows.append({"date": d, "game_key": gk, "event_id": ev["id"], "commence": ev["commence_time"],
                                             "snap": snap, "book": b["key"], "key": norm(o.get("description")),
                                             "player": o.get("description"), "line": o.get("point"),
                                             "side": "over" if o["name"].lower() == "over" else "under",
                                             "american": o.get("price")})
        d += timedelta(days=1)
    df = pd.DataFrame(rows)
    df["prob"] = df["american"].map(BP.american_to_prob)
    return df


def fair_table(lines: pd.DataFrame, snap: str, book: str = "pinnacle") -> pd.DataFrame:
    x = lines[(lines["snap"] == snap) & (lines["book"] == book)]
    w = x.pivot_table(index=["date", "game_key", "key", "line"], columns="side", values="prob", aggfunc="first").dropna()
    w["fair_over"] = [model.power_devig(o, u) for o, u in zip(w["over"], w["under"])]
    return w[["fair_over"]].rename(columns={"fair_over": f"{book}_{snap}"}).reset_index()


# ------------------------------------------------------------- metrics ----
def _ll(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def _boot_dates(df: pd.DataFrame, fn, n=1000, seed=3):
    days = df["date"].unique()
    rng = np.random.default_rng(seed)
    by = {d: g for d, g in df.groupby("date")}
    vals = []
    for _ in range(n):
        pick = rng.choice(days, len(days))
        vals.append(fn(pd.concat([by[d] for d in pick])))
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def calib(p, y, bins=(0, .2, .3, .4, .5, .6, .7, .8, 1)) -> list[str]:
    out = []
    c = pd.cut(p, bins)
    for b, g in pd.DataFrame({"p": p, "y": y, "b": c}).groupby("b", observed=True):
        out.append(f"| {b} | {len(g)} | {g['p'].mean():.3f} | {g['y'].mean():.3f} |")
    return out


# ----------------------------------------------------------------- main ----
def run() -> None:
    md = ["# Shots model v2 backtest", ""]
    s = load()
    s = s[s["n_prior"] >= 1]
    tr1, va = s[s["season"] == 2023], s[s["season"] == 2024]
    md += ["## 1. Validation (fit 2023-24, score 2024-25 skater-games)", "",
           "| Model | NB log score / game | Poisson dev. | Mean pred | Mean actual |", "|---|--:|--:|--:|--:|"]
    best, best_ls = None, -1e9
    for kind in ("glm", "hgb"):
        m = model.ShotsModel(kind).fit(tr1)
        mu = m.predict_mean(va)
        ls = float(m.log_score(mu, va["shots"].to_numpy()).mean())
        dev = float(np.mean(2 * (np.where(va["shots"] > 0, va["shots"] * np.log(va["shots"] / mu), 0) - (va["shots"] - mu))))
        md.append(f"| v2 {kind} (alpha {m.alpha:.3f}) | {ls:.4f} | {dev:.4f} | {mu.mean():.3f} | {va['shots'].mean():.3f} |")
        if ls > best_ls:
            best, best_ls = kind, ls
    mu1 = np.clip(model.baseline_v1(va), 0.05, None)
    from scipy import stats as st
    ls1 = float(st.poisson.logpmf(va["shots"], mu1).mean())
    md += [f"| old M4 formula (Poisson) | {ls1:.4f} | – | {mu1.mean():.3f} | {va['shots'].mean():.3f} |", "",
           f"Kept: **{best}** (higher log score is better).", ""]

    # coefficients (GLM) for interpretability
    glm = model.ShotsModel("glm").fit(tr1)
    coefs = glm.m.named_steps["poissonregressor"].coef_
    md += ["GLM effects (per 1 SD of each input, multiplicative on expected shots):", "",
           "| Input | Effect |", "|---|--:|"]
    for f, c in sorted(zip(model.FEATURES, coefs), key=lambda x: -abs(x[1])):
        md.append(f"| {f} | {np.exp(c) - 1:+.1%} |")
    md.append("")

    # ---- test season --------------------------------------------------------
    m = model.ShotsModel(best).fit(s[s["season"].isin([2023, 2024])])
    te = s[(s["season"] == 2025)].copy()
    te["mu"] = m.predict_mean(te)
    te["mu_v1"] = np.clip(model.baseline_v1(te), 0.05, None)
    ls2 = float(m.log_score(te["mu"].to_numpy(), te["shots"].to_numpy()).mean())
    ls1t = float(st.poisson.logpmf(te["shots"], te["mu_v1"]).mean())
    md += ["## 2. Test season 2025-26: every skater-game", "",
           f"- skater-games: {len(te):,}",
           f"- NB log score per game: v2 {ls2:.4f} vs old M4 {ls1t:.4f} (higher is better; difference {ls2 - ls1t:+.4f})",
           f"- mean predicted {te['mu'].mean():.3f} vs actual {te['shots'].mean():.3f}", ""]

    # ---- market lines -------------------------------------------------------
    L = sog_lines()
    L = L[L["line"].notna()]
    pin = fair_table(L, "pick").merge(fair_table(L, "close"), on=["date", "game_key", "key", "line"], how="left")
    te_key = te[["date", "game_key", "key", "mu", "mu_v1", "shots", "playerId", "teamAbbrev"]]
    J = pin.merge(te_key, on=["date", "game_key", "key"], how="inner")
    J["y"] = (J["shots"] > J["line"]).astype(int)
    J["p_v2"] = m.p_over(J["mu"].to_numpy(), J["line"].to_numpy())
    J["p_v1"] = model.poisson_over(J["mu_v1"].to_numpy(), J["line"].to_numpy())
    J.to_csv(ROOT / "lines.csv", index=False)
    matched = len(J) / max(len(pin), 1)
    md += ["## 3. Every Pinnacle-priced SOG line at pick time (2025-26)", "",
           f"- lines: {len(J):,} ({matched:.0%} of Pinnacle lines matched to a skater-game); with a Pinnacle close: {J['pinnacle_close'].notna().sum():,}",
           "", "| Forecast | Log loss (lower = better) | Brier |", "|---|--:|--:|"]
    for name, col in (("old M4 formula", "p_v1"), ("v2 model", "p_v2"), ("Pinnacle at 1:50 PM", "pinnacle_pick")):
        md.append(f"| {name} | {_ll(J[col], J['y']):.4f} | {np.mean((J[col] - J['y']) ** 2):.4f} |")
    jc = J.dropna(subset=["pinnacle_close"])
    md.append(f"| Pinnacle close (subset n={len(jc):,}) | {_ll(jc['pinnacle_close'], jc['y']):.4f} | {np.mean((jc['pinnacle_close'] - jc['y']) ** 2):.4f} |")
    md += ["", "Calibration of v2 (all lines):", "", "| Predicted bin | n | Avg predicted | Actual over rate |", "|---|--:|--:|--:|"]
    md += calib(J["p_v2"], J["y"]) + [""]

    # encompassing regression: does the model add information beyond Pinnacle?
    def enc(df):
        X = np.column_stack([model.logit(df["pinnacle_pick"]), model.logit(df["p_v2"])])
        lr = LogisticRegression(C=1e6, max_iter=1000).fit(X, df["y"])
        return lr
    lr = enc(J)
    lo, hi = _boot_dates(J, lambda d: enc(d).coef_[0][1], n=300)
    md += ["Encompassing test, outcome ~ a·logit(Pinnacle) + b·logit(v2):", "",
           f"- a (Pinnacle) = {lr.coef_[0][0]:.3f}, **b (v2) = {lr.coef_[0][1]:.3f} (95% CI {lo:.3f} to {hi:.3f})**",
           "- b > 0 with a CI above 0 means v2 knows something Pinnacle's 1:50 PM price doesn't.", ""]

    # ---- bets ---------------------------------------------------------------
    early = J[J["date"] < SPLIT]
    blend = enc(early)

    def p_blend(df):
        X = np.column_stack([model.logit(df["pinnacle_pick"]), model.logit(df["p_v2"])])
        return blend.predict_proba(X)[:, 1]

    offers = L[(L["snap"] == "pick") & L["book"].isin(BP.VENUES)].copy()
    offers["cost"] = np.where(offers["book"].isin(PICKEM), 1 / 1.73, offers["prob"])
    offers = offers.merge(J[["date", "game_key", "key", "line", "pinnacle_pick", "pinnacle_close", "p_v2", "y", "shots",
                             "teamAbbrev"]], on=["date", "game_key", "key", "line"], how="inner")
    offers["p_pure"] = np.where(offers["side"] == "over", offers["p_v2"], 1 - offers["p_v2"])
    pb = p_blend(offers)
    offers["p_blend"] = np.where(offers["side"] == "over", pb, 1 - pb)
    offers["win"] = np.where(offers["side"] == "over", offers["y"], 1 - offers["y"])
    offers["close_fair"] = np.where(offers["side"] == "over", offers["pinnacle_close"], 1 - offers["pinnacle_close"])

    def select(df, pcol):
        d = df.copy()
        d["edge"] = d[pcol] - d["cost"]
        d = d[(d["edge"] >= EDGE_MIN) & (d["edge"] <= EDGE_MAX)]
        d = d.sort_values("edge", ascending=False).drop_duplicates(["date", "key"])  # one bet per player, best price
        d = d.groupby(["date", "game_key"]).head(MAX_PER_GAME)
        d["profit"] = np.where(d["win"] == 1, 1 / d["cost"] - 1, -1.0)
        d["clv"] = d["close_fair"] - d["cost"]
        return d

    def summ(d, label):
        if d.empty:
            return f"| {label} | 0 | – | – | – | – | – | – |"
        roi = d["profit"].mean()
        rlo, rhi = _boot_dates(d, lambda x: x["profit"].mean())
        c = d.dropna(subset=["clv"])
        clo, chi = _boot_dates(c, lambda x: x["clv"].mean()) if len(c) > 20 else (np.nan, np.nan)
        return (f"| {label} | {len(d)} | {d['win'].mean():.1%} | {d['cost'].mean():.1%} | {roi:+.1%} ({rlo:+.1%}, {rhi:+.1%}) | "
                f"{c['clv'].mean() * 100:+.2f} ({clo * 100:+.2f}, {chi * 100:+.2f}) | {(c['clv'] > 0).mean():.0%} | "
                f"{d.groupby(['date', 'game_key']).size().mean():.2f} |")

    late = offers[offers["date"] >= SPLIT]
    bets_blend = select(late, "p_blend")
    bets_pure_late = select(late, "p_pure")
    bets_pure_all = select(offers, "p_pure")
    bets_pk = select(late[late["book"].isin(PICKEM)], "p_blend")
    md += ["## 4. Bets", "",
           f"Rule: edge ≥ {EDGE_MIN:.0%} and ≤ {EDGE_MAX:.0%}, best price per player, up to {MAX_PER_GAME} players per game. "
           "Blend weights fit on Oct–Dec 2025 only, then frozen. Win % should be compared with the breakeven (avg cost).", "",
           "| Strategy | Bets | Win % | Breakeven | ROI (95% CI) | CLV vs Pinnacle close, pp (95% CI) | Beat close | Bets/game |",
           "|---|--:|--:|--:|--:|--:|--:|--:|",
           summ(bets_blend, "v2 blended with Pinnacle, Jan–Apr (out of sample)"),
           summ(bets_pk, "  …pick'em apps only"),
           summ(bets_pure_late, "v2 pure model, Jan–Apr"),
           summ(bets_pure_all, "v2 pure model, full season"), ""]
    if not bets_blend.empty:
        sides = bets_blend.groupby("side").agg(n=("win", "size"), win=("win", "mean"), roi=("profit", "mean"))
        md += ["By side (blended, Jan–Apr):", "", "| Side | Bets | Win % | ROI |", "|---|--:|--:|--:|"]
        md += [f"| {k} | {r.n} | {r.win:.1%} | {r.roi:+.1%} |" for k, r in sides.iterrows()] + [""]
    pd.concat([bets_blend.assign(strategy="blend_late"), bets_pure_all.assign(strategy="pure_all")]).to_csv(ROOT / "bets.csv", index=False)

    # leak guard
    md += ["## Leak checks", "",
           "- every feature is built from games on earlier dates only (decayed sums exclude the current row; "
           "schedule features use only the schedule); model fit on 2023-24 / 2024-25 only",
           f"- Pinnacle pick-time prices are the 13:50 ET snapshot; close is ~2 min before each game",
           f"- blend weights fit on {early['date'].min()}–{early['date'].max()} and graded from {SPLIT}", ""]
    (ROOT / "report.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    run()
