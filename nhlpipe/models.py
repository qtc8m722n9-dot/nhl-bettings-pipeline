"""Stats models: M3 (xG game simulation) and M4 (player shots on goal).

All parameters below are starting values, written down before the test
(pre-registered). Change them only between test periods, never mid-period.
"""
import math

import numpy as np
import pandas as pd

from .names import norm

# ---- pre-registered parameters -------------------------------------------
TEAM_PRIOR_GP = 10       # shrink team rates toward league average (games)
GOALIE_PRIOR_GP = 25     # shrink goalie GSAx toward 0 (games); early-season GSAx is mostly noise
OT_GOALS_PER_TEAM = 0.075  # OT goals already in MoneyPuck 'other'; the sim adds OT itself
HOME_FACTOR = 1.04       # home scoring multiplier (away gets 1 / this)
B2B_FACTOR = 0.97        # team on 2nd night of back-to-back: own scoring x0.97, allowed x1/0.97
P1_SHARE = 0.30          # share of regulation goals scored in the 1st period
OT_HOME_WIN = 0.52       # P(home wins OT/shootout | tied after regulation)
N_SIMS = 20000
SKATER_PRIOR_MIN = 200   # shrink a skater's shot rate toward position mean (minutes)
OPP_FACTOR_WEIGHT = 0.5  # how much of the opponent shots-allowed factor to apply


def league_params(mp_teams: pd.DataFrame) -> dict:
    t = mp_teams
    p = {}
    games = t[t["situation"] == "all"]["games_played"].sum()
    for sit in ("5on5", "5on4", "other"):
        s = t[t["situation"] == sit]
        p[f"{sit}_min_pg"] = s["iceTime"].sum() / 60 / games  # minutes per team-game
        p[f"{sit}_xg60"] = s["xGoalsFor"].sum() / (s["iceTime"].sum() / 3600)
        p[f"{sit}_goals_pg"] = s["goalsFor"].sum() / games
    a = t[t["situation"] == "all"]
    p["calib"] = a["goalsFor"].sum() / a["xGoalsFor"].sum()  # actual goals / xG
    p["goals_pg"] = a["goalsFor"].sum() / games
    p["sog_against_pg"] = a["shotsOnGoalAgainst"].sum() / games
    return p


def _shrink(val, gp, prior, k):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return prior
    return (val * gp + prior * k) / (gp + k)


def team_lambdas(g: pd.Series, lp: dict) -> tuple[float, float]:
    """Expected regulation goals (home, away)."""
    lam = {}
    for side, opp in (("home", "away"), ("away", "home")):
        gp, ogp = g.get(f"{side}_gp", 0) or 0, g.get(f"{opp}_gp", 0) or 0
        ev_for = _shrink(g.get(f"{side}_ev_xgf60"), gp, lp["5on5_xg60"], TEAM_PRIOR_GP)
        ev_opp = _shrink(g.get(f"{opp}_ev_xga60"), ogp, lp["5on5_xg60"], TEAM_PRIOR_GP)
        pp_for = _shrink(g.get(f"{side}_pp_xgf60"), gp, lp["5on4_xg60"], TEAM_PRIOR_GP)
        pk_opp = _shrink(g.get(f"{opp}_pk_xga60"), ogp, lp["5on4_xg60"], TEAM_PRIOR_GP)
        ev = ev_for * ev_opp / lp["5on5_xg60"] * lp["5on5_min_pg"] / 60
        pp = pp_for * pk_opp / lp["5on4_xg60"] * lp["5on4_min_pg"] / 60
        # 4on5 (shorthanded) and everything else: league-average goals
        other = lp["goals_pg"] - (lp["5on5_xg60"] * lp["5on5_min_pg"] / 60 + lp["5on4_xg60"] * lp["5on4_min_pg"] / 60) * lp["calib"]
        x = (ev + pp) * lp["calib"] + max(other - OT_GOALS_PER_TEAM, 0)
        # opposing goalie: subtract shrunk GSAx per game
        ggp = g.get(f"{opp}_goalie_gp", 0) or 0
        gsax = g.get(f"{opp}_goalie_gsax")
        if gsax is not None and not (isinstance(gsax, float) and math.isnan(gsax)):
            x -= gsax / (ggp + GOALIE_PRIOR_GP)
        x *= HOME_FACTOR if side == "home" else 1 / HOME_FACTOR
        if g.get(f"{side}_b2b"):
            x *= B2B_FACTOR
        if g.get(f"{opp}_b2b"):
            x /= B2B_FACTOR
        lam[side] = max(x, 0.8)
    return lam["home"], lam["away"]


def simulate(lh: float, la: float, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    h = rng.poisson(lh, N_SIMS)
    a = rng.poisson(la, N_SIMS)
    tie = h == a
    ot_home = rng.random(N_SIMS) < OT_HOME_WIN
    hf = h + (tie & ot_home)
    af = a + (tie & ~ot_home)
    h1 = rng.poisson(lh * P1_SHARE, N_SIMS)
    a1 = rng.poisson(la * P1_SHARE, N_SIMS)
    return {"h": h, "a": a, "hf": hf, "af": af, "h1": h1, "a1": a1}


def game_prob(c: dict, sim: dict, home: str, away: str) -> float | None:
    """Model probability that the candidate's YES side happens."""
    m, t, line = c["market"], c.get("team"), c.get("line")
    hf, af = sim["hf"], sim["af"]
    if m == "ml":
        p = (hf > af).mean() if t == home else (af > hf).mean()
    elif m == "spread":
        # 'wins by over 1.5' -> regulation margin (OT wins are by 1)
        margin = (sim["h"] - sim["a"]) if t == home else (sim["a"] - sim["h"])
        p = (margin > line).mean()
    elif m == "total":
        p = ((hf + af) > line).mean()
    elif m == "team_total":
        p = ((hf if t == home else af) > line).mean()
    elif m == "p1_total":
        p = ((sim["h1"] + sim["a1"]) > line).mean()
    elif m == "p1_result":
        if t == "TIE":
            p = (sim["h1"] == sim["a1"]).mean()
        else:
            p = (sim["h1"] > sim["a1"]).mean() if t == home else (sim["a1"] > sim["h1"]).mean()
    else:
        return None
    return float(p)


# ---- M4: player shots on goal ---------------------------------------------
def skater_table(mp_skaters: pd.DataFrame, mp_teams: pd.DataFrame, lp: dict) -> dict:
    s = mp_skaters[mp_skaters["situation"] == "all"].copy()
    s = s[s["games_played"] > 0]
    s["sog60"] = s["I_F_shotsOnGoal"] / (s["icetime"] / 3600)
    s["toi_pg"] = s["icetime"] / s["games_played"] / 60  # minutes
    pos_mean = (
        s.groupby("position").apply(lambda d: d["I_F_shotsOnGoal"].sum() / (d["icetime"].sum() / 3600))
    ).to_dict()
    mins = s["icetime"] / 60
    s["sog60_shr"] = [
        (r * m + pos_mean.get(p, r) * SKATER_PRIOR_MIN) / (m + SKATER_PRIOR_MIN)
        for r, m, p in zip(s["sog60"], mins, s["position"])
    ]
    s["exp_sog"] = s["sog60_shr"] * s["toi_pg"] / 60
    a = mp_teams[mp_teams["situation"] == "all"].set_index("team")
    opp_factor = (a["shotsOnGoalAgainst"] / a["games_played"]) / lp["sog_against_pg"]
    return {
        "players": {norm(n): (team, e) for n, team, e in zip(s["name"], s["team"], s["exp_sog"])},
        "opp_factor": opp_factor.to_dict(),
    }


def _poisson_over(mu: float, line: float) -> float:
    k = int(math.floor(line))
    cdf = sum(math.exp(-mu) * mu**i / math.factorial(i) for i in range(k + 1))
    return 1 - cdf


def sog_prob(c: dict, sk: dict) -> float | None:
    hit = sk["players"].get(c.get("player_key"))
    if not hit or c["market"] != "player_sog":
        return None
    team, mu = hit
    away, home = c["game_key"].split("@")
    opp = home if team == away else away if team == home else None
    if opp is None:
        return None
    f = sk["opp_factor"].get(opp, 1.0)
    mu *= 1 + OPP_FACTOR_WEIGHT * (f - 1)
    p = _poisson_over(mu, c["line"])
    return p if c["side"] == "yes" else 1 - p
