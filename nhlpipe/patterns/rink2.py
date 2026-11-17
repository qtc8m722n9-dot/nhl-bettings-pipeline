"""Follow-up to H2 (Evan, 2026-11-17): instead of the team-adjusted rink factor, test the RAW
volume versions - arenas where the most shots get recorded, and the teams that shoot / allow the
most - against SOG prop prices. Exploratory (not pre-registered); same discovery/holdout/live split.
python -m nhlpipe.patterns.rink2 -> data/patterns/rink_volume.md"""
from datetime import date

import numpy as np
import pandas as pd

from .data import DATA, OUT
from .scan import _z, load, trend


def asof(dates):
    m = pd.read_csv(DATA / "shots2" / "mp_teams.csv.gz")
    a = m[m["situation"] == "all"].copy()
    a["d"] = pd.to_datetime(a["gameDate"].astype(str)).dt.date
    a["tot"] = a["shotsOnGoalFor"] + a["shotsOnGoalAgainst"]
    rows = []
    for D in sorted(set(dates)):
        S = D.year if D.month >= 8 else D.year - 1
        cur = a[(a["season"] == S) & (a["d"] < D)]
        w = a[(a["season"] == S - 1) | ((a["season"] == S) & (a["d"] < D))]
        h = w[w["home_or_away"] == "HOME"].groupby("team")["tot"].mean().rename("arena_raw_sog")
        hf = w[w["home_or_away"] == "HOME"].groupby("team")["shotsOnGoalFor"].mean().rename("home_team_sf_at_home")
        sf = cur.groupby("team")["shotsOnGoalFor"].mean().rename("team_sf_pg")
        sa = cur.groupby("team")["shotsOnGoalAgainst"].mean().rename("team_sa_pg")
        t = pd.concat([h, hf, sf, sa], axis=1).reset_index().rename(columns={"index": "team"})
        t["date"] = D
        rows.append(t)
    return pd.concat(rows, ignore_index=True)


def main():
    T = load()
    S = T["sog"].copy()
    S["arena"] = S["game_key"].str.split("@").str[1]
    S["opp"] = np.where(S["teamAbbrev"] == S["arena"], S["game_key"].str.split("@").str[0], S["arena"])
    A = asof(list(S["date"]))
    S = S.merge(A[["team", "date", "arena_raw_sog", "home_team_sf_at_home"]].rename(columns={"team": "arena"}), on=["arena", "date"], how="left")
    S = S.merge(A[["team", "date", "team_sf_pg"]].rename(columns={"team": "teamAbbrev"}), on=["teamAbbrev", "date"], how="left")
    S = S.merge(A[["team", "date", "team_sa_pg"]].rename(columns={"team": "opp", "team_sa_pg": "opp_sa_pg2"}), on=["opp", "date"], how="left")
    S["matchup_volume"] = S["team_sf_pg"] + S["opp_sa_pg2"]
    feats = {"arena_raw_sog": "Arenas where the most total shots get recorded (raw, both teams)",
             "home_team_sf_at_home": "Home team's own shots per game at home",
             "team_sf_pg": "Player's team shots per game (this season)",
             "opp_sa_pg2": "Opponent's shots allowed per game (this season)",
             "matchup_volume": "Team shots for + opponent shots allowed"}
    md = ["# Rink and shot-volume follow-up (exploratory)", "",
          f"Run {date.today().isoformat()}. Evan asked whether the rink test used raw shot volume (the arenas and teams with "
          "the most shots) rather than the team-adjusted rink factor. These are the raw versions. Edge = SOG over hit rate "
          "minus Pinnacle fair, in points; top / bottom quarter cut points come from discovery. Not pre-registered (asked "
          "after H2), so treat a hit as a lead.", "",
          "| Feature | Sample | Lines | Trend z | Top quarter over edge, pts (z) | Bottom quarter over edge, pts (z) |",
          "|---|---|--:|--:|--:|--:|"]
    for f, label in feats.items():
        disc = S[S["split"] == "discovery"]
        lo, hi = disc[f].quantile([0.25, 0.75])
        for sp in ("discovery", "holdout", "live"):
            q = S[(S["split"] == sp)].dropna(subset=["y", "fair_over", f])
            _, z = trend(q["y"].to_numpy(float), q["fair_over"].to_numpy(float), q[f].to_numpy(float), q["gid"].to_numpy())
            a, b = q[q[f] > hi], q[q[f] < lo]
            ea = _z(a["y"].to_numpy(float), a["fair_over"].to_numpy(float), a["gid"].to_numpy())
            eb = _z(b["y"].to_numpy(float), b["fair_over"].to_numpy(float), b["gid"].to_numpy())
            md.append(f"| {label} | {sp} | {len(q):,} | {z:+.2f} | {100 * ea[0]:+.1f} ({ea[1]:+.2f}) | {100 * eb[0]:+.1f} ({eb[1]:+.2f}) |")
    md += ["", "Most / fewest total shots recorded per game by arena (latest, previous + current season):", ""]
    last = A[A["date"] == A["date"].max()].sort_values("arena_raw_sog", ascending=False)
    md.append("Most: " + ", ".join(f"{r.team} {r.arena_raw_sog:.1f}" for r in last.head(5).itertuples()) +
              ". Fewest: " + ", ".join(f"{r.team} {r.arena_raw_sog:.1f}" for r in last.tail(5).itertuples()) + ".")
    (OUT / "rink_volume.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
