"""Shots model v2 in the live pipeline (methods M6_shots_v2 and M6_shots_v2_pickem).

Pre-registered 2026-11-02, frozen for the trial (do not refit mid-trial):
  model     Poisson GLM on shots/mu_base (offset), fit on 2023-24, 2024-25, 2025-26;
            negative binomial with the fitted dispersion; parameters in
            data/shots2/model_v2.json (no sklearn needed at run time)
  blend     P(over) = sigmoid(c + a*logit(Pinnacle no-vig, power method, pick time)
                               + b*logit(model)), a/b/c fit on every 2025-26 Pinnacle
            SOG line with out-of-sample model predictions; no Pinnacle price -> no bet
  bets      edge = blended P(side) - cost, 3% <= edge <= 12%; one bet per player
            (best price), up to 3 players per game, never both sides
  venues    M6_shots_v2         best sportsbook price (DK, FD, MGM, Caesars, BetRivers, ESPN BET)
            M6_shots_v2_pickem  Underdog (3.5x standard 2-pick x the pick's multiplier) / PrizePicks (3x)
"""
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from ..candidates import pickem_decimal
from ..names import norm
from . import features, model, pull

ROOT = pull.ROOT
PARAMS = ROOT / "model_v2.json"
HIST_SEASONS = ["20222023", "20232024", "20242025", "20252026"]
LIVE_CUTOFF = date(2026, 10, 1)  # league priors use games before the 2026-27 season
BOOKS = {"draftkings", "fanduel", "betmgm", "williamhill_us", "betrivers", "espnbet"}
PICKEM = {"underdog", "prizepicks"}
EDGE_MIN, EDGE_MAX, MAX_PER_GAME = 0.03, 0.12, 3


def season_of(d: date) -> str:
    y = d.year if d.month >= 8 else d.year - 1
    return f"{y}{y + 1}"


# --------------------------------------------------------------- freeze ----
def freeze() -> dict:
    """Fit on 2023-24..2025-26 and write data/shots2/model_v2.json (run once, locally)."""
    from sklearn.linear_model import LogisticRegression
    stats_df = pd.concat([pull.load_stats(s) for s in HIST_SEASONS], ignore_index=True)
    games = [g for s in HIST_SEASONS for g in pull.schedule(s)]
    mp = pd.read_csv(ROOT / "mp_teams.csv.gz")
    s = features.add_h2h(features.build(stats_df, games, mp, LIVE_CUTOFF))
    s = s[(s["gameId"] // 1_000_000).isin([2023, 2024, 2025]) & (s["n_prior"] >= 1) & s["mu_base"].notna()]
    m = model.ShotsModel("glm").fit(s)
    sc, pr = m.m.named_steps["standardscaler"], m.m.named_steps["poissonregressor"]
    J = pd.read_csv(ROOT / "lines.csv")  # out-of-sample 2025-26 predictions vs Pinnacle (backtest)
    X = np.column_stack([model.logit(J["pinnacle_pick"]), model.logit(J["p_v2"])])
    lr = LogisticRegression(C=1e6, max_iter=1000).fit(X, J["y"])
    params = {
        "frozen_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "train_rows": int(len(s)), "features": model.FEATURES,
        "mean": sc.mean_.tolist(), "scale": sc.scale_.tolist(),
        "coef": pr.coef_.tolist(), "intercept": float(pr.intercept_),
        "alpha": m.alpha, "fill": m.fill,
        "blend": {"a_pinnacle": float(lr.coef_[0][0]), "b_model": float(lr.coef_[0][1]), "c": float(lr.intercept_[0]),
                  "fit_rows": int(len(J))},
        "rules": {"edge_min": EDGE_MIN, "edge_max": EDGE_MAX, "max_per_game": MAX_PER_GAME},
    }
    PARAMS.write_text(json.dumps(params, indent=1))
    print(json.dumps({k: v for k, v in params.items() if k in ("frozen_utc", "train_rows", "alpha", "blend")}, indent=1))
    return params


class Frozen:
    def __init__(self, p: dict):
        self.p = p
        self.alpha = p["alpha"]

    def mean(self, s: pd.DataFrame) -> np.ndarray:
        X = model.design(s, self.p["fill"])[self.p["features"]].to_numpy(float)
        z = (X - np.array(self.p["mean"])) / np.array(self.p["scale"])
        rate = np.exp(self.p["intercept"] + z @ np.array(self.p["coef"]))
        return np.clip(rate, 0.05, 20) * s["mu_base"].clip(lower=0.05).to_numpy()

    def p_over(self, mu, line):
        n = 1.0 / self.alpha
        return stats.nbinom.sf(np.floor(line), n, n / (n + mu))

    def blend(self, p_pin, p_model):
        b = self.p["blend"]
        return model.sigmoid(b["c"] + b["a_pinnacle"] * model.logit(p_pin) + b["b_model"] * model.logit(p_model))


# ------------------------------------------------------------ tonight ----
def refresh(day: date) -> None:
    """Pull any new days for the current season (free; cached days are skipped)."""
    pull.pull_stats(season_of(day))
    pull.pull_mp_teams()


def tonight_rows(day: date, slate_games: list[dict], hist: pd.DataFrame, prop_keys: set[tuple[str, str]]) -> pd.DataFrame:
    """Placeholder stats rows for tonight (outcomes zeroed) for every skater with a SOG prop.

    A skater qualifies if his most recent game was for one of the two teams. The placeholder
    row only carries identity; every feature comes from earlier games."""
    last = hist.sort_values("gameDate").groupby("playerId").tail(1)
    last = last.assign(key=last["skaterFullName"].map(norm))
    rows = []
    for g in slate_games:
        for side, opp in (("home", "away"), ("away", "home")):
            team = g[side]
            for r in last[last["teamAbbrev"] == team].to_dict("records"):
                if (r["key"], f"{g['away']}@{g['home']}") not in prop_keys:
                    continue
                rows.append({"gameId": g["game_id"], "gameDate": day.isoformat(), "playerId": r["playerId"],
                             "skaterFullName": r["skaterFullName"], "teamAbbrev": team, "opponentTeamAbbrev": g[opp],
                             "homeRoad": "H" if side == "home" else "R", "positionCode": r["positionCode"],
                             "timeOnIce": 60, "evTimeOnIce": 60, "ppTimeOnIce": 0, "shTimeOnIce": 0, "shots": 0,
                             "totalShotAttempts": 0, "ppIndividualSatFor": 0, "ppShots": 0})
    return pd.DataFrame(rows)


def sog_offers(odds: pd.DataFrame) -> pd.DataFrame:
    o = odds[odds["market"].isin(["player_shots_on_goal", "player_shots_on_goal_alternate"])
             & odds["point"].notna() & odds["player"].notna()].copy()
    o["game_key"] = o["away"] + "@" + o["home"]
    o["key"] = o["player"].map(norm)
    o["side"] = np.where(o["outcome"].str.lower() == "over", "yes", "no")
    o["prob"] = o["price_american"].map(lambda a: 100 / (a + 100) if a > 0 else -a / (-a + 100))
    if "multiplier" not in o:
        o["multiplier"] = None
    dec = [pickem_decimal(b, a, m) for b, a, m in zip(o["book"], o["price_american"], o["multiplier"])]
    o["pk_cost"] = [1 / d if d else np.nan for d in dec]
    o = o[~(o["book"].isin(PICKEM) & o["pk_cost"].isna())]  # PrizePicks demons/goblins: no real price
    return o.sort_values("market").drop_duplicates(["book", "game_key", "key", "point", "side"])


def pinnacle_fair(o: pd.DataFrame) -> pd.DataFrame:
    p = o[o["book"] == "pinnacle"].pivot_table(index=["game_key", "key", "point"], columns="side", values="prob", aggfunc="first")
    p = p.dropna(subset=[c for c in ("yes", "no") if c in p.columns]) if {"yes", "no"} <= set(p.columns) else p.iloc[0:0]
    if p.empty:
        return pd.DataFrame(columns=["game_key", "key", "point", "pin_over"])
    p["pin_over"] = [model.power_devig(a, b) for a, b in zip(p["yes"], p["no"])]
    return p[["pin_over"]].reset_index()


def picks(day: date, slate: pd.DataFrame, odds: pd.DataFrame, refresh_data: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(picks for both M6 methods, candidate rows to add to the day's candidates file)."""
    fr = Frozen(json.loads(PARAMS.read_text()))
    if refresh_data:
        refresh(day)
    seasons = HIST_SEASONS + [season_of(day)]
    hist = pd.concat([pull.load_stats(s) for s in dict.fromkeys(seasons)], ignore_index=True)
    hist = hist[hist["gameDate"] < day.isoformat()]
    games = [g for s in dict.fromkeys(seasons) for g in pull.schedule(s, refresh=refresh_data)]
    tonight = [g for g in games if g["date"] == day.isoformat()]
    started = set(slate.loc[~slate["game_state"].isin(["FUT", "PRE"]), "game_id"]) if "game_id" in slate else set()
    tonight = [g for g in tonight if g["game_id"] not in started]
    o = sog_offers(odds)
    if o.empty or not tonight:
        return pd.DataFrame(), pd.DataFrame()
    rows = tonight_rows(day, tonight, hist, set(zip(o["key"], o["game_key"])))
    if rows.empty:
        return pd.DataFrame(), pd.DataFrame()
    mp = pd.read_csv(ROOT / "mp_teams.csv.gz")
    mp = mp[mp["gameDate"] < int(day.strftime("%Y%m%d"))]
    s = features.add_h2h(features.build(pd.concat([hist, rows], ignore_index=True), games, mp, LIVE_CUTOFF))
    s = s[(s["date"] == day) & (s["n_prior"] >= 1) & s["mu_base"].notna()].copy()
    s["mu"] = fr.mean(s)
    s["key"] = s["skaterFullName"].map(norm)
    s["game_key"] = s["opp"].where(s["home"] == 1, s["teamAbbrev"]) + "@" + s["teamAbbrev"].where(s["home"] == 1, s["opp"])

    o = o.merge(s[["game_key", "key", "mu", "teamAbbrev"]], on=["game_key", "key"], how="inner")
    o = o.merge(pinnacle_fair(o), on=["game_key", "key", "point"], how="left")
    o = o[o["pin_over"].notna()].copy()
    if o.empty:
        return pd.DataFrame(), pd.DataFrame()
    o["p_model_over"] = fr.p_over(o["mu"].to_numpy(), o["point"].to_numpy())
    o["p_blend_over"] = fr.blend(o["pin_over"].to_numpy(), o["p_model_over"].to_numpy())
    o["est_prob"] = np.where(o["side"] == "yes", o["p_blend_over"], 1 - o["p_blend_over"])
    o["cost"] = np.where(o["book"].isin(PICKEM), o["pk_cost"], o["prob"])
    o["edge"] = o["est_prob"] - o["cost"]
    o["venue"] = o["book"]
    o["market"] = "player_sog"
    o["line"] = o["point"]
    o["price"] = o["cost"]
    o["american"] = o["price_american"]
    o["team"] = None
    o["ticker"] = None
    o["player_key"] = o["key"]
    o["selection"] = o["player"] + np.where(o["side"] == "yes", " Over ", " Under ") + o["line"].astype(str) + " shots"
    o["cand_id"] = o["venue"] + "|" + o["game_key"] + "|player_sog|" + o["key"] + "|" + o["line"].astype(str) + "|" + o["side"]
    o["est_source"] = "shots_v2_blend"
    o["fair_prob"] = np.where(o["side"] == "yes", o["pin_over"], 1 - o["pin_over"])
    o["fair_source"] = "pinnacle"
    cand_cols = ["game_key", "venue", "ticker", "team", "player", "line", "market", "side", "price", "cost", "american",
                 "player_key", "selection", "cand_id", "fair_prob", "fair_source", "est_prob", "edge", "mu"]

    out = []
    for name, venues in (("M6_shots_v2", BOOKS), ("M6_shots_v2_pickem", PICKEM)):
        d = o[o["venue"].isin(venues) & (o["edge"] >= EDGE_MIN) & (o["edge"] <= EDGE_MAX)]
        d = d.sort_values(["edge", "cand_id"], ascending=[False, True]).drop_duplicates(["game_key", "key"])
        d = d.groupby("game_key", sort=False).head(MAX_PER_GAME).copy()
        d["method"] = name
        d["pick_no"] = range(1, len(d) + 1)
        out.append(d)
    pk = pd.concat(out, ignore_index=True)
    cand = o[o["venue"].isin(BOOKS)][cand_cols].drop_duplicates("cand_id")  # pick'em rows are already in the candidates
    print(f"shots v2: {len(s)} skaters projected, {len(o)} priced offers, "
          f"{(pk['method'] == 'M6_shots_v2').sum()} book bets, {(pk['method'] == 'M6_shots_v2_pickem').sum()} pick'em bets")
    return pk, cand


if __name__ == "__main__":
    import sys
    if "--freeze" in sys.argv:
        freeze()
