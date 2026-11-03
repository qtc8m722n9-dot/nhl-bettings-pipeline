# M3 totals bias: diagnosis

Question (STATUS step 3): M3 put overs at ~43-45% in 2025-26 while 51% went over. Where does the gap come from?
Code: `nhlpipe/backtest/m3totals.py` (collect, collect_past, report). Same point-in-time inputs and live M3 code.

## Mean goals per game

| Season | Model | Pred total | Actual | Pred reg. goals | Actual reg. | Scale s |
|---|---|--:|--:|--:|--:|--:|
| 2023-24 | no pull (pre 11-03) | 6.22 | 6.22 | 6.05 | 6.01 | 1.000 |
| 2023-24 | live (PULL_SCALE 0.93) | 6.13 | 6.22 | 5.92 | 6.01 | 0.930 |
| 2023-24 | mean-preserving scale | 6.26 | 6.22 | 6.05 | 6.01 | 0.953 |
| 2024-25 | no pull (pre 11-03) | 6.11 | 6.05 | 5.94 | 5.85 | 1.000 |
| 2024-25 | live (PULL_SCALE 0.93) | 6.03 | 6.05 | 5.82 | 5.85 | 0.930 |
| 2024-25 | mean-preserving scale | 6.16 | 6.05 | 5.94 | 5.85 | 0.951 |
| 2025-26 | no pull (pre 11-03) | 6.09 | 6.28 | 5.92 | 6.03 | 1.000 |
| 2025-26 | live (PULL_SCALE 0.93) | 6.01 | 6.28 | 5.80 | 6.03 | 0.930 |
| 2025-26 | mean-preserving scale | 6.14 | 6.28 | 5.92 | 6.03 | 0.951 |
| 2025-26, no goalie term | no pull (pre 11-03) | 6.15 | 6.28 | 5.98 | 6.03 | 1.000 |
| 2025-26, no goalie term | live (PULL_SCALE 0.93) | 6.07 | 6.28 | 5.85 | 6.03 | 0.930 |
| 2025-26, no goalie term | mean-preserving scale | 6.19 | 6.28 | 5.98 | 6.03 | 0.952 |

Goalie term (2025-26 only; no goalie logs cached for earlier seasons) lowers expected goals by 0.058/game on average.

## 2025-26 vs Pinnacle's main half-goal total at 1:50 PM

608 games (the other 600 had a whole-number main line). Pinnacle: avg P(over) 0.501, log loss 0.6881. Actual over rate 0.526.

| Model | Goalie term | Avg P(over) | Log loss | Blend weight Pinnacle / M3 |
|---|---|--:|--:|--:|
| no pull (pre 11-03) | yes | 0.471 | 0.6984 | 3.43 / -0.29 |
| live (PULL_SCALE 0.93) | yes | 0.457 | 0.7015 | 3.41 / -0.28 |
| mean-preserving scale | yes | 0.478 | 0.6975 | 3.45 / -0.31 |
| no pull (pre 11-03) | no | 0.480 | 0.6957 | 3.35 / -0.22 |
| live (PULL_SCALE 0.93) | no | 0.465 | 0.6991 | 3.39 / -0.30 |
| mean-preserving scale | no | 0.487 | 0.6955 | 3.39 / -0.27 |

## Side effects of the scale fix on markets M3 does bet (log loss)

| Season | Model | Home -1.5 | Away -1.5 | Goes to OT | Over 5.5 | Over 6.5 |
|---|---|--:|--:|--:|--:|--:|
| 2023-24 | live (PULL_SCALE 0.93) | 0.6184 | 0.5757 | 0.5144 | 0.6821 | 0.6878 |
| 2023-24 | mean-preserving scale | 0.6178 | 0.5752 | 0.5143 | 0.6808 | 0.6870 |
| 2024-25 | live (PULL_SCALE 0.93) | 0.6411 | 0.5648 | 0.5072 | 0.6931 | 0.6845 |
| 2024-25 | mean-preserving scale | 0.6419 | 0.5645 | 0.5072 | 0.6937 | 0.6856 |
| 2025-26 | live (PULL_SCALE 0.93) | 0.6067 | 0.5693 | 0.5636 | 0.6833 | 0.6939 |
| 2025-26 | mean-preserving scale | 0.6067 | 0.5695 | 0.5639 | 0.6802 | 0.6906 |

## Conclusions (2026-11-03)

1. **Where the 0.27 goals/game gap in 2025-26 comes from** (live M3 6.01 vs actual 6.28):
   - ~0.13: the goalie-pull scale. `PULL_SCALE = 0.93` was meant to keep the mean total unchanged, but it removes ~7% of regulation goals while the pull phase adds back only ~0.24. It lowers the mean in every season (2023-24 too: 6.13 vs 6.22 in the fit). The fit grid hit its edge (model ENG 0.22/game vs 0.34-0.40 actual), and the mean-total target had a loose tolerance, so the shortfall was accepted.
   - ~0.06: the goalie term (projected starters average positive GSAx).
   - ~0.09: 2025-26 scoring ran above the to-date league average (Pinnacle's main line rose from ~6.0 in October to ~6.4 in April). About 1 standard error, so partly noise.
2. **Fixing the level does not give M3 a totals edge.** In every variant, M3's totals log loss is worse than Pinnacle's and the blend weight on M3 stays negative (-0.22 to -0.31). The rule "no totals bets" stays. The bias was a symptom, not the reason M3 lacks totals information.
3. **Mean-preserving scale** (solve s per game so regulation goals including the pull phase average lh + la; `mean_scale()`) restores what PULL_SCALE was meant to do, has no new parameters, and barely moves the markets M3 bets (puck line / OT log loss within +/-0.0008 in all three seasons). Recommended for the next test period; **not applied** (pre-registered rule; needs Evan's approval).
4. Not worth more work now: refitting the pull with a wider grid (ENG rate), or a recent-window scoring level. M3 does not bet totals, and the combined model should treat M3's raw total probability as a weak input at best.
