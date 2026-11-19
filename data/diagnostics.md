# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-18. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 50 bets, CLV -3.6 pp, units +2.23
- B0_random: market = player_sog: 24 bets, CLV -5.2 pp, units -4.24
- B0_random: venue = underdog: 40 bets, CLV -4.7 pp, units +0.47
- B0_random: side_label = over: 58 bets, CLV -3.2 pp, units -0.60
- B0_random: side_label = under: 53 bets, CLV -2.7 pp, units +3.17
- B0_random: price_band = 45-55%: 31 bets, CLV -3.8 pp, units -5.21
- B0_random: price_band = 55-65%: 19 bets, CLV -4.6 pp, units +1.02
- B0_random: price_band = 65-75%: 21 bets, CLV -3.3 pp, units -2.45
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
| player_points | 50 | 54.0% | 51.5% | +2.23 | -3.6 |
| player_sog | 24 | 45.8% | 55.5% | -4.24 | -5.2 |
| spread | 2 | 50.0% | 73.4% | -0.64 | -2.7 |
| team_total | 12 | 33.3% | 44.6% | -2.32 | -0.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 75 | 48.0% | 51.8% | -1.92 | -1.8 |
| prizepicks | 4 | 75.0% | 57.7% | +1.20 | -7.3 |
| underdog | 40 | 52.5% | 54.4% | +0.47 | -4.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 8 | 37.5% | 60.0% | -2.83 | -2.6 |
| over | 58 | 41.4% | 44.6% | -0.60 | -3.2 |
| under | 53 | 62.3% | 60.8% | +3.17 | -2.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 23 | 34.8% | 25.2% | +6.80 | -1.7 |
| 35-45% | 12 | 50.0% | 41.1% | +2.66 | -2.6 |
| 45-55% | 31 | 41.9% | 49.8% | -5.21 | -3.8 |
| 55-65% | 19 | 63.2% | 60.4% | +1.02 | -4.6 |
| 65-75% | 21 | 61.9% | 70.2% | -2.45 | -3.3 |
| >75% | 13 | 61.5% | 80.9% | -3.07 | -0.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 119 | 50.4% | 52.8% | -0.26 | -2.9 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 10 | 100.0% | 84.9% | +1.77 | -0.6 |
| player_goals | 44 | 79.5% | 84.9% | -2.79 | -0.3 |
| player_points | 31 | 93.5% | 84.8% | +3.22 | +0.2 |
| spread | 11 | 81.8% | 84.6% | -0.36 | -1.0 |
| team_total | 13 | 69.2% | 84.6% | -2.38 | -1.7 |
| total | 18 | 88.9% | 84.8% | +0.86 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 127 | 85.0% | 84.8% | +0.32 | -0.4 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 11 | 81.8% | 84.6% | -0.36 | -1.0 |
| over | 23 | 87.0% | 84.9% | +0.56 | -0.5 |
| under | 93 | 84.9% | 84.8% | +0.13 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 127 | 85.0% | 84.8% | +0.32 | -0.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 127 | 85.0% | 84.8% | +0.32 | -0.4 |

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
| (0.4, 0.5] | 27 | 46.2% | 44.4% |
| (0.5, 0.6] | 52 | 54.5% | 51.9% |
| (0.6, 0.7] | 44 | 65.2% | 68.2% |
| (0.7, 0.8] | 2 | 72.2% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 125 | 56.0% | 52.5% | +8.19 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 28 | 46.4% | 52.6% | -4.01 | -0.0 |
| betrivers | 7 | 57.1% | 50.2% | +0.92 | +0.5 |
| draftkings | 48 | 64.6% | 53.8% | +8.75 | -0.2 |
| espnbet | 30 | 50.0% | 51.0% | +0.67 | +0.2 |
| fanduel | 12 | 58.3% | 52.4% | +1.86 | -1.0 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 46 | 52.2% | 48.6% | +2.54 | +0.3 |
| under | 79 | 58.2% | 54.8% | +5.65 | -0.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 23 | 39.1% | 41.3% | -1.42 | -0.5 |
| 45-55% | 53 | 52.8% | 49.9% | +4.00 | +0.1 |
| 55-65% | 44 | 70.5% | 60.1% | +7.58 | -0.1 |
| 65-75% | 5 | 40.0% | 65.6% | -1.96 | -0.6 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 100 | 58.0% | 52.4% | +10.45 | -0.2 |
| 5-8% | 22 | 50.0% | 52.8% | -0.94 | +0.4 |
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

## M7_shots_under_early

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 1 | 100.0% | 51.2% | +0.95 | -4.0 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| espnbet | 1 | 100.0% | 51.2% | +0.95 | -4.0 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| under | 1 | 100.0% | 51.2% | +0.95 | -4.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 1 | 100.0% | 51.2% | +0.95 | -4.0 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 1 | 100.0% | 51.2% | +0.95 | -4.0 |

## M8_scorer_price

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 5 | 13.8% | 40.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 5 | 40.0% | 10.2% | +16.97 | -0.7 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 5 | 40.0% | 10.2% | +16.97 | -0.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 5 | 40.0% | 10.2% | +16.97 | -0.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 5 | 40.0% | 10.2% | +16.97 | -0.7 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 5 | 40.0% | 10.2% | +16.97 | -0.7 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-18 | Cody Glass Over 0.5 goals | 16.0% | 12.7% | Cody Glass 0 goals |
| 2026-11-18 | Carter Mazur Over 0.5 goals | 13.9% | 9.6% | Carter Mazur 0 goals |
| 2026-11-18 | Sheldon Dries Over 0.5 goals | 13.3% | 9.6% | Sheldon Dries 0 goals |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M6_shots_v2 | 125 | -0.12 (-0.5, +0.2) | 6.6% (-5.5%, 20.5%) | undecided |
| C1_chalk | 127 | -0.38 (-0.8, +0.0) | 0.3% (-7.5%, 6.6%) | undecided |
| M3_xg_model | 52 | -1.10 (-1.4, -0.8) | -15.5% (-42.1%, 10.1%) | losing to the close |
| M2_goalie_news | 19 | -1.17 (-1.7, -0.3) | 1.1% (-43.1%, 44.8%) | losing to the close |
| M6_shots_v2_pickem | 27 | -1.18 (-2.1, -0.1) | -26.6% (-58.7%, 10.1%) | losing to the close |
| B0_random | 119 | -2.94 (-3.6, -2.4) | -0.2% (-12.2%, 12.7%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
| M7_shots_under_early | 1 | -4.01 (–, –) | 95.2% (–, –) | undecided |
| M8_scorer_price | 5 | -0.70 (–, –) | 339.4% (–, –) | undecided |
