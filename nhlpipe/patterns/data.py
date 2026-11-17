"""Tables for the pattern scan: one row per game (or per player prop line) with
point-in-time features, the market's fair probability at pick time ("expected"),
the close where it is cached, and the result ("observed").

Never calls a paid API: odds come only from files already cached in the repo
  2025-26  data/backtest/odds/featured (13:50 ET pick snapshot + later snapshots)
           data/backtest/odds/event    (props at the pick snapshot)
  2026-27  data/odds/<date>/<lock snapshot>/odds_long.csv (the live pick lock)
Features use only games dated before the pick date:
  team    MoneyPuck team game logs (data/shots2/mp_teams.csv.gz), same code both seasons
  sched   rest / back-to-back / travel from the published schedule (shots2.features.schedule_frame)
  goalie  projected starter: 2025-26 the backtest rule (features.Season; 83% right),
          2026-27 the live DailyFaceoff starter in data/slates (what a live bet would see)
  player  NHL per-game stats (data/shots2/nhlstats) and shots2 features

python -m nhlpipe.patterns.data   -> data/patterns/games.csv.gz, sog.csv.gz, points.csv.gz
"""
import gzip
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .. import fair
from ..names import norm
from ..backtest import nhldata, mpdata
from ..backtest.features import Season
from ..backtest.pipeline import TMAP, odds_frame, pick_dt
from ..shots2 import features as sfeat, pull as spull, live as slive

DATA = Path(__file__).resolve().parents[2] / "data"
OUT = DATA / "patterns"
ODDS25 = DATA / "backtest" / "odds"
US_BOOKS = ["draftkings", "fanduel", "betmgm", "williamhill_us", "betrivers", "espnbet"]
DIV = {t: d for d, ts in {
    "ATL": "BOS BUF DET FLA MTL OTT TBL TOR", "MET": "CAR CBJ NJD NYI NYR PHI PIT WSH",
    "CEN": "CHI COL DAL MIN NSH STL UTA WPG", "PAC": "ANA CGY EDM LAK SEA SJS VAN VGK"}.items() for t in ts.split()}
CONF = {t: ("E" if d in ("ATL", "MET") else "W") for t, d in DIV.items()}


# ------------------------------------------------------------------ odds ----
def _load(p: Path) -> dict:
    return json.loads(gzip.decompress(p.read_bytes()))


def _ts(p: Path) -> datetime:
    return datetime.strptime(p.name.split("_")[0], "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)


def _snaps25(kind: str, d: date) -> list[Path]:
    out = []
    for dd in (d, d + timedelta(days=1)):
        out += sorted((ODDS25 / kind / dd.isoformat()).glob("*.json.gz"))
    return out


def market_lines(od: pd.DataFrame) -> pd.DataFrame:
    """Per event from one snapshot: Pinnacle fair ml / main total / -1.5, Pinnacle's own prices,
    and the best US-book price on each side (lowest implied probability)."""
    if od.empty:
        return pd.DataFrame()
    od = od[od["implied_prob"].notna()].copy()
    od["player"] = od.get("player")
    dv = fair.devig(od[od["market"].isin(["h2h", "totals", "spreads"])])
    pin = dv[dv["book"] == "pinnacle"]
    rows = []
    for eid, e in od.groupby("event_id"):
        r0 = e.iloc[0]
        r = {"event_id": eid, "commence_utc": r0["commence_utc"], "home": r0["home"], "away": r0["away"]}
        p = pin[pin["event_id"] == eid]
        us = e[e["book"].isin(US_BOOKS)]
        h = p[(p["market"] == "h2h") & (p["outcome"] == r0["home_name"])]
        a = p[(p["market"] == "h2h") & (p["outcome"] == r0["away_name"])]
        if len(h) and len(a):
            r.update(ml_home_fair=h["fair"].iloc[0], pin_home_imp=h["implied_prob"].iloc[0], pin_away_imp=a["implied_prob"].iloc[0])
            uh = us[(us["market"] == "h2h") & (us["outcome"] == r0["home_name"])]["implied_prob"]
            ua = us[(us["market"] == "h2h") & (us["outcome"] == r0["away_name"])]["implied_prob"]
            r.update(best_home_imp=uh.min() if len(uh) else np.nan, best_away_imp=ua.min() if len(ua) else np.nan)
        t = p[p["market"] == "totals"]
        if len(t):
            piv = t.pivot_table(index="point", columns="outcome", values=["fair", "implied_prob"], aggfunc="first")
            piv = piv.dropna()
            if len(piv):
                line = (piv[("fair", "Over")] - 0.5).abs().idxmin()
                r.update(tot_line=float(line), over_fair=piv.loc[line, ("fair", "Over")],
                         pin_over_imp=piv.loc[line, ("implied_prob", "Over")], pin_under_imp=piv.loc[line, ("implied_prob", "Under")])
                ut = us[(us["market"] == "totals") & (us["point"] == line)]
                uo, uu = ut[ut["outcome"] == "Over"]["implied_prob"], ut[ut["outcome"] == "Under"]["implied_prob"]
                r.update(best_over_imp=uo.min() if len(uo) else np.nan, best_under_imp=uu.min() if len(uu) else np.nan)
        s = p[(p["market"] == "spreads") & (p["point"] == -1.5)]
        if len(s):
            fav = s.iloc[0]
            team = r0["home"] if fav["outcome"] == r0["home_name"] else r0["away"]
            r.update(pl_fav=team, pl_fav_fair=fav["fair"], pin_pl_imp=fav["implied_prob"])
        rows.append(r)
    return pd.DataFrame(rows)


def _close25(d: date, events: dict[str, str]) -> pd.DataFrame:
    """Last cached featured snapshot <= 30 min before each event's start (2025-26)."""
    best: dict[str, Path] = {}
    files = [(f, _ts(f)) for f in _snaps25("featured", d)]
    for eid, ct in events.items():
        start = datetime.fromisoformat(ct.replace("Z", "+00:00"))
        ok = [(f, t) for f, t in files if timedelta(0) < start - t <= timedelta(minutes=30)]
        if ok:
            best[eid] = max(ok, key=lambda x: x[1])[0]
    rows = []
    for f in set(best.values()):
        want = {e for e, ff in best.items() if ff == f}
        od = odds_frame([(_load(f), want)], TMAP)
        ml = market_lines(od)
        if len(ml):
            ml["close_min_before"] = [(datetime.fromisoformat(c.replace("Z", "+00:00")) - _ts(f)).total_seconds() / 60
                                      for c in ml["commence_utc"]]
            rows.append(ml)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


# --------------------------------------------------------- team features ----
def team_asof(mp: pd.DataFrame, dates: list[date]) -> pd.DataFrame:
    """(team, date) -> season-to-date and last-10 rates from games strictly before date."""
    m = mp.copy()
    m["d"] = pd.to_datetime(m["gameDate"].astype(str)).dt.date
    al, ev = m[m["situation"] == "all"], m[m["situation"] == "5on5"]
    pp, pk = m[m["situation"] == "5on4"], m[m["situation"] == "4on5"]
    out = []
    for D in sorted(set(dates)):
        season = D.year if D.month >= 8 else D.year - 1
        a = al[(al["season"] == season) & (al["d"] < D)]
        if a.empty:
            continue
        g = a.groupby("team")
        t = pd.DataFrame({"gp": g["gameId"].nunique(), "gf": g["goalsFor"].sum(), "ga": g["goalsAgainst"].sum(),
                          "xgf": g["xGoalsFor"].sum(), "xga": g["xGoalsAgainst"].sum(),
                          "sf": g["shotsOnGoalFor"].sum(), "sa": g["shotsOnGoalAgainst"].sum(),
                          "pen_for": g["penaltiesFor"].sum(), "pen_against": g["penaltiesAgainst"].sum()})
        for c in ["gf", "ga", "xgf", "xga", "sf", "sa", "pen_for", "pen_against"]:
            t[c + "_pg"] = t[c] / t["gp"]
        t["finish_pg"] = (t["gf"] - t["xgf"]) / t["gp"]          # scoring above expected
        t["save_pg"] = (t["xga"] - t["ga"]) / t["gp"]            # team goaltending above expected
        t["xg_pct"] = t["xgf"] / (t["xgf"] + t["xga"])
        t["gd_pg"] = (t["gf"] - t["ga"]) / t["gp"]
        last = a.sort_values("d").groupby("team").tail(10).groupby("team")
        t["l10_gf_pg"] = last["goalsFor"].mean()
        t["l10_ga_pg"] = last["goalsAgainst"].mean()
        t["l10_xg_pct"] = last["xGoalsFor"].sum() / (last["xGoalsFor"].sum() + last["xGoalsAgainst"].sum())
        e = ev[(ev["season"] == season) & (ev["d"] < D)].groupby("team")
        t["ev_xg_pct"] = e["xGoalsFor"].sum() / (e["xGoalsFor"].sum() + e["xGoalsAgainst"].sum())
        p_ = pp[(pp["season"] == season) & (pp["d"] < D)].groupby("team")
        k_ = pk[(pk["season"] == season) & (pk["d"] < D)].groupby("team")
        t["pp_xgf60"] = p_["xGoalsFor"].sum() / (p_["iceTime"].sum() / 3600)
        t["pk_xga60"] = k_["xGoalsAgainst"].sum() / (k_["iceTime"].sum() / 3600)
        prev = al[al["season"] == season - 1].groupby("team")
        t["prev_ga_pg"] = prev["goalsAgainst"].sum() / prev["gameId"].nunique()
        t["prev_xg_pct"] = prev["xGoalsFor"].sum() / (prev["xGoalsFor"].sum() + prev["xGoalsAgainst"].sum())
        # league percentile on this date (0 = lowest value) for the headline stats
        for c in ["ga_pg", "gf_pg", "xga_pg", "xgf_pg", "xg_pct", "save_pg", "finish_pg", "l10_ga_pg", "l10_gf_pg"]:
            t[c + "_pct"] = t[c].rank(pct=True)
        t["date"] = D
        out.append(t.reset_index())
    return pd.concat(out, ignore_index=True)


# ---------------------------------------------------------------- games ----
def _sched(seasons: list[str]) -> pd.DataFrame:
    games = [g for s in seasons for g in spull.schedule(s, refresh=False)]
    return sfeat.schedule_frame(games)


def _attach(df: pd.DataFrame, mp: pd.DataFrame, sched: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    ta = team_asof(mp, list(df["date"]))
    for side in ("home", "away"):
        x = ta.rename(columns={c: f"{side}_{c}" for c in ta.columns if c not in ("team", "date")}).rename(columns={"team": side})
        df = df.merge(x, on=[side, "date"], how="left")
        s = sched[["gameId", "team", "rest_days", "b2b", "tz_shift", "road_trip"]].rename(
            columns={"gameId": "game_id", "team": side, "rest_days": f"{side}_rest", "b2b": f"{side}_b2b",
                     "tz_shift": f"{side}_tz_shift", "road_trip": f"{side}_road_trip"})
        df = df.drop(columns=[c for c in s.columns if c not in ("game_id", side) and c in df.columns]).merge(s, on=["game_id", side], how="left")
    return df


def games_2025() -> pd.DataFrame:
    recs = nhldata.load_range(nhldata.SEASON_START, nhldata.SEASON_END)
    season = Season(recs, pd.read_csv(mpdata.ROOT / f"teams_{mpdata.SEASON}.csv.gz"),
                    pd.read_csv(mpdata.ROOT / f"goalies_{mpdata.SEASON}.csv.gz"))
    rows = []
    for ds, rec in sorted(recs.items()):
        d = date.fromisoformat(ds)
        t_pick = pick_dt(d).astimezone(timezone.utc)
        sched = [g for g in rec["games"] if datetime.fromisoformat(g["start_utc"].replace("Z", "+00:00")) > t_pick]
        if not sched:
            continue
        pf = [f for f in _snaps25("featured", d) if _ts(f) == t_pick]
        if not pf:
            continue
        od = odds_frame([_load(f) for f in pf], TMAP)
        ml = market_lines(od)
        if ml.empty:
            continue
        ml = ml[pd.to_datetime(ml["commence_utc"]).dt.tz_convert("America/New_York").dt.date == d]
        slate, _, _ = season.slate(d, sched)
        slate = slate[[c for c in slate.columns if "goalie" in c or c in ("game_id", "home", "away", "start_utc")]]
        g = slate.merge(ml, on=["home", "away"], how="inner")
        close = _close25(d, dict(zip(g["event_id"], g["commence_utc"])))
        if len(close):
            c = close[["event_id", "ml_home_fair", "tot_line", "over_fair", "close_min_before"]].rename(
                columns={"ml_home_fair": "close_home_fair", "tot_line": "close_tot_line", "over_fair": "close_over_fair"})
            g = g.merge(c, on="event_id", how="left")
        res = {x["game_id"]: x for x in sched}
        for r in g.to_dict("records"):
            x = res[r["game_id"]]
            if x["state"] not in ("OFF", "FINAL"):
                continue
            r.update(date=ds, home_score=x["home_score"], away_score=x["away_score"], last_period=x["last_period"])
            rows.append(r)
    df = pd.DataFrame(rows)
    df["season"] = 2025
    return df


def games_2026() -> pd.DataFrame:
    rows = []
    for od_dir in sorted((DATA / "odds").iterdir()):
        ds = od_dir.name
        pk, sl, rs = DATA / "picks" / f"{ds}.csv", DATA / "slates" / f"{ds}.csv", DATA / "results" / f"{ds}.json"
        if not (pk.exists() and sl.exists() and rs.exists()):
            continue
        snap = str(int(pd.read_csv(pk)["odds_snapshot"].dropna().iloc[0])).zfill(4)
        f = od_dir / snap / "odds_long.csv"
        if not f.exists():
            continue
        od = pd.read_csv(f)
        lock = pd.Timestamp(od["snapshot_et"].iloc[0])
        od = od[pd.to_datetime(od["commence_utc"]) > lock]
        ml = market_lines(od)
        if ml.empty:
            continue
        s = pd.read_csv(sl)
        s = s[[c for c in s.columns if "goalie" in c or c in ("game_id", "home", "away", "start_utc")]]
        g = s.merge(ml, on=["home", "away"], how="inner")
        res = json.loads(rs.read_text())["games"]
        sh = DATA / "shadow" / f"{ds}.csv"
        shd = pd.read_csv(sh) if sh.exists() else pd.DataFrame()
        for r in g.to_dict("records"):
            x = res.get(f"{r['away']}@{r['home']}")
            if not x or not x.get("final"):
                continue
            r.update(date=ds, home_score=x["home_score"], away_score=x["away_score"], last_period=x["last_period"])
            if len(shd) and "close_fair" in shd:  # close from the nightly shadow board (Pinnacle archive ~4 min before)
                k = shd[(shd["game_key"] == f"{r['away']}@{r['home']}") & shd["close_fair"].notna()]
                h = k[(k["market"] == "ml") & (k["team"] == r["home"]) & (k["side"] == "yes")]
                o = k[(k["market"] == "total") & (k["line"] == r.get("tot_line")) & (k["side"] == "yes")]
                r["close_home_fair"] = h["close_fair"].iloc[0] if len(h) else np.nan
                r["close_over_fair"] = o["close_fair"].iloc[0] if len(o) else np.nan
            rows.append(r)
    df = pd.DataFrame(rows)
    df["season"] = 2026
    return df


def derive(df: pd.DataFrame) -> pd.DataFrame:
    """Outcomes and game-level features (all from pick-time inputs)."""
    d = df.copy()
    d["total"] = d["home_score"] + d["away_score"]  # official final: shootout winner +1, as books settle
    d["y_over"] = np.where(d["total"] > d["tot_line"], 1.0, np.where(d["total"] < d["tot_line"], 0.0, np.nan))
    d["y_home"] = (d["home_score"] > d["away_score"]).astype(float)
    fav_home = d["pl_fav"] == d["home"]
    margin = np.where(fav_home, d["home_score"] - d["away_score"], d["away_score"] - d["home_score"])
    d["y_pl_fav"] = np.where(d["pl_fav"].notna(), (margin >= 2).astype(float), np.nan)
    d["pl_fav_home"] = fav_home.astype(float).where(d["pl_fav"].notna())
    st = pd.to_datetime(d["start_utc"], utc=True).dt.tz_convert("America/New_York")
    d["start_hour_et"] = st.dt.hour + st.dt.minute / 60
    d["early_start"] = (d["start_hour_et"] < 18.5).astype(float)
    d["weekend"] = (st.dt.dayofweek >= 5).astype(float)
    d["month"] = st.dt.month
    d["division_game"] = (d["home"].map(DIV) == d["away"].map(DIV)).astype(float)
    d["conference_game"] = (d["home"].map(CONF) == d["away"].map(CONF)).astype(float)
    for s in ("home", "away"):
        d[f"{s}_goalie_gsax_pg"] = d[f"{s}_goalie_gsax"] / d[f"{s}_goalie_gp"].replace(0, np.nan)
        d[f"{s}_goalie_share"] = d[f"{s}_goalie_gp"] / d[f"{s}_gp"]
        d[f"{s}_backup"] = ((d[f"{s}_goalie_share"] < 0.4) & (d[f"{s}_gp"] >= 8)).astype(float)
        d[f"{s}_3in4"] = np.nan  # filled below from rest days is not exact; use b2b + rest instead
    d = d.drop(columns=["home_3in4", "away_3in4"])
    # sums (totals) and differences (home minus away)
    for c in ["gf_pg", "ga_pg", "xgf_pg", "xga_pg", "sf_pg", "sa_pg", "finish_pg", "save_pg", "l10_gf_pg", "l10_ga_pg",
              "pen_for_pg", "pen_against_pg", "pp_xgf60", "pk_xga60", "goalie_gsax_pg", "goalie_gsax"]:
        d[f"sum_{c}"] = d[f"home_{c}"] + d[f"away_{c}"]
    for c in ["xg_pct", "ev_xg_pct", "gd_pg", "finish_pg", "save_pg", "goalie_gsax_pg", "l10_xg_pct", "rest", "prev_xg_pct", "pp_xgf60"]:
        d[f"diff_{c}"] = d[f"home_{c}"] - d[f"away_{c}"]
    # pace implied by stats vs the line: expected goals each way, averaged with goals each way
    d["xg_total"] = (d["home_xgf_pg"] + d["away_xga_pg"]) / 2 + (d["away_xgf_pg"] + d["home_xga_pg"]) / 2
    d["g_total"] = (d["home_gf_pg"] + d["away_ga_pg"]) / 2 + (d["away_gf_pg"] + d["home_ga_pg"]) / 2
    d["xg_total_minus_line"] = d["xg_total"] - d["tot_line"]
    d["g_total_minus_line"] = d["g_total"] - d["tot_line"]
    d["both_goalies_hot"] = ((d["home_goalie_gsax"] > 0) & (d["away_goalie_gsax"] > 0)).astype(float)
    d["both_goalies_cold"] = ((d["home_goalie_gsax"] < 0) & (d["away_goalie_gsax"] < 0)).astype(float)
    d["both_def_top_third"] = ((d["home_ga_pg_pct"] <= 1 / 3) & (d["away_ga_pg_pct"] <= 1 / 3)).astype(float)
    d["both_def_bottom_third"] = ((d["home_ga_pg_pct"] >= 2 / 3) & (d["away_ga_pg_pct"] >= 2 / 3)).astype(float)
    d["both_off_top_third"] = ((d["home_gf_pg_pct"] >= 2 / 3) & (d["away_gf_pg_pct"] >= 2 / 3)).astype(float)
    d["any_backup"] = ((d["home_backup"] == 1) | (d["away_backup"] == 1)).astype(float)
    d["away_b2b_only"] = ((d["away_b2b"] == 1) & (d["home_b2b"] == 0)).astype(float)
    d["home_b2b_only"] = ((d["home_b2b"] == 1) & (d["away_b2b"] == 0)).astype(float)
    d["both_b2b"] = ((d["home_b2b"] == 1) & (d["away_b2b"] == 1)).astype(float)
    d["line_55"] = (d["tot_line"] == 5.5).astype(float)
    d["line_65"] = (d["tot_line"] == 6.5).astype(float)
    d["line_whole"] = (d["tot_line"] % 1 == 0).astype(float)
    d["home_fav"] = (d["ml_home_fair"] > 0.5).astype(float)
    d["fav_fair"] = np.maximum(d["ml_home_fair"], 1 - d["ml_home_fair"])
    d["season_gp"] = (d["home_gp"] + d["away_gp"]) / 2
    # the user's own read (Evan, 2026-11-17), pre-specified before the scan was run:
    # both defences in the league's best third by goals against per game AND both
    # projected starters at or above expected (GSAx >= 0) -> the under hits more than priced
    d["evan_under"] = ((d["both_def_top_third"] == 1) & (d["home_goalie_gsax"] >= 0) & (d["away_goalie_gsax"] >= 0)).astype(float)
    return d


def build_games() -> pd.DataFrame:
    mp = pd.read_csv(DATA / "shots2" / "mp_teams.csv.gz")
    sched = _sched(["20252026", "20262027"])
    g = pd.concat([games_2025(), games_2026()], ignore_index=True)
    g = _attach(g, mp, sched)
    g = derive(g)
    OUT.mkdir(parents=True, exist_ok=True)
    g.to_csv(OUT / "games.csv.gz", index=False)
    return g


# ---------------------------------------------------------------- props ----
def _player_frames(season: str, cutoff: date, mu_from_lines: bool) -> pd.DataFrame:
    """shots2 point-in-time skater features for every skater-game of a season."""
    seasons = [s for s in ["20222023", "20232024", "20242025", "20252026", "20262027"] if s <= season]
    hist = pd.concat([spull.load_stats(s) for s in seasons], ignore_index=True)
    games = [g for s in seasons for g in spull.schedule(s, refresh=False)]
    mp = pd.read_csv(DATA / "shots2" / "mp_teams.csv.gz")
    mp = mp[mp["gameDate"] < int((date(int(season[4:]), 8, 1)).strftime("%Y%m%d"))]
    s = sfeat.add_h2h(sfeat.build(hist, games, mp, cutoff))
    y0 = int(season[:4])
    s = s[(s["gameId"] // 1_000_000 == y0) & (s["n_prior"] >= 1) & s["mu_base"].notna()].copy()
    s["key"] = s["skaterFullName"].map(norm)
    s["game_key"] = s["opp"].where(s["home"] == 1, s["teamAbbrev"]) + "@" + s["teamAbbrev"].where(s["home"] == 1, s["opp"])
    s["date"] = s["date"].astype(str)
    dup = s.duplicated(["date", "game_key", "key"], keep=False)
    return s[~dup]


def _season_rates(stats: pd.DataFrame) -> pd.DataFrame:
    """Per skater-game: season-to-date points/goals/toi per game from earlier games only."""
    st = stats.sort_values(["playerId", "gameDate", "gameId"]).copy()
    st["season"] = st["gameId"] // 1_000_000
    g = st.groupby(["playerId", "season"])
    for c in ("points", "goals", "assists", "ppPoints", "shots"):
        st[f"{c}_std"] = (g[c].cumsum() - st[c]) / g.cumcount().replace(0, np.nan)
    st["gp_std"] = g.cumcount()
    st["toi_std"] = (g["timeOnIce"].cumsum() - st["timeOnIce"]) / 60 / g.cumcount().replace(0, np.nan)
    st["pp_toi_std"] = (g["ppTimeOnIce"].cumsum() - st["ppTimeOnIce"]) / 60 / g.cumcount().replace(0, np.nan)
    st["pts_l10"] = g["points"].transform(lambda x: x.shift(1).rolling(10, min_periods=3).mean())
    return st[["playerId", "gameId", "points_std", "goals_std", "assists_std", "ppPoints_std", "shots_std",
               "gp_std", "toi_std", "pp_toi_std", "pts_l10", "points", "goals"]]


def build_sog(games: pd.DataFrame) -> pd.DataFrame:
    fr = slive.Frozen(json.loads(slive.PARAMS.read_text()))
    # 2025-26: lines.csv (Pinnacle pick + close, model mu fit on 2023-25 only = out of sample)
    L = pd.read_csv(DATA / "shots2" / "lines.csv")
    L = L.rename(columns={"pinnacle_pick": "fair_over", "pinnacle_close": "close_over"})
    L["p_model"] = L["p_v2"]
    s25 = _player_frames("20252026", date(2025, 10, 15), True)
    L = L.merge(s25.drop(columns=["shots"], errors="ignore"), on=["date", "game_key", "key"], how="inner", suffixes=("", "_f"))
    L["season"] = 2025
    # 2026-27: shadow board Pinnacle SOG lines (frozen model, fit before this season = out of sample)
    sh = pd.concat([pd.read_csv(f) for f in sorted((DATA / "shadow").glob("*.csv"))], ignore_index=True)
    sh = sh[(sh["market"] == "player_sog") & (sh["fair_source"] == "pinnacle") & sh["y"].notna() & (sh["side"] == "yes")]
    sh = sh.drop_duplicates(["date", "game_key", "player", "line"])
    sh = sh.assign(key=sh["player"].map(norm), fair_over=sh["fair_prob"], close_over=sh["close_fair"])
    s26 = _player_frames("20262027", slive.LIVE_CUTOFF, False)
    s26["mu"] = fr.mean(s26)
    S = sh[["date", "game_key", "key", "line", "fair_over", "close_over", "y"]].merge(s26, on=["date", "game_key", "key"], how="inner")
    S["p_model"] = fr.p_over(S["mu"].to_numpy(), S["line"].to_numpy())
    S["season"] = 2026
    P = pd.concat([L, S], ignore_index=True)
    P["model_minus_fair"] = P["p_model"] - P["fair_over"]
    P["mu_minus_line"] = P["mu"] - P["line"]
    P["base_minus_line"] = P["mu_base"] - P["line"]
    P["D"] = (P["positionCode"] == "D").astype(float)
    P["F"] = 1 - P["D"]
    P["toi_jump"] = np.log((P["toi_last"].fillna(P["toi_avg"]) + 1) / (P["toi_avg"] + 1)).clip(-1, 1)
    P["pp_jump"] = (P["pp_last"].fillna(P["pp_toi"]) - P["pp_toi"]).clip(-4, 4)
    # keep only pick-time columns + the result (the stats row of the game itself is dropped)
    keep = ["date", "game_key", "key", "line", "fair_over", "close_over", "y", "season", "playerId", "teamAbbrev",
            "positionCode", "mu", "p_model", "model_minus_fair", "mu_minus_line", "base_minus_line"] + \
        [c for c in ["D", "F", "mu_base", "ev_toi", "pp_toi", "toi_jump", "pp_jump", "on_net", "ev_att60", "oz_start", "home",
                     "b2b", "opp_b2b", "rest_days", "tz_shift", "road_trip", "opp_sa_ratio", "team_ca_ratio", "xg_edge",
                     "opp_pen_ratio", "missing_toi", "traded", "h2h_resid", "n_prior"]]
    P = _add_game_context(P[keep], games)
    P.to_csv(OUT / "sog.csv.gz", index=False)
    return P


def _add_game_context(P: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    g = games.copy()
    g["date"] = g["date"].astype(str)
    g["game_key"] = g["away"] + "@" + g["home"]
    ctx = g[["date", "game_key", "home", "tot_line", "over_fair", "ml_home_fair", "home_ga_pg_pct", "away_ga_pg_pct",
             "home_goalie_gsax_pg", "away_goalie_gsax_pg", "home_sa_pg", "away_sa_pg"]].rename(columns={"home": "g_home"})
    P = P.drop(columns=[c for c in ctx.columns if c not in ("date", "game_key") and c in P.columns])
    P = P.merge(ctx, on=["date", "game_key"], how="left")
    ih = P["teamAbbrev"] == P["g_home"]
    P["team_win_fair"] = np.where(ih, P["ml_home_fair"], 1 - P["ml_home_fair"])
    P["opp_ga_pct"] = np.where(ih, P["away_ga_pg_pct"], P["home_ga_pg_pct"])
    P["opp_goalie_gsax_pg"] = np.where(ih, P["away_goalie_gsax_pg"], P["home_goalie_gsax_pg"])
    P["opp_sa_pg"] = np.where(ih, P["away_sa_pg"], P["home_sa_pg"])
    P["game_over_fair"] = P["over_fair"]
    return P


def _points25() -> pd.DataFrame:
    """Pinnacle player_points lines at the 2025-26 pick snapshot (cached event odds)."""
    rows = []
    for dd in sorted((ODDS25 / "event").iterdir()):
        d = date.fromisoformat(dd.name)
        for cand in (d, d - timedelta(days=1)):  # files are filed by UTC date of the snapshot
            t_pick = pick_dt(cand).astimezone(timezone.utc)
            fs = [f for f in dd.glob("*.json.gz") if _ts(f) == t_pick]
            if not fs:
                continue
            od = odds_frame([_load(f) for f in fs], TMAP)
            od = od[(od["market"] == "player_points") & od["implied_prob"].notna()]
            if od.empty:
                continue
            dv = fair.devig(od)
            p = dv[(dv["book"] == "pinnacle") & (dv["outcome"] == "Over")]
            us = od[od["book"].isin(US_BOOKS)]
            for r in p.to_dict("records"):
                u = us[(us["event_id"] == r["event_id"]) & (us["player"] == r["player"]) & (us["point"] == r["point"])]
                rows.append({"date": cand.isoformat(), "game_key": f"{r['away']}@{r['home']}", "key": norm(r["player"]),
                             "line": r["point"], "fair_over": r["fair"], "pin_over_imp": r["implied_prob"],
                             "best_over_imp": u.loc[u["outcome"] == "Over", "implied_prob"].min(),
                             "best_under_imp": u.loc[u["outcome"] == "Under", "implied_prob"].min()})
    return pd.DataFrame(rows).drop_duplicates(["date", "game_key", "key", "line"])


def build_points(games: pd.DataFrame) -> pd.DataFrame:
    p25 = _points25()
    p25["season"] = 2025
    sh = pd.concat([pd.read_csv(f) for f in sorted((DATA / "shadow").glob("*.csv"))], ignore_index=True)
    sh = sh[(sh["market"] == "player_points") & (sh["fair_source"] == "pinnacle") & (sh["side"] == "yes")]
    sh = sh.drop_duplicates(["date", "game_key", "player", "line"])
    p26 = sh.assign(key=sh["player"].map(norm), fair_over=sh["fair_prob"], close_over=sh["close_fair"])[
        ["date", "game_key", "key", "line", "fair_over", "close_over"]]
    p26["season"] = 2026
    out = []
    for season, P in (("20252026", p25), ("20262027", p26)):
        stats = pd.concat([spull.load_stats(s) for s in ([season] if season == "20252026" else ["20262027"])], ignore_index=True)
        rates = _season_rates(stats)
        st = stats[["playerId", "gameId", "gameDate", "skaterFullName", "teamAbbrev", "opponentTeamAbbrev", "homeRoad",
                    "positionCode", "timeOnIce"]].copy()
        st["key"] = st["skaterFullName"].map(norm)
        st["game_key"] = np.where(st["homeRoad"] == "H", st["opponentTeamAbbrev"] + "@" + st["teamAbbrev"],
                                  st["teamAbbrev"] + "@" + st["opponentTeamAbbrev"])
        st["date"] = st["gameDate"].astype(str)
        st = st[~st.duplicated(["date", "game_key", "key"], keep=False)]
        st = st.merge(rates, on=["playerId", "gameId"], how="left")
        # the stats row only identifies the player and the result; features are the *_std columns (earlier games)
        m = P.merge(st, on=["date", "game_key", "key"], how="inner")
        m = m[m["timeOnIce"] > 0]
        m["y"] = np.where(m["points"] > m["line"], 1.0, 0.0)
        out.append(m)
    P = pd.concat(out, ignore_index=True)
    P["D"] = (P["positionCode"] == "D").astype(float)
    P["home"] = (P["homeRoad"] == "H").astype(float)
    P["pts_minus_line"] = P["points_std"] - P["line"]
    keep = ["date", "game_key", "key", "line", "fair_over", "close_over", "y", "season", "playerId", "teamAbbrev", "positionCode",
            "pin_over_imp", "best_over_imp", "best_under_imp", "D", "home", "pts_minus_line", "points_std", "goals_std",
            "assists_std", "ppPoints_std", "shots_std", "gp_std", "toi_std", "pp_toi_std", "pts_l10"]
    P = _add_game_context(P[[c for c in keep if c in P.columns]], games)
    P["team_implied_goals"] = P["tot_line"] * (0.5 + (P["team_win_fair"] - 0.5) * 0.6)  # rough split of the total
    P.to_csv(OUT / "points.csv.gz", index=False)
    return P


if __name__ == "__main__":
    g = build_games()
    print("games", g.groupby("season").size().to_dict())
    s = build_sog(g)
    print("sog lines", s.groupby("season").size().to_dict())
    p = build_points(g)
    print("points lines", p.groupby("season").size().to_dict())
