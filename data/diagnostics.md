# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-23. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 72 bets, CLV -3.7 pp, units -0.74
- B0_random: market = player_sog: 29 bets, CLV -5.5 pp, units -7.56
- B0_random: venue = underdog: 52 bets, CLV -4.8 pp, units -6.24
- B0_random: side_label = over: 75 bets, CLV -3.4 pp, units -6.59
- B0_random: side_label = under: 72 bets, CLV -2.8 pp, units +0.13
- B0_random: price_band = 35-45%: 17 bets, CLV -2.9 pp, units -2.34
- B0_random: price_band = 45-55%: 41 bets, CLV -3.8 pp, units -9.26
- B0_random: price_band = 55-65%: 29 bets, CLV -4.9 pp, units +2.89
- B0_random: price_band = 65-75%: 24 bets, CLV -3.1 pp, units -5.45
- M6_shots_v2_pickem: predicted 54% in (0.5, 0.6] but hit 26% (23 bets)
- M7_shots_under_early: market = player_sog: 26 bets, CLV -2.6 pp, units +3.59
- M7_shots_under_early: side_label = under: 26 bets, CLV -2.6 pp, units +3.59
- M9_scorer_blind: predicted 30% in (0.0, 0.4] but hit 0% (16 bets)

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 4 | 25.0% | 49.5% | -1.71 | -2.7 |
| p1_result | 3 | 33.3% | 58.3% | -1.48 | -2.5 |
| p1_total | 5 | 60.0% | 46.6% | +1.75 | -1.3 |
| player_goals | 28 | 53.6% | 53.8% | +3.39 | -0.9 |
| player_points | 72 | 51.4% | 51.8% | -0.74 | -3.7 |
| player_sog | 29 | 41.4% | 56.0% | -7.56 | -5.5 |
| spread | 3 | 33.3% | 59.8% | -1.64 | -2.0 |
| team_total | 13 | 30.8% | 44.1% | -3.32 | -0.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 98 | 46.9% | 51.1% | -4.98 | -1.9 |
| prizepicks | 7 | 57.1% | 57.7% | -0.07 | -7.6 |
| underdog | 52 | 46.2% | 53.9% | -6.24 | -4.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 8 | 37.5% | 60.0% | -2.83 | -2.6 |
| over | 75 | 38.7% | 44.5% | -6.59 | -3.4 |
| under | 72 | 58.3% | 60.2% | +0.13 | -2.8 |
| yes / favourite side | 2 | 0.0% | 36.1% | -2.00 | -2.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 30 | 33.3% | 25.9% | +6.50 | -2.0 |
| 35-45% | 17 | 35.3% | 40.4% | -2.34 | -2.9 |
| 45-55% | 41 | 39.0% | 50.0% | -9.26 | -3.8 |
| 55-65% | 29 | 65.5% | 59.8% | +2.89 | -4.9 |
| 65-75% | 24 | 54.2% | 69.8% | -5.45 | -3.1 |
| >75% | 16 | 62.5% | 81.1% | -3.62 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 157 | 47.1% | 52.3% | -11.29 | -3.1 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 13 | 100.0% | 84.9% | +2.30 | -0.8 |
| player_goals | 57 | 78.9% | 84.9% | -4.01 | -0.4 |
| player_points | 43 | 93.0% | 84.8% | +4.20 | +0.5 |
| spread | 15 | 86.7% | 84.7% | +0.34 | -0.7 |
| team_total | 19 | 78.9% | 84.7% | -1.30 | -1.4 |
| total | 18 | 88.9% | 84.8% | +0.86 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 165 | 86.1% | 84.8% | +2.40 | -0.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 15 | 86.7% | 84.7% | +0.34 | -0.7 |
| over | 30 | 90.0% | 84.9% | +1.81 | -0.7 |
| under | 120 | 85.0% | 84.8% | +0.24 | -0.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 165 | 86.1% | 84.8% | +2.40 | -0.3 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 165 | 86.1% | 84.8% | +2.40 | -0.3 |

## M1_sharp_price

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 2 | 36.7% | 50.0% |
| (0.4, 0.5] | 4 | 45.8% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 3 | 66.7% | 66.7% |
| (0.7, 0.8] | 11 | 73.8% | 72.7% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 5 | 20.0% | 38.2% | -2.11 | -2.2 |
| spread | 16 | 68.8% | 71.8% | -0.62 | -0.9 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 24 | 58.3% | 61.9% | -1.96 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 18 | 61.1% | 68.6% | -2.62 | -1.1 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 3 | 33.3% | 34.5% | -0.11 | -1.8 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 2 | 50.0% | 33.0% | +0.89 | -1.1 |
| 35-45% | 4 | 0.0% | 41.4% | -4.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 2 | 50.0% | 60.2% | -0.21 | -2.0 |
| 65-75% | 12 | 75.0% | 69.9% | +0.92 | -1.0 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 6 | 66.7% | 67.0% | -0.61 | -0.7 |
| 3-5% | 12 | 50.0% | 59.2% | -1.88 | -1.7 |
| 5-8% | 5 | 60.0% | 59.6% | +0.20 | -0.9 |
| >8% | 1 | 100.0% | 75.3% | +0.33 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-23 | WPG not to win by 2+ | 75.7% | 72.4% | UTA 2-4 WPG |
| 2026-11-12 | TBL not to win by 2+ | 74.1% | 71.5% | TBL 3-1 CBJ |
| 2026-11-09 | PHI not to win by 2+ | 70.7% | 67.6% | PHI 3-1 VAN |
| 2026-11-09 | EDM not to win by 2+ | 68.0% | 64.6% | NYR 1-3 EDM |

## M3_xg_model

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 6 | 32.3% | 16.7% |
| (0.4, 0.5] | 7 | 45.5% | 14.3% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 8 | 67.5% | 50.0% |
| (0.7, 0.8] | 25 | 73.4% | 68.0% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 10 | 10.0% | 38.7% | -7.11 | -2.1 |
| spread | 41 | 73.2% | 72.7% | -0.25 | -1.0 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 60 | 58.3% | 63.1% | -9.00 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 43 | 69.8% | 71.4% | -2.25 | -1.1 |
| over | 5 | 40.0% | 41.5% | -1.41 | -0.7 |
| under | 4 | 50.0% | 52.2% | -0.24 | -1.3 |
| yes / favourite side | 8 | 12.5% | 37.4% | -5.11 | -1.9 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 5 | 20.0% | 26.9% | -2.11 | -0.9 |
| 35-45% | 8 | 0.0% | 40.2% | -8.00 | -2.2 |
| 45-55% | 2 | 100.0% | 48.2% | +2.16 | -1.0 |
| 55-65% | 5 | 20.0% | 60.3% | -3.21 | -2.0 |
| 65-75% | 29 | 72.4% | 69.5% | +1.12 | -1.1 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 18 | 55.6% | 66.3% | -4.63 | -0.7 |
| 3-5% | 26 | 65.4% | 62.9% | -0.23 | -1.4 |
| 5-8% | 10 | 60.0% | 58.2% | -0.87 | -1.1 |
| >8% | 6 | 33.3% | 62.6% | -3.27 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-23 | WPG not to win by 2+ | 75.7% | 72.4% | UTA 2-4 WPG |
| 2026-10-31 | OTT not to win by 2+ | 74.7% | 66.6% | OTT 5-1 SJS |
| 2026-11-12 | TBL not to win by 2+ | 74.1% | 71.5% | TBL 3-1 CBJ |
| 2026-11-07 | MTL not to win by 2+ | 72.1% | 69.5% | MTL 4-2 TOR |

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
| (0.4, 0.5] | 35 | 46.3% | 42.9% |
| (0.5, 0.6] | 76 | 55.1% | 50.0% |
| (0.6, 0.7] | 56 | 64.7% | 67.9% |
| (0.7, 0.8] | 3 | 71.7% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 170 | 54.7% | 52.5% | +5.97 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 37 | 48.6% | 52.7% | -4.15 | -0.2 |
| betrivers | 9 | 55.6% | 50.5% | +0.84 | +0.3 |
| draftkings | 57 | 59.6% | 53.3% | +5.89 | -0.2 |
| espnbet | 48 | 52.1% | 51.6% | +1.26 | +0.3 |
| fanduel | 19 | 57.9% | 52.5% | +2.14 | -0.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 68 | 54.4% | 49.6% | +4.46 | +0.3 |
| under | 102 | 54.9% | 54.4% | +1.52 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 29 | 34.5% | 41.4% | -5.17 | -0.2 |
| 45-55% | 77 | 53.2% | 50.3% | +5.32 | +0.1 |
| 55-65% | 58 | 67.2% | 59.6% | +7.26 | -0.2 |
| 65-75% | 6 | 50.0% | 65.6% | -1.43 | -0.8 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 133 | 57.1% | 52.3% | +11.34 | -0.1 |
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
| (0.6, 0.7] | 7 | 65.6% | 57.1% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 26 | 57.7% | 50.3% | +3.59 | -2.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 6 | 66.7% | 51.4% | +1.44 | -2.9 |
| draftkings | 8 | 50.0% | 48.3% | +0.13 | -2.9 |
| espnbet | 9 | 55.6% | 51.6% | +1.17 | -1.9 |
| fanduel | 3 | 66.7% | 49.7% | +0.85 | -3.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| under | 26 | 57.7% | 50.3% | +3.59 | -2.6 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 8 | 50.0% | 42.8% | +1.20 | -2.2 |
| 45-55% | 11 | 63.6% | 49.1% | +3.04 | -2.9 |
| 55-65% | 6 | 50.0% | 60.0% | -1.18 | -2.5 |
| 65-75% | 1 | 100.0% | 65.5% | +0.53 | -2.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 7 | 71.4% | 53.0% | +1.97 | -3.2 |
| 3-5% | 10 | 70.0% | 47.4% | +4.65 | -3.2 |
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
| (0.0, 0.4] | 57 | 17.1% | 17.5% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 57 | 17.5% | 12.7% | +20.92 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 57 | 17.5% | 12.7% | +20.92 | -1.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 57 | 17.5% | 12.7% | +20.92 | -1.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 57 | 17.5% | 12.7% | +20.92 | -1.3 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 41 | 19.5% | 12.7% | +21.22 | -1.6 |
| 5-8% | 16 | 12.5% | 12.7% | -0.30 | -0.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-21 | Mason Marchment Over 0.5 goals | 29.9% | 25.3% | Mason Marchment 0 goals |
| 2026-11-21 | Mikael Backlund Over 0.5 goals | 26.4% | 22.2% | Mikael Backlund 0 goals |
| 2026-11-19 | Mathieu Olivier Over 0.5 goals | 25.9% | 18.0% | Mathieu Olivier 0 goals |
| 2026-11-23 | Mason Marchment Over 0.5 goals | 25.0% | 21.1% | Mason Marchment 0 goals |
| 2026-11-19 | Jason Zucker Over 0.5 goals | 24.2% | 19.0% | Jason Zucker 0 goals |

## M9_scorer_blind

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 16 | 30.1% | 0.0% |
| (0.4, 0.5] | 7 | 45.0% | 28.6% |
| (0.5, 0.6] | 2 | 51.5% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 25 | 16.0% | 31.5% | -15.67 | -0.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 25 | 16.0% | 31.5% | -15.67 | -0.5 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 25 | 16.0% | 31.5% | -15.67 | -0.5 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 15 | 0.0% | 25.1% | -15.00 | -0.7 |
| 35-45% | 9 | 33.3% | 40.3% | -1.77 | -0.1 |
| 45-55% | 1 | 100.0% | 47.7% | +1.09 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 19 | 10.5% | 30.6% | -14.62 | -0.6 |
| 5-8% | 6 | 33.3% | 34.3% | -1.05 | -0.2 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-23 | Matt Boldy Over 0.5 goals | 47.8% | 41.7% | Matt Boldy 0 goals |
| 2026-11-23 | Macklin Celebrini Over 0.5 goals | 44.1% | 40.7% | Macklin Celebrini 0 goals |
| 2026-11-22 | Wyatt Johnston Over 0.5 goals | 44.0% | 40.7% | Wyatt Johnston 0 goals |
| 2026-11-23 | Jack Hughes Over 0.5 goals | 43.8% | 40.7% | Jack Hughes 0 goals |
| 2026-11-21 | Steven Stamkos Over 0.5 goals | 42.0% | 38.6% | Steven Stamkos 0 goals |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M6_shots_v2 | 170 | -0.08 (-0.4, +0.2) | 3.5% (-7.1%, 14.6%) | undecided |
| C1_chalk | 165 | -0.33 (-0.7, -0.0) | 1.5% (-5.0%, 7.0%) | losing to the close |
| M9_scorer_blind | 25 | -0.50 (-0.9, -0.1) | -62.7% (-100.0%, -28.2%) | losing to the close |
| M3_xg_model | 60 | -1.19 (-1.5, -0.9) | -15.0% (-38.8%, 7.9%) | losing to the close |
| M2_goalie_news | 24 | -1.22 (-1.7, -0.6) | -8.2% (-45.6%, 30.0%) | losing to the close |
| M8_scorer_price | 57 | -1.34 (-2.1, -0.8) | 36.7% (-37.0%, 166.8%) | losing to the close |
| M6_shots_v2_pickem | 34 | -1.24 (-2.1, -0.4) | -26.6% (-54.1%, 1.3%) | losing to the close |
| M7_shots_under_early | 26 | -2.58 (-3.3, -2.0) | 13.8% (-24.5%, 49.8%) | losing to the close |
| B0_random | 157 | -3.09 (-3.6, -2.6) | -7.2% (-20.1%, 7.2%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
