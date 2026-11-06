# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-05. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 22 bets, CLV -3.5 pp, units -3.49
- B0_random: venue = kalshi: 30 bets, CLV -2.3 pp, units -3.81
- B0_random: side_label = over: 25 bets, CLV -3.1 pp, units -0.56
- B0_random: side_label = under: 17 bets, CLV -2.8 pp, units +2.33
- M1_sharp_price: predicted 66% in (0.6, 0.7] but hit 81% (21 bets)
- M4_shots_model: market = player_sog: 20 bets, CLV -5.8 pp, units -2.80
- M4_shots_model: venue = prizepicks: 15 bets, CLV -8.9 pp, units -1.15
- M4_shots_model: price_band = 55-65%: 15 bets, CLV -8.9 pp, units -1.15

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_result | 2 | 50.0% | 67.6% | -0.48 | -2.0 |
| p1_total | 1 | 100.0% | 29.4% | +2.40 | +1.5 |
| player_goals | 8 | 50.0% | 51.4% | +2.31 | -1.4 |
| player_points | 22 | 50.0% | 51.8% | -3.49 | -3.5 |
| player_sog | 6 | 66.7% | 54.8% | +0.90 | -6.8 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 5 | 40.0% | 48.6% | -0.35 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 30 | 40.0% | 50.8% | -3.81 | -2.3 |
| prizepicks | 5 | 100.0% | 57.7% | +3.66 | -5.3 |
| underdog | 10 | 60.0% | 54.8% | +0.44 | -4.0 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 3 | 33.3% | 69.5% | -1.48 | -2.7 |
| over | 25 | 40.0% | 41.2% | -0.56 | -3.1 |
| under | 17 | 70.6% | 66.0% | +2.33 | -2.8 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 12 | 33.3% | 25.2% | +2.39 | -2.1 |
| 35-45% | 2 | 50.0% | 41.2% | +0.24 | -3.2 |
| 45-55% | 9 | 33.3% | 50.4% | -3.28 | -3.4 |
| 55-65% | 10 | 90.0% | 60.0% | +5.12 | -4.6 |
| 65-75% | 5 | 40.0% | 70.3% | -2.05 | -3.2 |
| >75% | 7 | 57.1% | 81.5% | -2.12 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 45 | 51.1% | 52.5% | +0.29 | -2.9 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 5 | 100.0% | 84.9% | +0.89 | -0.8 |
| player_goals | 15 | 80.0% | 84.9% | -0.87 | -1.2 |
| player_points | 5 | 100.0% | 84.0% | +0.95 | -1.2 |
| spread | 5 | 80.0% | 84.8% | -0.28 | -0.4 |
| team_total | 8 | 75.0% | 84.6% | -0.91 | -1.2 |
| total | 7 | 71.4% | 84.8% | -1.10 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 45 | 82.2% | 84.7% | -1.32 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 5 | 80.0% | 84.8% | -0.28 | -0.4 |
| over | 11 | 81.8% | 84.9% | -0.39 | -0.7 |
| under | 29 | 82.8% | 84.6% | -0.65 | -1.1 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 45 | 82.2% | 84.7% | -1.32 | -0.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 45 | 82.2% | 84.7% | -1.32 | -0.9 |

## M1_sharp_price

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.6, 0.7] | 21 | 66.2% | 81.0% |
| (0.7, 0.8] | 1 | 70.9% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_points | 16 | 81.2% | 57.7% | +6.52 | +9.4 |
| player_sog | 6 | 83.3% | 57.7% | +2.66 | +7.0 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 22 | 81.8% | 57.7% | +9.18 | +8.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 22 | 81.8% | 57.7% | +9.18 | +8.8 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 55-65% | 22 | 81.8% | 57.7% | +9.18 | +8.8 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 1 | 100.0% | 57.7% | +0.73 | +5.1 |
| 5-8% | 10 | 80.0% | 57.7% | +3.86 | +7.5 |
| >8% | 11 | 81.8% | 57.7% | +4.59 | +10.6 |

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
| (0.7, 0.8] | 2 | 74.1% | 100.0% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 2 | 0.0% | 41.2% | -2.00 | -3.0 |
| spread | 5 | 80.0% | 76.9% | +0.32 | -0.6 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 10 | 60.0% | 61.4% | -0.91 | -1.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 6 | 66.7% | 71.5% | -0.68 | -1.0 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 1 | 0.0% | 37.6% | -1.00 | -3.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 3 | 0.0% | 41.0% | -3.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 1 | 100.0% | 55.7% | +0.79 | -1.5 |
| 65-75% | 2 | 100.0% | 70.0% | +0.86 | -1.3 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 2 | 100.0% | 79.1% | +0.56 | -1.0 |
| 3-5% | 2 | 0.0% | 41.2% | -2.00 | -3.0 |
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
| (0.4, 0.5] | 4 | 46.7% | 25.0% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 4 | 66.3% | 25.0% |
| (0.7, 0.8] | 5 | 74.3% | 60.0% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 4 | 0.0% | 41.3% | -4.00 | -2.3 |
| spread | 17 | 76.5% | 77.6% | -0.73 | -0.9 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 30 | 56.7% | 63.3% | -6.38 | -1.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 18 | 72.2% | 75.7% | -1.73 | -1.0 |
| over | 5 | 40.0% | 41.5% | -1.41 | -0.7 |
| under | 4 | 50.0% | 52.2% | -0.24 | -1.3 |
| yes / favourite side | 3 | 0.0% | 40.1% | -3.00 | -2.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 3 | 0.0% | 22.8% | -3.00 | -0.7 |
| 35-45% | 4 | 0.0% | 41.4% | -4.00 | -2.1 |
| 45-55% | 2 | 100.0% | 48.2% | +2.16 | -1.0 |
| 55-65% | 4 | 25.0% | 59.2% | -2.21 | -1.9 |
| 65-75% | 6 | 66.7% | 69.5% | -0.36 | -1.3 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 6 | 66.7% | 71.4% | -1.22 | -0.6 |
| 3-5% | 9 | 55.6% | 61.0% | -2.01 | -1.4 |
| 5-8% | 9 | 66.7% | 60.7% | +0.13 | -0.8 |
| >8% | 6 | 33.3% | 62.6% | -3.27 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-10-31 | OTT not to win by 2+ | 74.7% | 66.6% | OTT 5-1 SJS |
| 2026-11-01 | CAR not to win by 3+ | 70.4% | 66.6% | WPG 0-7 CAR |
| 2026-10-31 | PIT Under 3.5 | 70.0% | 61.7% | PIT 4-5 MTL |
| 2026-11-02 | COL not to win by 2+ | 67.5% | 57.7% | COL 5-2 CHI |

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
| (0.4, 0.5] | 6 | 46.8% | 66.7% |
| (0.5, 0.6] | 15 | 54.2% | 60.0% |
| (0.6, 0.7] | 5 | 64.4% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 26 | 69.2% | 50.4% | +9.37 | +0.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 5 | 80.0% | 55.1% | +2.24 | -0.5 |
| betrivers | 2 | 50.0% | 47.1% | -0.05 | -0.9 |
| draftkings | 11 | 63.6% | 50.1% | +2.60 | +0.2 |
| espnbet | 7 | 71.4% | 47.4% | +3.85 | +0.7 |
| fanduel | 1 | 100.0% | 58.0% | +0.72 | +3.6 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 11 | 63.6% | 48.6% | +2.90 | +0.6 |
| under | 15 | 73.3% | 51.7% | +6.47 | -0.1 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 4 | 50.0% | 42.0% | +0.75 | +1.0 |
| 45-55% | 16 | 62.5% | 49.2% | +4.43 | -0.2 |
| 55-65% | 5 | 100.0% | 57.7% | +3.67 | +1.3 |
| 65-75% | 1 | 100.0% | 66.1% | +0.51 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 23 | 73.9% | 50.4% | +10.68 | +0.1 |
| 5-8% | 2 | 0.0% | 46.0% | -2.00 | +1.4 |
| >8% | 1 | 100.0% | 59.2% | +0.69 | +0.4 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-05 | Lane Hutson Under 1.5 shots | 56.9% | 53.5% | Lane Hutson 3 sog |
| 2026-11-03 | Philip Broberg Under 1.5 shots | 56.3% | 52.4% | Philip Broberg 4 sog |
| 2026-11-03 | Josh Anderson Under 1.5 shots | 55.9% | 51.2% | Josh Anderson 2 sog |
| 2026-11-05 | Valeri Nichushkin Over 1.5 shots | 52.4% | 46.5% | Valeri Nichushkin 1 sog |
| 2026-11-05 | Porter Martone Over 1.5 shots | 51.3% | 47.6% | Porter Martone 1 sog |

## M6_shots_v2_pickem

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.5, 0.6] | 4 | 54.3% | 25.0% |
| (0.6, 0.7] | 7 | 61.9% | 85.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 11 | 63.6% | 55.1% | +1.29 | +1.7 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 6 | 83.3% | 57.7% | +2.66 | +3.0 |
| underdog | 5 | 40.0% | 52.0% | -1.37 | +0.1 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 8 | 75.0% | 56.1% | +2.53 | +2.5 |
| under | 3 | 33.3% | 52.7% | -1.24 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 4 | 25.0% | 50.8% | -2.13 | +0.3 |
| 55-65% | 7 | 85.7% | 57.6% | +3.42 | +2.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 10 | 60.0% | 54.9% | +0.56 | +1.6 |
| 5-8% | 1 | 100.0% | 57.7% | +0.73 | +2.7 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-03 | Zach Werenski Over 2.5 shots | 61.6% | 57.7% | Zach Werenski 2 sog |
| 2026-11-05 | Lane Hutson Under 1.5 shots | 56.9% | 53.5% | Lane Hutson 3 sog |
| 2026-11-05 | Valeri Nichushkin Over 1.5 shots | 52.4% | 48.6% | Valeri Nichushkin 1 sog |
| 2026-11-05 | Mavrik Bourque Under 1.5 shots | 51.1% | 47.7% | Mavrik Bourque 3 sog |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M1_sharp_price | 22 | +8.81 (+7.9, +9.7) | 41.7% (26.0%, 73.2%) | beating the close |
| M6_shots_v2 | 26 | +0.24 (-0.1, +0.5) | 36.0% (29.6%, 63.1%) | undecided |
| M6_shots_v2_pickem | 11 | +1.70 (-0.6, +2.6) | 11.7% (-100.0%, 53.6%) | undecided |
| C1_chalk | 45 | -0.93 (-1.5, -0.4) | -2.9% (-22.1%, 12.5%) | losing to the close |
| M3_xg_model | 30 | -1.12 (-1.7, -0.8) | -21.3% (-54.8%, 8.9%) | losing to the close |
| M2_goalie_news | 10 | -1.31 (-2.1, -0.3) | -9.1% (-60.8%, 36.1%) | losing to the close |
| B0_random | 45 | -2.92 (-3.9, -2.3) | 0.7% (-14.9%, 19.4%) | losing to the close |
| M4_shots_model | 20 | -5.82 (-8.4, -3.1) | -14.0% (-56.8%, -0.6%) | losing to the close |
