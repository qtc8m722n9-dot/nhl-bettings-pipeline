"""Shots model v2: fit, predict, probabilities.

Mean model: Poisson regression on the rate y / mu_base (weights mu_base), i.e.
a Poisson GLM with offset log(mu_base); a gradient-boosted variant (same
trick) is fit too and the better one on validation is kept.
Distribution: negative binomial, dispersion fit on the training window.
"""
import math

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import PoissonRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "log_mu_base", "F", "ev_toi", "pp_toi", "sh_toi", "toi_jump", "pp_jump", "on_net", "ev_att60", "pp_att60",
    "oz_start", "home", "b2b", "opp_b2b", "rest_days", "opp_rest_days", "tz_shift", "road_trip",
    "log_opp_sa", "log_team_ca", "xg_edge", "log_opp_pen", "missing_toi", "traded", "h2h_resid", "log_n_prior",
]


def design(s: pd.DataFrame, fill: dict | None = None) -> pd.DataFrame:
    x = pd.DataFrame(index=s.index)
    x["log_mu_base"] = np.log(s["mu_base"].clip(lower=0.05))
    for c in ("F", "ev_toi", "pp_toi", "sh_toi", "on_net", "ev_att60", "pp_att60", "oz_start", "home", "b2b",
              "opp_b2b", "rest_days", "opp_rest_days", "tz_shift", "road_trip", "xg_edge", "missing_toi", "traded"):
        x[c] = pd.to_numeric(s[c], errors="coerce")
    x["toi_jump"] = np.log((s["toi_last"].fillna(s["toi_avg"]) + 1) / (s["toi_avg"] + 1)).clip(-1, 1)
    x["pp_jump"] = (s["pp_last"].fillna(s["pp_toi"]) - s["pp_toi"]).clip(-4, 4)
    x["log_opp_sa"] = np.log(s["opp_sa_ratio"]).clip(-0.4, 0.4)
    x["log_team_ca"] = np.log(s["team_ca_ratio"]).clip(-0.4, 0.4)
    x["log_opp_pen"] = np.log(s["opp_pen_ratio"]).clip(-0.6, 0.6)
    x["h2h_resid"] = s["h2h_resid"].fillna(0).clip(-2, 2)
    x["log_n_prior"] = np.log1p(s["n_prior"].clip(upper=300))
    x["missing_toi"] = np.log1p(pd.to_numeric(s["missing_toi"], errors="coerce").clip(0, 60))
    return x.fillna(fill if fill is not None else {c: x[c].median() for c in x.columns})


class ShotsModel:
    def __init__(self, kind: str = "glm"):
        self.kind = kind
        if kind == "glm":
            self.m = make_pipeline(StandardScaler(), PoissonRegressor(alpha=1e-3, max_iter=1000))
        else:
            self.m = HistGradientBoostingRegressor(loss="poisson", max_iter=300, learning_rate=0.05,
                                                   max_leaf_nodes=15, min_samples_leaf=200, l2_regularization=1.0)
        self.alpha = 0.0

    def fit(self, s: pd.DataFrame) -> "ShotsModel":
        raw = design(s)
        self.fill = {c: float(raw[c].median()) for c in raw.columns}  # training medians, reused at predict time
        X = design(s, self.fill)[FEATURES]
        mu0 = s["mu_base"].clip(lower=0.05).to_numpy()
        y = s["shots"].to_numpy()
        if self.kind == "glm":
            self.m.fit(X, y / mu0, poissonregressor__sample_weight=mu0)
        else:
            self.m.fit(X, y / mu0, sample_weight=mu0)
        mu = self.predict_mean(s)
        self.alpha = max(float(np.mean((y - mu) ** 2 - mu) / np.mean(mu ** 2)), 1e-4)
        return self

    def predict_mean(self, s: pd.DataFrame) -> np.ndarray:
        X = design(s, self.fill)[FEATURES]
        return np.clip(self.m.predict(X), 0.05, 20) * s["mu_base"].clip(lower=0.05).to_numpy()

    def p_over(self, mu: np.ndarray, line: np.ndarray) -> np.ndarray:
        """P(shots > line) under NB(mean mu, variance mu + alpha mu^2)."""
        n = 1.0 / self.alpha
        p = n / (n + mu)
        return stats.nbinom.sf(np.floor(line), n, p)

    def log_score(self, mu: np.ndarray, y: np.ndarray) -> np.ndarray:
        n = 1.0 / self.alpha
        return stats.nbinom.logpmf(y, n, n / (n + mu))


def baseline_v1(s: pd.DataFrame) -> np.ndarray:
    """Old M4 mean, rebuilt point-in-time: in-season SOG/60 (200-min position prior) x in-season TOI/gm x half opp factor."""
    s = s.sort_values(["playerId", "date", "gameId"])
    season = s["gameId"] // 1_000_000
    g = s.groupby(["playerId", season])
    shots = g["shots"].cumsum() - s["shots"]
    mins = g["timeOnIce"].cumsum() - s["timeOnIce"]
    gp = g.cumcount()
    pos = s.groupby("F")["shots"].transform("sum") / (s.groupby("F")["timeOnIce"].transform("sum") / 60)
    rate = (shots + pos * 200 / 60) / ((mins + 200) / 60)
    toi = (mins / gp.replace(0, np.nan)).fillna(s["toi_avg"])
    opp = 1 + 0.5 * (s["opp_sa_ratio"].fillna(1) - 1)
    return (rate * toi / 60 * opp).reindex(s.index).to_numpy()


def poisson_over(mu, line):
    return stats.poisson.sf(np.floor(line), mu)


def power_devig(p_over: float, p_under: float) -> float | None:
    """Power method: find k with p_over^k + p_under^k = 1; returns fair P(over)."""
    if not (0 < p_over < 1 and 0 < p_under < 1):
        return None
    lo, hi = 0.5, 3.0
    for _ in range(60):
        k = (lo + hi) / 2
        if p_over ** k + p_under ** k > 1:
            lo = k
        else:
            hi = k
    return p_over ** k


def logit(p):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return np.log(p / (1 - p))


def sigmoid(z):
    return 1 / (1 + np.exp(-z))
