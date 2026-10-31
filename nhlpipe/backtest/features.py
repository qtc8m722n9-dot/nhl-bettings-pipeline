"""Point-in-time inputs for a pick date D: only games played before D.

Mirrors what the live 1:50 PM pull sees (yesterday's games included, today's
not): MoneyPuck team xG by situation, goalie GSAx, skater shot rates, rest.
Live uses DailyFaceoff's projected starter; the archive has none, so the
projected starter here is a rule using past starts only (accuracy reported):
  #1 = most starts in the team's last 10 games (ties -> most recent);
  on the 2nd night of a back-to-back, if #1 started yesterday, the other
  goalie with the most starts in the last 20 games.
Injuries are not used: the M3/M4 models don't use them.
"""
from datetime import date, timedelta

import pandas as pd

from .. import moneypuck
from ..names import norm


def _dint(d: date) -> int:
    return int(d.strftime("%Y%m%d"))


class Season:
    def __init__(self, days: dict[str, dict], mp_teams: pd.DataFrame, mp_goalies: pd.DataFrame):
        self.days = days
        self.mp_teams = mp_teams
        self.mp_goalies = mp_goalies
        rows, starts = [], []
        for d, rec in days.items():
            for g in rec["games"]:
                if g["state"] not in ("OFF", "FINAL"):
                    continue
                for s in g["skaters"]:
                    rows.append({**s, "date": d})
                for gl in g["goalies"]:
                    if gl["starter"]:
                        starts.append({"date": d, "team": gl["team"], "pid": gl["pid"], "name": gl["name"]})
        self.skaters = pd.DataFrame(rows)
        self.starts = pd.DataFrame(starts).sort_values("date") if starts else pd.DataFrame(columns=["date", "team", "pid", "name"])

    # ---- MoneyPuck aggregates as of D --------------------------------------
    def teams_asof(self, d: date) -> pd.DataFrame:
        t = self.mp_teams[self.mp_teams["gameDate"] < _dint(d)]
        num = ["iceTime", "xGoalsFor", "xGoalsAgainst", "goalsFor", "goalsAgainst", "shotsOnGoalFor", "shotsOnGoalAgainst"]
        agg = t.groupby(["team", "situation"])[num].sum()
        agg["games_played"] = t.groupby(["team", "situation"])["gameId"].nunique()
        agg = agg.reset_index()
        agg["xGoalsPercentage"] = agg["xGoalsFor"] / (agg["xGoalsFor"] + agg["xGoalsAgainst"])
        return agg

    def goalie_asof(self, pid: str, d: date) -> tuple[int, float]:
        g = self.mp_goalies[(self.mp_goalies["playerId"].astype(str) == str(pid)) & (self.mp_goalies["gameDate"] < _dint(d))]
        return len(g), float((g["xGoals"] - g["goals"]).sum())

    def skaters_asof(self, d: date) -> pd.DataFrame:
        s = self.skaters[(self.skaters["date"] < d.isoformat()) & (self.skaters["toi_sec"] > 0)]
        if s.empty:
            return pd.DataFrame(columns=["name", "team", "position", "situation", "games_played", "icetime", "I_F_shotsOnGoal"])
        s = s.sort_values("date")
        agg = s.groupby("pid").agg(name=("name", "last"), team=("team", "last"), position=("pos", "last"),
                                   games_played=("date", "count"), icetime=("toi_sec", "sum"),
                                   I_F_shotsOnGoal=("sog", "sum")).reset_index()
        agg["situation"] = "all"
        return agg

    # ---- schedule-based ----------------------------------------------------
    def played_on(self, d: date) -> set[str]:
        rec = self.days.get(d.isoformat(), {"games": []})
        return {g["home"] for g in rec["games"]} | {g["away"] for g in rec["games"]}

    def projected_starter(self, team: str, d: date) -> tuple[str | None, str | None]:
        st = self.starts[(self.starts["team"] == team) & (self.starts["date"] < d.isoformat())]
        if st.empty:
            return None, None
        last10, last20 = st.tail(10), st.tail(20)
        counts = last10.groupby("pid").agg(n=("date", "size"), last=("date", "max"), name=("name", "last"))
        top = counts.sort_values(["n", "last"], ascending=False).index[0]
        yday = (d - timedelta(days=1)).isoformat()
        y = st[st["date"] == yday]
        if len(y) and y.iloc[-1]["pid"] == top:
            others = last20[last20["pid"] != top].groupby("pid").agg(n=("date", "size"), last=("date", "max"))
            if len(others):
                alt = others.sort_values(["n", "last"], ascending=False).index[0]
                return alt, st[st["pid"] == alt].iloc[-1]["name"]
        return top, counts.loc[top, "name"]

    # ---- the slate for D ----------------------------------------------------
    def slate(self, d: date, games: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
        """(slate rows like data/slates/*.csv, MoneyPuck-style team table, as-of info)."""
        mp_t = self.teams_asof(d)
        feat = moneypuck.team_features(mp_t).set_index("team")
        yday = self.played_on(d - timedelta(days=1))
        rows = []
        # only schedule fields are read: never scores or box scores of day D
        games = [{k: g[k] for k in ("game_id", "start_utc", "home", "away", "home_name", "away_name")} for g in games]
        for g in games:
            r = {k: g[k] for k in ("game_id", "start_utc", "home", "away", "home_name", "away_name")}
            for side in ("home", "away"):
                ab = g[side]
                r[f"{side}_b2b"] = ab in yday
                if ab in feat.index:
                    for c, v in feat.loc[ab].items():
                        r[f"{side}_{c}"] = v
                pid, name = self.projected_starter(ab, d)
                r[f"{side}_goalie"], r[f"{side}_goalie_pid"] = name, pid
                if pid:
                    gp, gsax = self.goalie_asof(pid, d)
                    r[f"{side}_goalie_gp"], r[f"{side}_goalie_gsax"] = gp, gsax
            rows.append(r)
        asof = {
            "mp_max_gamedate": int(self.mp_teams.loc[self.mp_teams["gameDate"] < _dint(d), "gameDate"].max() or 0),
            "box_max_date": self.skaters.loc[self.skaters["date"] < d.isoformat(), "date"].max() if len(self.skaters) else None,
            "goalie_max_gamedate": int(self.mp_goalies.loc[self.mp_goalies["gameDate"] < _dint(d), "gameDate"].max() or 0),
        }
        return pd.DataFrame(rows), mp_t, asof


def results_dict(rec: dict) -> dict:
    """A data/backtest/nhl day record in the shape nhlpipe.grade expects."""
    games = {}
    for g in rec["games"]:
        players = {norm(s["name"]): {"name": s["name"], "team": s["team"], "goals": s["goals"], "assists": s["assists"],
                                     "points": s["points"], "sog": s["sog"], "toi_sec": s["toi_sec"]} for s in g["skaters"]}
        games[f"{g['away']}@{g['home']}"] = {
            **{k: g[k] for k in ("state", "home", "away", "home_score", "away_score", "p1_home", "p1_away", "last_period")},
            "final": g["state"] in ("OFF", "FINAL"), "players": players,
        }
    return {"games": games}
