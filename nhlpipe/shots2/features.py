"""Point-in-time features for shots model v2.

One row per skater-game. Every feature uses only games played on earlier
dates (never the same day), so a row can be built at the 1:50 PM pick lock.

Player role / skill (exponentially decayed over past games, all seasons):
  ev_toi, pp_toi, sh_toi        projected minutes (half-life ROLE_HL games)
  toi_last, pp_last             last game's minutes (role-change signal)
  ev_att60, pp_att60            shot attempts per 60 at EV / on the PP
                                (half-life SKILL_HL, shrunk to position mean)
  on_net                        shots on goal / attempts (half-life NET_HL, shrunk)
  mu_base                       ev_toi*ev_att60/60*on_net + pp_toi*pp_att60/60*on_net
                                + shorthanded / other minutes at a small rate
  oz_start                      offensive-zone start share (decayed)
Context:
  home, b2b, opp_b2b, rest_days, opp_rest_days, tz_shift (hours moved since
  last game), road_trip (consecutive away games)
  opp_sa_ratio                  opponent shot attempts allowed per 60 vs league (decayed, shrunk)
  team_ca_ratio                 own team shot attempts per 60 vs league
  xg_edge                       own minus opponent decayed xG share (score-effect proxy)
  opp_pen_ratio                 opponent penalties taken vs league (PP chances)
  missing_toi                   minutes per game of regular teammates absent from the team's
                                last game (players stepping up)
  h2h_resid                     shrunk mean of (SOG - prediction) in past games vs this opponent
"""
from datetime import date

import numpy as np
import pandas as pd
from scipy.signal import lfilter

ROLE_HL, SKILL_HL, NET_HL, TEAM_HL = 6, 40, 80, 20
ATT_PRIOR_MIN = 300.0      # minutes of position-average attempts added to each player's rate
NET_PRIOR_ATT = 150.0      # attempts of position-average on-net share added
TEAM_PRIOR_GP = 10.0

# team -> UTC offset (standard time) of home arena
TZ = {"ANA": -8, "LAK": -8, "SJS": -8, "SEA": -8, "VAN": -8, "VGK": -8, "CGY": -7, "EDM": -7, "COL": -7,
      "UTA": -7, "ARI": -7, "CHI": -6, "DAL": -6, "MIN": -6, "NSH": -6, "STL": -6, "WPG": -6}


def _tz(team: str) -> int:
    return TZ.get(team, -5)


def _decay(x: np.ndarray, hl: float) -> np.ndarray:
    """Exponentially decayed sum of strictly earlier values: s_t = sum_{k<t} d^(t-1-k) x_k."""
    d = 0.5 ** (1.0 / hl)
    s = lfilter([1.0], [1.0, -d], np.nan_to_num(x.astype(float)))
    return np.concatenate([[0.0], s[:-1]])


def _grouped_decay(df: pd.DataFrame, key: str, col: str, hl: float) -> np.ndarray:
    out = np.zeros(len(df))
    for _, idx in df.groupby(key, sort=False).indices.items():
        out[idx] = _decay(df[col].to_numpy()[idx], hl)
    return out


def player_frame(stats: pd.DataFrame) -> pd.DataFrame:
    """Clean per-player-game table from nhlpipe.shots2.pull.load_stats (seasons concatenated)."""
    s = stats.copy()
    s["date"] = pd.to_datetime(s["gameDate"]).dt.date
    s["F"] = (s["positionCode"] != "D").astype(int)
    for c in ("timeOnIce", "evTimeOnIce", "ppTimeOnIce", "shTimeOnIce"):
        s[c] = pd.to_numeric(s[c], errors="coerce").fillna(0) / 60.0
    for c in ("shots", "totalShotAttempts", "ppIndividualSatFor", "ppShots", "offensiveZoneStartPct"):
        s[c] = pd.to_numeric(s.get(c), errors="coerce")
    s["ppIndividualSatFor"] = s["ppIndividualSatFor"].fillna(0)
    s["ppShots"] = s["ppShots"].fillna(0)
    s["att"] = s["totalShotAttempts"].fillna(s["shots"])
    s["att_pp"] = s["ppIndividualSatFor"].clip(upper=s["att"])
    s["att_ev"] = (s["att"] - s["att_pp"]).clip(lower=0)
    s["other_toi"] = (s["timeOnIce"] - s["evTimeOnIce"] - s["ppTimeOnIce"]).clip(lower=0)
    s = s[s["timeOnIce"] > 0].sort_values(["playerId", "date", "gameId"]).reset_index(drop=True)
    return s


def add_player_features(s: pd.DataFrame, cutoff: date) -> pd.DataFrame:
    """League/position priors use only games before `cutoff` (the test season start)."""
    s = s.copy()
    pri = s[s["date"] < cutoff]
    g = "playerId"
    ones = np.ones(len(s))
    s["_one"] = ones
    w_role = _grouped_decay(s, g, "_one", ROLE_HL)
    s["n_prior"] = s.groupby(g).cumcount()
    for c, name in (("evTimeOnIce", "ev_toi"), ("ppTimeOnIce", "pp_toi"), ("shTimeOnIce", "sh_toi"),
                    ("other_toi", "oth_toi"), ("timeOnIce", "toi_avg")):
        s[name] = _grouped_decay(s, g, c, ROLE_HL) / np.where(w_role > 0, w_role, np.nan)
    prev = s.groupby(g)[["timeOnIce", "ppTimeOnIce", "date", "teamAbbrev"]].shift(1)
    s["toi_last"], s["pp_last"] = prev["timeOnIce"], prev["ppTimeOnIce"]
    s["prev_team"] = prev["teamAbbrev"]

    # skill rates: decayed sums of attempts and minutes, shrunk to position means
    for num, den, name, prior_min in (("att_ev", "evTimeOnIce", "ev_att60", ATT_PRIOR_MIN),
                                      ("att_pp", "ppTimeOnIce", "pp_att60", ATT_PRIOR_MIN / 4)):
        N = _grouped_decay(s, g, num, SKILL_HL)
        D = _grouped_decay(s, g, den, SKILL_HL)
        pr = pri.groupby("F")[num].sum() / (pri.groupby("F")[den].sum() / 60)
        pos_rate = s["F"].map(pr)
        s[name] = (N + pos_rate * prior_min / 60) / ((D + prior_min) / 60)
    N = _grouped_decay(s, g, "shots", NET_HL)
    A = _grouped_decay(s, g, "att", NET_HL)
    pos_net = s["F"].map(pri.groupby("F")["shots"].sum() / pri.groupby("F")["att"].sum())
    s["on_net"] = (N + pos_net * NET_PRIOR_ATT) / (A + NET_PRIOR_ATT)
    oz = s["offensiveZoneStartPct"].fillna(0.5).to_numpy()
    s["_oz"] = oz
    s["oz_start"] = _grouped_decay(s, g, "_oz", SKILL_HL) / np.where(_grouped_decay(s, g, "_one", SKILL_HL) > 0,
                                                                        _grouped_decay(s, g, "_one", SKILL_HL), np.nan)
    oth_rate = 0.6  # attempts / 60 shorthanded and other states (small)
    s["mu_base"] = ((s["ev_toi"] * s["ev_att60"] + s["pp_toi"] * s["pp_att60"]) / 60 * s["on_net"]
                    + (s["sh_toi"] + s["oth_toi"]) * oth_rate / 60 * s["on_net"])
    return s.drop(columns=["_one", "_oz"])


def schedule_frame(games: list[dict]) -> pd.DataFrame:
    """Team-game rows with rest / back-to-back / travel computed from the schedule only."""
    rows = []
    for g in games:
        for side, opp in (("home", "away"), ("away", "home")):
            rows.append({"gameId": g["game_id"], "date": date.fromisoformat(g["date"]), "team": g[side],
                         "opp": g[opp], "home": int(side == "home"), "venue_tz": _tz(g["home"])})
    t = pd.DataFrame(rows).sort_values(["team", "date", "gameId"]).reset_index(drop=True)
    gp = t.groupby("team")
    t["prev_date"] = gp["date"].shift(1)
    t["rest_days"] = [(d - p).days - 1 if isinstance(p, date) else 3 for d, p in zip(t["date"], t["prev_date"])]
    t["rest_days"] = t["rest_days"].clip(0, 4)
    t["b2b"] = (t["rest_days"] == 0).astype(int)
    t["tz_shift"] = (t["venue_tz"] - gp["venue_tz"].shift(1)).abs().fillna(0)
    away = 1 - t["home"]
    t["road_trip"] = away.groupby((away != away.shift()).cumsum()).cumsum() * away
    opp = t[["gameId", "team", "rest_days", "b2b"]].rename(columns={"team": "opp", "rest_days": "opp_rest_days",
                                                                    "b2b": "opp_b2b"})
    return t.merge(opp, on=["gameId", "opp"], how="left")


def team_frame(mp: pd.DataFrame, cutoff: date) -> pd.DataFrame:
    """Each team's decayed rates *after* each of its games (MoneyPuck team logs, all situations).

    Rows are keyed by (team, date of that game); attach to a later game with
    team_asof(), which takes the last state dated strictly before the game, so
    nothing from the game itself (or the same day) is used, and it works live
    before tonight's game has a row."""
    a = mp[mp["situation"] == "all"].copy()
    a["date"] = pd.to_datetime(a["gameDate"].astype(str)).dt.date
    a = a.sort_values(["playerTeam", "date"]).reset_index(drop=True)
    a["mins"] = a["iceTime"] / 60
    a["_one"] = 1.0
    g = "playerTeam"

    def after(col):  # decayed sum including this game = before-sum * d + x
        d = 0.5 ** (1.0 / TEAM_HL)
        return _grouped_decay(a, g, col, TEAM_HL) * d + a[col].to_numpy()

    pri = a[a["date"] < cutoff]
    M = after("mins")
    out = a[["playerTeam", "date"]].rename(columns={"playerTeam": "team"}).copy()
    for col, name in (("shotAttemptsFor", "cf60"), ("shotAttemptsAgainst", "ca60"),
                      ("shotsOnGoalFor", "sf60"), ("shotsOnGoalAgainst", "sa60"), ("penaltiesFor", "pen60")):
        lg = pri[col].sum() / (pri["mins"].sum() / 60)  # league rate from games before the cutoff only
        out[name] = (after(col) + lg * TEAM_PRIOR_GP) / ((M + TEAM_PRIOR_GP * 60) / 60)
        out[name + "_lg"] = lg
    XF, XA = after("xGoalsFor"), after("xGoalsAgainst")
    out["xg_share"] = (XF + 2.5 * TEAM_PRIOR_GP) / (XF + XA + 5.0 * TEAM_PRIOR_GP)
    out["team_gp"] = after("_one")
    return out


def team_asof(rows: pd.DataFrame, tm: pd.DataFrame, team_col: str, cols: list[str], prefix: str = "") -> pd.DataFrame:
    """Attach each team's last post-game state dated strictly before rows.date."""
    left = rows[["date", team_col]].copy()
    left["_i"] = np.arange(len(rows))
    left["_d"] = pd.to_datetime(left["date"])
    right = tm.rename(columns={"team": team_col}).copy()
    right["_d"] = pd.to_datetime(right["date"])
    m = pd.merge_asof(left.sort_values("_d"), right.drop(columns="date").sort_values("_d"), on="_d", by=team_col,
                      allow_exact_matches=False, direction="backward").sort_values("_i")
    out = rows.copy()
    for c in cols:
        out[prefix + c] = m[c].to_numpy()
    return out


def missing_regulars(s: pd.DataFrame) -> pd.DataFrame:
    """Per team-game: minutes/game of regulars (>=5 of the team's last 10 games) absent from the team's last game."""
    tg = s[["teamAbbrev", "gameId", "date"]].drop_duplicates().sort_values(["teamAbbrev", "date", "gameId"])
    roster = s.groupby(["teamAbbrev", "gameId"])["playerId"].apply(set).to_dict()
    toi = s.set_index(["playerId", "gameId"])["toi_avg"].to_dict()
    rows = []
    for team, grp in tg.groupby("teamAbbrev"):
        ids = grp["gameId"].tolist()
        for i, gid in enumerate(ids):
            if i == 0:
                rows.append((team, gid, 0.0))
                continue
            last10 = ids[max(0, i - 10):i]
            counts: dict = {}
            for x in last10:
                for p in roster[(team, x)]:
                    counts[p] = counts.get(p, 0) + 1
            regulars = {p for p, n in counts.items() if n >= min(5, len(last10))}
            absent = regulars - roster[(team, ids[i - 1])]
            # their typical minutes as of the last game they played (already prior-only)
            m = sum(toi.get((p, x), 0) or 0 for p in absent for x in [max((y for y in last10 if p in roster[(team, y)]), default=None)] if x)
            rows.append((team, gid, m))
    return pd.DataFrame(rows, columns=["teamAbbrev", "gameId", "missing_toi"])


def build(stats: pd.DataFrame, games: list[dict], mp: pd.DataFrame, cutoff: date) -> pd.DataFrame:
    s = add_player_features(player_frame(stats), cutoff)
    sch = schedule_frame(games).rename(columns={"team": "teamAbbrev"})
    s = s.merge(sch[["gameId", "teamAbbrev", "opp", "home", "rest_days", "b2b", "tz_shift", "road_trip",
                     "opp_rest_days", "opp_b2b"]], on=["gameId", "teamAbbrev"], how="left")
    tm = team_frame(mp, cutoff)
    s = team_asof(s, tm, "teamAbbrev", ["cf60", "cf60_lg", "xg_share", "team_gp"])
    s = team_asof(s, tm.rename(columns={"xg_share": "opp_xg_share"}), "opp", ["ca60", "ca60_lg", "opp_xg_share", "pen60", "pen60_lg"])
    s["opp_sa_ratio"] = s["ca60"] / s["ca60_lg"]
    s["team_ca_ratio"] = s["cf60"] / s["cf60_lg"]
    s["xg_edge"] = s["xg_share"] - s["opp_xg_share"]
    s["opp_pen_ratio"] = s["pen60"] / s["pen60_lg"]
    s = s.merge(missing_regulars(s), on=["teamAbbrev", "gameId"], how="left")
    s["traded"] = (s["prev_team"].notna() & (s["prev_team"] != s["teamAbbrev"])).astype(int)
    return s


def add_h2h(s: pd.DataFrame, pred_col: str = "mu_base", k: float = 4.0) -> pd.DataFrame:
    """Shrunk mean residual (shots - pred) over the player's earlier games vs the same opponent."""
    s = s.sort_values(["playerId", "opp", "date"]).copy()
    s["_r"] = s["shots"] - s[pred_col]
    grp = s.groupby(["playerId", "opp"])["_r"]
    csum = grp.cumsum() - s["_r"]
    n = grp.cumcount()
    s["h2h_resid"] = csum / (n + k)
    s["h2h_n"] = n
    return s.drop(columns="_r").sort_values(["playerId", "date", "gameId"])
