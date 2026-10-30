# nhl-bettings-pipeline

Nightly NHL data pipeline for **paper-testing** several betting methods head-to-head.
Judged on closing line value (CLV) first, profit second. No real money until a method earns it.

## Status
- [x] Step 1 – daily data pull (schedule, rest, standings, MoneyPuck xG/GSAx, DailyFaceoff goalies, ESPN injuries)
- [x] Step 2 – odds: Pinnacle + US books (main, 1P, props), Underdog & PrizePicks props via The Odds API, Kalshi game markets via its public API
- [ ] Step 3 – methods (6, each picks 4 bets/entries per night)
- [ ] Step 4 – paper-bet log, CLV, weekly summary, dashboard

## Layout
```
nhlpipe/            pipeline code
data/raw/<date>/    raw snapshots per source + status.json
data/slates/<date>.csv   one row per game with all features
.github/workflows/  scheduled runs (GitHub Actions, free tier)
```

## Run manually
GitHub → Actions → "Daily data pull" → Run workflow (optional date).

## Secrets
`ODDS_API_KEY` (repo Settings → Secrets and variables → Actions).

## Data credits
Advanced stats courtesy of [MoneyPuck.com](https://moneypuck.com) (non-commercial use).
Goalie projections: DailyFaceoff. Injuries: ESPN. Schedule/standings: NHL API.
