# Status and next steps (read this first in a new session)

Last updated: 2026-11-05. Paper bets only. Owner: Evan (Montreal, Quebec).

## What runs by itself (GitHub Actions)
| Workflow | When (ET) | Does |
|---|---|---|
| Daily data pull | 9:30 AM, 12:30 PM | schedule, standings, MoneyPuck, DailyFaceoff goalies, ESPN injuries |
| Pick lock | weekdays 12:50 PM, weekends 10:30 AM | odds snapshot + every method's picks -> `data/picks/<date>.csv` |
| Closing prices | ~28 min before each start slot | live closes (often late/skipped by GitHub; backfilled next morning) |
| Grade & scoreboard | 7:17 AM (+ 11:17 AM retry) | exact closes (Kalshi candles + Odds API archive), grades, `data/scoreboard.md`, `data/shadow/`, `data/diagnostics.md`, `data/hypotheses.md` |
| Backtest (manual) | on demand | `nhlpipe/backtest/cli.py` tasks; every pull cached in `data/backtest/` |
| Weekly flaw review | Mondays 3:37 PM (Claude scheduled task) | reads diagnostics, tests suspected flaws, fixes bugs, reports to Evan |

## Methods (live)
- B0 random, C1 chalk: baselines.
- M1 sharp price: venue price vs power-de-vigged Pinnacle/consensus. Multi-snapshot test (Dec 2025 pilot): no extra bets; not worth more credits.
- M2 goalie news: games with a backup starter, using M3 v2. "Back the backup" tested on all of 2025-26: +0.8 pts vs close (95% -1.8, +3.4) = no edge; rule unchanged.
- M3 v2 xG game model: goalie-pull/empty-net phase (fit 2023-24, better on 2024-25 out of sample) + blend with fair price per market (`data/backtest/m3eng/blend.json`): moneyline and +/-1.5 only; no totals (model weight negative).
- M4: retired 2026-11-04 (replaced by M6).
- M5 pick'em entries: Underdog only, picks from different games, payout = product of pick payouts.
- Bullseye (research component, not a betting method; `nhlpipe/bullseye.py`, `data/bullseye/report.md`): game-winner model on 12 factors (xG strength, finishing, goalie, home, rest/b2b/3-in-4, travel, lineup). Public-model quality (log loss 0.660 on 2024-25 OOS) but no edge on Pinnacle alone in 2025-26 (blend weight 0.20, CI includes 0). Leads: away back-to-back under-priced (home 60.6% vs Pinnacle 56.3%, n=254), market leans on goals over xG.
- M6 shots model v2 (`nhlpipe/shots2/`): NB GLM on role/usage/opponent/schedule features, frozen params `data/shots2/model_v2.json`, blended with Pinnacle; edge 3-12%, up to 3 players/game. `M6_shots_v2` = sportsbook prices (paper benchmark only, not usable from Quebec), `M6_shots_v2_pickem` = Underdog.

## Pricing facts (verified)
- Underdog: 3.5x standard 2-pick since 2026-02-20 -> 1.871 per standard pick x the API's per-pick `multiplier` (Evan confirmed 1.87x in the app, 2026-11-03). Alternate markets pulled for non-standard picks.
- PrizePicks: left Canada 2026-04-03; paper only, 3x 2-pick; demons/goblins skipped.
- Kalshi: taker fee 0.07*C*p*(1-p) rounded up per order (maker 0.0175); never voids (DNP/postponed settle at fair price). Evan says Kalshi works for him from Quebec.
- Odds API: 100,000 credits/month (reset ~1 month after the 2026-10-31 upgrade). ~82k left on 2026-11-03. Live use ~4k/month + shadow closes ~15-20k/month.

## Key results so far
- 2025-26 backtest (`data/backtest/report.md`): no original method beat Pinnacle's close; M1 8 bets all +CLV.
- Shots v2 backtest (`data/shots2/report.md`): beats old M4 and slightly beats Pinnacle on log loss; encompassing weight on model 0.65 (0.50-0.80); bets +3% ROI, CI includes 0.
- Live grades independently verified vs ESPN box scores and Kalshi settlements (10-30, 10-31).

## Next steps (in order)
1. Let the shadow board accumulate (every priced line graded nightly from 2026-11-04).
2. Build the combined model: inputs = fair price, M3 raw/blend, M6 mu/probability, sog_prob, backup-goalie flag, venue, market, line moves; train on shadow board + 2025-26 backtest tables (`data/shots2/lines.csv`, `data/backtest/m3eng/blend_rows.csv`); judge strictly out of sample vs the strongest single method on CLV and log loss. Add Bullseye inputs (prob, a_b2b, ev_xgd, fin; rebuildable from cached data via `bullseye_bt`). Away-b2b hypothesis H1 pre-registered 2026-11-05 (Evan approved; spec in `nhlpipe/hypotheses.py`, graded nightly into `data/hypotheses.md`, games from the 2026-11-05 slate on). 2026-12-31 is an interim look; a verdict needs ~400 games. Review 2026-12-31.
3. M3 totals bias - DONE 2026-11-03 (`data/backtest/m3eng/totals_report.md`): gap 0.27 goals/game = pull scale ~0.13 (PULL_SCALE 0.93 does not preserve the mean as intended) + goalie term ~0.06 + 2025-26 scoring above to-date average ~0.09. Fixing it gives no totals edge (blend weight on M3 still negative) -> no-totals rule stays. Mean-preserving scale adopted 2026-11-05 (Evan approved), live from the 2026-11-06 slate: `models.simulate` now solves the scale per game (`models.mean_scale`); `PULL_SCALE` kept only to reproduce older backtests (`simulate(..., scale=PULL_SCALE)`). Blend weights in `blend.json` were fit on the old scale; the report shows puck line/OT log loss moves < 0.001, so they were not refit.
4. Kalshi: paper-test resting limit orders at fair value (fill rate + CLV on filled orders only).
5. Keep weekly flaw reviews; never change pre-registered rules without Evan's approval.
