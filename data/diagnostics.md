# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-13. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 41 bets, CLV -3.7 pp, units -0.15
- B0_random: market = player_sog: 16 bets, CLV -5.6 pp, units -5.65
- B0_random: venue = kalshi: 51 bets, CLV -2.1 pp, units -0.68
- B0_random: venue = underdog: 29 bets, CLV -4.6 pp, units -3.52
- B0_random: side_label = over: 45 bets, CLV -3.4 pp, units -1.69
- B0_random: side_label = under: 35 bets, CLV -3.0 pp, units +1.16
- B0_random: price_band = 45-55%: 21 bets, CLV -3.9 pp, units -11.22
- M3_xg_model: predicted 73% in (0.7, 0.8] but hit 60% (15 bets)

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 1 | 0.0% | 48.7% | -1.00 | -2.9 |
| p1_result | 2 | 50.0% | 67.6% | -0.48 | -2.0 |
| p1_total | 3 | 33.3% | 37.9% | +0.40 | -0.5 |
| player_goals | 12 | 58.3% | 51.8% | +4.57 | -1.3 |
| player_points | 41 | 51.2% | 50.3% | -0.15 | -3.7 |
| player_sog | 16 | 37.5% | 54.5% | -5.65 | -5.6 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 8 | 37.5% | 41.7% | +0.30 | -0.7 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 51 | 45.1% | 48.7% | -0.68 | -2.1 |
| prizepicks | 4 | 75.0% | 57.7% | +1.20 | -7.3 |
| underdog | 29 | 44.8% | 53.4% | -3.52 | -4.6 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 4 | 25.0% | 64.3% | -2.48 | -2.7 |
| over | 45 | 37.8% | 41.9% | -1.69 | -3.4 |
| under | 35 | 60.0% | 60.5% | +1.16 | -3.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 20 | 35.0% | 25.1% | +6.62 | -1.9 |
| 35-45% | 10 | 50.0% | 41.3% | +2.37 | -2.6 |
| 45-55% | 21 | 23.8% | 49.7% | -11.22 | -3.9 |
| 55-65% | 11 | 72.7% | 60.8% | +2.25 | -5.6 |
| 65-75% | 13 | 61.5% | 69.4% | -1.38 | -3.7 |
| >75% | 9 | 66.7% | 81.3% | -1.64 | -1.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 84 | 46.4% | 50.7% | -3.00 | -3.2 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 7 | 100.0% | 84.9% | +1.24 | -0.4 |
| player_goals | 32 | 78.1% | 84.9% | -2.57 | -0.5 |
| player_points | 20 | 100.0% | 84.7% | +3.63 | -0.0 |
| spread | 8 | 87.5% | 84.7% | +0.27 | -0.6 |
| team_total | 13 | 69.2% | 84.6% | -2.38 | -1.7 |
| total | 13 | 84.6% | 84.9% | -0.04 | -0.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 93 | 84.9% | 84.8% | +0.15 | -0.5 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 8 | 87.5% | 84.7% | +0.27 | -0.6 |
| over | 20 | 85.0% | 84.9% | +0.03 | -0.4 |
| under | 65 | 84.6% | 84.8% | -0.14 | -0.6 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 93 | 84.9% | 84.8% | +0.15 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 93 | 84.9% | 84.8% | +0.15 | -0.5 |

## M1_sharp_price

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.4, 0.5] | 3 | 45.7% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 2 | 65.6% | 50.0% |
| (0.7, 0.8] | 6 | 73.2% | 66.7% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 2 | 0.0% | 41.2% | -2.00 | -3.0 |
| spread | 10 | 60.0% | 72.6% | -1.78 | -0.6 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 15 | 53.3% | 63.7% | -3.01 | -1.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 11 | 54.5% | 70.1% | -2.78 | -0.8 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 1 | 0.0% | 37.6% | -1.00 | -3.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 3 | 0.0% | 41.0% | -3.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 2 | 50.0% | 60.2% | -0.21 | -2.0 |
| 65-75% | 6 | 66.7% | 69.5% | -0.24 | -0.6 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 3 | 66.7% | 76.6% | -0.44 | +0.2 |
| 3-5% | 6 | 33.3% | 58.8% | -3.10 | -2.0 |
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
| (0.0, 0.4] | 4 | 30.2% | 0.0% |
| (0.4, 0.5] | 6 | 45.4% | 16.7% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 7 | 67.3% | 42.9% |
| (0.7, 0.8] | 15 | 73.3% | 60.0% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 7 | 0.0% | 39.7% | -7.00 | -2.3 |
| spread | 30 | 70.0% | 73.7% | -2.11 | -0.9 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 46 | 54.3% | 63.2% | -10.76 | -1.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 31 | 67.7% | 72.8% | -3.11 | -0.9 |
| over | 5 | 40.0% | 41.5% | -1.41 | -0.7 |
| under | 4 | 50.0% | 52.2% | -0.24 | -1.3 |
| yes / favourite side | 6 | 0.0% | 38.9% | -6.00 | -2.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 3 | 0.0% | 22.8% | -3.00 | -0.7 |
| 35-45% | 7 | 0.0% | 39.8% | -7.00 | -2.2 |
| 45-55% | 2 | 100.0% | 48.2% | +2.16 | -1.0 |
| 55-65% | 5 | 20.0% | 60.3% | -3.21 | -2.0 |
| 65-75% | 18 | 66.7% | 69.2% | -0.74 | -0.9 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 14 | 57.1% | 68.1% | -3.47 | -0.6 |
| 3-5% | 16 | 56.2% | 62.2% | -3.15 | -1.4 |
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
| (0.4, 0.5] | 18 | 46.2% | 55.6% |
| (0.5, 0.6] | 36 | 54.1% | 58.3% |
| (0.6, 0.7] | 20 | 65.1% | 75.0% |
| (0.7, 0.8] | 2 | 72.2% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 76 | 61.8% | 51.4% | +15.66 | -0.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 19 | 57.9% | 52.0% | +1.76 | -0.1 |
| betrivers | 5 | 60.0% | 48.9% | +1.15 | +0.8 |
| draftkings | 27 | 66.7% | 53.2% | +6.59 | -0.5 |
| espnbet | 20 | 55.0% | 48.6% | +3.61 | +0.2 |
| fanduel | 5 | 80.0% | 53.3% | +2.55 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 33 | 57.6% | 48.6% | +5.55 | +0.3 |
| under | 43 | 65.1% | 53.6% | +10.12 | -0.6 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 16 | 43.8% | 41.4% | +0.70 | -0.4 |
| 45-55% | 37 | 62.2% | 49.7% | +9.87 | +0.1 |
| 55-65% | 20 | 80.0% | 60.4% | +6.57 | -0.4 |
| 65-75% | 3 | 33.3% | 65.7% | -1.49 | -1.0 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 63 | 66.7% | 51.3% | +19.51 | -0.1 |
| 5-8% | 11 | 36.4% | 52.3% | -3.53 | +0.1 |
| >8% | 2 | 50.0% | 50.9% | -0.31 | -2.1 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 65.5% | Taylor Hall 3 sog |
| 2026-11-10 | Noah Dobson Under 2.5 shots | 69.5% | 65.5% | Noah Dobson 3 sog |
| 2026-11-12 | Kent Johnson Under 2.5 shots | 68.3% | 64.3% | Kent Johnson 4 sog |
| 2026-11-07 | Vince Dunn Under 2.5 shots | 66.7% | 63.6% | Vince Dunn 6 sog |
| 2026-11-12 | Charle-Edouard D'Astous Under 1.5 shots | 63.2% | 57.4% | Charle-Edouard D'Astous 3 sog |

## M6_shots_v2_pickem

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.5, 0.6] | 11 | 54.7% | 27.3% |
| (0.6, 0.7] | 3 | 61.7% | 66.7% |
| (0.7, 0.8] | 3 | 71.9% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 17 | 41.2% | 55.0% | -4.63 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| underdog | 17 | 41.2% | 55.0% | -4.63 | -1.5 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 6 | 33.3% | 52.5% | -2.16 | -0.7 |
| under | 11 | 45.5% | 56.3% | -2.47 | -1.9 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 11 | 27.3% | 50.9% | -5.14 | -1.4 |
| 55-65% | 3 | 66.7% | 58.3% | +0.46 | -2.4 |
| 65-75% | 3 | 66.7% | 66.3% | +0.05 | -0.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 14 | 35.7% | 54.0% | -4.68 | -1.5 |
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
| M6_shots_v2 | 76 | -0.17 (-0.7, +0.2) | 20.6% (5.5%, 34.3%) | undecided |
| C1_chalk | 93 | -0.54 (-1.0, -0.1) | 0.2% (-9.2%, 8.5%) | losing to the close |
| M3_xg_model | 46 | -1.10 (-1.5, -0.8) | -23.4% (-49.9%, -0.2%) | losing to the close |
| M2_goalie_news | 15 | -1.09 (-1.8, +0.0) | -20.1% (-62.7%, 20.6%) | undecided |
| M6_shots_v2_pickem | 17 | -1.47 (-2.7, +0.1) | -27.3% (-71.4%, 33.0%) | undecided |
| B0_random | 84 | -3.20 (-3.9, -2.6) | -3.6% (-15.6%, 9.2%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
