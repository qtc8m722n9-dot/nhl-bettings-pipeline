# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-17. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 48 bets, CLV -3.7 pp, units +2.87
- B0_random: market = player_sog: 24 bets, CLV -5.2 pp, units -4.24
- B0_random: venue = underdog: 39 bets, CLV -4.6 pp, units +0.10
- B0_random: side_label = over: 58 bets, CLV -3.2 pp, units -0.60
- B0_random: side_label = under: 51 bets, CLV -2.7 pp, units +3.81
- B0_random: price_band = 45-55%: 31 bets, CLV -3.8 pp, units -5.21
- B0_random: price_band = 55-65%: 19 bets, CLV -4.6 pp, units +1.02
- B0_random: price_band = 65-75%: 19 bets, CLV -3.1 pp, units -3.18
- M3_xg_model: predicted 73% in (0.7, 0.8] but hit 63% (19 bets)
- M6_shots_v2_pickem: predicted 55% in (0.5, 0.6] but hit 28% (18 bets)

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 4 | 25.0% | 49.5% | -1.71 | -2.7 |
| p1_result | 2 | 50.0% | 67.6% | -0.48 | -2.0 |
| p1_total | 5 | 60.0% | 46.6% | +1.75 | -1.3 |
| player_goals | 20 | 60.0% | 56.7% | +5.14 | -0.8 |
| player_points | 48 | 54.2% | 50.5% | +2.87 | -3.7 |
| player_sog | 24 | 45.8% | 55.5% | -4.24 | -5.2 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 12 | 33.3% | 44.6% | -2.32 | -0.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 73 | 47.9% | 51.1% | -1.28 | -1.9 |
| prizepicks | 4 | 75.0% | 57.7% | +1.20 | -7.3 |
| underdog | 39 | 51.3% | 53.9% | +0.10 | -4.6 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 7 | 28.6% | 58.1% | -3.19 | -2.7 |
| over | 58 | 41.4% | 44.6% | -0.60 | -3.2 |
| under | 51 | 62.7% | 60.2% | +3.81 | -2.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 23 | 34.8% | 25.2% | +6.80 | -1.7 |
| 35-45% | 12 | 50.0% | 41.1% | +2.66 | -2.6 |
| 45-55% | 31 | 41.9% | 49.8% | -5.21 | -3.8 |
| 55-65% | 19 | 63.2% | 60.4% | +1.02 | -4.6 |
| 65-75% | 19 | 57.9% | 69.8% | -3.18 | -3.1 |
| >75% | 12 | 66.7% | 81.0% | -2.07 | -0.8 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 116 | 50.0% | 52.3% | +0.02 | -3.0 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 9 | 100.0% | 84.9% | +1.60 | -0.7 |
| player_goals | 44 | 79.5% | 84.9% | -2.79 | -0.3 |
| player_points | 29 | 93.1% | 84.7% | +2.87 | +0.3 |
| spread | 11 | 81.8% | 84.6% | -0.36 | -1.0 |
| team_total | 13 | 69.2% | 84.6% | -2.38 | -1.7 |
| total | 18 | 88.9% | 84.8% | +0.86 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 124 | 84.7% | 84.8% | -0.21 | -0.4 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 11 | 81.8% | 84.6% | -0.36 | -1.0 |
| over | 22 | 86.4% | 84.9% | +0.38 | -0.6 |
| under | 91 | 84.6% | 84.8% | -0.23 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 124 | 84.7% | 84.8% | -0.21 | -0.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 124 | 84.7% | 84.8% | -0.21 | -0.4 |

## M1_sharp_price

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 1 | 39.3% | 100.0% |
| (0.4, 0.5] | 3 | 45.7% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 3 | 66.7% | 66.7% |
| (0.7, 0.8] | 8 | 73.6% | 75.0% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 3 | 33.3% | 39.0% | -0.11 | -1.9 |
| spread | 13 | 69.2% | 71.9% | -0.45 | -1.0 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 19 | 63.2% | 63.1% | +0.21 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 14 | 64.3% | 70.0% | -1.45 | -1.1 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 2 | 50.0% | 36.1% | +0.89 | -1.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 1 | 100.0% | 34.5% | +1.89 | +0.5 |
| 35-45% | 3 | 0.0% | 41.0% | -3.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 2 | 50.0% | 60.2% | -0.21 | -2.0 |
| 65-75% | 9 | 77.8% | 69.5% | +1.08 | -1.1 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 3 | 66.7% | 76.6% | -0.44 | +0.2 |
| 3-5% | 10 | 60.0% | 59.6% | +0.12 | -1.8 |
| 5-8% | 5 | 60.0% | 59.6% | +0.20 | -0.9 |
| >8% | 1 | 100.0% | 75.3% | +0.33 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-12 | TBL not to win by 2+ | 74.1% | 71.5% | TBL 3-1 CBJ |
| 2026-11-09 | PHI not to win by 2+ | 70.7% | 67.6% | PHI 3-1 VAN |
| 2026-11-09 | EDM not to win by 2+ | 68.0% | 64.6% | NYR 1-3 EDM |
| 2026-11-05 | VGK NOT to win | 48.7% | 44.7% | VGK 2-1 DET |

## M3_xg_model

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 5 | 32.0% | 20.0% |
| (0.4, 0.5] | 6 | 45.4% | 16.7% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 8 | 67.5% | 50.0% |
| (0.7, 0.8] | 19 | 73.2% | 63.2% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 8 | 12.5% | 39.1% | -5.11 | -1.9 |
| spread | 35 | 71.4% | 73.0% | -1.33 | -0.9 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 52 | 57.7% | 63.2% | -8.08 | -1.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 36 | 69.4% | 72.2% | -2.33 | -1.0 |
| over | 5 | 40.0% | 41.5% | -1.41 | -0.7 |
| under | 4 | 50.0% | 52.2% | -0.24 | -1.3 |
| yes / favourite side | 7 | 14.3% | 38.3% | -4.11 | -1.8 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 4 | 25.0% | 25.8% | -1.11 | -0.4 |
| 35-45% | 7 | 0.0% | 39.8% | -7.00 | -2.2 |
| 45-55% | 2 | 100.0% | 48.2% | +2.16 | -1.0 |
| 55-65% | 5 | 20.0% | 60.3% | -3.21 | -2.0 |
| 65-75% | 23 | 69.6% | 69.1% | +0.04 | -1.0 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 15 | 53.3% | 68.0% | -4.47 | -0.6 |
| 3-5% | 21 | 66.7% | 62.2% | +0.53 | -1.3 |
| 5-8% | 10 | 60.0% | 58.2% | -0.87 | -1.1 |
| >8% | 6 | 33.3% | 62.6% | -3.27 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-10-31 | OTT not to win by 2+ | 74.7% | 66.6% | OTT 5-1 SJS |
| 2026-11-12 | TBL not to win by 2+ | 74.1% | 71.5% | TBL 3-1 CBJ |
| 2026-11-07 | MTL not to win by 2+ | 72.1% | 69.5% | MTL 4-2 TOR |
| 2026-11-11 | TBL not to win by 2+ | 71.5% | 68.6% | TBL 8-3 BUF |

## M4_shots_model

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.6, 0.7] | 10 | 64.4% | 50.0% |
| (0.8, 1.0] | 1 | 82.5% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 11 | 54.5% | 57.1% | -0.73 | -5.8 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 6 | 66.7% | 57.8% | +0.92 | -8.9 |
| underdog | 5 | 40.0% | 56.3% | -1.65 | -2.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 1 | 100.0% | 57.8% | +0.73 | -7.0 |
| under | 10 | 50.0% | 57.0% | -1.46 | -5.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 4 | 25.0% | 53.5% | -2.13 | -3.1 |
| 55-65% | 6 | 66.7% | 57.8% | +0.92 | -8.9 |
| 65-75% | 1 | 100.0% | 67.7% | +0.48 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 2 | 100.0% | 57.8% | +1.46 | -10.9 |
| 5-8% | 6 | 16.7% | 55.6% | -4.27 | -6.1 |
| >8% | 3 | 100.0% | 59.6% | +2.08 | -3.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-01 | Cutter Gauthier Under 3.5 shots | 64.0% | 57.8% | Cutter Gauthier 5 sog |
| 2026-11-01 | Adam Fox Under 1.5 shots | 63.9% | 57.8% | Adam Fox 2 sog |
| 2026-10-31 | David Pastrnak Under 3.5 shots | 63.8% | 53.5% | David Pastrnak 4 sog |
| 2026-10-31 | Dylan Cozens Under 2.5 shots | 63.8% | 53.5% | Dylan Cozens 5 sog |
| 2026-11-02 | Sam Malinski Under 1.5 shots | 63.3% | 53.5% | Sam Malinski 2 sog |

## M6_shots_v2

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.4, 0.5] | 26 | 46.2% | 46.2% |
| (0.5, 0.6] | 51 | 54.4% | 52.9% |
| (0.6, 0.7] | 43 | 65.2% | 67.4% |
| (0.7, 0.8] | 2 | 72.2% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 122 | 56.6% | 52.5% | +9.57 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 26 | 46.2% | 52.2% | -3.64 | -0.1 |
| betrivers | 7 | 57.1% | 50.2% | +0.92 | +0.5 |
| draftkings | 47 | 66.0% | 54.0% | +9.75 | -0.2 |
| espnbet | 30 | 50.0% | 51.0% | +0.67 | +0.2 |
| fanduel | 12 | 58.3% | 52.4% | +1.86 | -1.0 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 45 | 53.3% | 48.5% | +3.54 | +0.4 |
| under | 77 | 58.4% | 54.9% | +6.03 | -0.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 22 | 40.9% | 41.2% | -0.42 | -0.3 |
| 45-55% | 52 | 53.8% | 49.8% | +5.00 | +0.1 |
| 55-65% | 43 | 69.8% | 60.1% | +6.95 | -0.1 |
| 65-75% | 5 | 40.0% | 65.6% | -1.96 | -0.6 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 98 | 59.2% | 52.5% | +12.45 | -0.2 |
| 5-8% | 21 | 47.6% | 52.4% | -1.57 | +0.4 |
| >8% | 3 | 33.3% | 53.1% | -1.31 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 65.5% | Taylor Hall 3 sog |
| 2026-11-14 | John Carlson Under 2.5 shots | 69.6% | 65.5% | John Carlson 4 sog |
| 2026-11-10 | Noah Dobson Under 2.5 shots | 69.5% | 65.5% | Noah Dobson 3 sog |
| 2026-11-12 | Kent Johnson Under 2.5 shots | 68.3% | 64.3% | Kent Johnson 4 sog |
| 2026-11-15 | Mavrik Bourque Under 2.5 shots | 68.1% | 62.3% | Mavrik Bourque 3 sog |

## M6_shots_v2_pickem

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.5, 0.6] | 18 | 54.8% | 27.8% |
| (0.6, 0.7] | 6 | 63.1% | 66.7% |
| (0.7, 0.8] | 3 | 71.9% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 27 | 40.7% | 54.4% | -7.17 | -1.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| underdog | 27 | 40.7% | 54.4% | -7.17 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 8 | 37.5% | 53.5% | -2.48 | -0.9 |
| under | 19 | 42.1% | 54.8% | -4.69 | -1.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 18 | 27.8% | 50.8% | -8.05 | -1.2 |
| 55-65% | 6 | 66.7% | 59.4% | +0.83 | -1.3 |
| 65-75% | 3 | 66.7% | 66.3% | +0.05 | -0.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 22 | 40.9% | 53.6% | -5.22 | -1.3 |
| 5-8% | 5 | 40.0% | 58.2% | -1.95 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 67.7% | Taylor Hall 3 sog |
| 2026-11-15 | Mavrik Bourque Under 2.5 shots | 68.1% | 62.9% | Mavrik Bourque 3 sog |
| 2026-11-10 | Blake Coleman Over 1.5 shots | 62.7% | 59.4% | Blake Coleman 1 sog |
| 2026-11-17 | Jack Roslovic Under 2.5 shots | 58.1% | 53.5% | Jack Roslovic 3 sog |
| 2026-11-06 | Kiefer Sherwood Over 1.5 shots | 57.3% | 53.5% | Kiefer Sherwood 1 sog |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M6_shots_v2 | 122 | -0.10 (-0.5, +0.3) | 7.8% (-4.3%, 21.5%) | undecided |
| C1_chalk | 124 | -0.38 (-0.8, +0.0) | -0.2% (-8.1%, 6.4%) | undecided |
| M3_xg_model | 52 | -1.10 (-1.4, -0.8) | -15.5% (-42.1%, 10.1%) | losing to the close |
| M2_goalie_news | 19 | -1.17 (-1.7, -0.3) | 1.1% (-43.1%, 44.8%) | losing to the close |
| M6_shots_v2_pickem | 27 | -1.18 (-2.1, -0.1) | -26.6% (-58.7%, 10.1%) | losing to the close |
| B0_random | 116 | -2.98 (-3.7, -2.5) | 0.0% (-13.5%, 12.6%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
