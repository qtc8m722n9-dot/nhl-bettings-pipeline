# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-27. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 85 bets, CLV -3.7 pp, units +7.77
- B0_random: market = player_sog: 40 bets, CLV -5.6 pp, units -8.89
- B0_random: venue = underdog: 63 bets, CLV -5.0 pp, units -7.21
- B0_random: side_label = over: 87 bets, CLV -3.4 pp, units -8.91
- B0_random: side_label = under: 90 bets, CLV -3.1 pp, units +4.92
- B0_random: price_band = <35%: 34 bets, CLV -2.0 pp, units +6.62
- B0_random: price_band = 35-45%: 18 bets, CLV -2.8 pp, units -1.00
- B0_random: price_band = 45-55%: 48 bets, CLV -3.8 pp, units -8.33
- B0_random: price_band = 55-65%: 39 bets, CLV -5.0 pp, units +2.75
- B0_random: price_band = 65-75%: 29 bets, CLV -3.4 pp, units -4.72
- M2_goalie_news: predicted 74% in (0.7, 0.8] but hit 60% (15 bets)
- M6_shots_v2_pickem: predicted 54% in (0.5, 0.6] but hit 35% (26 bets)
- M7_shots_under_early: predicted 55% in (0.5, 0.6] but hit 67% (15 bets)
- M7_shots_under_early: market = player_sog: 38 bets, CLV -2.5 pp, units +3.38
- M7_shots_under_early: side_label = under: 38 bets, CLV -2.5 pp, units +3.38
- M7_shots_under_early: price_band = 45-55%: 17 bets, CLV -2.7 pp, units +5.39
- M7_shots_under_early: edge_band = 3-5%: 15 bets, CLV -3.3 pp, units +7.70
- M9_scorer_blind: predicted 29% in (0.0, 0.4] but hit 11% (36 bets)

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 4 | 25.0% | 49.5% | -1.71 | -2.7 |
| p1_result | 3 | 33.3% | 58.3% | -1.48 | -2.5 |
| p1_total | 5 | 60.0% | 46.6% | +1.75 | -1.3 |
| player_goals | 32 | 50.0% | 53.7% | +0.70 | -0.9 |
| player_points | 85 | 56.5% | 52.7% | +7.77 | -3.7 |
| player_sog | 40 | 45.0% | 57.1% | -8.89 | -5.6 |
| spread | 3 | 33.3% | 59.8% | -1.64 | -2.0 |
| team_total | 15 | 26.7% | 42.6% | -5.32 | -0.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 114 | 49.1% | 51.5% | -1.99 | -1.9 |
| prizepicks | 10 | 60.0% | 57.7% | +0.39 | -7.5 |
| underdog | 63 | 47.6% | 55.0% | -7.21 | -5.0 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 8 | 37.5% | 60.0% | -2.83 | -2.6 |
| over | 87 | 37.9% | 44.8% | -8.91 | -3.4 |
| under | 90 | 62.2% | 60.7% | +4.92 | -3.1 |
| yes / favourite side | 2 | 0.0% | 36.1% | -2.00 | -2.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 34 | 32.4% | 25.9% | +6.62 | -2.0 |
| 35-45% | 18 | 38.9% | 40.6% | -1.00 | -2.8 |
| 45-55% | 48 | 41.7% | 50.0% | -8.33 | -3.8 |
| 55-65% | 39 | 64.1% | 59.9% | +2.75 | -5.0 |
| 65-75% | 29 | 58.6% | 69.8% | -4.72 | -3.4 |
| >75% | 19 | 63.2% | 80.9% | -4.13 | -0.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 187 | 49.2% | 53.0% | -8.81 | -3.2 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 15 | 100.0% | 84.9% | +2.66 | -1.0 |
| player_goals | 66 | 77.3% | 84.9% | -5.95 | -0.4 |
| player_points | 51 | 90.2% | 84.8% | +3.26 | +0.6 |
| spread | 19 | 84.2% | 84.7% | -0.12 | -0.8 |
| team_total | 23 | 82.6% | 84.7% | -0.59 | -1.1 |
| total | 21 | 85.7% | 84.8% | +0.23 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 195 | 84.6% | 84.8% | -0.51 | -0.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 19 | 84.2% | 84.7% | -0.12 | -0.8 |
| over | 36 | 91.7% | 84.9% | +2.89 | -0.7 |
| under | 140 | 82.9% | 84.8% | -3.27 | -0.1 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 195 | 84.6% | 84.8% | -0.51 | -0.3 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 195 | 84.6% | 84.8% | -0.51 | -0.3 |

## M1_sharp_price

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 2 | 36.7% | 50.0% |
| (0.4, 0.5] | 4 | 45.8% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 3 | 66.7% | 66.7% |
| (0.7, 0.8] | 15 | 73.8% | 60.0% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 5 | 20.0% | 38.2% | -2.11 | -2.2 |
| spread | 20 | 60.0% | 71.4% | -3.18 | -1.1 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 28 | 53.6% | 63.1% | -4.52 | -1.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 22 | 54.5% | 68.9% | -5.18 | -1.2 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 3 | 33.3% | 34.5% | -0.11 | -1.8 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 2 | 50.0% | 33.0% | +0.89 | -1.1 |
| 35-45% | 4 | 0.0% | 41.4% | -4.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 2 | 50.0% | 60.2% | -0.21 | -2.0 |
| 65-75% | 16 | 62.5% | 69.9% | -1.64 | -1.2 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 6 | 66.7% | 67.0% | -0.61 | -0.7 |
| 3-5% | 16 | 43.8% | 61.9% | -4.44 | -1.7 |
| 5-8% | 5 | 60.0% | 59.6% | +0.20 | -0.9 |
| >8% | 1 | 100.0% | 75.3% | +0.33 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-23 | WPG not to win by 2+ | 75.7% | 72.4% | UTA 2-4 WPG |
| 2026-11-27 | LAK not to win by 2+ | 75.2% | 71.5% | LAK 5-3 ANA |
| 2026-11-12 | TBL not to win by 2+ | 74.1% | 71.5% | TBL 3-1 CBJ |
| 2026-11-25 | CAR not to win by 2+ | 73.8% | 70.5% | CAR 3-1 TBL |

## M3_xg_model

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 6 | 32.3% | 16.7% |
| (0.4, 0.5] | 7 | 45.5% | 14.3% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 8 | 67.5% | 50.0% |
| (0.7, 0.8] | 34 | 73.5% | 64.7% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 10 | 10.0% | 38.7% | -7.11 | -2.1 |
| spread | 50 | 70.0% | 72.3% | -2.10 | -1.1 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 69 | 58.0% | 64.0% | -10.85 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 52 | 67.3% | 71.2% | -4.10 | -1.1 |
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
| 65-75% | 38 | 68.4% | 69.7% | -0.73 | -1.1 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 21 | 57.1% | 66.9% | -4.77 | -0.8 |
| 3-5% | 32 | 62.5% | 64.2% | -1.94 | -1.4 |
| 5-8% | 10 | 60.0% | 58.2% | -0.87 | -1.1 |
| >8% | 6 | 33.3% | 62.6% | -3.27 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-23 | WPG not to win by 2+ | 75.7% | 72.4% | UTA 2-4 WPG |
| 2026-11-27 | LAK not to win by 2+ | 75.2% | 71.5% | LAK 5-3 ANA |
| 2026-10-31 | OTT not to win by 2+ | 74.7% | 66.6% | OTT 5-1 SJS |
| 2026-11-25 | FLA not to win by 2+ | 74.1% | 71.5% | OTT 3-5 FLA |

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
| (0.4, 0.5] | 40 | 46.3% | 40.0% |
| (0.5, 0.6] | 89 | 55.1% | 50.6% |
| (0.6, 0.7] | 66 | 64.4% | 65.2% |
| (0.7, 0.8] | 3 | 71.7% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 198 | 53.5% | 52.5% | +2.09 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 47 | 48.9% | 52.1% | -4.94 | -0.2 |
| betrivers | 9 | 55.6% | 50.5% | +0.84 | +0.3 |
| draftkings | 65 | 60.0% | 53.0% | +7.24 | -0.3 |
| espnbet | 58 | 48.3% | 52.5% | -3.18 | +0.2 |
| fanduel | 19 | 57.9% | 52.5% | +2.14 | -0.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 77 | 54.5% | 49.9% | +4.62 | +0.3 |
| under | 121 | 52.9% | 54.1% | -2.53 | -0.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 33 | 33.3% | 41.3% | -6.82 | -0.3 |
| 45-55% | 89 | 52.8% | 50.2% | +5.00 | +0.1 |
| 55-65% | 70 | 64.3% | 59.4% | +5.35 | -0.3 |
| 65-75% | 6 | 50.0% | 65.6% | -1.43 | -0.8 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 156 | 55.8% | 52.5% | +8.47 | -0.2 |
| 5-8% | 39 | 46.2% | 52.2% | -5.06 | +0.2 |
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
| (0.5, 0.6] | 26 | 54.5% | 34.6% |
| (0.6, 0.7] | 7 | 62.7% | 71.4% |
| (0.7, 0.8] | 4 | 71.6% | 75.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 37 | 45.9% | 53.9% | -6.15 | -1.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| underdog | 37 | 45.9% | 53.9% | -6.15 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 12 | 50.0% | 53.5% | -0.98 | -0.9 |
| under | 25 | 44.0% | 54.1% | -5.17 | -1.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 26 | 34.6% | 50.6% | -8.28 | -1.1 |
| 55-65% | 7 | 71.4% | 59.1% | +1.59 | -1.7 |
| 65-75% | 4 | 75.0% | 66.4% | +0.55 | -1.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 32 | 46.9% | 53.3% | -4.20 | -1.3 |
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
| (0.4, 0.5] | 14 | 47.3% | 42.9% |
| (0.5, 0.6] | 15 | 54.5% | 66.7% |
| (0.6, 0.7] | 9 | 65.7% | 55.6% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 38 | 55.3% | 50.3% | +3.38 | -2.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 11 | 63.6% | 52.4% | +2.09 | -2.8 |
| draftkings | 12 | 41.7% | 47.6% | -1.77 | -3.0 |
| espnbet | 12 | 58.3% | 51.2% | +2.22 | -1.7 |
| fanduel | 3 | 66.7% | 49.7% | +0.85 | -3.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| under | 38 | 55.3% | 50.3% | +3.38 | -2.5 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 11 | 36.4% | 42.8% | -1.80 | -2.2 |
| 45-55% | 17 | 64.7% | 49.1% | +5.39 | -2.7 |
| 55-65% | 9 | 55.6% | 60.0% | -0.73 | -2.6 |
| 65-75% | 1 | 100.0% | 65.5% | +0.53 | -2.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 11 | 54.5% | 51.6% | +0.07 | -3.2 |
| 3-5% | 15 | 73.3% | 48.4% | +7.70 | -3.3 |
| 5-8% | 11 | 36.4% | 51.7% | -3.39 | -1.2 |
| >8% | 1 | 0.0% | 48.8% | -1.00 | -1.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-19 | Colton Dach Under 1.5 shots | 65.6% | 60.0% | Colton Dach 3 sog |
| 2026-11-19 | Ryan Leonard Under 2.5 shots | 65.4% | 57.4% | Ryan Leonard 4 sog |
| 2026-11-25 | Seth Jarvis Under 2.5 shots | 65.3% | 63.6% | Seth Jarvis 4 sog |
| 2026-11-21 | Rasmus Dahlin Under 2.5 shots | 61.7% | 55.6% | Rasmus Dahlin 3 sog |
| 2026-11-19 | Adam Fantilli Under 2.5 shots | 59.9% | 48.8% | Adam Fantilli 5 sog |

## M8_scorer_price

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 107 | 17.5% | 15.9% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 107 | 15.9% | 13.0% | +22.59 | -1.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 107 | 15.9% | 13.0% | +22.59 | -1.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 107 | 15.9% | 13.0% | +22.59 | -1.1 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 107 | 15.9% | 13.0% | +22.59 | -1.1 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 73 | 17.8% | 12.4% | +26.43 | -1.3 |
| 5-8% | 34 | 11.8% | 14.1% | -3.84 | -0.7 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-27 | William Nylander Over 0.5 goals | 33.8% | 28.4% | William Nylander 0 goals |
| 2026-11-27 | Trevor Connelly Over 0.5 goals | 30.0% | 25.3% | Trevor Connelly 0 goals |
| 2026-11-21 | Mason Marchment Over 0.5 goals | 29.9% | 25.3% | Mason Marchment 0 goals |
| 2026-11-27 | Brad Marchand Over 0.5 goals | 29.4% | 23.2% | Brad Marchand 0 goals |
| 2026-11-25 | Mason Marchment Over 0.5 goals | 27.5% | 22.2% | Mason Marchment 0 goals |

## M9_scorer_blind

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 36 | 28.9% | 11.1% |
| (0.4, 0.5] | 14 | 44.9% | 35.7% |
| (0.5, 0.6] | 2 | 51.5% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 52 | 21.2% | 29.7% | -16.98 | -0.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 52 | 21.2% | 29.7% | -16.98 | -0.5 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 52 | 21.2% | 29.7% | -16.98 | -0.5 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 33 | 9.1% | 23.6% | -17.33 | -0.7 |
| 35-45% | 18 | 38.9% | 39.9% | -0.74 | +0.0 |
| 45-55% | 1 | 100.0% | 47.7% | +1.09 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 42 | 21.4% | 29.0% | -11.92 | -0.5 |
| 5-8% | 10 | 20.0% | 32.6% | -5.05 | -0.2 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-25 | Macklin Celebrini Over 0.5 goals | 48.5% | 43.7% | Macklin Celebrini 0 goals |
| 2026-11-23 | Matt Boldy Over 0.5 goals | 47.8% | 41.7% | Matt Boldy 0 goals |
| 2026-11-23 | Macklin Celebrini Over 0.5 goals | 44.1% | 40.7% | Macklin Celebrini 0 goals |
| 2026-11-22 | Wyatt Johnston Over 0.5 goals | 44.0% | 40.7% | Wyatt Johnston 0 goals |
| 2026-11-23 | Jack Hughes Over 0.5 goals | 43.8% | 40.7% | Jack Hughes 0 goals |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M6_shots_v2 | 198 | -0.14 (-0.5, +0.2) | 1.1% (-8.6%, 11.4%) | undecided |
| C1_chalk | 195 | -0.28 (-0.6, +0.0) | -0.3% (-6.0%, 4.8%) | undecided |
| M9_scorer_blind | 52 | -0.47 (-0.8, -0.1) | -32.6% (-72.9%, 1.4%) | losing to the close |
| M3_xg_model | 69 | -1.20 (-1.5, -0.9) | -15.7% (-37.3%, 5.6%) | losing to the close |
| M8_scorer_price | 107 | -1.12 (-1.6, -0.8) | 21.1% (-44.9%, 103.7%) | losing to the close |
| M2_goalie_news | 28 | -1.30 (-1.7, -0.8) | -16.1% (-51.7%, 19.7%) | losing to the close |
| M6_shots_v2_pickem | 37 | -1.23 (-2.0, -0.5) | -16.6% (-47.2%, 15.8%) | losing to the close |
| M7_shots_under_early | 38 | -2.54 (-3.1, -2.1) | 8.9% (-19.5%, 36.9%) | losing to the close |
| B0_random | 187 | -3.21 (-3.6, -2.8) | -4.7% (-16.7%, 9.2%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
