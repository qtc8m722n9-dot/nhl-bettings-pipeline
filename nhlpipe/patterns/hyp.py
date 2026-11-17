"""Tests of pre-registered hypotheses H2, H4, H5 (docs/hypotheses_2026-11-17.md).

python -m nhlpipe.patterns.hyp   -> data/patterns/hypotheses_h2_h5.md
Uses the tables built by nhlpipe.patterns.data; no API calls.
"""
import glob
import json
import math
from datetime import date

import numpy as np
import pandas as pd
from scipy import stats

from .data import DATA, OUT
from .scan import _logit, _z, trend, load

POPULAR = {"TOR", "MTL", "EDM", "NYR", "BOS"}
CANADIAN = {"TOR", "MTL", "EDM", "OTT", "WPG", "CGY", "VAN"}
SHRINK_GAMES = 20


# ------------------------------------------------------------------ H2 ----
def rink_factors(dates: list[date]) -> pd.DataFrame:
    """(arena, date) -> rink factor from the previous season + current season before the date."""
    m = pd.read_csv(DATA / "shots2" / "mp_teams.csv.gz")
    a = m[m["situation"] == "all"].copy()
    a["d"] = pd.to_datetime(a["gameDate"].astype(str)).dt.date
    a["tot"] = a["shotsOnGoalFor"] + a["shotsOnGoalAgainst"]
    a["arena"] = np.where(a["home_or_away"] == "HOME", a["team"], a["opposingTeam"])
    out = []
    for D in sorted(set(dates)):
        S = D.year if D.month >= 8 else D.year - 1
        w = a[(a["season"] == S - 1) | ((a["season"] == S) & (a["d"] < D))]
        # each team's average total SOG in games NOT at arena X
        all_s = w.groupby("team")["tot"].agg(["sum", "count"])
        at = w.groupby(["team", "arena"])["tot"].agg(["sum", "count"])
        def not_at(team, arena):
            s, n = all_s.loc[team, "sum"], all_s.loc[team, "count"]
            if (team, arena) in at.index:
                s, n = s - at.loc[(team, arena), "sum"], n - at.loc[(team, arena), "count"]
            return s / n if n else np.nan
        h = w[w["home_or_away"] == "HOME"]
        for arena, g in h.groupby("team"):
            exp = np.array([0.5 * (not_at(arena, arena) + not_at(o, arena)) for o in g["opposingTeam"]])
            obs = g["tot"].to_numpy(float)
            ok = ~np.isnan(exp)
            if ok.sum() == 0:
                continue
            avg = exp[ok].mean()
            rf = (obs[ok].sum() + SHRINK_GAMES * avg) / (exp[ok].sum() + SHRINK_GAMES * avg)
            out.append({"arena": arena, "date": D, "rink_factor": rf, "rink_games": int(ok.sum())})
    return pd.DataFrame(out)


def _ll(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def h2(T) -> list[str]:
    from ..shots2.live import Frozen, PARAMS
    fr = Frozen(json.loads(PARAMS.read_text()))
    S = T["sog"].copy()
    S["arena"] = S["game_key"].str.split("@").str[1]
    rf = rink_factors(list(S["date"]))
    S = S.merge(rf, on=["arena", "date"], how="left")
    S["log_rf"] = np.log(S["rink_factor"])
    out = ["Rink factor = total shots recorded in an arena's games / what the same two teams record elsewhere "
           f"(previous season + this season before the game, shrunk with {SHRINK_GAMES} games at 1.0).", ""]
    top = rf[rf["date"] == rf["date"].max()].sort_values("rink_factor")
    out += [f"Latest factors ({top['date'].iloc[0]}): most generous " +
            ", ".join(f"{r.arena} {r.rink_factor:.3f}" for r in top.tail(4).iloc[::-1].itertuples()) +
            "; stingiest " + ", ".join(f"{r.arena} {r.rink_factor:.3f}" for r in top.head(4).itertuples()) + ".", ""]
    q_lo, q_hi = S.loc[S["split"] == "discovery", "rink_factor"].quantile([0.25, 0.75])
    out += ["| Sample | Lines | Trend z (pre-registered metric) | Over edge, generous quarter (RF > %.3f), pts | Over edge, stingy quarter (RF < %.3f), pts |" % (q_hi, q_lo),
            "|---|--:|--:|--:|--:|"]
    res = {}
    for sp in ("discovery", "holdout", "live"):
        q = S[(S["split"] == sp)].dropna(subset=["y", "fair_over", "log_rf"])
        _, z = trend(q["y"].to_numpy(float), q["fair_over"].to_numpy(float), q["log_rf"].to_numpy(float), q["gid"].to_numpy())
        hi, lo = q[q["rink_factor"] > q_hi], q[q["rink_factor"] < q_lo]
        eh = _z(hi["y"].to_numpy(float), hi["fair_over"].to_numpy(float), hi["gid"].to_numpy())
        el = _z(lo["y"].to_numpy(float), lo["fair_over"].to_numpy(float), lo["gid"].to_numpy())
        res[sp] = z
        out.append(f"| {sp} | {len(q):,} | {z:+.2f} | {100 * eh[0]:+.1f} (z {eh[1]:+.2f}, n {len(hi)}) | {100 * el[0]:+.1f} (z {el[1]:+.2f}, n {len(lo)}) |")
    p_hold = stats.norm.sf(res["holdout"])
    verdict = "PASSES" if (res["discovery"] > 0 and p_hold < 0.05) else "does not pass"
    out += ["", f"Pre-registered rule (discovery z > 0 and holdout one-sided p < 0.05): holdout p = {p_hold:.3f} -> **{verdict}**.", ""]
    # secondary: does a rink-adjusted M6 projection beat the plain one vs Pinnacle?
    out += ["Secondary: shots model with its projection multiplied by the rink factor (log loss, lower = better; "
            "the model alone, not blended):", "", "| Sample | Lines | Pinnacle | Model | Model x rink |", "|---|--:|--:|--:|--:|"]
    for sp in ("discovery", "holdout", "live"):
        q = S[(S["split"] == sp)].dropna(subset=["y", "fair_over", "mu", "rink_factor"])
        p0 = fr.p_over(q["mu"].to_numpy(), q["line"].to_numpy())
        p1 = fr.p_over(q["mu"].to_numpy() * q["rink_factor"].to_numpy(), q["line"].to_numpy())
        y = q["y"].to_numpy(float)
        out.append(f"| {sp} | {len(q):,} | {_ll(q['fair_over'].to_numpy(), y).mean():.4f} | {_ll(p0, y).mean():.4f} | {_ll(p1, y).mean():.4f} |")
    out += ["", "(2025-26 uses the out-of-sample projections from the backtest; the NB dispersion is the frozen live one.)"]
    return out


# ------------------------------------------------------------------ H4 ----
def h4(T) -> list[str]:
    g = T["games"]
    g = g[g["pl_fav"].notna() & g["y_over"].notna() & g["over_fair"].notna() & g["pl_fav_fair"].notna()].copy()
    fav_won = np.where(g["pl_fav_home"] == 1, g["y_home"], 1 - g["y_home"])
    fav_ml = np.where(g["pl_fav_home"] == 1, g["ml_home_fair"], 1 - g["ml_home_fair"])
    corners = {
        "Fav -1.5 AND over (pre-registered)": (g["y_pl_fav"] * g["y_over"], g["pl_fav_fair"] * g["over_fair"], (g["pin_pl_imp"], g["pin_over_imp"])),
        "Fav -1.5 AND under": (g["y_pl_fav"] * (1 - g["y_over"]), g["pl_fav_fair"] * (1 - g["over_fair"]), (g["pin_pl_imp"], g["pin_under_imp"])),
        "Dog +1.5 AND over": ((1 - g["y_pl_fav"]) * g["y_over"], (1 - g["pl_fav_fair"]) * g["over_fair"], (None, g["pin_over_imp"])),
        "Dog +1.5 AND under": ((1 - g["y_pl_fav"]) * (1 - g["y_over"]), (1 - g["pl_fav_fair"]) * (1 - g["over_fair"]), (None, g["pin_under_imp"])),
        "Fav moneyline AND over": (pd.Series(fav_won, index=g.index) * g["y_over"], pd.Series(fav_ml, index=g.index) * g["over_fair"], (None, g["pin_over_imp"])),
    }
    out = ["Observed rate of both legs hitting vs the product of the two Pinnacle fair prices (= what a venue that prices "
           "the legs as unrelated would charge). Edge > 0 = the pair hits more than an independent price assumes.", "",
           "| Pair | Sample | Games | Both hit | Product of fair prices | Edge, pts | z | ROI buying both legs at Pinnacle's own prices |",
           "|---|---|--:|--:|--:|--:|--:|--:|"]
    res = {}
    for name, (y, p, (c1, c2)) in corners.items():
        for sp in ("discovery", "holdout", "live"):
            m = (g["split"] == sp).to_numpy()
            yy, pp = y.to_numpy(float)[m], p.to_numpy(float)[m]
            e, z, _ = _z(yy, pp, None)
            r = "–"
            if c1 is not None:
                cost = (c1.to_numpy(float) * c2.to_numpy(float))[m]
                r = f"{np.nanmean(yy / cost - 1):+.1%}"
            res[(name, sp)] = z
            out.append(f"| {name} | {sp} | {m.sum()} | {yy.mean():.1%} | {pp.mean():.1%} | {100 * e:+.1f} | {z:+.2f} | {r} |")
    k = "Fav -1.5 AND over (pre-registered)"
    p_hold = stats.norm.sf(res[(k, "holdout")])
    verdict = "PASSES" if (res[(k, "discovery")] > 0 and p_hold < 0.05) else "does not pass"
    out += ["", f"Pre-registered rule (discovery and holdout joint > product, holdout one-sided p < 0.05): holdout p = {p_hold:.3f} -> **{verdict}**.", ""]
    # by favourite strength
    g["fav_band"] = pd.cut(np.maximum(g["ml_home_fair"], 1 - g["ml_home_fair"]), [0.5, 0.6, 0.67, 1.0], labels=["50-60%", "60-67%", "67%+"])
    out += ["Fav -1.5 AND over by favourite strength (all 2025-26 + live):", "", "| Favourite win chance | Games | Both hit | Product | Edge, pts | z |", "|---|--:|--:|--:|--:|--:|"]
    for b, q in g.groupby("fav_band", observed=True):
        yy, pp = (q["y_pl_fav"] * q["y_over"]).to_numpy(float), (q["pl_fav_fair"] * q["over_fair"]).to_numpy(float)
        e, z, _ = _z(yy, pp, None)
        out.append(f"| {b} | {len(q)} | {yy.mean():.1%} | {pp.mean():.1%} | {100 * e:+.1f} | {z:+.2f} |")
    out += ["", "Kalshi (live): the same pair bought as two separate Kalshi markets at the pick-lock ask (incl. fees):", ""]
    out += kalshi_pair()
    return out


def kalshi_pair() -> list[str]:
    rows = []
    for f in sorted((DATA / "shadow").glob("*.csv")):
        s = pd.read_csv(f)
        k = s[(s["venue"] == "kalshi") & s["y"].notna() & s["cost"].notna()]
        sp = k[(k["market"] == "spread") & (k["line"] == 1.5) & (k["side"] == "yes")]
        tt = k[(k["market"] == "total") & (k["side"] == "yes")]
        for gk, a in sp.groupby("game_key"):
            fav = a.sort_values("fair_prob", ascending=False).iloc[0] if a["fair_prob"].notna().any() else a.sort_values("cost").iloc[-1]
            t = tt[tt["game_key"] == gk]
            if t.empty:
                continue
            t = t.iloc[(t["fair_prob"].fillna(t["cost"]) - 0.5).abs().argsort()[:1]].iloc[0]
            rows.append({"date": f.stem, "game_key": gk, "cost": fav["cost"] * t["cost"], "y": fav["y"] * t["y"],
                         "fair": (fav["fair_prob"] * t["fair_prob"]) if pd.notna(fav["fair_prob"]) and pd.notna(t["fair_prob"]) else np.nan})
    d = pd.DataFrame(rows)
    if d.empty:
        return ["No Kalshi spread + total pairs found."]
    return [f"{len(d)} games; both hit {d['y'].mean():.1%}; average cost {d['cost'].mean():.1%} "
            f"(product of Pinnacle fair {d['fair'].mean():.1%}); ROI {np.mean(d['y'] / d['cost'] - 1):+.1%}. "
            "Kalshi's ask plus fees sits above fair on each leg, so the pair starts behind before any correlation gain."]


# ------------------------------------------------------------------ H5 ----
def h5() -> list[str]:
    rows = []
    for od in sorted((DATA / "odds").iterdir()):
        pk = DATA / "picks" / f"{od.name}.csv"
        cf = DATA / "picks" / f"{od.name}_candidates.csv.gz"
        sh = DATA / "shadow" / f"{od.name}.csv"
        if not (pk.exists() and cf.exists() and sh.exists()):
            continue
        snap = str(int(pd.read_csv(pk)["odds_snapshot"].dropna().iloc[0])).zfill(4)
        kf = od / snap / "kalshi.csv"
        if not kf.exists():
            continue
        k = pd.read_csv(kf).drop_duplicates("ticker").set_index("ticker")
        c = pd.read_csv(cf)
        c = c[(c["venue"] == "kalshi") & (c["market"] == "ml") & (c["side"] == "yes") & c["fair_prob"].notna()]
        res = pd.read_csv(sh)[["cand_id", "y"]].drop_duplicates("cand_id").set_index("cand_id")["y"]
        for r in c.to_dict("records"):
            if r["ticker"] not in k.index or r["cand_id"] not in res.index or pd.isna(res[r["cand_id"]]):
                continue
            q = k.loc[r["ticker"]]
            mid = (q["yes_bid"] + q["yes_ask"]) / 2 if pd.notna(q["yes_bid"]) and pd.notna(q["yes_ask"]) else np.nan
            rows.append({"date": od.name, "game_key": r["game_key"], "team": r["team"], "fair": r["fair_prob"],
                         "cost": r["cost"], "mid": mid, "y": res[r["cand_id"]]})
    d = pd.DataFrame(rows).drop_duplicates(["date", "game_key", "team"])
    if d.empty:
        return ["No Kalshi game markets found."]
    d["premium_mid"] = d["mid"] - d["fair"]
    d["premium_ask"] = d["cost"] - d["fair"]
    d["popular"] = d["team"].isin(POPULAR)
    d["canadian"] = d["team"].isin(CANADIAN)
    out = ["Premium = Kalshi price of the team's YES - Pinnacle fair at the pick lock, in points (mid = halfway between "
           "bid and ask; ask = what we'd pay incl. fees). 95% CI by resampling slates.", "",
           "| Group | Markets | Premium at mid, pts | Premium at ask, pts | Won | Fair |", "|---|--:|--:|--:|--:|--:|"]
    rng = np.random.default_rng(3)
    days = d["date"].unique()

    def ci(mask, col):
        v = []
        for _ in range(2000):
            pick = rng.choice(days, len(days))
            q = pd.concat([d[(d["date"] == x) & mask(d)] for x in pick])
            v.append(q[col].mean())
        return np.nanpercentile(v, [2.5, 97.5])

    groups = {"Popular 5 (TOR MTL EDM NYR BOS)": lambda x: x["popular"], "All other teams": lambda x: ~x["popular"],
              "Canadian 7": lambda x: x["canadian"], "Non-Canadian": lambda x: ~x["canadian"]}
    for name, m in groups.items():
        q = d[m(d)]
        lo, hi = ci(m, "premium_mid")
        out.append(f"| {name} | {len(q)} | {100 * q['premium_mid'].mean():+.2f} ({100 * lo:+.2f}, {100 * hi:+.2f}) | "
                   f"{100 * q['premium_ask'].mean():+.2f} | {q['y'].mean():.1%} | {q['fair'].mean():.1%} |")
    diff = []
    for _ in range(2000):
        pick = rng.choice(days, len(days))
        q = pd.concat([d[d["date"] == x] for x in pick])
        diff.append(q.loc[q["popular"], "premium_mid"].mean() - q.loc[~q["popular"], "premium_mid"].mean())
    lo, hi = np.nanpercentile(diff, [2.5, 97.5])
    point = d.loc[d["popular"], "premium_mid"].mean() - d.loc[~d["popular"], "premium_mid"].mean()
    n_pop = int(d["popular"].sum())
    out += ["", f"Primary metric (popular minus others, at mid): {100 * point:+.2f} pts (95% CI {100 * lo:+.2f} to {100 * hi:+.2f}); "
            f"{n_pop} popular-team markets so far (verdict at 300). Interim only.", "",
            "By team (YES premium at mid, pts; sorted):", "", "| Team | Markets | Premium |", "|---|--:|--:|"]
    for t, q in d.groupby("team")["premium_mid"].agg(["size", "mean"]).sort_values("mean", ascending=False).iterrows():
        out.append(f"| {t} | {int(q['size'])} | {100 * q['mean']:+.2f} |")
    return out


def report() -> str:
    T = load()
    md = ["# Hypotheses H2-H5: results", "",
          f"Run {date.today().isoformat()} by `python -m nhlpipe.patterns.hyp`. Specs: `docs/hypotheses_2026-11-17.md` "
          "(committed before these tests ran). Research only.", "",
          "## H2 Rink scorekeeper effect (SOG props)", "", *h2(T), "",
          "## H3 Morning line promotions", "",
          "Collection started 2026-11-17 (`nhlpipe/lines.py`, saved each pull as `data/raw/<date>/df_lines.csv`). "
          "No history exists, so there is nothing to test yet: first look at 150 promoted lines.", "",
          "## H4 Favourite -1.5 and the over together", "", *h4(T), "",
          "## H5 Popular-team premium on Kalshi (interim)", "", *h5(), ""]
    txt = "\n".join(md) + "\n"
    (OUT / "hypotheses_h2_h5.md").write_text(txt)
    return txt


if __name__ == "__main__":
    print(report())
