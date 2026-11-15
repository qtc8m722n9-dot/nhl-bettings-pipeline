# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-14. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 44 bets, CLV -3.7 pp, units +2.91
- B0_random: market = player_sog: 17 bets, CLV -5.5 pp, units -4.78
- B0_random: venue = underdog: 31 bets, CLV -4.7 pp, units -1.46
- B0_random: side_label = over: 50 bets, CLV -3.2 pp, units -0.05
- B0_random: side_label = under: 43 bets, CLV -2.8 pp, units +4.89
- B0_random: price_band = 45-55%: 26 bets, CLV -3.8 pp, units -10.02
- B0_random: price_band = 65-75%: 16 bets, CLV -3.0 pp, units -0.18
- M3_xg_model: predicted 73% in (0.7, 0.8] but hit 62% (16 bets)

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 2 | 0.0% | 48.7% | -2.00 | -3.0 |
| p1_result | 2 | 50.0% | 67.6% | -0.48 | -2.0 |
| p1_total | 4 | 50.0% | 42.9% | +1.13 | -0.9 |
| player_goals | 16 | 68.8% | 54.4% | +7.89 | -1.1 |
| player_points | 44 | 54.5% | 50.3% | +2.91 | -3.7 |
| player_sog | 17 | 41.2% | 54.4% | -4.78 | -5.5 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 12 | 33.3% | 44.6% | -2.32 | -0.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 63 | 49.2% | 49.9% | +1.63 | -1.9 |
| prizepicks | 4 | 75.0% | 57.7% | +1.20 | -7.3 |
| underdog | 31 | 48.4% | 53.1% | -1.46 | -4.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 5 | 20.0% | 61.2% | -3.48 | -2.8 |
| over | 50 | 40.0% | 42.8% | -0.05 | -3.2 |
| under | 43 | 65.1% | 59.9% | +4.89 | -2.8 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 22 | 36.4% | 25.1% | +7.80 | -1.8 |
| 35-45% | 10 | 50.0% | 41.3% | +2.37 | -2.6 |
| 45-55% | 26 | 30.8% | 49.5% | -10.02 | -3.8 |
| 55-65% | 14 | 71.4% | 60.3% | +2.71 | -4.8 |
| 65-75% | 16 | 68.8% | 69.8% | -0.18 | -3.0 |
| >75% | 10 | 70.0% | 80.7% | -1.32 | -1.1 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 98 | 50.0% | 51.2% | +1.37 | -3.0 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 8 | 100.0% | 84.9% | +1.42 | -0.6 |
| player_goals | 37 | 78.4% | 84.9% | -2.86 | -0.6 |
| player_points | 25 | 100.0% | 84.7% | +4.51 | -0.1 |
| spread | 10 | 80.0% | 84.6% | -0.54 | -0.9 |
| team_total | 13 | 69.2% | 84.6% | -2.38 | -1.7 |
| total | 14 | 85.7% | 84.9% | +0.14 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 107 | 85.0% | 84.8% | +0.29 | -0.6 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 10 | 80.0% | 84.6% | -0.54 | -0.9 |
| over | 21 | 85.7% | 84.9% | +0.20 | -0.5 |
| under | 76 | 85.5% | 84.8% | +0.63 | -0.6 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 107 | 85.0% | 84.8% | +0.29 | -0.6 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 107 | 85.0% | 84.8% | +0.29 | -0.6 |

## M1_sharp_price

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 1 | 39.3% | 100.0% |
| (0.4, 0.5] | 3 | 45.7% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 3 | 66.7% | 66.7% |
| (0.7, 0.8] | 7 | 73.2% | 71.4% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 3 | 33.3% | 39.0% | -0.11 | -1.9 |
| spread | 12 | 66.7% | 71.8% | -0.83 | -0.9 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 18 | 61.1% | 62.6% | -0.17 | -1.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 13 | 61.5% | 69.8% | -1.83 | -1.0 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 2 | 50.0% | 36.1% | +0.89 | -1.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 1 | 100.0% | 34.5% | +1.89 | +0.5 |
| 35-45% | 3 | 0.0% | 41.0% | -3.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 2 | 50.0% | 60.2% | -0.21 | -2.0 |
| 65-75% | 8 | 75.0% | 69.2% | +0.70 | -1.0 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 3 | 66.7% | 76.6% | -0.44 | +0.2 |
| 3-5% | 9 | 55.6% | 58.1% | -0.26 | -1.7 |
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
| (0.7, 0.8] | 16 | 73.3% | 62.5% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 8 | 12.5% | 39.1% | -5.11 | -1.9 |
| spread | 32 | 71.9% | 73.4% | -1.16 | -1.0 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 49 | 57.1% | 62.8% | -7.92 | -1.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 33 | 69.7% | 72.5% | -2.16 | -1.0 |
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
| 65-75% | 20 | 70.0% | 69.1% | +0.20 | -1.0 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 14 | 57.1% | 68.1% | -3.47 | -0.6 |
| 3-5% | 19 | 63.2% | 61.3% | -0.31 | -1.4 |
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
| (0.4, 0.5] | 21 | 46.1% | 52.4% |
| (0.5, 0.6] | 39 | 54.0% | 56.4% |
| (0.6, 0.7] | 28 | 65.4% | 71.4% |
| (0.7, 0.8] | 2 | 72.2% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 90 | 60.0% | 51.9% | +14.48 | +0.0 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 24 | 50.0% | 51.8% | -1.64 | -0.0 |
| betrivers | 5 | 60.0% | 48.9% | +1.15 | +0.8 |
| draftkings | 33 | 66.7% | 54.1% | +7.48 | -0.2 |
| espnbet | 22 | 54.5% | 49.6% | +3.35 | +0.5 |
| fanduel | 6 | 83.3% | 50.9% | +4.13 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 36 | 55.6% | 48.0% | +5.13 | +0.3 |
| under | 54 | 63.0% | 54.5% | +9.36 | -0.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 18 | 44.4% | 41.1% | +1.28 | -0.4 |
| 45-55% | 41 | 58.5% | 49.5% | +8.02 | +0.2 |
| 55-65% | 26 | 76.9% | 60.3% | +7.14 | +0.2 |
| 65-75% | 5 | 40.0% | 65.6% | -1.96 | -0.6 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 72 | 62.5% | 51.9% | +15.34 | -0.0 |
| 5-8% | 16 | 50.0% | 51.9% | -0.55 | +0.6 |
| >8% | 2 | 50.0% | 50.9% | -0.31 | -2.1 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 65.5% | Taylor Hall 3 sog |
| 2026-11-14 | John Carlson Under 2.5 shots | 69.6% | 65.5% | John Carlson 4 sog |
| 2026-11-10 | Noah Dobson Under 2.5 shots | 69.5% | 65.5% | Noah Dobson 3 sog |
| 2026-11-12 | Kent Johnson Under 2.5 shots | 68.3% | 64.3% | Kent Johnson 4 sog |
| 2026-11-07 | Vince Dunn Under 2.5 shots | 66.7% | 63.6% | Vince Dunn 6 sog |

## M6_shots_v2_pickem

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.5, 0.6] | 13 | 54.3% | 30.8% |
| (0.6, 0.7] | 3 | 61.7% | 66.7% |
| (0.7, 0.8] | 3 | 71.9% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 19 | 42.1% | 54.3% | -4.56 | -1.4 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| underdog | 19 | 42.1% | 54.3% | -4.56 | -1.4 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 6 | 33.3% | 52.5% | -2.16 | -0.7 |
| under | 13 | 46.2% | 55.1% | -2.39 | -1.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 13 | 30.8% | 50.5% | -5.07 | -1.3 |
| 55-65% | 3 | 66.7% | 58.3% | +0.46 | -2.4 |
| 65-75% | 3 | 66.7% | 66.3% | +0.05 | -0.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 16 | 37.5% | 53.3% | -4.61 | -1.4 |
| 5-8% | 3 | 66.7% | 59.4% | +0.05 | -1.4 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 67.7% | Taylor Hall 3 sog |
| 2026-11-10 | Blake Coleman Over 1.5 shots | 62.7% | 59.4% | Blake Coleman 1 sog |
| 2026-11-06 | Kiefer Sherwood Over 1.5 shots | 57.3% | 53.5% | Kiefer Sherwood 1 sog |
| 2026-11-07 | Jamie Benn Under 1.5 shots | 57.2% | 53.5% | Jamie Benn 3 sog |
| 2026-11-05 | Lane Hutson Under 1.5 shots | 56.9% | 53.5% | Lane Hutson 3 sog |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M6_shots_v2 | 90 | +0.03 (-0.5, +0.5) | 16.1% (2.8%, 29.8%) | undecided |
| C1_chalk | 107 | -0.58 (-1.0, -0.2) | 0.3% (-8.3%, 7.1%) | losing to the close |
| M3_xg_model | 49 | -1.11 (-1.5, -0.8) | -16.2% (-44.8%, 7.6%) | losing to the close |
| M2_goalie_news | 18 | -1.12 (-1.7, -0.3) | -1.0% (-49.2%, 43.7%) | losing to the close |
| M6_shots_v2_pickem | 19 | -1.41 (-2.6, +0.1) | -24.0% (-67.3%, 25.0%) | undecided |
| B0_random | 98 | -2.99 (-3.7, -2.4) | 1.4% (-12.5%, 15.2%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
