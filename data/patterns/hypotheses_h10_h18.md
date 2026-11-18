# H10-H18: shots model patterns and shot factors

Run 2026-11-18 by `python -m nhlpipe.patterns.hyp3`. Specs in `docs/hypotheses_2026-11-17.md`, committed before the 2024-25 data was bought. Residual = SOG over hit - Pinnacle no-vig fair at pick time. Primary sample = 2024-25 (never looked at; H11 uses 2025-26 because 2024-25 has no closing prices). z is in the direction of the prediction's sign; pass = survives Benjamini-Hochberg (q 0.10) over the 9 and the supporting season has the same sign.

| ID | Pattern | Metric | Predicted sign | z 2024-25 (n) | z 2025-26 (n) | z live (n) | Primary p (one-sided) | Passes |
|---|---|---|---|--:|--:|--:|--:|---|
| H10 | Model sharpens with games played | interaction dm x log(1+gp) | + | +0.62 (15,955) | +0.87 (16,155) | +1.47 (1,266) | 0.269 | no |
| H11 | Model beats quiet lines | interaction dm x quiet | + | – | -0.52 (15,674) | +1.44 (1,166) | 0.697 | no |
| H12 | Tired opponent | opp_b2b = 1 | + | -1.17 (15,955) | +2.66 (16,155) | +0.65 (1,266) | 0.879 | no |
| H13 | Game script | trend on team win fair | - | +0.28 (15,955) | +0.66 (16,155) | +1.16 (1,266) | 0.612 | no |
| H14 | Returning from absence | missed team's last game = 1 | - | +0.71 (15,955) | +0.18 (16,155) | +0.80 (1,266) | 0.762 | no |
| H15 | Opponent shot blocking | trend on opponent blocks/game | - | -0.02 (15,893) | +0.95 (16,155) | -0.45 (1,266) | 0.490 | no |
| H16 | Overtime chance (top-TOI players) | trend on closeness | + | +0.81 (5,318) | +0.18 (5,021) | +0.37 (354) | 0.210 | no |
| H17 | Blowout benching | heavy-favourite top-TOI = 1 | - | -1.42 (15,955) | -0.64 (16,155) | -0.98 (1,266) | 0.078 | no |
| H18 | Power-play opportunities (top-PP players) | trend on opponent PIM/game | + | +0.57 (5,291) | -0.92 (6,388) | -0.20 (637) | 0.285 | no |

## Slices (descriptive)

| Slice | Sample | Lines | Over edge vs Pinnacle, pts | z |
|---|---|--:|--:|--:|
| Opponent on a back-to-back | 2024-25 (fresh) | 2,367 | -1.3 | -1.17 |
| Opponent on a back-to-back | 2025-26 | 2,747 | +2.7 | +2.66 |
| Opponent on a back-to-back | 2026-27 live | 180 | +2.4 | +0.65 |
| Returning from absence | 2024-25 (fresh) | 120 | +3.2 | +0.71 |
| Returning from absence | 2025-26 | 183 | +0.7 | +0.18 |
| Star on a heavy favourite (67%+) | 2024-25 (fresh) | 626 | -2.8 | -1.42 |
| Star on a heavy favourite (67%+) | 2025-26 | 324 | -1.8 | -0.64 |
| Star on a heavy favourite (67%+) | 2026-27 live | 25 | -9.7 | -0.98 |
| Big underdog's players (team win < 35%) (shown as UNDER edge) | 2024-25 (fresh) | 1,680 | +1.7 | +1.31 |
| Big underdog's players (team win < 35%) (shown as UNDER edge) | 2025-26 | 883 | -0.6 | -0.33 |
| Big underdog's players (team win < 35%) (shown as UNDER edge) | 2026-27 live | 93 | +0.5 | +0.09 |
| Model says over by 5+ pts, player has 20+ games | 2024-25 (fresh) | 1,981 | +2.1 | +1.77 |
| Model says over by 5+ pts, player has 20+ games | 2025-26 | 612 | +2.2 | +1.12 |
| Model says over by 5+ pts, player has < 20 games | 2024-25 (fresh) | 256 | +2.2 | +0.69 |
| Model says over by 5+ pts, player has < 20 games | 2025-26 | 354 | +4.0 | +1.44 |
| Model says over by 5+ pts, player has < 20 games | 2026-27 live | 89 | +1.5 | +0.27 |
| Model says under by 5+ pts, player has 20+ games (shown as UNDER edge) | 2024-25 (fresh) | 794 | +2.4 | +1.35 |
| Model says under by 5+ pts, player has 20+ games (shown as UNDER edge) | 2025-26 | 2,782 | +3.0 | +3.09 |
| Model says under by 5+ pts, player has < 20 games (shown as UNDER edge) | 2024-25 (fresh) | 1,075 | +8.2 | +5.29 |
| Model says under by 5+ pts, player has < 20 games (shown as UNDER edge) | 2025-26 | 547 | +5.3 | +2.52 |
| Model says under by 5+ pts, player has < 20 games (shown as UNDER edge) | 2026-27 live | 184 | -0.5 | -0.14 |

2024-25 sample: 15,955 Pinnacle SOG lines matched to skaters (2024-10-08 - 2025-04-17).

