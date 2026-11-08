# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-07. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 29 bets, CLV -3.5 pp, units -0.31
- B0_random: venue = kalshi: 36 bets, CLV -2.3 pp, units -4.56
- B0_random: venue = underdog: 16 bets, CLV -4.4 pp, units -0.62
- B0_random: side_label = over: 33 bets, CLV -3.5 pp, units +0.83
- B0_random: side_label = under: 24 bets, CLV -2.9 pp, units -0.42
- M1_sharp_price: predicted 66% in (0.6, 0.7] but hit 88% (34 bets)
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
| player_points | 29 | 58.6% | 53.0% | -0.31 | -3.5 |
| player_sog | 12 | 50.0% | 55.2% | -1.64 | -6.2 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 5 | 40.0% | 48.6% | -0.35 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 36 | 41.7% | 50.5% | -4.56 | -2.3 |
| prizepicks | 8 | 87.5% | 57.7% | +4.12 | -6.1 |
| underdog | 16 | 56.2% | 55.9% | -0.62 | -4.4 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 3 | 33.3% | 69.5% | -1.48 | -2.7 |
| over | 33 | 45.5% | 43.9% | +0.83 | -3.5 |
| under | 24 | 62.5% | 63.2% | -0.42 | -2.9 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 13 | 30.8% | 25.0% | +1.39 | -2.3 |
| 35-45% | 5 | 40.0% | 41.3% | -0.24 | -2.1 |
| 45-55% | 12 | 33.3% | 50.1% | -4.29 | -3.7 |
| 55-65% | 14 | 78.6% | 59.7% | +4.59 | -5.1 |
| 65-75% | 8 | 62.5% | 69.4% | -0.64 | -3.9 |
| >75% | 8 | 62.5% | 81.2% | -1.86 | -1.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 60 | 51.7% | 52.9% | -1.06 | -3.2 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 6 | 100.0% | 84.9% | +1.06 | -0.7 |
| player_goals | 21 | 76.2% | 84.9% | -2.16 | -0.8 |
| player_points | 8 | 100.0% | 84.3% | +1.49 | -0.7 |
| spread | 6 | 83.3% | 84.8% | -0.10 | -0.6 |
| team_total | 10 | 70.0% | 84.6% | -1.73 | -1.9 |
| total | 8 | 75.0% | 84.8% | -0.92 | -0.4 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 59 | 81.4% | 84.7% | -2.37 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 6 | 83.3% | 84.8% | -0.10 | -0.6 |
| over | 13 | 84.6% | 84.9% | -0.04 | -0.7 |
| under | 40 | 80.0% | 84.7% | -2.23 | -1.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 59 | 81.4% | 84.7% | -2.37 | -0.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 59 | 81.4% | 84.7% | -2.37 | -0.9 |

## M1_sharp_price

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.6, 0.7] | 34 | 65.8% | 88.2% |
| (0.7, 0.8] | 2 | 71.2% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_points | 29 | 89.7% | 57.7% | +16.03 | +8.8 |
| player_sog | 7 | 85.7% | 57.7% | +3.39 | +6.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 36 | 88.9% | 57.7% | +19.43 | +8.4 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 36 | 88.9% | 57.7% | +19.43 | +8.4 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 55-65% | 36 | 88.9% | 57.7% | +19.43 | +8.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 3 | 100.0% | 57.7% | +2.20 | +5.0 |
| 5-8% | 17 | 88.2% | 57.7% | +8.98 | +7.0 |
| >8% | 16 | 87.5% | 57.7% | +8.25 | +10.9 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-03 | Jake Guentzel Over 0.5 points | 67.7% | 57.7% | Jake Guentzel 0 points |
| 2026-11-03 | Sebastian Aho Over 0.5 points | 66.6% | 57.7% | Sebastian Aho 0 points |
| 2026-11-05 | Jason Robertson Over 0.5 points | 64.8% | 57.7% | Jason Robertson 0 points |
| 2026-11-03 | Mason McTavish Over 1.5 shots | 63.9% | 57.7% | Mason McTavish 1 sog |

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.4, 0.5] | 3 | 45.7% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 1 | 63.3% | 100.0% |
| (0.7, 0.8] | 3 | 73.0% | 100.0% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 2 | 0.0% | 41.2% | -2.00 | -3.0 |
| spread | 6 | 83.3% | 75.1% | +0.82 | -0.5 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 11 | 63.6% | 61.9% | -0.41 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 7 | 71.4% | 70.8% | -0.18 | -0.8 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 1 | 0.0% | 37.6% | -1.00 | -3.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 3 | 0.0% | 41.0% | -3.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 1 | 100.0% | 55.7% | +0.79 | -1.5 |
| 65-75% | 3 | 100.0% | 68.9% | +1.36 | -0.8 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 2 | 100.0% | 79.1% | +0.56 | -1.0 |
| 3-5% | 3 | 33.3% | 49.6% | -1.50 | -2.0 |
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
| (0.7, 0.8] | 9 | 73.6% | 66.7% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 5 | 0.0% | 40.1% | -5.00 | -2.6 |
| spread | 22 | 77.3% | 75.6% | +0.12 | -0.9 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 36 | 58.3% | 63.3% | -6.53 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 23 | 73.9% | 74.2% | -0.88 | -1.0 |
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
| 65-75% | 11 | 72.7% | 69.2% | +0.48 | -1.1 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 9 | 66.7% | 71.1% | -1.41 | -0.9 |
| 3-5% | 11 | 63.6% | 61.9% | -0.98 | -1.2 |
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
| (0.4, 0.5] | 7 | 47.1% | 71.4% |
| (0.5, 0.6] | 24 | 54.5% | 54.2% |
| (0.6, 0.7] | 8 | 64.4% | 87.5% |
| (0.7, 0.8] | 1 | 72.2% | 0.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 40 | 62.5% | 51.6% | +9.19 | +0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 9 | 66.7% | 56.1% | +1.82 | -0.6 |
| betrivers | 4 | 50.0% | 49.1% | +0.07 | +0.5 |
| draftkings | 14 | 64.3% | 51.0% | +3.70 | +0.1 |
| espnbet | 10 | 60.0% | 48.1% | +3.10 | +0.5 |
| fanduel | 3 | 66.7% | 56.0% | +0.49 | +0.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 17 | 52.9% | 49.5% | +1.12 | +0.6 |
| under | 23 | 69.6% | 53.1% | +8.07 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 5 | 60.0% | 42.5% | +2.00 | +1.1 |
| 45-55% | 25 | 56.0% | 50.0% | +3.61 | -0.1 |
| 55-65% | 8 | 87.5% | 58.8% | +4.07 | +0.3 |
| 65-75% | 2 | 50.0% | 65.8% | -0.49 | -1.6 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 34 | 67.6% | 51.1% | +11.73 | +0.1 |
| 5-8% | 5 | 20.0% | 53.0% | -3.23 | -0.4 |
| >8% | 1 | 100.0% | 59.2% | +0.69 | +0.4 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 65.5% | Taylor Hall 3 sog |
| 2026-11-07 | Vince Dunn Under 2.5 shots | 66.7% | 63.6% | Vince Dunn 6 sog |
| 2026-11-07 | Evgeni Malkin Over 1.5 shots | 58.2% | 55.0% | Evgeni Malkin 1 sog |
| 2026-11-06 | Kiefer Sherwood Over 1.5 shots | 57.3% | 51.2% | Kiefer Sherwood 1 sog |
| 2026-11-07 | Jamie Benn Under 1.5 shots | 57.2% | 53.5% | Jamie Benn 3 sog |

## M6_shots_v2_pickem

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.5, 0.6] | 7 | 55.0% | 28.6% |
| (0.6, 0.7] | 8 | 61.9% | 87.5% |
| (0.7, 0.8] | 1 | 72.2% | 0.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 16 | 56.2% | 55.6% | +0.01 | +0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 6 | 83.3% | 57.7% | +2.66 | +3.0 |
| underdog | 10 | 40.0% | 54.3% | -2.65 | -1.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 9 | 66.7% | 55.8% | +1.53 | +2.0 |
| under | 7 | 42.9% | 55.3% | -1.52 | -2.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 7 | 28.6% | 51.4% | -3.11 | -0.9 |
| 55-65% | 8 | 87.5% | 57.8% | +4.12 | +1.5 |
| 65-75% | 1 | 0.0% | 67.7% | -1.00 | -3.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 15 | 53.3% | 55.4% | -0.72 | -0.1 |
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
| M1_sharp_price | 36 | +8.44 (+7.7, +9.3) | 54.0% (33.2%, 73.2%) | beating the close |
| M6_shots_v2 | 40 | +0.09 (-0.3, +0.4) | 23.0% (2.7%, 40.4%) | undecided |
| C1_chalk | 59 | -0.87 (-1.6, -0.4) | -4.0% (-17.9%, 7.8%) | losing to the close |
| M3_xg_model | 36 | -1.16 (-1.6, -0.9) | -18.2% (-48.9%, 8.3%) | losing to the close |
| M2_goalie_news | 11 | -1.18 (-2.0, -0.1) | -3.7% (-47.7%, 39.2%) | losing to the close |
| M6_shots_v2_pickem | 16 | +0.09 (-3.4, +2.2) | 0.1% (-100.0%, 45.0%) | undecided |
| B0_random | 60 | -3.17 (-3.9, -2.4) | -1.8% (-15.2%, 16.2%) | losing to the close |
| M4_shots_model | 20 | -5.82 (-8.4, -3.1) | -14.0% (-56.8%, -0.6%) | losing to the close |
