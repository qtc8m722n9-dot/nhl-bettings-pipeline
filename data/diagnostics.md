# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-25. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 78 bets, CLV -3.7 pp, units +3.09
- B0_random: market = player_sog: 35 bets, CLV -5.6 pp, units -10.35
- B0_random: venue = underdog: 58 bets, CLV -5.0 pp, units -8.67
- B0_random: side_label = over: 82 bets, CLV -3.4 pp, units -11.25
- B0_random: side_label = under: 80 bets, CLV -3.0 pp, units +2.82
- B0_random: price_band = 35-45%: 18 bets, CLV -2.8 pp, units -1.00
- B0_random: price_band = 45-55%: 47 bets, CLV -3.8 pp, units -9.20
- B0_random: price_band = 55-65%: 33 bets, CLV -5.0 pp, units +0.62
- B0_random: price_band = 65-75%: 26 bets, CLV -3.2 pp, units -4.56
- M3_xg_model: predicted 73% in (0.7, 0.8] but hit 61% (28 bets)
- M6_shots_v2_pickem: predicted 54% in (0.5, 0.6] but hit 32% (25 bets)
- M7_shots_under_early: market = player_sog: 32 bets, CLV -2.5 pp, units +3.84
- M7_shots_under_early: side_label = under: 32 bets, CLV -2.5 pp, units +3.84
- M7_shots_under_early: price_band = 45-55%: 15 bets, CLV -2.7 pp, units +5.29
- M9_scorer_blind: predicted 30% in (0.0, 0.4] but hit 11% (27 bets)

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 4 | 25.0% | 49.5% | -1.71 | -2.7 |
| p1_result | 3 | 33.3% | 58.3% | -1.48 | -2.5 |
| p1_total | 5 | 60.0% | 46.6% | +1.75 | -1.3 |
| player_goals | 29 | 51.7% | 53.0% | +2.39 | -0.8 |
| player_points | 78 | 53.8% | 51.9% | +3.09 | -3.7 |
| player_sog | 35 | 40.0% | 56.4% | -10.35 | -5.6 |
| spread | 3 | 33.3% | 59.8% | -1.64 | -2.0 |
| team_total | 15 | 26.7% | 42.6% | -5.32 | -0.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 106 | 47.2% | 50.7% | -5.25 | -1.9 |
| prizepicks | 8 | 62.5% | 57.7% | +0.66 | -7.6 |
| underdog | 58 | 44.8% | 54.2% | -8.67 | -5.0 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 8 | 37.5% | 60.0% | -2.83 | -2.6 |
| over | 82 | 36.6% | 44.5% | -11.25 | -3.4 |
| under | 80 | 60.0% | 59.8% | +2.82 | -3.0 |
| yes / favourite side | 2 | 0.0% | 36.1% | -2.00 | -2.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 32 | 31.2% | 25.8% | +4.50 | -1.9 |
| 35-45% | 18 | 38.9% | 40.6% | -1.00 | -2.8 |
| 45-55% | 47 | 40.4% | 49.9% | -9.20 | -3.8 |
| 55-65% | 33 | 60.6% | 59.7% | +0.62 | -5.0 |
| 65-75% | 26 | 57.7% | 69.7% | -4.56 | -3.2 |
| >75% | 16 | 62.5% | 81.1% | -3.62 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 172 | 47.1% | 52.2% | -13.26 | -3.1 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 14 | 100.0% | 84.9% | +2.48 | -0.9 |
| player_goals | 61 | 78.7% | 84.9% | -4.48 | -0.4 |
| player_points | 47 | 91.5% | 84.8% | +3.73 | +0.4 |
| spread | 18 | 88.9% | 84.7% | +0.88 | -0.7 |
| team_total | 21 | 81.0% | 84.7% | -0.95 | -1.2 |
| total | 19 | 84.2% | 84.8% | -0.14 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 180 | 85.6% | 84.8% | +1.53 | -0.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 18 | 88.9% | 84.7% | +0.88 | -0.7 |
| over | 32 | 90.6% | 84.9% | +2.17 | -0.7 |
| under | 130 | 83.8% | 84.8% | -1.52 | -0.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 180 | 85.6% | 84.8% | +1.53 | -0.3 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 180 | 85.6% | 84.8% | +1.53 | -0.3 |

## M1_sharp_price

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 2 | 36.7% | 50.0% |
| (0.4, 0.5] | 4 | 45.8% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 3 | 66.7% | 66.7% |
| (0.7, 0.8] | 13 | 73.7% | 61.5% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 5 | 20.0% | 38.2% | -2.11 | -2.2 |
| spread | 18 | 61.1% | 71.5% | -2.62 | -0.9 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 26 | 53.8% | 62.5% | -3.96 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 20 | 55.0% | 68.7% | -4.62 | -1.1 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 3 | 33.3% | 34.5% | -0.11 | -1.8 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 2 | 50.0% | 33.0% | +0.89 | -1.1 |
| 35-45% | 4 | 0.0% | 41.4% | -4.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 2 | 50.0% | 60.2% | -0.21 | -2.0 |
| 65-75% | 14 | 64.3% | 69.9% | -1.08 | -1.0 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 6 | 66.7% | 67.0% | -0.61 | -0.7 |
| 3-5% | 14 | 42.9% | 60.7% | -3.88 | -1.6 |
| 5-8% | 5 | 60.0% | 59.6% | +0.20 | -0.9 |
| >8% | 1 | 100.0% | 75.3% | +0.33 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-23 | WPG not to win by 2+ | 75.7% | 72.4% | UTA 2-4 WPG |
| 2026-11-12 | TBL not to win by 2+ | 74.1% | 71.5% | TBL 3-1 CBJ |
| 2026-11-25 | CAR not to win by 2+ | 73.8% | 70.5% | CAR 3-1 TBL |
| 2026-11-25 | BUF not to win by 2+ | 72.8% | 68.6% | NYR 1-5 BUF |

## M3_xg_model

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 6 | 32.3% | 16.7% |
| (0.4, 0.5] | 7 | 45.5% | 14.3% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 8 | 67.5% | 50.0% |
| (0.7, 0.8] | 28 | 73.5% | 60.7% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 10 | 10.0% | 38.7% | -7.11 | -2.1 |
| spread | 44 | 68.2% | 72.6% | -3.25 | -1.0 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 63 | 55.6% | 63.4% | -12.00 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 46 | 65.2% | 71.3% | -5.25 | -1.1 |
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
| 65-75% | 32 | 65.6% | 69.6% | -1.88 | -1.1 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 19 | 52.6% | 66.5% | -5.63 | -0.8 |
| 3-5% | 28 | 60.7% | 63.3% | -2.23 | -1.4 |
| 5-8% | 10 | 60.0% | 58.2% | -0.87 | -1.1 |
| >8% | 6 | 33.3% | 62.6% | -3.27 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-23 | WPG not to win by 2+ | 75.7% | 72.4% | UTA 2-4 WPG |
| 2026-10-31 | OTT not to win by 2+ | 74.7% | 66.6% | OTT 5-1 SJS |
| 2026-11-25 | FLA not to win by 2+ | 74.1% | 71.5% | OTT 3-5 FLA |
| 2026-11-12 | TBL not to win by 2+ | 74.1% | 71.5% | TBL 3-1 CBJ |

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
| (0.4, 0.5] | 37 | 46.2% | 40.5% |
| (0.5, 0.6] | 83 | 55.1% | 50.6% |
| (0.6, 0.7] | 61 | 64.6% | 67.2% |
| (0.7, 0.8] | 3 | 71.7% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 184 | 54.3% | 52.5% | +4.56 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 41 | 48.8% | 52.2% | -4.48 | -0.1 |
| betrivers | 9 | 55.6% | 50.5% | +0.84 | +0.3 |
| draftkings | 62 | 59.7% | 53.1% | +6.60 | -0.2 |
| espnbet | 53 | 50.9% | 52.3% | -0.53 | +0.3 |
| fanduel | 19 | 57.9% | 52.5% | +2.14 | -0.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 74 | 54.1% | 49.6% | +4.04 | +0.3 |
| under | 110 | 54.5% | 54.4% | +0.52 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 31 | 32.3% | 41.3% | -7.17 | -0.2 |
| 45-55% | 83 | 53.0% | 50.2% | +5.24 | +0.1 |
| 55-65% | 64 | 67.2% | 59.6% | +7.92 | -0.2 |
| 65-75% | 6 | 50.0% | 65.6% | -1.43 | -0.8 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 144 | 56.9% | 52.5% | +10.78 | -0.1 |
| 5-8% | 37 | 45.9% | 52.3% | -4.91 | +0.2 |
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
| (0.5, 0.6] | 25 | 54.4% | 32.0% |
| (0.6, 0.7] | 7 | 62.7% | 71.4% |
| (0.7, 0.8] | 4 | 71.6% | 75.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 36 | 44.4% | 54.0% | -7.11 | -1.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| underdog | 36 | 44.4% | 54.0% | -7.11 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 12 | 50.0% | 53.5% | -0.98 | -0.9 |
| under | 24 | 41.7% | 54.3% | -6.13 | -1.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 25 | 32.0% | 50.6% | -9.25 | -1.0 |
| 55-65% | 7 | 71.4% | 59.1% | +1.59 | -1.7 |
| 65-75% | 4 | 75.0% | 66.4% | +0.55 | -1.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 31 | 45.2% | 53.3% | -5.16 | -1.3 |
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
| (0.4, 0.5] | 11 | 47.4% | 45.5% |
| (0.5, 0.6] | 13 | 54.1% | 69.2% |
| (0.6, 0.7] | 8 | 65.6% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 32 | 56.2% | 50.3% | +3.84 | -2.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 8 | 62.5% | 52.2% | +1.64 | -3.1 |
| draftkings | 9 | 44.4% | 47.8% | -0.87 | -2.9 |
| espnbet | 12 | 58.3% | 51.2% | +2.22 | -1.7 |
| fanduel | 3 | 66.7% | 49.7% | +0.85 | -3.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| under | 32 | 56.2% | 50.3% | +3.84 | -2.5 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 9 | 44.4% | 42.9% | +0.20 | -2.3 |
| 45-55% | 15 | 66.7% | 49.1% | +5.29 | -2.7 |
| 55-65% | 7 | 42.9% | 60.5% | -2.18 | -2.5 |
| 65-75% | 1 | 100.0% | 65.5% | +0.53 | -2.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 9 | 55.6% | 53.1% | -0.03 | -3.2 |
| 3-5% | 13 | 76.9% | 47.6% | +7.90 | -3.2 |
| 5-8% | 9 | 33.3% | 51.7% | -3.03 | -1.1 |
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
| (0.0, 0.4] | 82 | 17.2% | 19.5% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 82 | 19.5% | 12.7% | +41.68 | -1.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 82 | 19.5% | 12.7% | +41.68 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 82 | 19.5% | 12.7% | +41.68 | -1.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 82 | 19.5% | 12.7% | +41.68 | -1.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 58 | 22.4% | 12.4% | +41.43 | -1.4 |
| 5-8% | 24 | 12.5% | 13.6% | +0.26 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-21 | Mason Marchment Over 0.5 goals | 29.9% | 25.3% | Mason Marchment 0 goals |
| 2026-11-25 | Mason Marchment Over 0.5 goals | 27.5% | 22.2% | Mason Marchment 0 goals |
| 2026-11-21 | Mikael Backlund Over 0.5 goals | 26.4% | 22.2% | Mikael Backlund 0 goals |
| 2026-11-19 | Mathieu Olivier Over 0.5 goals | 25.9% | 18.0% | Mathieu Olivier 0 goals |
| 2026-11-23 | Mason Marchment Over 0.5 goals | 25.0% | 21.1% | Mason Marchment 0 goals |

## M9_scorer_blind

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 27 | 30.0% | 11.1% |
| (0.4, 0.5] | 10 | 44.8% | 30.0% |
| (0.5, 0.6] | 2 | 51.5% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_goals | 39 | 20.5% | 30.5% | -11.55 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 39 | 20.5% | 30.5% | -11.55 | -0.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 39 | 20.5% | 30.5% | -11.55 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 25 | 12.0% | 24.9% | -9.33 | -0.6 |
| 35-45% | 13 | 30.8% | 40.1% | -3.31 | +0.2 |
| 45-55% | 1 | 100.0% | 47.7% | +1.09 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 32 | 18.8% | 29.8% | -9.49 | -0.3 |
| 5-8% | 7 | 28.6% | 33.8% | -2.05 | -0.2 |

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
| M6_shots_v2 | 184 | -0.07 (-0.4, +0.2) | 2.5% (-7.5%, 13.6%) | undecided |
| C1_chalk | 180 | -0.34 (-0.6, -0.0) | 0.8% (-4.9%, 5.6%) | losing to the close |
| M9_scorer_blind | 39 | -0.32 (-0.7, -0.0) | -29.6% (-83.2%, 11.2%) | losing to the close |
| M3_xg_model | 63 | -1.19 (-1.5, -0.9) | -19.1% (-43.6%, 3.8%) | losing to the close |
| M2_goalie_news | 26 | -1.21 (-1.7, -0.6) | -15.2% (-53.3%, 24.0%) | losing to the close |
| M8_scorer_price | 82 | -1.15 (-1.7, -0.8) | 50.8% (-17.8%, 131.0%) | losing to the close |
| M6_shots_v2_pickem | 36 | -1.19 (-2.0, -0.4) | -19.8% (-47.2%, 11.4%) | losing to the close |
| M7_shots_under_early | 32 | -2.54 (-3.2, -2.0) | 12.0% (-20.4%, 46.5%) | losing to the close |
| B0_random | 172 | -3.14 (-3.6, -2.7) | -7.7% (-20.7%, 6.5%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
