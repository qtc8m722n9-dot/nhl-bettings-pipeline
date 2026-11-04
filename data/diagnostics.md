# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-03. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: venue = kalshi: 25 bets, CLV -2.4 pp, units -6.06
- B0_random: side_label = over: 17 bets, CLV -2.8 pp, units -1.15
- M4_shots_model: market = player_sog: 20 bets, CLV -5.8 pp, units -2.80
- M4_shots_model: venue = prizepicks: 15 bets, CLV -8.9 pp, units -1.15
- M4_shots_model: price_band = 55-65%: 15 bets, CLV -8.9 pp, units -1.15

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_result | 1 | 100.0% | 65.6% | +0.52 | -3.5 |
| player_goals | 8 | 50.0% | 51.4% | +2.31 | -1.4 |
| player_points | 13 | 38.5% | 52.3% | -5.39 | -3.4 |
| player_sog | 2 | 100.0% | 58.2% | +1.43 | -6.4 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 5 | 40.0% | 48.6% | -0.35 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 25 | 36.0% | 51.8% | -6.06 | -2.4 |
| prizepicks | 1 | 100.0% | 57.7% | +0.73 | – |
| underdog | 4 | 100.0% | 59.0% | +2.87 | -4.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 2 | 50.0% | 69.5% | -0.48 | -3.7 |
| over | 17 | 35.3% | 38.6% | -1.15 | -2.8 |
| under | 11 | 63.6% | 72.3% | -0.84 | -2.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 10 | 30.0% | 25.1% | +0.99 | -2.2 |
| 35-45% | 1 | 0.0% | 37.6% | -1.00 | -3.1 |
| 45-55% | 4 | 50.0% | 51.1% | -0.26 | -3.0 |
| 55-65% | 4 | 75.0% | 61.2% | +0.98 | -4.4 |
| 65-75% | 4 | 50.0% | 70.4% | -1.05 | -3.9 |
| >75% | 7 | 57.1% | 81.5% | -2.12 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 30 | 46.7% | 53.0% | -2.47 | -2.6 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 3 | 100.0% | 84.9% | +0.53 | -0.7 |
| player_goals | 12 | 75.0% | 84.9% | -1.40 | -1.4 |
| player_points | 3 | 100.0% | 83.7% | +0.59 | -1.0 |
| spread | 3 | 66.7% | 84.9% | -0.65 | -0.2 |
| team_total | 5 | 80.0% | 84.6% | -0.28 | -1.1 |
| total | 4 | 75.0% | 84.7% | -0.45 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 30 | 80.0% | 84.7% | -1.66 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 3 | 66.7% | 84.9% | -0.65 | -0.2 |
| over | 6 | 100.0% | 84.8% | +1.08 | -0.7 |
| under | 21 | 76.2% | 84.6% | -2.10 | -1.1 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 30 | 80.0% | 84.7% | -1.66 | -0.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 30 | 80.0% | 84.7% | -1.66 | -0.9 |

## M1_sharp_price

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.6, 0.7] | 10 | 66.8% | 70.0% |
| (0.7, 0.8] | 1 | 70.9% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_points | 8 | 75.0% | 57.7% | +2.39 | +9.9 |
| player_sog | 3 | 66.7% | 57.7% | +0.46 | +7.8 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 11 | 72.7% | 57.7% | +2.86 | +9.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 11 | 72.7% | 57.7% | +2.86 | +9.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 55-65% | 11 | 72.7% | 57.7% | +2.86 | +9.7 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 5-8% | 4 | 75.0% | 57.7% | +1.20 | +8.4 |
| >8% | 7 | 71.4% | 57.7% | +1.66 | +10.5 |

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
| (0.4, 0.5] | 1 | 48.8% | 100.0% |
| (0.5, 0.6] | 3 | 56.4% | 33.3% |
| (0.6, 0.7] | 3 | 63.9% | 100.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 7 | 71.4% | 54.7% | +2.08 | -0.0 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| draftkings | 5 | 80.0% | 54.8% | +2.35 | -0.4 |
| espnbet | 1 | 0.0% | 51.2% | -1.00 | -1.9 |
| fanduel | 1 | 100.0% | 58.0% | +0.72 | +3.6 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 2 | 100.0% | 55.7% | +1.59 | +3.3 |
| under | 5 | 60.0% | 54.3% | +0.48 | -1.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 4 | 50.0% | 50.6% | +0.07 | -0.5 |
| 55-65% | 2 | 100.0% | 57.3% | +1.49 | +1.7 |
| 65-75% | 1 | 100.0% | 66.1% | +0.51 | -1.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 7 | 71.4% | 54.7% | +2.08 | -0.0 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-03 | Philip Broberg Under 1.5 shots | 56.3% | 52.4% | Philip Broberg 4 sog |
| 2026-11-03 | Josh Anderson Under 1.5 shots | 55.9% | 51.2% | Josh Anderson 2 sog |

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
| M3_xg_model | 26 | -0.92 (-1.1, -0.7) | -14.6% (-48.5%, 14.4%) | losing to the close |
| C1_chalk | 30 | -0.95 (-1.9, -0.4) | -5.5% (-36.5%, 18.0%) | losing to the close |
| B0_random | 30 | -2.64 (-3.4, -2.0) | -8.2% (-18.6%, 15.8%) | losing to the close |
| M4_shots_model | 20 | -5.82 (-8.4, -3.1) | -14.0% (-56.8%, -0.6%) | losing to the close |
| M1_sharp_price | 11 | +9.68 (–, –) | 26.0% (26.0%, 26.0%) | undecided |
| M2_goalie_news | 7 | -0.80 (–, –) | 9.6% (–, –) | undecided |
| M6_shots_v2 | 7 | -0.03 (–, –) | 29.7% (–, –) | undecided |
| M6_shots_v2_pickem | 8 | +2.56 (–, –) | 53.6% (–, –) | undecided |
