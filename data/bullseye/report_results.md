# Bullseye: game-winner component

2025-26 test: 1205 games with a Pinnacle moneyline at 1:50 PM and an M3 price. Model frozen before this run (trained on 2023-24 + 2024-25, `data/bullseye/model.json`). Lower log loss is better.

## 1. Log loss, 2025-26 (out of sample)

| Model | Log loss | vs Pinnacle (95% CI) |
|---|--:|--:|
| Pinnacle no-vig | 0.6834 | – |
| Bullseye | 0.6893 | +0.0059 (-0.0022, +0.0138) |
| Bullseye without goalie term | 0.6910 | +0.0076 (-0.0000, +0.0148) |
| M3 raw | 0.6830 | -0.0004 (-0.0085, +0.0071) |
| M3 live blend (fit on this season) | 0.6809 | -0.0024 (-0.0068, +0.0017) |
| Home-win rate only | 0.6918 | |

## 2. Does Bullseye know something Pinnacle doesn't? (logit-blend weights, 2025-26)

y ~ a·logit(Pinnacle) + b·logit(model). b clearly > 0 = the model adds information. CI by resampling nights.

| Inputs | a (Pinnacle) | b (Bullseye) | c (M3) | b 95% CI |
|---|--:|--:|--:|--:|
| Pinnacle + Bullseye | 0.52 | 0.20 | nan | (-0.18, 0.60) |
| Pinnacle + M3 | 0.48 | – | 0.46 | |
| Pinnacle + Bullseye + M3 | 0.44 | 0.08 | 0.39 | (-0.35, 0.58) |

## 3. Walk-forward: blend fit on Oct-Dec 2025, judged on Jan-Apr 2026

Train 552 games, test 653 games.

| Model | Log loss Jan-Apr | vs Pinnacle (95% CI) |
|---|--:|--:|
| Pinnacle | 0.6795 | – |
| Pinnacle + Bullseye (weights pin 0.38, bull 0.25) | 0.6792 | -0.0003 (-0.0078, +0.0066) |
| Pinnacle + M3 (weights pin 0.39, m3 0.53) | 0.6786 | -0.0009 (-0.0076, +0.0052) |
| Pinnacle + Bullseye + M3 (weights pin 0.29, bull 0.14, m3 0.45) | 0.6787 | -0.0008 (-0.0077, +0.0059) |

## 4. Factor by factor against the market (2025-26)

y ~ a·logit(Pinnacle) + intercept + g·factor (factor in its own units, home minus away where paired). g ≠ 0 means Pinnacle under- (same sign as Bullseye) or over-reacts to that factor. 12 tests: expect ~1 false hit at 95%.

| Factor | Bullseye coef (2023-25) | g vs market | g 95% CI | Read |
|---|--:|--:|--:|---|
| ev_xgd | +0.814 | +0.605 | (+0.002, +1.192) | market under-weights |
| st_xgd | +0.667 | -0.405 | (-1.154, +0.298) | priced in / no signal |
| fin | +0.610 | -0.388 | (-0.786, +0.054) | priced in / no signal |
| goalie | +0.814 | +0.548 | (-0.171, +1.207) | priced in / no signal |
| h_b2b | +0.010 | +0.255 | (-0.053, +0.555) | priced in / no signal |
| a_b2b | +0.337 | +0.329 | (+0.072, +0.598) | market under-weights |
| h_3in4 | -0.336 | +0.137 | (-0.101, +0.369) | priced in / no signal |
| a_3in4 | -0.143 | +0.198 | (-0.098, +0.510) | priced in / no signal |
| rest_diff | +0.090 | +0.087 | (-0.031, +0.207) | priced in / no signal |
| a_tz_shift | +0.083 | +0.048 | (-0.073, +0.155) | priced in / no signal |
| a_km | +0.055 | -0.009 | (-0.131, +0.094) | priced in / no signal |
| lineup | -0.133 | -0.029 | (-2.010, +1.536) | priced in / no signal |

## 5. Pinnacle moneyline calibration (2025-26)

y ~ intercept + a·logit(Pinnacle): a = 0.74, intercept = -0.010 (a = 1 and 0 = perfectly calibrated; a > 1 = favourites under-priced). Home teams won 0.526, Pinnacle said 0.538.

| Pinnacle home prob | Games | Pinnacle avg | Bullseye avg | Actual |
|---|--:|--:|--:|--:|
| (0.0, 0.35] | 27 | 0.314 | 0.322 | 0.370 |
| (0.35, 0.45] | 190 | 0.417 | 0.430 | 0.458 |
| (0.45, 0.55] | 442 | 0.503 | 0.516 | 0.500 |
| (0.55, 0.65] | 409 | 0.594 | 0.608 | 0.550 |
| (0.65, 1.0] | 137 | 0.698 | 0.688 | 0.664 |
