# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-04. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 15 bets, CLV -3.4 pp, units -5.15
- B0_random: venue = kalshi: 26 bets, CLV -2.4 pp, units -4.83
- B0_random: side_label = over: 20 bets, CLV -3.3 pp, units -2.42
- M4_shots_model: market = player_sog: 20 bets, CLV -5.8 pp, units -2.80
- M4_shots_model: venue = prizepicks: 15 bets, CLV -8.9 pp, units -1.15
- M4_shots_model: price_band = 55-65%: 15 bets, CLV -8.9 pp, units -1.15

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_result | 1 | 100.0% | 65.6% | +0.52 | -3.5 |
| player_goals | 8 | 50.0% | 51.4% | +2.31 | -1.4 |
| player_points | 15 | 40.0% | 51.9% | -5.15 | -3.4 |
| player_sog | 4 | 75.0% | 55.5% | +1.17 | -6.8 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 5 | 40.0% | 48.6% | -0.35 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 26 | 38.5% | 51.6% | -4.83 | -2.4 |
| prizepicks | 2 | 100.0% | 57.7% | +1.46 | -7.7 |
| underdog | 6 | 66.7% | 56.2% | +0.87 | -4.6 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 2 | 50.0% | 69.5% | -0.48 | -3.7 |
| over | 20 | 35.0% | 40.7% | -2.42 | -3.3 |
| under | 12 | 66.7% | 70.0% | +0.40 | -2.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 10 | 30.0% | 25.1% | +0.99 | -2.2 |
| 35-45% | 2 | 50.0% | 41.2% | +0.24 | -3.2 |
| 45-55% | 6 | 33.3% | 50.9% | -2.26 | -3.7 |
| 55-65% | 5 | 80.0% | 60.5% | +1.71 | -5.3 |
| 65-75% | 4 | 50.0% | 70.4% | -1.05 | -3.9 |
| >75% | 7 | 57.1% | 81.5% | -2.12 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 34 | 47.1% | 52.7% | -2.50 | -3.0 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 3 | 100.0% | 84.9% | +0.53 | -0.7 |
| player_goals | 14 | 78.6% | 84.9% | -1.05 | -1.2 |
| player_points | 4 | 100.0% | 84.0% | +0.76 | -1.1 |
| spread | 3 | 66.7% | 84.9% | -0.65 | -0.2 |
| team_total | 5 | 80.0% | 84.6% | -0.28 | -1.1 |
| total | 5 | 60.0% | 84.8% | -1.45 | +0.0 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 34 | 79.4% | 84.7% | -2.13 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 3 | 66.7% | 84.9% | -0.65 | -0.2 |
| over | 7 | 85.7% | 84.8% | +0.08 | -0.5 |
| under | 24 | 79.2% | 84.7% | -1.56 | -1.1 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 34 | 79.4% | 84.7% | -2.13 | -0.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 34 | 79.4% | 84.7% | -2.13 | -0.9 |

## M1_sharp_price

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.6, 0.7] | 13 | 66.8% | 76.9% |
| (0.7, 0.8] | 1 | 70.9% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_points | 11 | 81.8% | 57.7% | +4.59 | +9.7 |
| player_sog | 3 | 66.7% | 57.7% | +0.46 | +7.8 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 14 | 78.6% | 57.7% | +5.05 | +9.6 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 14 | 78.6% | 57.7% | +5.05 | +9.6 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 55-65% | 14 | 78.6% | 57.7% | +5.05 | +9.6 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 5-8% | 5 | 80.0% | 57.7% | +1.93 | +7.6 |
| >8% | 9 | 77.8% | 57.7% | +3.12 | +10.7 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-03 | Jake Guentzel Over 0.5 points | 67.7% | 57.7% | Jake Guentzel 0 points |
| 2026-11-03 | Sebastian Aho Over 0.5 points | 66.6% | 57.7% | Sebastian Aho 0 points |
| 2026-11-03 | Mason McTavish Over 1.5 shots | 63.9% | 57.7% | Mason McTavish 1 sog |

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.4, 0.5] | 1 | 46.4% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 1 | 63.3% | 100.0% |
| (0.7, 0.8] | 1 | 75.2% | 100.0% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| spread | 4 | 75.0% | 78.4% | -0.10 | -0.4 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 7 | 71.4% | 65.8% | +0.67 | -0.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 4 | 75.0% | 78.4% | -0.10 | -0.4 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 1 | 0.0% | 40.7% | -1.00 | -1.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 1 | 100.0% | 55.7% | +0.79 | -1.5 |
| 65-75% | 1 | 100.0% | 69.5% | +0.44 | -1.1 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 1 | 100.0% | 87.8% | +0.14 | -0.5 |
| 5-8% | 5 | 60.0% | 59.6% | +0.20 | -0.9 |
| >8% | 1 | 100.0% | 75.3% | +0.33 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-01 | EDM Under 2.5 | 46.4% | 40.7% | EDM 4-1 NYR |

## M3_xg_model

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 2 | 27.9% | 0.0% |
| (0.4, 0.5] | 2 | 48.1% | 50.0% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 4 | 66.3% | 25.0% |
| (0.7, 0.8] | 4 | 74.6% | 50.0% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 1 | 0.0% | 61.7% | -1.00 | -1.1 |
| spread | 16 | 75.0% | 78.0% | -1.15 | -0.9 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 26 | 61.5% | 66.4% | -3.80 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 16 | 75.0% | 78.0% | -1.15 | -0.9 |
| over | 5 | 40.0% | 41.5% | -1.41 | -0.7 |
| under | 4 | 50.0% | 52.2% | -0.24 | -1.3 |
| yes / favourite side | 1 | 0.0% | 61.7% | -1.00 | -1.1 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 2 | 0.0% | 23.7% | -2.00 | +0.0 |
| 35-45% | 2 | 0.0% | 41.7% | -2.00 | -1.2 |
| 45-55% | 2 | 100.0% | 48.2% | +2.16 | -1.0 |
| 55-65% | 4 | 25.0% | 59.2% | -2.21 | -1.9 |
| 65-75% | 5 | 60.0% | 69.3% | -0.78 | -1.2 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 5 | 60.0% | 71.6% | -1.64 | -0.4 |
| 3-5% | 6 | 83.3% | 74.2% | +0.99 | -0.8 |
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
| (0.4, 0.5] | 3 | 47.4% | 66.7% |
| (0.5, 0.6] | 6 | 55.2% | 66.7% |
| (0.6, 0.7] | 3 | 63.9% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 12 | 75.0% | 51.7% | +5.23 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 1 | 100.0% | 51.2% | +0.95 | -0.1 |
| betrivers | 1 | 100.0% | 51.2% | +0.95 | -1.2 |
| draftkings | 7 | 71.4% | 51.9% | +2.40 | -0.3 |
| espnbet | 2 | 50.0% | 48.3% | +0.20 | -0.2 |
| fanduel | 1 | 100.0% | 58.0% | +0.72 | +3.6 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 4 | 75.0% | 50.9% | +1.55 | +1.3 |
| under | 8 | 75.0% | 52.1% | +3.68 | -0.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 1 | 0.0% | 40.8% | -1.00 | -0.2 |
| 45-55% | 8 | 75.0% | 49.9% | +4.22 | -0.3 |
| 55-65% | 2 | 100.0% | 57.3% | +1.49 | +1.7 |
| 65-75% | 1 | 100.0% | 66.1% | +0.51 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 12 | 75.0% | 51.7% | +5.23 | -0.1 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-03 | Philip Broberg Under 1.5 shots | 56.3% | 52.4% | Philip Broberg 4 sog |
| 2026-11-03 | Josh Anderson Under 1.5 shots | 55.9% | 51.2% | Josh Anderson 2 sog |
| 2026-11-04 | Brandon Montour Over 2.5 shots | 44.5% | 40.8% | Brandon Montour 1 sog |

## M6_shots_v2_pickem

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.5, 0.6] | 1 | 57.0% | 100.0% |
| (0.6, 0.7] | 7 | 61.9% | 85.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 8 | 87.5% | 57.1% | +4.29 | +2.6 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 6 | 83.3% | 57.7% | +2.66 | +3.0 |
| underdog | 2 | 100.0% | 55.2% | +1.63 | +1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 7 | 85.7% | 57.1% | +3.53 | +3.0 |
| under | 1 | 100.0% | 56.9% | +0.76 | -0.6 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 1 | 100.0% | 53.5% | +0.87 | +3.0 |
| 55-65% | 7 | 85.7% | 57.6% | +3.42 | +2.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 7 | 85.7% | 57.0% | +3.56 | +2.5 |
| 5-8% | 1 | 100.0% | 57.7% | +0.73 | +2.7 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-03 | Zach Werenski Over 2.5 shots | 61.6% | 57.7% | Zach Werenski 2 sog |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M1_sharp_price | 14 | +9.56 (+9.3, +9.7) | 36.1% (26.0%, 73.2%) | beating the close |
| M6_shots_v2 | 12 | -0.05 (-0.1, -0.0) | 43.6% (29.7%, 63.1%) | losing to the close |
| M3_xg_model | 26 | -0.92 (-1.1, -0.7) | -14.6% (-48.5%, 14.4%) | losing to the close |
| C1_chalk | 34 | -0.88 (-1.7, -0.3) | -6.3% (-28.0%, 14.3%) | losing to the close |
| B0_random | 34 | -2.97 (-4.1, -2.2) | -7.3% (-17.8%, 10.1%) | losing to the close |
| M4_shots_model | 20 | -5.82 (-8.4, -3.1) | -14.0% (-56.8%, -0.6%) | losing to the close |
| M2_goalie_news | 7 | -0.80 (–, –) | 9.6% (–, –) | undecided |
| M6_shots_v2_pickem | 8 | +2.56 (–, –) | 53.6% (–, –) | undecided |
