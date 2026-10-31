# nhl-bettings-pipeline

Nightly NHL data pipeline for **paper-testing** several betting methods head-to-head.
Judged on closing line value (CLV) first, profit second. No real money until a method earns it.

## Status
- [x] Step 1 – daily data pull (schedule, rest, standings, MoneyPuck xG/GSAx, DailyFaceoff goalies, ESPN injuries)
- [x] Step 2 – odds: Pinnacle + US books (main, 1P, props), Underdog & PrizePicks props via The Odds API, Kalshi game markets via its public API
- [x] Step 3 – 7 methods (B0 random, C1 chalk, M1 sharp price, M2 goalie news, M3 xG model, M4 shots model, M5 pick'em entries), locked daily by the "Pick lock" workflow
- [x] Step 4 – closing prices + grading + scoreboard
  - "Closing prices" sleeps until ~10 min before each picked game and snapshots it once (sharp fair close via The Odds API, Kalshi quote)
  - "Grade & scoreboard" (each morning) grades every past slate from NHL API boxscores, replaces Kalshi closes with the exact 1-minute candle at listed start, and rewrites **[data/scoreboard.md](data/scoreboard.md)** (+ `data/scoreboard.csv`)
- [ ] Step 5 – weekly summary, dashboard
- [~] Backtest 2025-26 (M1, M3, M4) – `nhlpipe/backtest/`, run from Actions → "Backtest (manual)"; results in `data/backtest/report.md`

## Backtest
`nhlpipe/backtest/` replays the 2025-26 regular season with The Odds API historical archive
(13:50 ET pick snapshot, closing snapshot ~2 min before each game) and point-in-time stats
(MoneyPuck game logs and NHL box scores dated before each pick date). The live methods in
`nhlpipe/methods.py` and models in `nhlpipe/models.py` are used unchanged. Every external pull is cached
under `data/backtest/` and never repeated; Odds API credits are logged in `data/backtest/odds/ledger.csv`.
Actions → "Backtest (manual)": task `pull` / `run` with `START END`, then `report`.

## Scoreboard
Open [data/scoreboard.md](data/scoreboard.md) on GitHub. Per method, singles and parlays/entries separate, last 7 days and season:
bets, W-L, win %, units, ROI, average fair CLV, average Kalshi CLV, % of bets beating the close.
Per-pick grades: `data/graded/<date>.csv`. Settlement rules are at the top of `nhlpipe/grade.py`
(OT counts and a shootout adds 1 goal for game markets, like Kalshi; player props use boxscore stats;
a player who doesn't dress → void; parlays reprice without void legs; a 2-pick entry with a void leg is refunded).

## Layout
```
nhlpipe/            pipeline code
data/raw/<date>/    raw snapshots per source + status.json
data/slates/<date>.csv   one row per game with all features
data/picks/<date>.csv    locked picks (+ candidates, model games)
data/closing/<date>.csv  closing prices per picked bet
data/results/<date>.json final scores, 1st-period goals, skater stats (NHL API)
data/graded/<date>.csv   per-pick result, units, CLV
data/scoreboard.md/.csv  per-method scoreboard
.github/workflows/  scheduled runs (GitHub Actions, free tier)
```

## Run manually
GitHub → Actions → "Daily data pull" → Run workflow (optional date).
GitHub → Actions → "Grade & scoreboard" → Run workflow (optional date to re-grade).

## Secrets
`ODDS_API_KEY` (repo Settings → Secrets and variables → Actions).

## Data credits
Advanced stats courtesy of [MoneyPuck.com](https://moneypuck.com) (non-commercial use).
Goalie projections: DailyFaceoff. Injuries: ESPN. Schedule/standings: NHL API.
