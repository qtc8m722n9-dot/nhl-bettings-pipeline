# M3 late-game goalie pull (empty-net) test

Fit on 2023-24 (1248 games): q1e=0.4, q1t=0.14, q2e=0.4, q2c=0.12, scoring scale s=0.93

| Season | Model | Reg. tie | 1-goal | 2-goal | ENG / game | Mean total |
|---|---|--:|--:|--:|--:|--:|
| 2023-24 (fit) | actual | 0.210 | 0.175 | 0.200 | 0.335 | 6.22 |
| 2023-24 (fit) | M3 now | 0.163 | 0.298 | 0.230 | 0.000 | 6.22 |
| 2023-24 (fit) | M3 + goalie pull | 0.212 | 0.169 | 0.235 | 0.216 | 6.13 |
| 2024-25 (test) | actual | 0.205 | 0.179 | 0.216 | 0.400 | 6.05 |
| 2024-25 (test) | M3 now | 0.165 | 0.302 | 0.231 | 0.000 | 6.11 |
| 2024-25 (test) | M3 + goalie pull | 0.215 | 0.171 | 0.236 | 0.218 | 6.03 |

Out-of-sample log loss on 2024-25 (lower is better):

| Market | M3 now | M3 + goalie pull | Actual rate |
|---|--:|--:|--:|
| Home -1.5 | 0.6473 | 0.6407 | 0.354 |
| Away -1.5 | 0.5657 | 0.5645 | 0.262 |
| Over 5.5 | 0.6930 | 0.6926 | 0.535 |
| Over 6.5 | 0.6857 | 0.6844 | 0.420 |
| Goes to OT | 0.5127 | 0.5080 | 0.205 |

Note: puck-line outcomes use regulation goals; OT/shootout games are one-goal games, so -1.5 always loses there.

## 2025-26 vs Pinnacle at 1:50 PM (all games; this season was already looked at, so treat as a check, not proof)

| Market | n | M3 now | M3 + goalie pull | Pinnacle | Avg P: now / new / Pinnacle / actual |
|---|--:|--:|--:|--:|--:|
| puck line -1.5 | 1205 | 0.6241 | 0.6242 | 0.6212 | 0.304 / 0.344 / 0.355 / 0.325 |
| totals | 1150 | 0.7003 | 0.7049 | 0.6904 | 0.447 / 0.433 / 0.501 / 0.513 |
- puck line -1.5, old: weight on Pinnacle 1.06, on M3 0.38 (M3 adds information only if clearly > 0)
- puck line -1.5, new: weight on Pinnacle 1.08, on M3 0.37 (M3 adds information only if clearly > 0)
- totals, old: weight on Pinnacle 1.92, on M3 0.41 (M3 adds information only if clearly > 0)
- totals, new: weight on Pinnacle 1.94, on M3 0.37 (M3 adds information only if clearly > 0)

## Blend weights (2025-26 Pinnacle lines at 1:50 PM, M3 with goalie pull)

| Market | n | weight Pinnacle | weight M3 | log loss Pinnacle | M3 | blend (in-sample) |
|---|--:|--:|--:|--:|--:|--:|
| ml | 1208 | 0.480 | 0.460 | 0.6834 | 0.6830 | 0.6810 |
| spread | 1205 | 0.973 | 0.267 | 0.6212 | 0.6236 | 0.6181 |
| total | 608 | 3.386 | -0.249 | 0.6881 | 0.7011 | 0.6831 |
