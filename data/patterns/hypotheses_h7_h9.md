# Hypotheses H7-H9: results

Run 2026-11-17 by `python -m nhlpipe.patterns.hyp2`. Specs in `docs/hypotheses_2026-11-17.md`, committed before this ran. Splits: discovery Oct-Jan 2025-26, holdout Feb-Apr 2026, live 2026-27.

## H7 Trailing coach's goalie-pull aggressiveness -> favourite -1.5

Pull proxy = empty-net goals a team conceded per regulation loss (previous + current season before the game, shrunk to the league rate with 20 losses). Higher = its coach pulls earlier or more often.

| Sample | Games | Primary: trend z, fav -1.5 on the underdog's pull proxy | Fav -1.5 edge, top third, pts (z) | Fav -1.5 edge, bottom third, pts (z) | Secondary: trend z, over |
|---|--:|--:|--:|--:|--:|
| discovery | 781 | -0.80 | -6.4 (-2.16) | -3.0 (-1.02) | +0.38 |
| holdout | 424 | +1.91 | +6.4 (+1.77) | -3.3 (-0.58) | +1.36 |
| live | 112 | +1.21 | +10.3 (+1.21) | -5.3 (-0.64) | -0.41 |

Rule: discovery z > 0 and holdout one-sided p < 0.05. Holdout p = 0.028 -> **does not pass**.

Highest pull proxies now: NYR 0.52, WSH 0.51, FLA 0.48, TOR 0.47, SEA 0.46; lowest: VGK 0.31, BOS 0.32, EDM 0.32, PHI 0.32, OTT 0.33.

## H8 Power-play role change -> points (and SOG) overs

PP share = player PP time / team PP time; shift = last 3 games minus the 17 before. Positive z = overs beat the price after a promotion.

| Test | Sample | Lines | Trend z |
|---|---|--:|--:|
| Primary: points overs | discovery | 9,439 | -0.02 |
| Primary: points overs | holdout | 6,385 | +0.22 |
| Primary: points overs | live | 1,390 | -0.04 |
| Secondary: SOG overs | discovery | 8,096 | +0.43 |
| Secondary: SOG overs | holdout | 5,577 | +2.40 |
| Secondary: SOG overs | live | 1,146 | +0.56 |
| Secondary: defencemen points overs | discovery | 2,200 | -0.25 |
| Secondary: defencemen points overs | holdout | 1,573 | -1.24 |
| Secondary: defencemen points overs | live | 296 | +1.14 |

Rule: discovery z > 0 and holdout one-sided p < 0.05. Holdout p = 0.413 -> **does not pass**.

- discovery: players whose PP share rose 15+ points: 1314 points lines, over edge +1.3 pts (z +0.82).
- holdout: players whose PP share rose 15+ points: 798 points lines, over edge +1.8 pts (z +0.98).
- live: players whose PP share rose 15+ points: 183 points lines, over edge -3.1 pts (z -0.67).

## H9 Shooting-luck regression in points props

Finishing luck = goals above (shots x expected shooting %) per game, season to date. Negative z = hot finishers' points overs lose to the price, as predicted.

| Test | Sample | Lines | Trend z |
|---|---|--:|--:|
| Primary: points overs | discovery | 11,864 | -0.81 |
| Primary: points overs | holdout | 6,901 | -1.74 |
| Primary: points overs | live | 1,544 | +0.66 |

Rule: discovery z < 0 and holdout one-sided p < 0.05 (negative direction). Holdout p = 0.041 -> **PASSES**.

- discovery: luckiest 10% over edge +0.4 pts (z +0.23, n 1187); unluckiest 10% +1.3 pts (z +0.85, n 1187).
- holdout: luckiest 10% over edge -4.6 pts (z -1.46, n 264); unluckiest 10% -1.0 pts (z -0.23, n 132).
- live: luckiest 10% over edge +1.4 pts (z +0.42, n 269); unluckiest 10% +2.7 pts (z +0.76, n 205).

