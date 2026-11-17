# Hypotheses H2-H5: results

Run 2026-11-17 by `python -m nhlpipe.patterns.hyp`. Specs: `docs/hypotheses_2026-11-17.md` (committed before these tests ran). Research only.

## H2 Rink scorekeeper effect (SOG props)

Rink factor = total shots recorded in an arena's games / what the same two teams record elsewhere (previous season + this season before the game, shrunk with 20 games at 1.0).

Latest factors (2026-11-15): most generous COL 1.047, MIN 1.037, FLA 1.031, SJS 1.025; stingiest CHI 0.938, DAL 0.948, PHI 0.956, CAR 0.977.

| Sample | Lines | Trend z (pre-registered metric) | Over edge, generous quarter (RF > 1.019), pts | Over edge, stingy quarter (RF < 0.984), pts |
|---|--:|--:|--:|--:|
| discovery | 10,141 | +0.76 | +1.1 (z +1.10, n 2535) | -1.1 (z -1.07, n 2525) |
| holdout | 6,014 | +0.01 | -2.2 (z -1.51, n 1418) | -1.6 (z -1.12, n 1617) |
| live | 1,266 | +0.63 | +7.1 (z +1.98, n 345) | +1.8 (z +0.59, n 263) |

Pre-registered rule (discovery z > 0 and holdout one-sided p < 0.05): holdout p = 0.497 -> **does not pass**.

Secondary: shots model with its projection multiplied by the rink factor (log loss, lower = better; the model alone, not blended):

| Sample | Lines | Pinnacle | Model | Model x rink |
|---|--:|--:|--:|--:|
| discovery | 10,141 | 0.6804 | 0.6813 | 0.6813 |
| holdout | 6,014 | 0.6831 | 0.6818 | 0.6821 |
| live | 1,266 | 0.6870 | 0.6909 | 0.6908 |

(2025-26 uses the out-of-sample projections from the backtest; the NB dispersion is the frozen live one.)

## H3 Morning line promotions

Collection started 2026-11-17 (`nhlpipe/lines.py`, saved each pull as `data/raw/<date>/df_lines.csv`). No history exists, so there is nothing to test yet: first look at 150 promoted lines.

## H4 Favourite -1.5 and the over together

Observed rate of both legs hitting vs the product of the two Pinnacle fair prices (= what a venue that prices the legs as unrelated would charge). Edge > 0 = the pair hits more than an independent price assumes.

| Pair | Sample | Games | Both hit | Product of fair prices | Edge, pts | z | ROI buying both legs at Pinnacle's own prices |
|---|---|--:|--:|--:|--:|--:|--:|
| Fav -1.5 AND over (pre-registered) | discovery | 747 | 16.5% | 17.7% | -1.2 | -0.87 | -15.0% |
| Fav -1.5 AND over (pre-registered) | holdout | 401 | 19.0% | 18.1% | +0.9 | +0.46 | -6.2% |
| Fav -1.5 AND over (pre-registered) | live | 108 | 16.7% | 17.8% | -1.1 | -0.30 | -17.0% |
| Fav -1.5 AND under | discovery | 747 | 12.7% | 17.6% | -4.9 | -3.54 | -34.7% |
| Fav -1.5 AND under | holdout | 401 | 17.7% | 18.0% | -0.2 | -0.13 | -8.8% |
| Fav -1.5 AND under | live | 108 | 17.6% | 17.5% | +0.1 | +0.02 | -6.1% |
| Dog +1.5 AND over | discovery | 747 | 35.9% | 32.4% | +3.5 | +2.06 | – |
| Dog +1.5 AND over | holdout | 401 | 30.2% | 32.1% | -1.9 | -0.83 | – |
| Dog +1.5 AND over | live | 108 | 32.4% | 32.6% | -0.2 | -0.04 | – |
| Dog +1.5 AND under | discovery | 747 | 34.9% | 32.3% | +2.6 | +1.53 | – |
| Dog +1.5 AND under | holdout | 401 | 33.2% | 31.9% | +1.3 | +0.55 | – |
| Dog +1.5 AND under | live | 108 | 33.3% | 32.2% | +1.2 | +0.26 | – |
| Fav moneyline AND over | discovery | 747 | 26.9% | 28.9% | -2.0 | -1.20 | – |
| Fav moneyline AND over | holdout | 401 | 30.2% | 29.4% | +0.8 | +0.35 | – |
| Fav moneyline AND over | live | 108 | 30.6% | 29.1% | +1.5 | +0.34 | – |

Pre-registered rule (discovery and holdout joint > product, holdout one-sided p < 0.05): holdout p = 0.322 -> **does not pass**.

Fav -1.5 AND over by favourite strength (all 2025-26 + live):

| Favourite win chance | Games | Both hit | Product | Edge, pts | z |
|---|--:|--:|--:|--:|--:|
| 50-60% | 859 | 14.2% | 16.2% | -2.0 | -1.60 |
| 60-67% | 275 | 22.9% | 20.2% | +2.7 | +1.12 |
| 67%+ | 112 | 28.6% | 24.5% | +4.0 | +1.00 |

Kalshi (live): the same pair bought as two separate Kalshi markets at the pick-lock ask (incl. fees):

118 games; both hit 18.6%; average cost 19.9% (product of Pinnacle fair 18.3%); ROI -9.2%. Kalshi's ask plus fees sits above fair on each leg, so the pair starts behind before any correlation gain.

## H5 Popular-team premium on Kalshi (interim)

Premium = Kalshi price of the team's YES - Pinnacle fair at the pick lock, in points (mid = halfway between bid and ask; ask = what we'd pay incl. fees). 95% CI by resampling slates.

| Group | Markets | Premium at mid, pts | Premium at ask, pts | Won | Fair |
|---|--:|--:|--:|--:|--:|
| Popular 5 (TOR MTL EDM NYR BOS) | 38 | -0.01 (-0.22, +0.23) | +2.19 | 57.9% | 52.7% |
| All other teams | 198 | -0.11 (-0.15, -0.08) | +2.05 | 48.5% | 49.5% |
| Canadian 7 | 56 | -0.14 (-0.31, +0.04) | +2.02 | 51.8% | 46.4% |
| Non-Canadian | 180 | -0.09 (-0.15, -0.03) | +2.08 | 49.4% | 51.1% |

Primary metric (popular minus others, at mid): +0.10 pts (95% CI -0.11 to +0.32); 38 popular-team markets so far (verdict at 300). Interim only.

By team (YES premium at mid, pts; sorted):

| Team | Markets | Premium |
|---|--:|--:|
| CBJ | 7 | +0.58 |
| BOS | 6 | +0.55 |
| NYR | 8 | +0.35 |
| NJD | 8 | +0.28 |
| VGK | 8 | +0.21 |
| CGY | 9 | +0.18 |
| SEA | 4 | +0.17 |
| NYI | 6 | +0.13 |
| SJS | 9 | +0.08 |
| VAN | 8 | +0.05 |
| TBL | 8 | +0.04 |
| EDM | 9 | +0.01 |
| PIT | 7 | +0.01 |
| STL | 7 | -0.01 |
| LAK | 6 | -0.02 |
| WSH | 6 | -0.02 |
| DET | 8 | -0.07 |
| CHI | 7 | -0.10 |
| WPG | 8 | -0.12 |
| DAL | 7 | -0.20 |
| NSH | 8 | -0.20 |
| CAR | 5 | -0.21 |
| COL | 8 | -0.29 |
| OTT | 7 | -0.31 |
| ANA | 8 | -0.38 |
| MTL | 8 | -0.42 |
| UTA | 8 | -0.46 |
| TOR | 7 | -0.46 |
| FLA | 9 | -0.48 |
| BUF | 7 | -0.48 |
| MIN | 7 | -0.57 |
| PHI | 8 | -0.72 |

