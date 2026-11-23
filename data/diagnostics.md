# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-22. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 66 bets, CLV -3.7 pp, units -0.93
- B0_random: market = player_sog: 29 bets, CLV -5.5 pp, units -7.56
- B0_random: venue = underdog: 51 bets, CLV -4.8 pp, units -5.24
- B0_random: side_label = over: 71 bets, CLV -3.4 pp, units -8.13
- B0_random: side_label = under: 69 bets, CLV -2.8 pp, units -1.34
- B0_random: price_band = 35-45%: 17 bets, CLV -2.9 pp, units -2.34
- B0_random: price_band = 45-55%: 39 bets, CLV -3.8 pp, units -7.26
- B0_random: price_band = 55-65%: 27 bets, CLV -5.1 pp, units +1.59
- B0_random: price_band = 65-75%: 24 bets, CLV -3.1 pp, units -5.45
- M6_shots_v2_pickem: predicted 54% in (0.5, 0.6] but hit 26% (23 bets)
- M7_shots_under_early: market = player_sog: 24 bets, CLV -2.6 pp, units +2.51
- M7_shots_under_early: side_label = under: 24 bets, CLV -2.6 pp, units +2.51

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 4 | 25.0% | 49.5% | -1.71 | -2.7 |
| p1_result | 3 | 33.3% | 58.3% | -1.48 | -2.5 |
| p1_total | 5 | 60.0% | 46.6% | +1.75 | -1.3 |
| player_goals | 27 | 51.9% | 54.8% | +0.59 | -0.9 |
| player_points | 66 | 51.5% | 52.2% | -0.93 | -3.7 |
| player_sog | 29 | 41.4% | 56.0% | -7.56 | -5.5 |
| spread | 3 | 33.3% | 59.8% | -1.64 | -2.0 |
| team_total | 13 | 30.8% | 44.1% | -3.32 | -0.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 92 | 45.7% | 51.6% | -8.98 | -1.8 |
| prizepicks | 7 | 57.1% | 57.7% | -0.07 | -7.6 |
| underdog | 51 | 47.1% | 54.0% | -5.24 | -4.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 8 | 37.5% | 60.0% | -2.83 | -2.6 |
| over | 71 | 38.0% | 44.7% | -8.13 | -3.4 |
| under | 69 | 58.0% | 60.6% | -1.34 | -2.8 |
| yes / favourite side | 2 | 0.0% | 36.1% | -2.00 | -2.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 27 | 29.6% | 25.6% | +2.80 | -1.6 |
| 35-45% | 17 | 35.3% | 40.4% | -2.34 | -2.9 |
| 45-55% | 39 | 41.0% | 49.9% | -7.26 | -3.8 |
| 55-65% | 27 | 63.0% | 59.7% | +1.59 | -5.1 |
| 65-75% | 24 | 54.2% | 69.8% | -5.45 | -3.1 |
| >75% | 16 | 62.5% | 81.1% | -3.62 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 150 | 46.7% | 52.7% | -14.29 | -3.1 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 13 | 100.0% | 84.9% | +2.30 | -0.8 |
| player_goals | 53 | 79.2% | 84.9% | -3.54 | -0.4 |
| player_points | 41 | 92.7% | 84.8% | +3.84 | +0.6 |
| spread | 15 | 86.7% | 84.7% | +0.34 | -0.7 |
| team_total | 18 | 77.8% | 84.7% | -1.48 | -1.4 |
| total | 18 | 88.9% | 84.8% | +0.86 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 158 | 86.1% | 84.8% | +2.34 | -0.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 15 | 86.7% | 84.7% | +0.34 | -0.7 |
| over | 29 | 89.7% | 84.9% | +1.64 | -0.7 |
| under | 114 | 85.1% | 84.8% | +0.36 | -0.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 158 | 86.1% | 84.8% | +2.34 | -0.3 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 158 | 86.1% | 84.8% | +2.34 | -0.3 |

## M1_sharp_price

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 1 | 39.3% | 100.0% |
| (0.4, 0.5] | 4 | 45.8% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 3 | 66.7% | 66.7% |
| (0.7, 0.8] | 9 | 73.7% | 77.8% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 4 | 25.0% | 39.9% | -1.11 | -2.0 |
| spread | 14 | 71.4% | 71.9% | -0.05 | -1.1 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 21 | 61.9% | 62.5% | -0.40 | -1.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 16 | 62.5% | 68.3% | -2.05 | -1.3 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 2 | 50.0% | 36.1% | +0.89 | -1.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 1 | 100.0% | 34.5% | +1.89 | +0.5 |
| 35-45% | 4 | 0.0% | 41.4% | -4.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 2 | 50.0% | 60.2% | -0.21 | -2.0 |
| 65-75% | 10 | 80.0% | 69.7% | +1.48 | -1.2 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 4 | 75.0% | 75.3% | -0.04 | -0.5 |
| 3-5% | 11 | 54.5% | 58.0% | -0.88 | -1.8 |
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
| (0.4, 0.5] | 7 | 45.5% | 14.3% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 8 | 67.5% | 50.0% |
| (0.7, 0.8] | 23 | 73.4% | 69.6% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 9 | 11.1% | 39.5% | -6.11 | -2.0 |
| spread | 39 | 74.4% | 72.8% | +0.31 | -1.1 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 57 | 59.6% | 63.4% | -7.44 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 41 | 70.7% | 71.4% | -1.69 | -1.2 |
| over | 5 | 40.0% | 41.5% | -1.41 | -0.7 |
| under | 4 | 50.0% | 52.2% | -0.24 | -1.3 |
| yes / favourite side | 7 | 14.3% | 38.3% | -4.11 | -1.8 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 4 | 25.0% | 25.8% | -1.11 | -0.4 |
| 35-45% | 8 | 0.0% | 40.2% | -8.00 | -2.2 |
| 45-55% | 2 | 100.0% | 48.2% | +2.16 | -1.0 |
| 55-65% | 5 | 20.0% | 60.3% | -3.21 | -2.0 |
| 65-75% | 27 | 74.1% | 69.4% | +1.68 | -1.2 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 16 | 56.2% | 68.2% | -4.07 | -0.7 |
| 3-5% | 25 | 68.0% | 62.5% | +0.77 | -1.5 |
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
| (0.4, 0.5] | 34 | 46.2% | 44.1% |
| (0.5, 0.6] | 72 | 55.0% | 48.6% |
| (0.6, 0.7] | 55 | 64.7% | 67.3% |
| (0.7, 0.8] | 3 | 71.7% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 164 | 54.3% | 52.5% | +4.72 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 35 | 45.7% | 52.7% | -5.90 | -0.1 |
| betrivers | 9 | 55.6% | 50.5% | +0.84 | +0.3 |
| draftkings | 56 | 60.7% | 53.4% | +6.89 | -0.2 |
| espnbet | 45 | 51.1% | 51.4% | +0.76 | +0.2 |
| fanduel | 19 | 57.9% | 52.5% | +2.14 | -0.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 65 | 52.3% | 49.4% | +2.04 | +0.3 |
| under | 99 | 55.6% | 54.5% | +2.68 | -0.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 29 | 34.5% | 41.4% | -5.17 | -0.2 |
| 45-55% | 73 | 53.4% | 50.3% | +5.53 | +0.1 |
| 55-65% | 56 | 66.1% | 59.7% | +5.79 | -0.2 |
| 65-75% | 6 | 50.0% | 65.6% | -1.43 | -0.8 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 127 | 56.7% | 52.3% | +10.09 | -0.1 |
| 5-8% | 34 | 47.1% | 53.1% | -4.06 | +0.2 |
| >8% | 3 | 33.3% | 53.1% | -1.31 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 65.5% | Taylor Hall 3 sog |
| 2026-11-14 | John Carlson Under 2.5 shots | 69.6% | 65.5% | John Carlson 4 sog |
| 2026-11-10 | Noah Dobson Under 2.5 shots | 69.5% | 65.5% | Noah Dobson 3 sog |
| 2026-11-12 | Kent Johnson Under 2.5 shots | 68.3% | 64.3% | Kent Johnson 4 sog |
| 2026-11-22 | Alexis Lafrenière Under 2.5 shots | 68.3% | 64.3% | Alexis Lafrenière 3 sog |

## M6_shots_v2_pickem

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.5, 0.6] | 23 | 54.4% | 26.1% |
| (0.6, 0.7] | 7 | 62.7% | 71.4% |
| (0.7, 0.8] | 4 | 71.6% | 75.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 34 | 41.2% | 54.2% | -9.04 | -1.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| underdog | 34 | 41.2% | 54.2% | -9.04 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 11 | 45.5% | 53.5% | -1.85 | -1.2 |
| under | 23 | 39.1% | 54.5% | -7.19 | -1.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 23 | 26.1% | 50.6% | -11.18 | -1.1 |
| 55-65% | 7 | 71.4% | 59.1% | +1.59 | -1.7 |
| 65-75% | 4 | 75.0% | 66.4% | +0.55 | -1.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 29 | 41.4% | 53.5% | -7.09 | -1.4 |
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
| (0.4, 0.5] | 10 | 47.6% | 50.0% |
| (0.5, 0.6] | 9 | 54.3% | 66.7% |
| (0.6, 0.7] | 5 | 64.4% | 40.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 24 | 54.2% | 49.1% | +2.51 | -2.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 6 | 66.7% | 51.4% | +1.44 | -2.9 |
| draftkings | 7 | 42.9% | 45.9% | -0.40 | -2.9 |
| espnbet | 9 | 55.6% | 51.6% | +1.17 | -1.9 |
| fanduel | 2 | 50.0% | 42.2% | +0.30 | -3.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| under | 24 | 54.2% | 49.1% | +2.51 | -2.6 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 8 | 50.0% | 42.8% | +1.20 | -2.2 |
| 45-55% | 11 | 63.6% | 49.1% | +3.04 | -2.9 |
| 55-65% | 5 | 40.0% | 59.1% | -1.73 | -2.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 6 | 66.7% | 50.9% | +1.44 | -3.4 |
| 3-5% | 9 | 66.7% | 45.5% | +4.10 | -3.2 |
| 5-8% | 8 | 37.5% | 51.8% | -2.03 | -1.5 |
| >8% | 1 | 0.0% | 48.8% | -1.00 | -1.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-19 | Colton Dach Under 1.5 shots | 65.6% | 60.0% | Colton Dach 3 sog |
| 2026-11-19 | Ryan Leonard Under 2.5 shots | 65.4% | 57.4% | Ryan Leonard 4 sog |
| 2026-11-21 | Rasmus Dahlin Under 2.5 shots | 61.7% | 55.6% | Rasmus Dahlin 3 sog |
| 2026-11-19 | Adam Fantilli Under 2.5 shots | 59.9% | 48.8% | Adam Fantilli 5 sog |
| 2026-11-21 | Ivan Provorov Under 1.5 shots | 52.5% | 45.5% | Ivan Provorov 2 sog |

## M8_scorer_price

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 47 | 17.1% | 17.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 47 | 17.0% | 12.8% | +17.17 | -1.4 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 47 | 17.0% | 12.8% | +17.17 | -1.4 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 47 | 17.0% | 12.8% | +17.17 | -1.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 47 | 17.0% | 12.8% | +17.17 | -1.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 34 | 20.6% | 12.6% | +22.32 | -1.6 |
| 5-8% | 13 | 7.7% | 13.1% | -5.15 | -0.8 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-21 | Mason Marchment Over 0.5 goals | 29.9% | 25.3% | Mason Marchment 0 goals |
| 2026-11-21 | Mikael Backlund Over 0.5 goals | 26.4% | 22.2% | Mikael Backlund 0 goals |
| 2026-11-19 | Mathieu Olivier Over 0.5 goals | 25.9% | 18.0% | Mathieu Olivier 0 goals |
| 2026-11-19 | Jason Zucker Over 0.5 goals | 24.2% | 19.0% | Jason Zucker 0 goals |
| 2026-11-19 | Jiri Kulich Over 0.5 goals | 23.0% | 16.9% | Jiri Kulich 0 goals |

## M9_scorer_blind

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 11 | 29.8% | 0.0% |
| (0.4, 0.5] | 4 | 44.8% | 50.0% |
| (0.5, 0.6] | 2 | 51.5% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 17 | 23.5% | 31.5% | -7.67 | -0.7 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 17 | 23.5% | 31.5% | -7.67 | -0.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 17 | 23.5% | 31.5% | -7.67 | -0.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 10 | 0.0% | 24.7% | -10.00 | -0.8 |
| 35-45% | 6 | 50.0% | 40.0% | +1.23 | -0.3 |
| 45-55% | 1 | 100.0% | 47.7% | +1.09 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 14 | 14.3% | 30.3% | -9.62 | -0.8 |
| 5-8% | 3 | 66.7% | 36.9% | +1.95 | -0.2 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-22 | Wyatt Johnston Over 0.5 goals | 44.0% | 40.7% | Wyatt Johnston 0 goals |
| 2026-11-21 | Steven Stamkos Over 0.5 goals | 42.0% | 38.6% | Steven Stamkos 0 goals |
| 2026-11-21 | William Nylander Over 0.5 goals | 39.8% | 35.6% | William Nylander 0 goals |
| 2026-11-19 | Mark Scheifele Over 0.5 goals | 38.5% | 34.5% | Mark Scheifele 0 goals |
| 2026-11-21 | Matthew Tkachuk Over 0.5 goals | 36.1% | 32.5% | Matthew Tkachuk 0 goals |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M6_shots_v2 | 164 | -0.11 (-0.5, +0.2) | 2.9% (-7.6%, 15.0%) | undecided |
| C1_chalk | 158 | -0.33 (-0.7, -0.0) | 1.5% (-4.4%, 6.8%) | losing to the close |
| M9_scorer_blind | 17 | -0.71 (-0.9, -0.3) | -45.1% (-100.0%, -23.7%) | losing to the close |
| M3_xg_model | 57 | -1.21 (-1.6, -0.9) | -13.1% (-36.3%, 11.0%) | losing to the close |
| M2_goalie_news | 21 | -1.29 (-1.9, -0.6) | -1.9% (-43.2%, 36.8%) | losing to the close |
| M6_shots_v2_pickem | 34 | -1.24 (-2.1, -0.4) | -26.6% (-54.1%, 1.3%) | losing to the close |
| M8_scorer_price | 47 | -1.40 (-2.2, -0.7) | 36.5% (-51.4%, 208.4%) | losing to the close |
| M7_shots_under_early | 24 | -2.57 (-3.4, -2.0) | 10.5% (-31.4%, 49.5%) | losing to the close |
| B0_random | 150 | -3.07 (-3.6, -2.6) | -9.5% (-22.6%, 3.8%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
