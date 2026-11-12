# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-11. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 36 bets, CLV -3.8 pp, units -3.72
- B0_random: venue = kalshi: 44 bets, CLV -2.4 pp, units -2.37
- B0_random: venue = underdog: 25 bets, CLV -4.4 pp, units -4.44
- B0_random: side_label = over: 36 bets, CLV -3.6 pp, units -1.26
- B0_random: side_label = under: 33 bets, CLV -3.2 pp, units -1.87
- B0_random: price_band = <35%: 16 bets, CLV -2.2 pp, units +2.05
- B0_random: price_band = 45-55%: 19 bets, CLV -3.9 pp, units -9.22
- M6_shots_v2: predicted 65% in (0.6, 0.7] but hit 80% (15 bets)

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 1 | 0.0% | 48.7% | -1.00 | -2.9 |
| p1_result | 2 | 50.0% | 67.6% | -0.48 | -2.0 |
| p1_total | 3 | 33.3% | 37.9% | +0.40 | -0.5 |
| player_goals | 11 | 54.5% | 49.9% | +4.19 | -1.4 |
| player_points | 36 | 50.0% | 51.3% | -3.72 | -3.8 |
| player_sog | 14 | 42.9% | 54.2% | -3.65 | -5.4 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 5 | 40.0% | 48.6% | -0.35 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 44 | 43.2% | 48.9% | -2.37 | -2.4 |
| prizepicks | 4 | 75.0% | 57.7% | +1.20 | -7.3 |
| underdog | 25 | 48.0% | 55.5% | -4.44 | -4.4 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 4 | 25.0% | 64.3% | -2.48 | -2.7 |
| over | 36 | 38.9% | 41.5% | -1.26 | -3.6 |
| under | 33 | 57.6% | 61.2% | -1.87 | -3.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 16 | 31.2% | 25.4% | +2.05 | -2.2 |
| 35-45% | 8 | 50.0% | 40.8% | +2.08 | -2.8 |
| 45-55% | 19 | 26.3% | 49.8% | -9.22 | -3.9 |
| 55-65% | 11 | 72.7% | 60.8% | +2.25 | -5.6 |
| 65-75% | 10 | 60.0% | 69.0% | -1.12 | -4.1 |
| >75% | 9 | 66.7% | 81.3% | -1.64 | -1.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 73 | 46.6% | 51.6% | -5.61 | -3.4 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 6 | 100.0% | 84.9% | +1.06 | -0.7 |
| player_goals | 27 | 77.8% | 84.9% | -2.28 | -0.8 |
| player_points | 17 | 100.0% | 84.6% | +3.09 | +0.0 |
| spread | 7 | 85.7% | 84.8% | +0.08 | -0.6 |
| team_total | 12 | 66.7% | 84.6% | -2.56 | -1.7 |
| total | 12 | 83.3% | 84.9% | -0.21 | -0.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 81 | 84.0% | 84.8% | -0.81 | -0.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 7 | 85.7% | 84.8% | +0.08 | -0.6 |
| over | 18 | 83.3% | 84.9% | -0.33 | -0.5 |
| under | 56 | 83.9% | 84.8% | -0.56 | -0.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 81 | 84.0% | 84.8% | -0.81 | -0.7 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 81 | 84.0% | 84.8% | -0.81 | -0.7 |

## M1_sharp_price

## M2_goalie_news

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.4, 0.5] | 3 | 45.7% | 0.0% |
| (0.5, 0.6] | 1 | 56.3% | 100.0% |
| (0.6, 0.7] | 2 | 65.6% | 50.0% |
| (0.7, 0.8] | 5 | 73.0% | 80.0% |
| (0.8, 1.0] | 3 | 88.0% | 66.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 2 | 0.0% | 41.2% | -2.00 | -3.0 |
| spread | 9 | 66.7% | 72.7% | -0.78 | -1.0 |
| team_total | 3 | 66.7% | 49.1% | +0.76 | -1.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 14 | 57.1% | 63.1% | -2.01 | -1.3 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 10 | 60.0% | 69.9% | -1.78 | -1.2 |
| under | 3 | 66.7% | 49.1% | +0.76 | -1.3 |
| yes / favourite side | 1 | 0.0% | 37.6% | -1.00 | -3.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 3 | 0.0% | 41.0% | -3.00 | -2.5 |
| 45-55% | 1 | 100.0% | 50.7% | +0.97 | -1.0 |
| 55-65% | 2 | 50.0% | 60.2% | -0.21 | -2.0 |
| 65-75% | 5 | 80.0% | 69.1% | +0.76 | -1.2 |
| >75% | 3 | 66.7% | 81.4% | -0.53 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 2 | 100.0% | 79.1% | +0.56 | -1.0 |
| 3-5% | 6 | 33.3% | 58.8% | -3.10 | -2.0 |
| 5-8% | 5 | 60.0% | 59.6% | +0.20 | -0.9 |
| >8% | 1 | 100.0% | 75.3% | +0.33 | -0.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-11-09 | PHI not to win by 2+ | 70.7% | 67.6% | PHI 3-1 VAN |
| 2026-11-09 | EDM not to win by 2+ | 68.0% | 64.6% | NYR 1-3 EDM |
| 2026-11-05 | VGK NOT to win | 48.7% | 44.7% | VGK 2-1 DET |
| 2026-11-01 | EDM Under 2.5 | 46.4% | 40.7% | EDM 4-1 NYR |

## M3_xg_model

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.0, 0.4] | 4 | 30.2% | 0.0% |
| (0.4, 0.5] | 6 | 45.4% | 16.7% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 7 | 67.3% | 42.9% |
| (0.7, 0.8] | 13 | 73.2% | 61.5% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 7 | 0.0% | 39.7% | -7.00 | -2.3 |
| spread | 28 | 71.4% | 73.9% | -1.55 | -1.0 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 44 | 54.5% | 62.8% | -10.20 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 29 | 69.0% | 72.9% | -2.55 | -1.1 |
| over | 5 | 40.0% | 41.5% | -1.41 | -0.7 |
| under | 4 | 50.0% | 52.2% | -0.24 | -1.3 |
| yes / favourite side | 6 | 0.0% | 38.9% | -6.00 | -2.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 3 | 0.0% | 22.8% | -3.00 | -0.7 |
| 35-45% | 7 | 0.0% | 39.8% | -7.00 | -2.2 |
| 45-55% | 2 | 100.0% | 48.2% | +2.16 | -1.0 |
| 55-65% | 5 | 20.0% | 60.3% | -3.21 | -2.0 |
| 65-75% | 16 | 68.8% | 69.0% | -0.18 | -1.1 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 12 | 58.3% | 67.7% | -2.90 | -0.8 |
| 3-5% | 16 | 56.2% | 62.2% | -3.15 | -1.4 |
| 5-8% | 10 | 60.0% | 58.2% | -0.87 | -1.1 |
| >8% | 6 | 33.3% | 62.6% | -3.27 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-10-31 | OTT not to win by 2+ | 74.7% | 66.6% | OTT 5-1 SJS |
| 2026-11-07 | MTL not to win by 2+ | 72.1% | 69.5% | MTL 4-2 TOR |
| 2026-11-11 | TBL not to win by 2+ | 71.5% | 68.6% | TBL 8-3 BUF |
| 2026-11-09 | PHI not to win by 2+ | 70.7% | 67.6% | PHI 3-1 VAN |

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
| (0.4, 0.5] | 13 | 46.4% | 53.8% |
| (0.5, 0.6] | 33 | 54.1% | 54.5% |
| (0.6, 0.7] | 15 | 64.6% | 80.0% |
| (0.7, 0.8] | 2 | 72.2% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 63 | 60.3% | 51.4% | +10.84 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 16 | 56.2% | 54.0% | +0.11 | +0.1 |
| betrivers | 5 | 60.0% | 48.9% | +1.15 | +0.8 |
| draftkings | 22 | 59.1% | 52.6% | +2.44 | -0.4 |
| espnbet | 15 | 60.0% | 47.2% | +4.59 | +0.1 |
| fanduel | 5 | 80.0% | 53.3% | +2.55 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 28 | 53.6% | 49.3% | +1.88 | +0.2 |
| under | 35 | 65.7% | 53.1% | +8.97 | -0.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 12 | 41.7% | 41.6% | -0.10 | -0.5 |
| 45-55% | 33 | 57.6% | 49.8% | +5.65 | +0.1 |
| 55-65% | 15 | 86.7% | 59.9% | +6.77 | -0.1 |
| 65-75% | 3 | 33.3% | 65.7% | -1.49 | -1.0 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 53 | 66.0% | 51.3% | +15.84 | -0.1 |
| 5-8% | 8 | 25.0% | 52.1% | -4.69 | -0.2 |
| >8% | 2 | 50.0% | 50.9% | -0.31 | -0.3 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 65.5% | Taylor Hall 3 sog |
| 2026-11-10 | Noah Dobson Under 2.5 shots | 69.5% | 65.5% | Noah Dobson 3 sog |
| 2026-11-07 | Vince Dunn Under 2.5 shots | 66.7% | 63.6% | Vince Dunn 6 sog |
| 2026-11-08 | Nikita Kucherov Over 2.5 shots | 60.5% | 57.4% | Nikita Kucherov 1 sog |
| 2026-11-07 | Evgeni Malkin Over 1.5 shots | 58.2% | 55.0% | Evgeni Malkin 1 sog |

## M6_shots_v2_pickem

Calibration (does the stated probability come true?):

| Predicted | n | Avg predicted | Actual |
|---|--:|--:|--:|
| (0.5, 0.6] | 11 | 54.7% | 27.3% |
| (0.6, 0.7] | 3 | 61.7% | 66.7% |
| (0.7, 0.8] | 2 | 72.2% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 16 | 37.5% | 54.3% | -5.15 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| underdog | 16 | 37.5% | 54.3% | -5.15 | -1.5 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 6 | 33.3% | 52.5% | -2.16 | -0.7 |
| under | 10 | 40.0% | 55.3% | -2.98 | -2.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 11 | 27.3% | 50.9% | -5.14 | -1.4 |
| 55-65% | 3 | 66.7% | 58.3% | +0.46 | -2.4 |
| 65-75% | 2 | 50.0% | 66.4% | -0.47 | -1.3 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 14 | 35.7% | 54.0% | -4.68 | -1.5 |
| 5-8% | 2 | 50.0% | 56.0% | -0.47 | -1.9 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-07 | Taylor Hall Under 2.5 shots | 72.2% | 67.7% | Taylor Hall 3 sog |
| 2026-11-10 | Blake Coleman Over 1.5 shots | 62.7% | 59.4% | Blake Coleman 1 sog |
| 2026-11-06 | Kiefer Sherwood Over 1.5 shots | 57.3% | 53.5% | Kiefer Sherwood 1 sog |
| 2026-11-07 | Jamie Benn Under 1.5 shots | 57.2% | 53.5% | Jamie Benn 3 sog |
| 2026-11-05 | Lane Hutson Under 1.5 shots | 56.9% | 53.5% | Lane Hutson 3 sog |

## Toward one model

Goal: one final model that uses what every method has learned. The combined model takes each method's signal (game model, shots model, goalie news, sharp price, pick'em prices) plus the fair price as inputs, trained on the shadow board (every priced line, data/shadow/). It replaces the strongest single method only if it beats it out of sample on CLV and log loss. Review point: 2026-12-31, or once each live method has 300 settled singles. Single methods whose CLV interval is entirely below 0 add no value as bets, but their signals can still help the combined model.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M6_shots_v2 | 63 | -0.12 (-0.7, +0.3) | 17.2% (0.6%, 32.6%) | undecided |
| C1_chalk | 81 | -0.65 (-1.2, -0.2) | -1.0% (-11.6%, 8.3%) | losing to the close |
| M3_xg_model | 44 | -1.19 (-1.6, -0.9) | -23.2% (-49.7%, 0.0%) | losing to the close |
| M2_goalie_news | 14 | -1.34 (-2.0, -0.6) | -14.4% (-59.4%, 27.8%) | losing to the close |
| M6_shots_v2_pickem | 16 | -1.55 (-3.0, +0.3) | -32.2% (-78.1%, 30.0%) | undecided |
| B0_random | 73 | -3.38 (-4.1, -2.7) | -7.7% (-19.6%, 4.1%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
