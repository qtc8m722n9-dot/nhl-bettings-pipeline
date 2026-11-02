"""Leak test for shots v2: rebuild features for a date with that day's results and
every later game deleted, and check predictions are identical.
python -m nhlpipe.shots2.leaktest 2025-11-18 2026-01-27 2026-03-21"""
import sys
from datetime import date

import numpy as np
import pandas as pd

from . import backtest as B
from . import features, model, pull


def main(days: list[str]) -> None:
    stats = pd.concat([pull.load_stats(s) for s in B.SEASONS], ignore_index=True)
    games = [g for s in B.SEASONS for g in pull.schedule(s)]
    mp = pd.read_csv(pull.ROOT / "mp_teams.csv.gz")
    full = features.add_h2h(features.build(stats, games, mp, B.TEST_START))
    ok = full[(full.gameId // 1_000_000).isin([2023, 2024]) & (full.n_prior >= 1) & full.mu_base.notna()]
    m = model.ShotsModel("glm").fit(ok)
    for D in days:
        st = stats[stats.gameDate <= D].copy()
        today = st.gameDate == D
        for c in ("shots", "totalShotAttempts", "missedShots", "shotAttemptsBlocked", "ppShots", "ppIndividualSatFor"):
            st.loc[today, c] = 0
        for c in ("timeOnIce", "evTimeOnIce", "ppTimeOnIce", "shTimeOnIce"):
            st.loc[today, c] = 60
        mpx = mp[mp.gameDate < int(D.replace("-", ""))]
        gx = [g for g in games if g["date"] <= D]
        cut = features.add_h2h(features.build(st, gx, mpx, B.TEST_START))
        d = date.fromisoformat(D)
        a = full[(full.date == d) & (full.n_prior >= 1)].set_index(["playerId", "gameId"])
        b = cut[cut.date == d].set_index(["playerId", "gameId"]).loc[a.index]
        ma, mb = m.predict_mean(a), m.predict_mean(b)
        print(f"LEAK TEST {D}: {len(a)} skater-games, max |difference| {np.nanmax(np.abs(ma - mb)):.2e}, "
              f"identical: {np.allclose(ma, mb, equal_nan=True)}")


if __name__ == "__main__":
    main(sys.argv[1:])
