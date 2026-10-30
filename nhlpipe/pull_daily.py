"""Nightly data pull -> one 'slate' row per game with everything the methods need.

Usage:  python -m nhlpipe.pull_daily [YYYY-MM-DD]
Writes:
  data/raw/<date>/*.json|csv     raw source snapshots (for debugging/backtests)
  data/slates/<date>.csv         joined per-game features
  data/raw/<date>/status.json    which sources worked
Each source fails independently: a broken scraper never kills the run.
"""
import json
import sys
import traceback
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from . import goalies, injuries, moneypuck, nhl_api
from .names import norm

ET = ZoneInfo("America/New_York")
ROOT = Path(__file__).resolve().parent.parent / "data"
OUT_STATUSES = {"out", "injured reserve", "ir", "long term injured reserve", "ltir"}


def _try(status: dict, name: str, fn):
    try:
        res = fn()
        status[name] = "ok"
        return res
    except Exception as e:  # noqa: BLE001 - we want every source isolated
        status[name] = f"FAILED: {type(e).__name__}: {e}"
        traceback.print_exc()
        return None


def run(day: date) -> pd.DataFrame:
    raw = ROOT / "raw" / day.isoformat()
    raw.mkdir(parents=True, exist_ok=True)
    status: dict = {"pulled_at_et": datetime.now(ET).isoformat(timespec="seconds")}

    games = _try(status, "schedule", lambda: nhl_api.schedule(day)) or []
    stand = _try(status, "standings", lambda: nhl_api.standings(day)) or []
    mp_t = _try(status, "moneypuck_teams", lambda: moneypuck.teams(day))
    mp_g = _try(status, "moneypuck_goalies", lambda: moneypuck.goalies(day))
    mp_s = _try(status, "moneypuck_skaters", lambda: moneypuck.skaters(day))
    df_res = _try(status, "dailyfaceoff_goalies", lambda: goalies.starters(day))
    inj = _try(status, "espn_injuries", injuries.injuries) or []

    # --- raw snapshots -------------------------------------------------------
    (raw / "schedule.json").write_text(json.dumps(games, indent=1))
    (raw / "standings.json").write_text(json.dumps(stand, indent=1))
    (raw / "injuries.json").write_text(json.dumps(inj, indent=1))
    for name, df in (("mp_teams", mp_t), ("mp_goalies", mp_g), ("mp_skaters", mp_s)):
        if df is not None:
            df.to_csv(raw / f"{name}.csv.gz", index=False, compression="gzip")
    starters = []
    if df_res:
        starters, df_raw = df_res
        (raw / "dailyfaceoff.json").write_text(json.dumps(starters, indent=1))
        if not starters:  # structure changed: keep the page JSON to fix the parser
            (raw / "dailyfaceoff_page.json").write_text(json.dumps(df_raw)[:2_000_000])
            status["dailyfaceoff_goalies"] = "PARSED 0 GAMES (raw page saved)"

    if not games:
        status["games"] = 0
        (raw / "status.json").write_text(json.dumps(status, indent=1))
        print(json.dumps(status, indent=1))
        return pd.DataFrame()

    tmap = nhl_api.team_name_map(games, stand)

    # --- per-team features ---------------------------------------------------
    team = pd.DataFrame(stand).set_index("team") if stand else pd.DataFrame()
    if mp_t is not None:
        team = team.join(moneypuck.team_features(mp_t).set_index("team"), rsuffix="_mp", how="outer")

    inj_df = pd.DataFrame(inj)
    if not inj_df.empty:
        inj_df["team"] = inj_df["team_name"].map(lambda n: nhl_api.lookup_team(n, tmap))
        inj_df["is_out"] = inj_df["status"].fillna("").str.lower().isin(OUT_STATUSES)
        inj_df.to_csv(raw / "injuries.csv", index=False)
        counts = inj_df[inj_df["is_out"]].groupby("team").size().rename("players_out")
        team = team.join(counts, how="left")
        names = (
            inj_df[inj_df["is_out"]].groupby("team")["player"].apply(lambda s: "; ".join(s))
        ).rename("out_list")
        team = team.join(names, how="left")

    # --- starting goalies + GSAx -------------------------------------------
    g_feat = moneypuck.goalie_features(mp_g) if mp_g is not None else None
    start_by_team = {}
    for s in starters:
        ab = nhl_api.lookup_team(s.get("team_name"), tmap)
        if not ab:
            continue
        row = {"goalie": s.get("goalie"), "goalie_status": s.get("status"), "goalie_updated": s.get("updated")}
        if g_feat is not None and s.get("goalie"):
            hit = g_feat[g_feat["name"].map(norm) == norm(s["goalie"])]
            if len(hit):
                h = hit.sort_values("icetime", ascending=False).iloc[0]
                row.update(goalie_gp=h["games_played"], goalie_gsax=h["gsax"], goalie_gsax60=h["gsax_per60"])
        start_by_team[ab] = row

    # --- assemble slate ------------------------------------------------------
    rows = []
    for g in games:
        r = dict(g)
        for side in ("home", "away"):
            ab = g[side]
            if ab in team.index:
                for c, v in team.loc[ab].items():
                    r[f"{side}_{c}"] = v
            for c, v in start_by_team.get(ab, {}).items():
                r[f"{side}_{c}"] = v
        rows.append(r)
    slate = pd.DataFrame(rows)
    (ROOT / "slates").mkdir(parents=True, exist_ok=True)
    slate.to_csv(ROOT / "slates" / f"{day.isoformat()}.csv", index=False)

    status["games"] = len(games)
    status["goalies_matched"] = sum(1 for g in games for s in ("home", "away") if g[s] in start_by_team)
    (raw / "status.json").write_text(json.dumps(status, indent=1))
    print(json.dumps(status, indent=1))
    return slate


if __name__ == "__main__":
    d = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.now(ET).date()
    run(d)
