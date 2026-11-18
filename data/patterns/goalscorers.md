# H21 Goalscorer models: price-driven (P) vs price-blind (B)

Run 2026-11-18 by `python -m nhlpipe.patterns.scorer`. Spec: `docs/hypotheses_2026-11-18_goalscorers.md` (committed before the data was bought or looked at). P(score) = chance of at least one goal.

**Model P** uses Pinnacle's game total and moneyline for each team's expected goals, times the player's share. **Model B** never sees a betting price: shots-rate x shooting % baseline plus game factors, fitted on 2022-23 to 2024-25.

## 1. Accuracy on the same player-games (log loss, lower = better)

| Sample | Player-games | Pinnacle no-vig | Model P | Model B | Actual scoring rate | Avg Pinnacle | Avg P | Avg B |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| 2025-26 | 15,322 | 0.5646 | 0.5625 | 0.5616 | 26.1% | 23.2% | 26.0% | 25.6% |
| 2026-27 live | 1,340 | 0.5551 | 0.5554 | 0.5546 | 25.2% | 25.0% | 26.5% | 27.1% |

Without the price filter (every skater-game the models can score, 2025-26 and live):

| Sample | Player-games | Model P | Model B |
|---|--:|--:|--:|
| 2025-26 | 43,280 | 0.3943 | 0.3920 |
| 2026-27 live | 4,223 | 0.3947 | 0.3933 |

## 2. Calibration (2025-26 + live, priced player-games)

| Predicted band | Model P n / actual | Model B n / actual | Pinnacle n / actual |
|---|--:|--:|--:|
| 0%-10% | 14 / 14.3% | 18 / 11.1% | 28 / 14.3% |
| 10%-15% | 123 / 16.3% | 405 / 16.8% | 2,623 / 17.6% |
| 15%-20% | 2,655 / 17.7% | 3,992 / 18.4% | 4,220 / 21.2% |
| 20%-25% | 5,481 / 22.2% | 4,416 / 22.9% | 3,494 / 24.5% |
| 25%-30% | 4,224 / 26.9% | 3,358 / 28.3% | 2,710 / 30.2% |
| 30%-35% | 2,531 / 33.3% | 2,298 / 31.6% | 1,982 / 33.4% |
| 35%-45% | 1,579 / 39.1% | 1,935 / 38.0% | 1,463 / 39.4% |
| 45%-100% | 55 / 40.0% | 240 / 43.8% | 142 / 43.0% |

## 3. Single legs: model P(score) at least 3 pts above the price (YES)

| Model | Sample | Venue | Legs | Hit | Avg cost | ROI | Edge vs Pinnacle fair, pts (z) |
|---|---|---|--:|--:|--:|--:|--:|
| Model P | 2025-26 | best US book | 1,647 | 22.3% | 21.6% | +3.8% | +4.4 (+4.02) |
| Model P | 2026-27 live | best US book | 76 | 27.6% | 22.3% | +29.4% | +8.4 (+1.89) |
| Model P | 2026-27 live | Kalshi (ask + fee) | 407 | 15.0% | 14.4% | +2.4% | +5.0 (+1.15) |
| Model B | 2025-26 | best US book | 912 | 29.5% | 27.2% | +11.2% | +5.1 (+3.32) |
| Model B | 2026-27 live | best US book | 144 | 31.2% | 32.7% | -1.3% | +0.8 (+0.21) |
| Model B | 2026-27 live | Kalshi (ask + fee) | 155 | 27.1% | 28.6% | -5.1% | -0.4 (-0.10) |

Primary comparison (pre-registered): edge vs Pinnacle fair of each model's single legs on 2025-26, one-sided p:

- Model P: +4.37 pts over 1,647 legs, z +4.02, p = 0.000 -> beats Pinnacle
- Model B: +5.11 pts over 912 legs, z +3.32, p = 0.000 -> beats Pinnacle

## 4. Paper parlays: each night the 3 biggest-edge legs from different games (best US-book price)

| Model | Sample | Nights | Hit (all 3) | Avg payout (x stake) | ROI |
|---|---|--:|--:|--:|--:|
| Model P | 2025-26 | 126 | 1.6% | 135.4 | +100.1% |
| Model P | 2026-27 live | 8 | 0.0% | 151.7 | -100.0% |
| Model B | 2025-26 | 96 | 3.1% | 61.8 | +24.4% |
| Model B | 2026-27 live | 10 | 0.0% | 26.1 | -100.0% |

## 5. Model B: which factors matter

Coefficient = change in log scoring rate per 1 standard deviation (beyond the shots x shooting % baseline), fit 2022-25. Drop = how much worse 2025-26 log loss gets when the factor is removed and the model refit (x 10,000; bigger = more important).

| Factor | Coefficient | SE | Drop |
|---|--:|--:|--:|
| ev_toi | +0.061 | 0.012 | +1.1 |
| pp_toi | +0.094 | 0.008 | +4.7 |
| D | -0.017 | 0.012 | -0.1 |
| home | +0.032 | 0.007 | +0.5 |
| b2b | -0.027 | 0.007 | +0.6 |
| opp_b2b | +0.023 | 0.007 | -0.3 |
| opp_xga_pg | +0.086 | 0.006 | +1.8 |
| opp_save_pg | -0.029 | 0.006 | +0.1 |
| team_xgf_pg | +0.011 | 0.006 | +0.2 |
| opp_pen_ratio | -0.008 | 0.007 | -0.1 |
| log_n_prior | +0.007 | 0.007 | +0.2 |
| (intercept vs baseline) | -0.093 | 0.008 | |

## 6. Caveat found after the run: the de-vig method flatters both models

Pinnacle's anytime-goal market is lopsided (YES +150 to +400, NO heavily odds-on). Our standard power de-vig moves
too much of the margin onto the YES side: on 2025-26 it says 23.2% while players actually scored 26.1% of the time,
and Pinnacle's raw YES price (margin included) was 27.7%. Simple proportional ("multiplicative") de-vig gives 25.9%
and the better log loss (0.5615 vs 0.5646). Against that fairer reference the single-leg edges shrink:

| Model | Legs (2025-26) | Edge vs power fair (registered) | Edge vs multiplicative fair | ROI at best US book (95% CI by slate) | Same legs at Pinnacle's own YES price |
|---|--:|--:|--:|--:|--:|
| P (price-driven) | 1,647 | +4.4 pts (z 4.0) | +1.1 pts (z 1.0) | +3.8% (-5.3%, +14.0%) | -1.2% |
| B (price-blind) | 912 | +5.1 pts (z 3.3) | +2.5 pts (z 1.65) | +11.2% (+0.9%, +21.3%) | +5.0% |

Baseline: buying EVERY anytime-goal YES at the best US book lost 2.7%; at Pinnacle 5.8%.
Reading: Model B (no prices) matches Pinnacle's accuracy (log loss 0.5616 vs 0.5615) and its legs made money at the
best book price, but only October 2025 was large (+47% on 125 legs); without it the months range -3% to +19%.
Parlay results (2 and 3 hits out of 96-126 nights) are noise. Live paper test from 2026-11-19: M8_scorer_price
(Model P) and M9_scorer_blind (Model B) on Kalshi, verdict at 300 legs each.
Separate proposal (not adopted): use multiplicative de-vig for anytime-goal / player-goals markets in `nhlpipe/fair.py`;
today's power de-vig understates YES and so overstates the fair price of the NO side that C1 buys on Kalshi.
