# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-19. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 56 bets, CLV -3.5 pp, units -0.31
- B0_random: market = player_sog: 27 bets, CLV -5.5 pp, units -5.56
- B0_random: venue = underdog: 45 bets, CLV -4.8 pp, units -1.22
- B0_random: side_label = over: 62 bets, CLV -3.2 pp, units -4.60
- B0_random: side_label = under: 61 bets, CLV -2.9 pp, units +0.31
- B0_random: price_band = 45-55%: 36 bets, CLV -3.8 pp, units -8.38
- B0_random: price_band = 55-65%: 22 bets, CLV -4.9 pp, units +1.33
- B0_random: price_band = 65-75%: 23 bets, CLV -3.1 pp, units -4.45
- M6_shots_v2_pickem: predicted 55% in (0.5, 0.6] but hit 26% (19 bets)

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 4 | 25.0% | 49.5% | -1.71 | -2.7 |
| p1_result | 2 | 50.0% | 67.6% | -0.48 | -2.0 |
| p1_total | 5 | 60.0% | 46.6% | +1.75 | -1.3 |
| player_goals | 23 | 52.2% | 54.9% | +2.14 | -0.8 |
| player_points | 56 | 51.8% | 52.0% | -0.31 | -3.5 |
| player_sog | 27 | 44.4% | 55.6% | -5.56 | -5.5 |
| spread | 2 | 50.0% | 73.4% | -0.64 | -2.7 |
| team_total | 12 | 33.3% | 44.6% | -2.32 | -0.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 81 | 45.7% | 51.6% | -6.09 | -1.8 |
| prizepicks | 5 | 60.0% | 57.7% | +0.20 | -7.3 |
| underdog | 45 | 51.1% | 54.5% | -1.22 | -4.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 8 | 37.5% | 60.0% | -2.83 | -2.6 |
| over | 62 | 38.7% | 44.3% | -4.60 | -3.2 |
| under | 61 | 59.0% | 60.6% | +0.31 | -2.9 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 24 | 33.3% | 25.1% | +5.80 | -1.6 |
| 35-45% | 13 | 46.2% | 40.7% | +1.66 | -2.5 |
| 45-55% | 36 | 38.9% | 50.1% | -8.38 | -3.8 |
| 55-65% | 22 | 63.6% | 60.3% | +1.33 | -4.9 |
| 65-75% | 23 | 56.5% | 70.0% | -4.45 | -3.1 |
| >75% | 13 | 61.5% | 80.9% | -3.07 | -0.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 131 | 48.1% | 52.8% | -7.12 | -3.0 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 11 | 100.0% | 84.9% | +1.95 | -0.5 |
| player_goals | 46 | 78.3% | 84.9% | -3.62 | -0.2 |
| player_points | 37 | 91.9% | 84.8% | +3.11 | +0.2 |
| spread | 13 | 84.6% | 84.6% | -0.01 | -0.9 |
| team_total | 14 | 71.4% | 84.7% | -2.20 | -1.6 |
| total | 18 | 88.9% | 84.8% | +0.86 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 139 | 84.9% | 84.8% | +0.09 | -0.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 13 | 84.6% | 84.6% | -0.01 | -0.9 |
| over | 25 | 88.0% | 84.9% | +0.91 | -0.5 |
| under | 101 | 84.2% | 84.8% | -0.81 | -0.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 139 | 84.9% | 84.8% | +0.09 | -0.3 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 139 | 84.9% | 84.8% | +0.09 | -0.3 |

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
| (0.7, 0.8] | 20 | 73.4% | 65.0% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 8 | 12.5% | 39.1% | -5.11 | -1.9 |
| spread | 36 | 72.2% | 73.0% | -0.96 | -1.0 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 53 | 58.5% | 63.4% | -7.72 | -1.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 37 | 70.3% | 72.3% | -1.96 | -1.0 |
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
| 65-75% | 24 | 70.8% | 69.3% | +0.40 | -1.0 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 15 | 53.3% | 68.0% | -4.47 | -0.6 |
| 3-5% | 22 | 68.2% | 62.7% | +0.89 | -1.4 |
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
| (0.4, 0.5] | 30 | 46.1% | 43.3% |
| (0.5, 0.6] | 58 | 54.7% | 48.3% |
| (0.6, 0.7] | 48 | 65.0% | 68.8% |
| (0.7, 0.8] | 2 | 72.2% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 138 | 54.3% | 52.4% | +4.30 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 32 | 46.9% | 52.7% | -4.51 | -0.0 |
| betrivers | 8 | 50.0% | 50.3% | -0.08 | +0.4 |
| draftkings | 50 | 66.0% | 53.7% | +10.69 | -0.1 |
| espnbet | 35 | 45.7% | 51.3% | -2.66 | +0.2 |
| fanduel | 13 | 53.8% | 51.5% | +0.86 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 52 | 50.0% | 48.7% | +0.12 | +0.4 |
| under | 86 | 57.0% | 54.7% | +4.18 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 25 | 36.0% | 41.2% | -3.42 | -0.4 |
| 45-55% | 59 | 50.8% | 49.9% | +2.03 | +0.2 |
| 55-65% | 49 | 69.4% | 59.9% | +7.65 | -0.1 |
| 65-75% | 5 | 40.0% | 65.6% | -1.96 | -0.6 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 110 | 56.4% | 52.3% | +7.89 | -0.1 |
| 5-8% | 25 | 48.0% | 52.9% | -2.28 | +0.2 |
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
| (0.5, 0.6] | 19 | 54.7% | 26.3% |
| (0.6, 0.7] | 6 | 63.1% | 66.7% |
| (0.7, 0.8] | 3 | 71.9% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 28 | 39.3% | 54.3% | -8.17 | -1.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| underdog | 28 | 39.3% | 54.3% | -8.17 | -1.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 9 | 33.3% | 53.2% | -3.48 | -0.8 |
| under | 19 | 42.1% | 54.8% | -4.69 | -1.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 19 | 26.3% | 50.8% | -9.05 | -1.1 |
| 55-65% | 6 | 66.7% | 59.4% | +0.83 | -1.3 |
| 65-75% | 3 | 66.7% | 66.3% | +0.05 | -0.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 23 | 39.1% | 53.5% | -6.22 | -1.2 |
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

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.4, 0.5] | 3 | 46.5% | 33.3% |
| (0.5, 0.6] | 4 | 55.6% | 50.0% |
| (0.6, 0.7] | 3 | 65.4% | 33.3% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 10 | 40.0% | 50.9% | -2.30 | -3.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 2 | 50.0% | 51.7% | -0.17 | -2.9 |
| draftkings | 3 | 33.3% | 45.3% | -0.75 | -3.6 |
| espnbet | 4 | 50.0% | 57.2% | -0.38 | -3.4 |
| fanduel | 1 | 0.0% | 41.0% | -1.00 | -3.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| under | 10 | 40.0% | 50.9% | -2.30 | -3.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 3 | 33.3% | 42.7% | -0.75 | -3.6 |
| 45-55% | 4 | 50.0% | 50.8% | -0.21 | -3.7 |
| 55-65% | 3 | 33.3% | 59.1% | -1.33 | -2.7 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 3 | 66.7% | 48.9% | +0.79 | -4.5 |
| 3-5% | 2 | 0.0% | 45.7% | -2.00 | -3.7 |
| 5-8% | 4 | 50.0% | 55.5% | -0.08 | -3.2 |
| >8% | 1 | 0.0% | 48.8% | -1.00 | -1.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-19 | Colton Dach Under 1.5 shots | 65.6% | 60.0% | Colton Dach 3 sog |
| 2026-11-19 | Ryan Leonard Under 2.5 shots | 65.4% | 57.4% | Ryan Leonard 4 sog |
| 2026-11-19 | Adam Fantilli Under 2.5 shots | 59.9% | 48.8% | Adam Fantilli 5 sog |
| 2026-11-19 | Matty Beniers Under 1.5 shots | 52.2% | 48.8% | Matty Beniers 7 sog |
| 2026-11-19 | Jordan Eberle Under 1.5 shots | 46.2% | 42.6% | Jordan Eberle 3 sog |

## M8_scorer_price

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 24 | 16.6% | 12.5% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 24 | 12.5% | 12.1% | +4.71 | -0.7 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 24 | 12.5% | 12.1% | +4.71 | -0.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 24 | 12.5% | 12.1% | +4.71 | -0.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 24 | 12.5% | 12.1% | +4.71 | -0.7 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 16 | 18.8% | 11.4% | +12.71 | -0.9 |
| 5-8% | 8 | 0.0% | 13.5% | -8.00 | -0.4 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-19 | Mathieu Olivier Over 0.5 goals | 25.9% | 18.0% | Mathieu Olivier 0 goals |
| 2026-11-19 | Jason Zucker Over 0.5 goals | 24.2% | 19.0% | Jason Zucker 0 goals |
| 2026-11-19 | Jiri Kulich Over 0.5 goals | 23.0% | 16.9% | Jiri Kulich 0 goals |
| 2026-11-19 | Cole Knuble Over 0.5 goals | 20.1% | 13.8% | Cole Knuble 0 goals |
| 2026-11-19 | Joel Armia Over 0.5 goals | 18.5% | 13.8% | Joel Armia 0 goals |

## M9_scorer_blind

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 4 | 0.0% | 23.9% | -4.00 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 4 | 0.0% | 23.9% | -4.00 | -0.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 4 | 0.0% | 23.9% | -4.00 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 4 | 0.0% | 23.9% | -4.00 | -0.3 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 3 | 0.0% | 22.1% | -3.00 | -0.2 |
| 5-8% | 1 | 0.0% | 29.4% | -1.00 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-19 | Mark Scheifele Over 0.5 goals | 38.5% | 34.5% | Mark Scheifele 0 goals |
| 2026-11-19 | Sidney Crosby Over 0.5 goals | 35.9% | 29.4% | Sidney Crosby 0 goals |
| 2026-11-19 | Jiri Kulich Over 0.5 goals | 20.1% | 16.9% | Jiri Kulich 0 goals |
| 2026-11-19 | Darren Raddysh Over 0.5 goals | 19.1% | 14.8% | Darren Raddysh 0 goals |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M6_shots_v2 | 138 | -0.07 (-0.4, +0.3) | 3.1% (-9.0%, 16.9%) | undecided |
| C1_chalk | 139 | -0.34 (-0.7, +0.0) | 0.1% (-7.1%, 5.9%) | undecided |
| M8_scorer_price | 24 | -0.74 (-0.8, -0.7) | 19.6% (-64.5%, 339.4%) | losing to the close |
| M3_xg_model | 53 | -1.12 (-1.4, -0.8) | -14.6% (-41.1%, 9.1%) | losing to the close |
| M2_goalie_news | 19 | -1.17 (-1.7, -0.3) | 1.1% (-43.1%, 44.8%) | losing to the close |
| M6_shots_v2_pickem | 28 | -1.12 (-2.0, -0.1) | -29.2% (-59.1%, 3.3%) | losing to the close |
| B0_random | 131 | -3.01 (-3.6, -2.5) | -5.4% (-20.1%, 9.7%) | losing to the close |
| M7_shots_under_early | 10 | -3.31 (-4.0, -3.2) | -23.0% (-36.1%, 95.2%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
| M9_scorer_blind | 4 | -0.25 (–, –) | -100.0% (–, –) | undecided |
