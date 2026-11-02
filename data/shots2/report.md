# Shots model v2 backtest

## 1. Validation (fit 2023-24, score 2024-25 skater-games)

| Model | NB log score / game | Poisson dev. | Mean pred | Mean actual |
|---|--:|--:|--:|--:|
| v2 glm (alpha 0.047) | -1.5428 | 1.2275 | 1.651 | 1.572 |
| v2 hgb (alpha 0.041) | -1.5435 | 1.2286 | 1.643 | 1.572 |
| old M4 formula (Poisson) | -1.5562 | – | 1.594 | 1.572 |

Kept: **glm** (higher log score is better).

GLM effects (per 1 SD of each input, multiplicative on expected shots):

| Input | Effect |
|---|--:|
| log_mu_base | +12.6% |
| ev_toi | -6.2% |
| on_net | -4.8% |
| log_opp_sa | +4.3% |
| toi_jump | +2.5% |
| F | -2.0% |
| xg_edge | +1.7% |
| b2b | -1.6% |
| rest_days | -1.4% |
| home | +1.4% |
| opp_b2b | +1.4% |
| pp_toi | -1.2% |
| log_team_ca | -1.1% |
| road_trip | -0.9% |
| pp_jump | +0.7% |
| tz_shift | +0.7% |
| log_n_prior | +0.6% |
| pp_att60 | -0.5% |
| opp_rest_days | +0.5% |
| h2h_resid | +0.4% |
| ev_att60 | -0.4% |
| missing_toi | -0.3% |
| log_opp_pen | +0.2% |
| traded | +0.1% |
| sh_toi | -0.0% |
| oz_start | +0.0% |

## 2. Test season 2025-26: every skater-game

- skater-games: 47,110
- NB log score per game: v2 -1.5317 vs old M4 -1.5461 (higher is better; difference +0.0144)
- mean predicted 1.541 vs actual 1.547

## 3. Every Pinnacle-priced SOG line at pick time (2025-26)

- lines: 16,267 (98% of Pinnacle lines matched to a skater-game); with a Pinnacle close: 15,786

| Forecast | Log loss (lower = better) | Brier |
|---|--:|--:|
| old M4 formula | 0.6874 | 0.2470 |
| v2 model | 0.6806 | 0.2438 |
| Pinnacle at 1:50 PM | 0.6820 | 0.2445 |
| Pinnacle close (subset n=15,786) | 0.6823 | 0.2446 |

Calibration of v2 (all lines):

| Predicted bin | n | Avg predicted | Actual over rate |
|---|--:|--:|--:|
| (0.0, 0.2] | 44 | 0.172 | 0.159 |
| (0.2, 0.3] | 100 | 0.271 | 0.370 |
| (0.3, 0.4] | 2236 | 0.367 | 0.387 |
| (0.4, 0.5] | 5724 | 0.453 | 0.464 |
| (0.5, 0.6] | 6440 | 0.548 | 0.557 |
| (0.6, 0.7] | 1718 | 0.624 | 0.623 |
| (0.7, 0.8] | 5 | 0.711 | 0.800 |

Encompassing test, outcome ~ a·logit(Pinnacle) + b·logit(v2):

- a (Pinnacle) = 0.357, **b (v2) = 0.651 (95% CI 0.500 to 0.803)**
- b > 0 with a CI above 0 means v2 knows something Pinnacle's 1:50 PM price doesn't.

## 4. Bets

Rule: edge ≥ 3% and ≤ 12%, best price per player, up to 3 players per game. Blend weights fit on Oct–Dec 2025 only, then frozen. Win % should be compared with the breakeven (avg cost).

| Strategy | Bets | Win % | Breakeven | ROI (95% CI) | CLV vs Pinnacle close, pp (95% CI) | Beat close | Bets/game |
|---|--:|--:|--:|--:|--:|--:|--:|
| v2 blended with Pinnacle, Jan–Apr (out of sample) | 495 | 54.7% | 53.4% | +3.0% (-6.3%, +11.4%) | -1.39 (-1.65, -1.13) | 21% | 1.61 |
|   …pick'em apps only | 9 | 77.8% | 57.8% | +34.6% (-23.1%, +73.0%) | -7.77 (+nan, +nan) | 0% | 1.00 |
| v2 pure model, Jan–Apr | 1451 | 52.6% | 50.6% | +3.4% (-1.5%, +8.2%) | -2.14 (-2.27, -2.00) | 11% | 2.41 |
| v2 pure model, full season | 2493 | 52.6% | 50.9% | +3.1% (-0.7%, +7.0%) | -2.01 (-2.10, -1.92) | 12% | 2.29 |

By side (blended, Jan–Apr):

| Side | Bets | Win % | ROI |
|---|--:|--:|--:|
| over | 22.0 | 45.5% | -17.9% |
| under | 473.0 | 55.2% | +4.0% |

## Leak checks

- every feature is built from games on earlier dates only (decayed sums exclude the current row; schedule features use only the schedule); model fit on 2023-24 / 2024-25 only
- Pinnacle pick-time prices are the 13:50 ET snapshot; close is ~2 min before each game
- blend weights fit on 2025-10-15–2025-12-31 and graded from 2026-01-01

