# Status and next steps (read this first in a new session)

Last updated: 2026-11-17. Paper bets only. Owner: Evan (Montreal, Quebec).

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
- PrizePicks: left Canada 2026-04-03; paper only, 3x 2-pick; demons/goblins skipped. Goblins = The Odds API `*_alternate` markets at -137 (Over only, line below the standard projection). Until 2026-11-09 they slipped into candidates as standard 3x picks: every M1 bet to date (and some B0/M4/M6-pickem picks) was a goblin, so M1's +8 pt CLV was a pricing artifact. Fixed in `candidates.pickem`; past goblin picks graded void (`grade.pp_goblins`).
- Kalshi: taker fee 0.07*C*p*(1-p) rounded up per order (maker 0.0175); never voids (DNP/postponed settle at fair price). Evan says Kalshi works for him from Quebec.
- Odds API: 100,000 credits/month (reset ~1 month after the 2026-10-31 upgrade). ~82k left on 2026-11-03. Live use ~4k/month + shadow closes ~15-20k/month.

## Key results so far
- 2025-26 backtest (`data/backtest/report.md`): no original method beat Pinnacle's close; M1 8 bets all +CLV.
- Shots v2 backtest (`data/shots2/report.md`): beats old M4 and slightly beats Pinnacle on log loss; encompassing weight on model 0.65 (0.50-0.80); bets +3% ROI, CI includes 0.
- Live grades independently verified vs ESPN box scores and Kalshi settlements (10-30, 10-31).

## Weekly flaw review 2026-11-09
- Bug: PrizePicks goblins priced as standard picks (above). All graded slates + shadow board regraded.
- Bug: 'Yegor' vs NHL 'Egor' Chinakhov not matched (first-name variants in `names.first_key`).
- Bug: two skaters with the same name in one game (VAN's Elias Petterssons; CAR/NYI Sebastian Aho) overwrote each other in `results`; now keyed by sweater number, bare-name bets on them graded 'error' (ambiguous). Results for 10-31, 11-03, 11-05, 11-07 refetched.

## Weekly flaw review 2026-11-16
- Bug: M6 paired a prop on a same-name skater (VAN's Elias Petterssons) with BOTH projections and kept the bigger edge (the 11-13 "Pettersson Under 1.5", edge 11.8%). `shots2/live.picks` now skips same-name skaters in a game; replaying 11-13 removes only that pick.
- No other grading/pricing bugs found. Live M6 projections are identical to a full-history rebuild (max diff 0.4%), so no live leak or pipeline drift. H1 control (home teams 39% vs 54% fair) checked against box scores: real (away teams went 12-2 on 11-14).
- Finding: for every method, closing drift (close minus pick-time fair) is ~0, so CLV = pick-time fair minus price paid: it measures price shopping, not the model. For SOG props the Pinnacle close is no sharper than the pick-time price (live LL 0.6863 vs 0.6860; backtest 0.6823 vs 0.6820), so CLV can't judge M6.
- Finding: on 1,168 live Pinnacle SOG lines (11-03..11-15) the M6 blend is slightly worse than Pinnacle (LL 0.6874 vs 0.6860); raw model worse on 11 of 13 days; outcome slope on (blend - Pinnacle) 0.05 (95% -0.45, 0.69; 1.0 = blend right). Model under-projects shots for lined players (2.18 vs 2.27). Backtest Oct 2025 was also the model's weakest month. Proposed (not adopted): judge M6 on blend-vs-Pinnacle log loss on the shadow board, not CLV.

## Pattern scan 2026-11-17 (`nhlpipe/patterns/`, report `data/patterns/report.md`)
- Observed vs expected (Pinnacle no-vig at pick time) on 1,326 games, 17k SOG lines, 20k points lines; discovery Oct-Jan 2025-26, untouched holdout Feb-Apr 2026, live 2026-27. 712 discovery tests, 0 survive BH (q 0.10); z-scores look like noise overall (KS p 0.84). No API credits used; leak spot checks passed.
- Evan's under rule (both D top third + both goalies GSAx >= 0, pre-specified): 67 games 2025-26, under 50.7% vs 50.1% priced, close didn't move -> no edge. Game totals: nothing.
- Held up out of sample: the shots model's disagreement with Pinnacle (trend z +3.6 discovery, +5.2 holdout) but only from December on (Oct/Nov z 0.7/1.5; live Nov 0.2). M6's flat November fits this.
- Consistent but too small to beat the margin: defencemen points Over 0.5 hit 2.6-4.7 pts above Pinnacle in all three samples; best US book still -2% ROI. Candidate for Kalshi resting (maker) orders.

## Next steps (in order)
1. Let the shadow board accumulate (every priced line graded nightly from 2026-11-04).
2. Build the combined model: inputs = fair price, M3 raw/blend, M6 mu/probability, sog_prob, backup-goalie flag, venue, market, line moves; train on shadow board + 2025-26 backtest tables (`data/shots2/lines.csv`, `data/backtest/m3eng/blend_rows.csv`); judge strictly out of sample vs the strongest single method on CLV and log loss. Add Bullseye inputs (prob, a_b2b, ev_xgd, fin; rebuildable from cached data via `bullseye_bt`). Away-b2b hypothesis H1 pre-registered 2026-11-05 (Evan approved; spec in `nhlpipe/hypotheses.py`, graded nightly into `data/hypotheses.md`, games from the 2026-11-05 slate on). 2026-12-31 is an interim look; a verdict needs ~400 games. Review 2026-12-31.
3. M3 totals bias - DONE 2026-11-03 (`data/backtest/m3eng/totals_report.md`): gap 0.27 goals/game = pull scale ~0.13 (PULL_SCALE 0.93 does not preserve the mean as intended) + goalie term ~0.06 + 2025-26 scoring above to-date average ~0.09. Fixing it gives no totals edge (blend weight on M3 still negative) -> no-totals rule stays. Mean-preserving scale adopted 2026-11-05 (Evan approved), live from the 2026-11-06 slate: `models.simulate` now solves the scale per game (`models.mean_scale`); `PULL_SCALE` kept only to reproduce older backtests (`simulate(..., scale=PULL_SCALE)`). Blend weights in `blend.json` were fit on the old scale; the report shows puck line/OT log loss moves < 0.001, so they were not refit.
4. Kalshi: paper-test resting limit orders at fair value (fill rate + CLV on filled orders only).
5. Keep weekly flaw reviews; never change pre-registered rules without Evan's approval.
