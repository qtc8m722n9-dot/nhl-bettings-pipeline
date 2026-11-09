# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-08. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 31 bets, CLV -3.5 pp, units -0.58
- B0_random: market = player_sog: 15 bets, CLV -6.6 pp, units -1.17
- B0_random: venue = kalshi: 36 bets, CLV -2.3 pp, units -4.56
- B0_random: venue = underdog: 18 bets, CLV -4.8 pp, units -2.62
- B0_random: side_label = over: 36 bets, CLV -3.4 pp, units +3.03
- B0_random: side_label = under: 26 bets, CLV -3.2 pp, units -2.42
- B0_random: price_band = 55-65%: 17 bets, CLV -4.5 pp, units +6.78
- M1_sharp_price: predicted 66% in (0.6, 0.7] but hit 82% (40 bets)
- M4_shots_model: market = player_sog: 20 bets, CLV -5.8 pp, units -2.80
- M4_shots_model: venue = prizepicks: 15 bets, CLV -8.9 pp, units -1.15
- M4_shots_model: price_band = 55-65%: 15 bets, CLV -8.9 pp, units -1.15

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_result | 2 | 50.0% | 67.6% | -0.48 | -2.0 |
| p1_total | 3 | 33.3% | 37.9% | +0.40 | -0.5 |
| player_goals | 8 | 50.0% | 51.4% | +2.31 | -1.4 |
| player_points | 31 | 58.1% | 53.6% | -0.58 | -3.5 |
| player_sog | 15 | 53.3% | 54.9% | -1.17 | -6.6 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 5 | 40.0% | 48.6% | -0.35 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 36 | 41.7% | 50.5% | -4.56 | -2.3 |
| prizepicks | 11 | 90.9% | 57.7% | +6.32 | -4.7 |
| underdog | 18 | 50.0% | 56.1% | -2.62 | -4.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 3 | 33.3% | 69.5% | -1.48 | -2.7 |
| over | 36 | 50.0% | 45.1% | +3.03 | -3.4 |
| under | 26 | 57.7% | 62.7% | -2.42 | -3.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 13 | 30.8% | 25.0% | +1.39 | -2.3 |
| 35-45% | 5 | 40.0% | 41.3% | -0.24 | -2.1 |
| 45-55% | 13 | 30.8% | 49.8% | -5.29 | -4.2 |
| 55-65% | 17 | 82.4% | 59.4% | +6.78 | -4.5 |
| 65-75% | 9 | 55.6% | 69.3% | -1.64 | -4.1 |
| >75% | 8 | 62.5% | 81.2% | -1.86 | -1.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 65 | 52.3% | 53.3% | -0.86 | -3.3 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 6 | 100.0% | 84.9% | +1.06 | -0.7 |
| player_goals | 23 | 78.3% | 84.9% | -1.81 | -1.0 |
| player_points | 10 | 100.0% | 84.4% | +1.85 | -0.1 |
| spread | 7 | 85.7% | 84.8% | +0.08 | -0.6 |
| team_total | 11 | 63.6% | 84.6% | -2.73 | -1.9 |
| total | 8 | 75.0% | 84.8% | -0.92 | -0.4 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 65 | 81.5% | 84.8% | -2.47 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 7 | 85.7% | 84.8% | +0.08 | -0.6 |
| over | 14 | 78.6% | 84.9% | -1.04 | -0.7 |
| under | 44 | 81.8% | 84.7% | -1.51 | -0.9 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 65 | 81.5% | 84.8% | -2.47 | -0.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 65 | 81.5% | 84.8% | -2.47 | -0.9 |

## M1_sharp_price

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.6, 0.7] | 40 | 65.8% | 82.5% |
| (0.7, 0.8] | 2 | 71.2% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_points | 34 | 82.4% | 57.7% | +14.50 | +8.9 |
| player_sog | 8 | 87.5% | 57.7% | +4.12 | +6.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 42 | 83.3% | 57.7% | +18.62 | +8.4 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 42 | 83.3% | 57.7% | +18.62 | +8.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 55-65% | 42 | 83.3% | 57.7% | +18.62 | +8.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 4 | 100.0% | 57.7% | +2.93 | +4.8 |
| 5-8% | 18 | 88.9% | 57.7% | +9.71 | +7.0 |
| >8% | 20 | 75.0% | 57.7% | +5.98 | +10.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-03 | Jake Guentzel Over 0.5 points | 67.7% | 57.7% | Jake Guentzel 0 points |
| 2026-11-08 | Jake Guentzel Over 0.5 points | 67.7% | 57.7% | Jake Guentzel 0 points |
| 2026-11-08 | Leo Carlsson Over 0.5 points | 67.5% | 57.7% | Leo Carlsson 0 points |
| 2026-11-03 | Sebastian Aho Over 0.5 points | 66.6% | 57.7% | Sebastian Aho 0 points |
| 2026-11-08 | Auston Matthews Over 0.5 points | 66.6% | 57.7% | Auston Matthews 0 points |

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.4, 0.5] | 3 | 45.7% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 1 | 63.3% | 100.0% |
| (0.7, 0.8] | 4 | 73.5% | 100.0% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 2 | 0.0% | 41.2% | -2.00 | -3.0 |
| spread | 7 | 85.7% | 74.6% | +1.22 | -0.7 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 12 | 66.7% | 62.7% | -0.01 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 8 | 75.0% | 70.9% | +0.22 | -0.9 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 1 | 0.0% | 37.6% | -1.00 | -3.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 3 | 0.0% | 41.0% | -3.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 1 | 100.0% | 55.7% | +0.79 | -1.5 |
| 65-75% | 4 | 100.0% | 69.5% | +1.76 | -1.0 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 2 | 100.0% | 79.1% | +0.56 | -1.0 |
| 3-5% | 4 | 50.0% | 55.1% | -1.10 | -1.9 |
| 5-8% | 5 | 60.0% | 59.6% | +0.20 | -0.9 |
| >8% | 1 | 100.0% | 75.3% | +0.33 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-05 | VGK NOT to win | 48.7% | 44.7% | VGK 2-1 DET |
| 2026-11-01 | EDM Under 2.5 | 46.4% | 40.7% | EDM 4-1 NYR |
| 2026-11-05 | NYI to win | 41.8% | 37.6% | CAR 5-3 NYI |

## M3_xg_model

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 3 | 27.1% | 0.0% |
| (0.4, 0.5] | 5 | 45.6% | 20.0% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 5 | 66.8% | 40.0% |
| (0.7, 0.8] | 10 | 73.7% | 70.0% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 5 | 0.0% | 40.1% | -5.00 | -2.6 |
| spread | 23 | 78.3% | 75.4% | +0.51 | -1.0 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 37 | 59.5% | 63.5% | -6.13 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 24 | 75.0% | 74.1% | -0.49 | -1.0 |
| over | 5 | 40.0% | 41.5% | -1.41 | -0.7 |
| under | 4 | 50.0% | 52.2% | -0.24 | -1.3 |
| yes / favourite side | 4 | 0.0% | 39.0% | -4.00 | -2.6 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 3 | 0.0% | 22.8% | -3.00 | -0.7 |
| 35-45% | 5 | 0.0% | 40.3% | -5.00 | -2.4 |
| 45-55% | 2 | 100.0% | 48.2% | +2.16 | -1.0 |
| 55-65% | 4 | 25.0% | 59.2% | -2.21 | -1.9 |
| 65-75% | 12 | 75.0% | 69.4% | +0.88 | -1.2 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 9 | 66.7% | 71.1% | -1.41 | -0.9 |
| 3-5% | 12 | 66.7% | 62.7% | -0.58 | -1.2 |
| 5-8% | 10 | 60.0% | 58.2% | -0.87 | -1.1 |
| >8% | 6 | 33.3% | 62.6% | -3.27 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-10-31 | OTT not to win by 2+ | 74.7% | 66.6% | OTT 5-1 SJS |
| 2026-11-07 | MTL not to win by 2+ | 72.1% | 69.5% | MTL 4-2 TOR |
| 2026-11-01 | CAR not to win by 3+ | 70.4% | 66.6% | WPG 0-7 CAR |
| 2026-10-31 | PIT Under 3.5 | 70.0% | 61.7% | PIT 4-5 MTL |

## M4_shots_model

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.6, 0.7] | 10 | 64.4% | 50.0% |
| (0.7, 0.8] | 9 | 71.9% | 44.4% |
| (0.8, 1.0] | 1 | 82.5% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 20 | 50.0% | 57.4% | -2.80 | -5.8 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 15 | 53.3% | 57.8% | -1.15 | -8.9 |
| underdog | 5 | 40.0% | 56.3% | -1.65 | -2.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 10 | 50.0% | 57.7% | -1.34 | -7.0 |
| under | 10 | 50.0% | 57.0% | -1.46 | -5.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 4 | 25.0% | 53.5% | -2.13 | -3.1 |
| 55-65% | 15 | 53.3% | 57.8% | -1.15 | -8.9 |
| 65-75% | 1 | 100.0% | 67.7% | +0.48 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 2 | 100.0% | 57.8% | +1.46 | -10.9 |
| 5-8% | 6 | 16.7% | 55.6% | -4.27 | -6.1 |
| >8% | 12 | 58.3% | 58.2% | +0.01 | -3.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-03 | Jackson Blake Over 1.5 shots | 72.3% | 57.7% | Jackson Blake 1 sog |
| 2026-11-03 | Connor McDavid Over 1.5 shots | 72.2% | 57.7% | Connor McDavid 1 sog |
| 2026-11-03 | Jeremy Lauzon Over 0.5 shots | 72.2% | 57.7% | Jeremy Lauzon 0 sog |
| 2026-11-03 | Pavel Dorofeyev Over 1.5 shots | 72.0% | 57.7% | Pavel Dorofeyev 1 sog |
| 2026-11-03 | Jake Guentzel Over 1.5 shots | 71.6% | 57.7% | Jake Guentzel 0 sog |

## M6_shots_v2

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.4, 0.5] | 9 | 46.5% | 55.6% |
| (0.5, 0.6] | 27 | 54.3% | 55.6% |
| (0.6, 0.7] | 9 | 64.0% | 77.8% |
| (0.7, 0.8] | 1 | 72.2% | 0.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 46 | 58.7% | 51.0% | +7.25 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 10 | 60.0% | 55.2% | +0.82 | -0.5 |
| betrivers | 4 | 50.0% | 49.1% | +0.07 | +0.5 |
| draftkings | 16 | 56.2% | 50.8% | +1.70 | -0.2 |
| espnbet | 11 | 54.5% | 47.2% | +2.10 | +0.6 |
| fanduel | 5 | 80.0% | 53.3% | +2.55 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 21 | 47.6% | 49.0% | -0.86 | +0.1 |
| under | 25 | 68.0% | 52.8% | +8.11 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 7 | 42.9% | 41.8% | +0.00 | +0.6 |
| 45-55% | 28 | 57.1% | 49.8% | +4.67 | -0.2 |
| 55-65% | 9 | 77.8% | 58.6% | +3.07 | +0.1 |
| 65-75% | 2 | 50.0% | 65.8% | -0.49 | -1.6 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 40 | 62.5% | 50.6% | +9.79 | -0.1 |
| 5-8% | 5 | 20.0% | 53.0% | -3.23 | -0.4 |
| >8% | 1 | 100.0% | 59.2% | +0.69 | +0.4 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 65.5% | Taylor Hall 3 sog |
| 2026-11-07 | Vince Dunn Under 2.5 shots | 66.7% | 63.6% | Vince Dunn 6 sog |
| 2026-11-08 | Nikita Kucherov Over 2.5 shots | 60.5% | 57.4% | Nikita Kucherov 1 sog |
| 2026-11-07 | Evgeni Malkin Over 1.5 shots | 58.2% | 55.0% | Evgeni Malkin 1 sog |
| 2026-11-06 | Kiefer Sherwood Over 1.5 shots | 57.3% | 51.2% | Kiefer Sherwood 1 sog |

## M6_shots_v2_pickem

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.5, 0.6] | 8 | 54.9% | 37.5% |
| (0.6, 0.7] | 8 | 61.9% | 87.5% |
| (0.7, 0.8] | 1 | 72.2% | 0.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 17 | 58.8% | 55.3% | +0.98 | -0.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 6 | 83.3% | 57.7% | +2.66 | +3.0 |
| underdog | 11 | 45.5% | 54.0% | -1.68 | -2.0 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 10 | 70.0% | 55.3% | +2.50 | +1.3 |
| under | 7 | 42.9% | 55.3% | -1.52 | -2.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 8 | 37.5% | 51.3% | -2.14 | -1.5 |
| 55-65% | 8 | 87.5% | 57.8% | +4.12 | +1.5 |
| 65-75% | 1 | 0.0% | 67.7% | -1.00 | -3.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 16 | 56.2% | 55.2% | +0.24 | -0.4 |
| 5-8% | 1 | 100.0% | 57.7% | +0.73 | +2.7 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 67.7% | Taylor Hall 3 sog |
| 2026-11-03 | Zach Werenski Over 2.5 shots | 61.6% | 57.7% | Zach Werenski 2 sog |
| 2026-11-06 | Kiefer Sherwood Over 1.5 shots | 57.3% | 53.5% | Kiefer Sherwood 1 sog |
| 2026-11-07 | Jamie Benn Under 1.5 shots | 57.2% | 53.5% | Jamie Benn 3 sog |
| 2026-11-05 | Lane Hutson Under 1.5 shots | 56.9% | 53.5% | Lane Hutson 3 sog |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M1_sharp_price | 42 | +8.43 (+7.8, +9.1) | 44.3% (17.3%, 73.2%) | beating the close |
| M6_shots_v2 | 46 | -0.10 (-0.7, +0.3) | 15.8% (-7.1%, 35.0%) | undecided |
| C1_chalk | 65 | -0.86 (-1.5, -0.4) | -3.8% (-16.3%, 7.2%) | losing to the close |
| M3_xg_model | 37 | -1.18 (-1.7, -0.9) | -16.6% (-44.6%, 7.8%) | losing to the close |
| M2_goalie_news | 12 | -1.22 (-1.9, -0.4) | -0.1% (-40.0%, 41.7%) | losing to the close |
| M6_shots_v2_pickem | 17 | -0.22 (-3.9, +2.1) | 5.7% (-71.9%, 51.5%) | undecided |
| B0_random | 65 | -3.27 (-4.1, -2.6) | -1.3% (-13.7%, 15.8%) | losing to the close |
| M4_shots_model | 20 | -5.82 (-8.4, -3.1) | -14.0% (-56.8%, -0.6%) | losing to the close |
