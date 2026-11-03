# Diagnostics: where the methods miss

Trial period 2026-10-31 – 2026-11-02. Singles only. CLV = closing fair (or Kalshi mid) minus price paid, in percentage points; it measures the price, independent of luck. Rule of thumb: bad results with good CLV = variance; bad results with bad CLV = a real flaw. Kalshi CLV is against the mid, so buying at the ask starts about half a spread behind.

## Flags to investigate

- B0_random: venue = kalshi: 17 bets, CLV -2.4 pp, units -2.58

## B0_random

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_result | 1 | 100.0% | 65.6% | +0.52 | -3.5 |
| player_goals | 5 | 60.0% | 56.1% | +0.80 | -2.1 |
| player_points | 7 | 57.1% | 53.7% | -0.81 | -3.1 |
| spread | 1 | 0.0% | 73.4% | -1.00 | -4.0 |
| team_total | 5 | 40.0% | 48.6% | -0.35 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 17 | 47.1% | 54.8% | -2.58 | -2.4 |
| underdog | 2 | 100.0% | 53.5% | +1.74 | -2.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 2 | 50.0% | 69.5% | -0.48 | -3.7 |
| over | 9 | 22.2% | 36.0% | -2.52 | -2.5 |
| under | 8 | 87.5% | 71.9% | +2.16 | -2.2 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 6 | 33.3% | 26.3% | +0.48 | -2.2 |
| 35-45% | 1 | 0.0% | 37.6% | -1.00 | -3.1 |
| 45-55% | 3 | 66.7% | 50.9% | +0.74 | -3.3 |
| 55-65% | 1 | 100.0% | 64.6% | +0.55 | -2.5 |
| 65-75% | 2 | 50.0% | 69.5% | -0.48 | -3.7 |
| >75% | 6 | 66.7% | 81.1% | -1.12 | -1.7 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 19 | 52.6% | 54.7% | -0.83 | -2.5 |

## C1_chalk

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| p1_total | 2 | 100.0% | 84.9% | +0.35 | -0.5 |
| player_goals | 9 | 88.9% | 84.9% | +0.42 | -1.4 |
| player_points | 2 | 100.0% | 83.5% | +0.39 | -2.7 |
| spread | 1 | 100.0% | 84.9% | +0.18 | -0.5 |
| team_total | 3 | 66.7% | 84.6% | -0.65 | -1.3 |
| total | 2 | 50.0% | 84.9% | -0.82 | -1.2 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 19 | 84.2% | 84.7% | -0.12 | -1.4 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 1 | 100.0% | 84.9% | +0.18 | -0.5 |
| over | 4 | 100.0% | 84.9% | +0.71 | -1.1 |
| under | 14 | 78.6% | 84.7% | -1.01 | -1.5 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| >75% | 19 | 84.2% | 84.7% | -0.12 | -1.4 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| nan | 19 | 84.2% | 84.7% | -0.12 | -1.4 |

## M2_goalie_news

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| spread | 2 | 50.0% | 78.2% | -0.67 | +0.0 |
| team_total | 2 | 50.0% | 48.2% | -0.21 | -1.5 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 4 | 50.0% | 63.2% | -0.88 | -0.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 2 | 50.0% | 78.2% | -0.67 | +0.0 |
| under | 2 | 50.0% | 48.2% | -0.21 | -1.5 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 35-45% | 1 | 0.0% | 40.7% | -1.00 | -1.5 |
| 55-65% | 1 | 100.0% | 55.7% | +0.79 | -1.5 |
| >75% | 2 | 50.0% | 78.2% | -0.67 | +0.0 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 5-8% | 3 | 33.3% | 59.2% | -1.21 | -0.8 |
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
| (0.5, 0.6] | 1 | 52.2% | 0.0% |
| (0.6, 0.7] | 3 | 66.9% | 33.3% |
| (0.7, 0.8] | 2 | 72.6% | 0.0% |
| (0.8, 1.0] | 7 | 87.3% | 85.7% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| spread | 10 | 60.0% | 76.1% | -2.62 | -0.9 |
| team_total | 5 | 20.0% | 44.0% | -3.21 | -1.1 |
| total | 2 | 50.0% | 37.1% | +0.19 | -0.3 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| kalshi | 17 | 47.1% | 62.1% | -5.63 | -0.9 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| no / dog side | 10 | 60.0% | 76.1% | -2.62 | -0.9 |
| over | 4 | 25.0% | 34.0% | -1.81 | -0.5 |
| under | 3 | 33.3% | 52.7% | -1.21 | -1.3 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <35% | 2 | 0.0% | 23.7% | -2.00 | +0.0 |
| 35-45% | 2 | 0.0% | 41.7% | -2.00 | -1.2 |
| 45-55% | 1 | 100.0% | 45.7% | +1.19 | -1.1 |
| 55-65% | 3 | 33.3% | 58.4% | -1.21 | -2.2 |
| 65-75% | 2 | 0.0% | 66.6% | -2.00 | -1.6 |
| >75% | 7 | 85.7% | 81.5% | +0.38 | -0.2 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| <3% | 2 | 50.0% | 59.5% | -0.90 | +0.0 |
| 3-5% | 4 | 75.0% | 69.6% | +0.60 | -0.4 |
| 5-8% | 6 | 50.0% | 59.0% | -1.66 | -0.8 |
| >8% | 5 | 20.0% | 60.8% | -3.67 | -1.6 |

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
| (0.6, 0.7] | 9 | 63.9% | 44.4% |

By market:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| player_sog | 9 | 44.4% | 56.4% | -2.08 | -7.0 |

By venue:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| prizepicks | 6 | 66.7% | 57.8% | +0.92 | -8.9 |
| underdog | 3 | 0.0% | 53.5% | -3.00 | -3.8 |

By side:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| over | 1 | 100.0% | 57.8% | +0.73 | -7.0 |
| under | 8 | 37.5% | 56.2% | -2.81 | -7.0 |

By price paid:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 45-55% | 3 | 0.0% | 53.5% | -3.00 | -3.8 |
| 55-65% | 6 | 66.7% | 57.8% | +0.92 | -8.9 |

By stated edge:

| Slice | Bets | Win % | Breakeven | Units | Avg CLV pp |
|---|--:|--:|--:|--:|--:|
| 3-5% | 2 | 100.0% | 57.8% | +1.46 | -10.9 |
| 5-8% | 6 | 16.7% | 55.6% | -4.27 | -6.1 |
| >8% | 1 | 100.0% | 57.8% | +0.73 | -8.5 |

Most confident misses:

| Date | Pick | Stated P | Price | Detail |
|---|---|--:|--:|---|
| 2026-11-01 | Cutter Gauthier Under 3.5 shots | 64.0% | 57.8% | Cutter Gauthier 5 sog |
| 2026-11-01 | Adam Fox Under 1.5 shots | 63.9% | 57.8% | Adam Fox 2 sog |
| 2026-10-31 | David Pastrnak Under 3.5 shots | 63.8% | 53.5% | David Pastrnak 4 sog |
| 2026-10-31 | Dylan Cozens Under 2.5 shots | 63.8% | 53.5% | Dylan Cozens 5 sog |
| 2026-11-02 | Sam Malinski Under 1.5 shots | 63.3% | 53.5% | Sam Malinski 2 sog |

## Narrowing to one model

Pre-registered rule: on 2026-12-31 or once every live method has 300 settled singles, drop every method whose CLV 95% interval is entirely below 0; of the rest, keep the one with the highest lower CLV bound, using ROI only to break ties.

| Method | Bets | Avg CLV pp (95% CI) | ROI (95% CI) | Status |
|---|--:|--:|--:|---|
| M3_xg_model | 17 | -0.86 (-1.1, -0.6) | -33.1% (-54.6%, 3.7%) | losing to the close |
| C1_chalk | 19 | -1.39 (-2.6, -1.0) | -0.6% (-52.9%, 18.7%) | losing to the close |
| B0_random | 19 | -2.48 (-3.7, -2.0) | -4.4% (-22.6%, 17.0%) | losing to the close |
| M2_goalie_news | 4 | -0.75 (–, –) | -22.0% (–, –) | undecided |
| M4_shots_model | 9 | -6.98 (–, –) | -23.1% (–, –) | undecided |
