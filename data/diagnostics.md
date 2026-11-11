# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-10. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: market = player_points: 33 bets, CLV -3.8 pp, units -3.31
- B0_random: venue = kalshi: 40 bets, CLV -2.4 pp, units -5.83
- B0_random: venue = underdog: 24 bets, CLV -4.5 pp, units -3.44
- B0_random: side_label = over: 32 bets, CLV -3.6 pp, units -3.50
- B0_random: side_label = under: 31 bets, CLV -3.3 pp, units -1.09
- B0_random: price_band = <35%: 15 bets, CLV -2.3 pp, units -0.61
- B0_random: price_band = 45-55%: 18 bets, CLV -3.9 pp, units -8.22

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 1 | 0.0% | 48.7% | -1.00 | -2.9 |
| p1_result | 2 | 50.0% | 67.6% | -0.48 | -2.0 |
| p1_total | 3 | 33.3% | 37.9% | +0.40 | -0.5 |
| player_goals | 9 | 44.4% | 48.8% | +1.31 | -1.5 |
| player_points | 33 | 51.5% | 51.7% | -3.31 | -3.8 |
| player_sog | 13 | 46.2% | 54.5% | -2.65 | -5.6 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 5 | 40.0% | 48.6% | -0.35 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 40 | 40.0% | 48.9% | -5.83 | -2.4 |
| prizepicks | 3 | 100.0% | 57.7% | +2.20 | -7.5 |
| underdog | 24 | 50.0% | 55.7% | -3.44 | -4.5 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 4 | 25.0% | 64.3% | -2.48 | -2.7 |
| over | 32 | 37.5% | 41.4% | -3.50 | -3.6 |
| under | 31 | 58.1% | 60.8% | -1.09 | -3.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 15 | 26.7% | 25.3% | -0.61 | -2.3 |
| 35-45% | 6 | 50.0% | 40.5% | +1.49 | -2.5 |
| 45-55% | 18 | 27.8% | 49.7% | -8.22 | -3.9 |
| 55-65% | 10 | 80.0% | 61.1% | +3.25 | -5.5 |
| 65-75% | 10 | 60.0% | 69.0% | -1.12 | -4.1 |
| >75% | 8 | 62.5% | 81.2% | -1.86 | -1.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 67 | 46.3% | 51.8% | -7.07 | -3.4 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 6 | 100.0% | 84.9% | +1.06 | -0.7 |
| player_goals | 25 | 80.0% | 84.9% | -1.45 | -0.9 |
| player_points | 15 | 100.0% | 84.6% | +2.74 | +0.0 |
| spread | 7 | 85.7% | 84.8% | +0.08 | -0.6 |
| team_total | 11 | 63.6% | 84.6% | -2.73 | -1.9 |
| total | 11 | 81.8% | 84.9% | -0.39 | -0.1 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 75 | 84.0% | 84.8% | -0.70 | -0.7 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 7 | 85.7% | 84.8% | +0.08 | -0.6 |
| over | 15 | 80.0% | 84.9% | -0.86 | -0.6 |
| under | 53 | 84.9% | 84.7% | +0.08 | -0.7 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 75 | 84.0% | 84.8% | -0.70 | -0.7 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 75 | 84.0% | 84.8% | -0.70 | -0.7 |

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
| (0.0, 0.4] | 3 | 27.1% | 0.0% |
| (0.4, 0.5] | 6 | 45.4% | 16.7% |
| (0.5, 0.6] | 2 | 54.2% | 50.0% |
| (0.6, 0.7] | 7 | 67.3% | 42.9% |
| (0.7, 0.8] | 12 | 73.4% | 66.7% |
| (0.8, 1.0] | 12 | 87.5% | 91.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| ml | 6 | 0.0% | 40.2% | -6.00 | -2.6 |
| spread | 27 | 74.1% | 74.1% | -0.55 | -1.0 |
| team_total | 7 | 42.9% | 48.9% | -1.84 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 42 | 57.1% | 63.3% | -8.20 | -1.2 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 28 | 71.4% | 73.1% | -1.55 | -1.1 |
| over | 5 | 40.0% | 41.5% | -1.41 | -0.7 |
| under | 4 | 50.0% | 52.2% | -0.24 | -1.3 |
| yes / favourite side | 5 | 0.0% | 39.3% | -5.00 | -2.5 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 3 | 0.0% | 22.8% | -3.00 | -0.7 |
| 35-45% | 6 | 0.0% | 40.3% | -6.00 | -2.5 |
| 45-55% | 2 | 100.0% | 48.2% | +2.16 | -1.0 |
| 55-65% | 5 | 20.0% | 60.3% | -3.21 | -2.0 |
| 65-75% | 15 | 73.3% | 69.1% | +0.82 | -1.1 |
| >75% | 11 | 90.9% | 83.2% | +1.03 | -0.5 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 10 | 70.0% | 70.7% | -0.90 | -0.8 |
| 3-5% | 16 | 56.2% | 62.2% | -3.15 | -1.4 |
| 5-8% | 10 | 60.0% | 58.2% | -0.87 | -1.1 |
| >8% | 6 | 33.3% | 62.6% | -3.27 | -1.6 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-10-31 | EDM not to win by 3+ | 88.9% | 81.1% | EDM 4-0 NYI |
| 2026-10-31 | OTT not to win by 2+ | 74.7% | 66.6% | OTT 5-1 SJS |
| 2026-11-07 | MTL not to win by 2+ | 72.1% | 69.5% | MTL 4-2 TOR |
| 2026-11-09 | PHI not to win by 2+ | 70.7% | 67.6% | PHI 3-1 VAN |
| 2026-11-01 | CAR not to win by 3+ | 70.4% | 66.6% | WPG 0-7 CAR |

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
| (0.4, 0.5] | 11 | 46.6% | 54.5% |
| (0.5, 0.6] | 32 | 54.1% | 56.2% |
| (0.6, 0.7] | 11 | 64.4% | 72.7% |
| (0.7, 0.8] | 2 | 72.2% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 56 | 58.9% | 51.2% | +8.94 | -0.0 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| betmgm | 14 | 57.1% | 54.1% | +0.39 | -0.0 |
| betrivers | 5 | 60.0% | 48.9% | +1.15 | +0.8 |
| draftkings | 19 | 57.9% | 52.3% | +2.24 | -0.1 |
| espnbet | 13 | 53.8% | 46.4% | +2.60 | +0.2 |
| fanduel | 5 | 80.0% | 53.3% | +2.55 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 24 | 54.2% | 48.6% | +2.72 | +0.3 |
| under | 32 | 62.5% | 53.1% | +6.23 | -0.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 10 | 40.0% | 42.0% | -0.50 | +0.0 |
| 45-55% | 32 | 59.4% | 49.9% | +6.65 | -0.0 |
| 55-65% | 11 | 81.8% | 59.3% | +4.27 | +0.2 |
| 65-75% | 3 | 33.3% | 65.7% | -1.49 | -1.0 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 48 | 62.5% | 50.7% | +11.94 | +0.0 |
| 5-8% | 6 | 33.3% | 55.0% | -2.69 | -0.0 |
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
| (0.5, 0.6] | 10 | 54.8% | 30.0% |
| (0.6, 0.7] | 3 | 61.7% | 66.7% |
| (0.7, 0.8] | 2 | 72.2% | 50.0% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 15 | 40.0% | 54.6% | -4.15 | -1.8 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| underdog | 15 | 40.0% | 54.6% | -4.15 | -1.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 5 | 40.0% | 53.2% | -1.16 | -1.3 |
| under | 10 | 40.0% | 55.3% | -2.98 | -2.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 10 | 30.0% | 51.1% | -4.14 | -1.7 |
| 55-65% | 3 | 66.7% | 58.3% | +0.46 | -2.4 |
| 65-75% | 2 | 50.0% | 66.4% | -0.47 | -1.3 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 13 | 38.5% | 54.4% | -3.68 | -1.8 |
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
| M6_shots_v2 | 56 | -0.00 (-0.5, +0.4) | 16.0% (-3.1%, 31.7%) | undecided |
| C1_chalk | 75 | -0.71 (-1.4, -0.3) | -0.9% (-11.6%, 8.9%) | losing to the close |
| M3_xg_model | 42 | -1.21 (-1.7, -0.9) | -19.5% (-47.9%, 4.6%) | losing to the close |
| M2_goalie_news | 14 | -1.34 (-2.0, -0.6) | -14.4% (-59.4%, 27.8%) | losing to the close |
| M6_shots_v2_pickem | 15 | -1.78 (-3.2, -0.1) | -27.7% (-77.4%, 37.0%) | losing to the close |
| B0_random | 67 | -3.41 (-4.2, -2.7) | -10.6% (-21.9%, 2.2%) | losing to the close |
| M4_shots_model | 11 | -5.82 (-8.4, -3.1) | -6.7% (-58.1%, 38.5%) | losing to the close |
| M1_sharp_price | 0 | – (–, –) | – (–, –) | undecided |
