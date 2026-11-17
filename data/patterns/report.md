# Pattern scan: observed vs expected

Built 2026-11-17 by `python -m nhlpipe.patterns.scan`. Research only: no bets, no method changed. Rules are in the docstring of `nhlpipe/patterns/scan.py` and were fixed before the first run.

**How to read it.** *Expected* = Pinnacle's no-vig chance at pick time. *Edge* = actual hit rate minus expected, in percentage points. *z* = how many standard errors the edge is from zero (|z| ≈ 2 is the usual 5% bar for ONE test; with hundreds of tests, several will pass that bar by luck, which is what the Benjamini-Hochberg (BH) correction and the untouched holdout are for). A pattern only counts if it was found in DISCOVERY and then showed up again in the HOLDOUT. To make money an edge must also beat the bookmaker's margin, roughly 2 to 2.5 points on game lines and more on props.

## 1. Data

| Table | Sample | Rows | Dates |
|---|---|--:|---|
| games | discovery | 782 | 2025-10-15 – 2026-01-31 |
| games | holdout | 426 | 2026-02-01 – 2026-04-16 |
| games | live | 118 | 2026-10-30 – 2026-11-16 |
| sog | discovery | 10,141 | 2025-10-15 – 2026-01-31 |
| sog | holdout | 6,014 | 2026-02-01 – 2026-04-16 |
| sog | live | 1,266 | 2026-10-30 – 2026-11-15 |
| points | discovery | 11,874 | 2025-10-15 – 2026-01-31 |
| points | holdout | 6,902 | 2026-02-01 – 2026-04-16 |
| points | live | 1,545 | 2026-10-30 – 2026-11-15 |

Discovery tests run: **712** (slices + trend tests, all markets). Expected false positives at p < 0.05 by luck alone: ~36. Discovery tests surviving BH at q = 0.1: **0**.

## 2. Is the market itself biased? (calibration, no features)

**total** (expected = over_fair; 'over/home/fav' side):

| Sample | n | Hit rate | Expected | Edge, pts | z | Chi-square by price band (df) | p |
|---|--:|--:|--:|--:|--:|--:|--:|
| discovery | 747 | 52.3% | 50.0% | +2.3 | +1.27 | 1.7 (2) | 0.42 |
| holdout | 403 | 49.4% | 50.2% | -0.8 | -0.32 | 3.5 (2) | 0.17 |
| live | 114 | 49.1% | 50.3% | -1.1 | -0.24 | 0.1 (2) | 0.96 |

**home** (expected = ml_home_fair; 'over/home/fav' side):

| Sample | n | Hit rate | Expected | Edge, pts | z | Chi-square by price band (df) | p |
|---|--:|--:|--:|--:|--:|--:|--:|
| discovery | 782 | 52.6% | 53.7% | -1.1 | -0.65 | 9.5 (7) | 0.22 |
| holdout | 426 | 52.8% | 54.1% | -1.3 | -0.53 | 3.3 (7) | 0.86 |
| live | 118 | 45.8% | 53.2% | -7.5 | -1.67 | 7.7 (6) | 0.26 |

**pl_fav** (expected = pl_fav_fair; 'over/home/fav' side):

| Sample | n | Hit rate | Expected | Edge, pts | z | Chi-square by price band (df) | p |
|---|--:|--:|--:|--:|--:|--:|--:|
| discovery | 781 | 30.3% | 35.3% | -4.9 | -2.89 | 11.7 (5) | 0.04 |
| holdout | 424 | 36.6% | 36.1% | +0.5 | +0.21 | 2.3 (5) | 0.80 |
| live | 112 | 36.6% | 35.3% | +1.3 | +0.28 | 0.8 (3) | 0.84 |

**sog** (expected = fair_over; 'over/home/fav' side):

| Sample | n | Hit rate | Expected | Edge, pts | z | Chi-square by price band (df) | p |
|---|--:|--:|--:|--:|--:|--:|--:|
| discovery | 10,141 | 51.6% | 51.6% | +0.1 | +0.12 | 1.8 (6) | 0.94 |
| holdout | 6,014 | 49.2% | 50.4% | -1.3 | -1.77 | 12.1 (6) | 0.06 |
| live | 1,266 | 50.5% | 48.6% | +1.9 | +1.18 | 7.0 (6) | 0.32 |

**points** (expected = fair_over; 'over/home/fav' side):

| Sample | n | Hit rate | Expected | Edge, pts | z | Chi-square by price band (df) | p |
|---|--:|--:|--:|--:|--:|--:|--:|
| discovery | 11,874 | 48.0% | 47.3% | +0.7 | +1.06 | 14.3 (8) | 0.07 |
| holdout | 6,902 | 46.9% | 45.7% | +1.2 | +1.57 | 11.9 (8) | 0.16 |
| live | 1,545 | 50.1% | 48.4% | +1.7 | +0.96 | 12.8 (7) | 0.08 |

## 3. Evan's under rule (pre-specified)

Pre-specified before the scan: both teams in the league's best third for goals against per game (as of the morning of the game) AND both projected starters with GSAx >= 0 -> the under hits more often than Pinnacle's price says. Tested on all of 2025-26 (no search was involved, so no multiple-testing penalty) and live.

| Version | Sample | Games | Under hit | Under expected | Edge, pts (95% CI) | z | ROI at Pinnacle | ROI best US book | Close move toward under, pts |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Evan's rule (both D top third + both goalies GSAx >= 0) | 2025-26 (all) | 67 | 50.7% | 50.1% | +0.6 (-11.3, +12.6) | +0.10 | -1.5% | -1.7% | +0.0 (n=66) |
| Evan's rule (both D top third + both goalies GSAx >= 0) | 2026-27 live | 3 | 33.3% | 50.7% | -17.3 (-73.9, +39.2) | -0.60 | -34.3% | -34.9% | – |
| Both D top third (goalies any) | 2025-26 (all) | 97 | 49.5% | 50.2% | -0.7 (-10.7, +9.2) | -0.14 | -4.0% | -4.1% | -0.3 (n=96) |
| Both D top third (goalies any) | 2026-27 live | 10 | 30.0% | 50.2% | -20.2 (-51.2, +10.8) | -1.28 | -40.5% | -41.2% | -0.2 (n=1) |
| Both goalies GSAx >= 0 (defence any) | 2025-26 (all) | 346 | 49.1% | 49.9% | -0.8 (-6.1, +4.5) | -0.30 | -4.4% | -5.0% | +0.1 (n=343) |
| Both goalies GSAx >= 0 (defence any) | 2026-27 live | 25 | 48.0% | 49.8% | -1.8 (-21.4, +17.7) | -0.18 | -5.7% | -6.7% | +0.2 (n=11) |
| Both D top half + both goalies GSAx >= 0 | 2025-26 (all) | 136 | 47.8% | 50.2% | -2.4 (-10.8, +6.0) | -0.57 | -7.5% | -7.7% | -0.1 (n=134) |
| Both D top half + both goalies GSAx >= 0 | 2026-27 live | 7 | 57.1% | 50.1% | +7.1 (-30.0, +44.1) | +0.37 | +11.3% | +10.3% | -0.5 (n=2) |
| Combined GA/g in lowest third (discovery cut) | 2025-26 (all) | 347 | 48.4% | 50.2% | -1.8 (-7.1, +3.5) | -0.67 | -6.6% | -7.5% | -0.1 (n=344) |
| Combined GA/g in lowest third (discovery cut) | 2026-27 live | 30 | 46.7% | 50.2% | -3.5 (-21.4, +14.3) | -0.39 | -9.6% | -11.0% | -0.6 (n=8) |

MTL-NYR games in the data:

| Date | Game | Line | Pinnacle P(under) | Goals | Evan's rule flag | Both D top third | Goalies GSAx (home, away) |
|---|---|--:|--:|--:|--:|--:|---|
| 2025-10-18 | NYR@MTL | 6.0 | 50.5% | 7 | 0 | 0 | -2.8, +6.9 |
| 2025-12-13 | MTL@NYR | 6.0 | 52.9% | 9 | 0 | 0 | +8.6, -4.1 |
| 2026-04-02 | MTL@NYR | 6.5 | 51.4% | 5 | 0 | 0 | +22.4, +17.7 |
| 2026-11-16 | MTL@NYR | 6.0 | 49.0% | 4 | 0 | 0 | +1.2, +13.7 |

## 4. Is there more signal than chance? (normality check of the z-scores)

If every feature were noise, the trend z-scores would look like draws from a standard normal. Trend tests: 157; |z| > 1.96: 8.9% (5% expected under pure noise); |z| > 2.58: 3.8% (1% expected); largest |z| 3.60. Kolmogorov-Smirnov vs N(0,1): D = 0.048, p = 0.844; Shapiro-Wilk normality p = 0.390. Single-feature slices: 359; |z| > 1.96: 8.9% (slices of one feature overlap, so this is a rough guide).

Per market:

| Market | Trend tests | Share with abs(z) > 1.96 | KS p (vs normal) |
|---|--:|--:|--:|
| home | 36 | 11% | 0.08 |
| pl_fav | 19 | 11% | 0.71 |
| points | 20 | 10% | 0.58 |
| sog | 33 | 18% | 0.57 |
| total | 49 | 0% | 0.83 |

## 5. Candidates from discovery and whether they held up

Sorted by discovery |z|. Direction = the side the slice beat its price on. Holdout p is one-sided in that direction. 'Holds up' = holdout p < 0.05 and survives BH across all candidates. Drift = average move of Pinnacle's price toward the pattern between pick time and the close (positive = the market later agreed).

| Market | Slice | Why picked | Side | Disc n | Disc edge | Disc z | Hold n | Hold edge | Hold p | Live n | Live edge | Hold ROI Pinnacle | Hold drift | Holds up |
|---|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|
| home | away_goalie_gsax_pg mid | lead | away | 260 | -8.4 | -2.76 | 222 | +0.3 | 0.459 | 39 | +11.3 | -3.2% | -0.1 | no |
| home | diff_finish_pg low & diff_rest high | lead | home | 75 | +13.2 | +2.34 | 34 | +8.4 | 0.159 | 11 | +13.1 | +17.4% | -0.0 | no |
| home | diff_finish_pg low & away_backup=1 | lead | home | 53 | +15.2 | +2.25 | 26 | -1.8 | 0.575 | 6 | -11.7 | +0.0% | +0.4 | no |
| home | home_fav = 1 | lead | away | 507 | -4.8 | -2.21 | 276 | +2.3 | 0.218 | 64 | +5.0 | +1.6% | +0.0 | no |
| home | early_start = 1 | lead | home | 97 | +9.5 | +1.90 | 55 | +0.5 | 0.467 | 19 | -3.8 | +0.3% | +0.0 | no |
| home | diff_finish_pg low & ml_home_fair high | lead | away | 84 | -9.4 | -1.81 | 26 | +0.7 | 0.472 | 5 | +11.7 | -2.7% | -0.6 | no |
| home | ml_home_fair low (<= 0.496) | lead | home | 261 | +5.5 | +1.79 | 141 | +0.3 | 0.469 | 50 | -9.3 | -3.3% | -0.2 | no |
| home | diff_finish_pg high & diff_goalie_gsax_pg high | lead | away | 81 | -9.7 | -1.79 | 33 | -7.0 | 0.798 | 18 | -1.4 | -17.6% | -0.1 | no |
| home | diff_finish_pg high (> 0.189) | lead | away | 261 | -5.4 | -1.78 | 111 | -2.9 | 0.736 | 44 | +7.5 | -12.2% | +0.1 | no |
| home | diff_prev_xg_pct high (> 0.0184) | lead | away | 261 | -5.3 | -1.78 | 156 | -2.4 | 0.736 | 38 | +8.6 | -9.5% | +0.2 | no |
| pl_fav | division_game = 1 | lead | dog +1.5 | 201 | -12.4 | -3.70 | 171 | -1.8 | 0.690 | 30 | +2.7 | – | – | no |
| pl_fav | season_gp low (<= 20) | lead | dog +1.5 | 269 | -7.7 | -2.64 | 0 | – | nan | 106 | -2.6 | – | – | no |
| pl_fav | fav_fair_pl mid | lead | dog +1.5 | 260 | -7.7 | -2.62 | 146 | +3.4 | 0.191 | 33 | +3.7 | – | – | no |
| pl_fav | dog_pk_xga60 high (> 7.77) | lead | dog +1.5 | 260 | -7.5 | -2.55 | 131 | -8.2 | 0.976 | 70 | -7.4 | – | – | no |
| pl_fav | fav_xg_edge low (<= 0.0077) | lead | dog +1.5 | 261 | -7.3 | -2.54 | 125 | +4.3 | 0.150 | 28 | +13.8 | – | – | no |
| pl_fav | dog_goalie_gsax_pg mid | lead | dog +1.5 | 259 | -7.4 | -2.50 | 236 | -2.2 | 0.758 | 38 | -14.3 | – | – | no |
| pl_fav | fav_b2b = 1 | lead | dog +1.5 | 91 | -11.3 | -2.28 | 54 | +7.0 | 0.139 | 11 | -12.4 | – | – | no |
| pl_fav | dog_finish_pg low (<= -0.136) | lead | dog +1.5 | 261 | -6.6 | -2.27 | 148 | -4.2 | 0.857 | 71 | +2.3 | – | – | no |
| pl_fav | early_start = 1 | lead | dog +1.5 | 97 | -10.9 | -2.27 | 55 | +1.8 | 0.389 | 18 | +6.2 | – | – | no |
| pl_fav | fav_gd_edge low (<= 0.0476) | lead | dog +1.5 | 261 | -6.5 | -2.25 | 106 | -0.1 | 0.511 | 27 | +16.5 | – | – | no |
| points | D = 1 | lead | over | 2764 | +2.3 | +2.38 | 1677 | +2.6 | 0.018 | 331 | +4.9 | -2.8% | – | no |
| points | tot_line > 6 | lead | over | 3831 | +2.6 | +2.33 | 2954 | +2.0 | 0.054 | 765 | +2.5 | -2.9% | – | no |
| points | pts_l10 low (<= 0.5) | lead | over | 4184 | +1.8 | +2.16 | 2628 | +1.5 | 0.079 | 458 | +0.6 | -5.9% | – | no |
| points | toi_std high (> 20.1) | lead | over | 3955 | +2.0 | +2.16 | 2128 | +2.1 | 0.037 | 480 | +3.9 | -3.0% | – | no |
| points | pts_minus_line low (<= 0.0152) | lead | over | 3958 | +1.7 | +1.99 | 2472 | +2.2 | 0.028 | 477 | +2.0 | -4.7% | – | no |
| points | goals_std low (<= 0.182) | lead | over | 4020 | +1.6 | +1.84 | 2044 | +2.3 | 0.025 | 520 | +1.7 | -4.5% | – | no |
| points | fair_over low (<= 0.408) | lead | over | 3962 | +1.5 | +1.82 | 2770 | +1.1 | 0.146 | 440 | +4.1 | -7.4% | – | no |
| points | game_over_fair high (> 0.511) | lead | over | 3834 | +1.9 | +1.68 | 2441 | +1.8 | 0.087 | 568 | -0.3 | -3.0% | – | no |
| points | points_std low (<= 0.545) | lead | over | 3970 | +1.4 | +1.60 | 2561 | +1.8 | 0.059 | 455 | +2.0 | -5.6% | – | no |
| points | home = 1 | lead | over | 6052 | +1.3 | +1.52 | 3570 | +0.8 | 0.250 | 789 | +1.4 | -5.8% | – | no |
| sog | opp_b2b = 1 | lead | over | 1631 | +3.5 | +2.73 | 1116 | +1.4 | 0.190 | 180 | +2.4 | – | +0.1 | no |
| sog | model_minus_fair low (<= -0.0216) | lead | under | 3381 | -2.0 | -2.41 | 3590 | +3.9 | 0.000 | 507 | -1.5 | – | +0.2 | YES |
| sog | model_minus_fair high (> 0.013) | lead | over | 3380 | +1.8 | +2.11 | 788 | +6.4 | 0.000 | 371 | +1.1 | – | +0.5 | YES |
| sog | missing_toi low (<= 18.8) | lead | over | 3388 | +1.7 | +1.99 | 1940 | -2.0 | 0.934 | 444 | +3.2 | – | +0.0 | no |
| sog | D = 1 | lead | over | 2081 | +2.1 | +1.97 | 1298 | -2.1 | 0.939 | 244 | -0.1 | – | -0.1 | no |
| sog | team_ca_ratio low (<= 0.977) | lead | under | 3382 | -1.6 | -1.87 | 2277 | +3.2 | 0.003 | 704 | -3.5 | – | +0.0 | YES |
| sog | on_net high (> 0.532) | lead | under | 3380 | -1.5 | -1.82 | 1716 | +3.2 | 0.005 | 329 | -2.5 | – | -0.1 | YES |
| sog | toi_jump high (> 0.0493) | lead | over | 3380 | +1.5 | +1.79 | 1899 | -0.9 | 0.764 | 437 | +3.1 | – | -0.0 | no |
| sog | opp_ga_pct mid | lead | under | 3304 | -1.5 | -1.78 | 1840 | +2.4 | 0.043 | 394 | +0.7 | – | -0.0 | no |
| sog | team_ca_ratio mid | lead | over | 3385 | +1.5 | +1.76 | 1861 | +0.0 | 0.497 | 227 | -1.2 | – | -0.0 | no |
| total | away_tz_shift high (> 1) | lead | over | 82 | +15.7 | +2.85 | 43 | -1.0 | 0.551 | 16 | -6.4 | -5.0% | -0.1 | no |
| total | sum_pk_xga60 low (<= 13.6) | lead | over | 250 | +7.3 | +2.32 | 55 | +4.4 | 0.255 | 14 | -21.4 | +5.3% | +0.1 | no |
| total | sum_gf_pg high & any_backup=1 | lead | over | 83 | +12.1 | +2.21 | 62 | +2.3 | 0.356 | 26 | +14.7 | +1.6% | -1.0 | no |
| total | sum_gf_pg high (> 6.32) | lead | over | 250 | +7.0 | +2.20 | 152 | +0.1 | 0.488 | 56 | -0.5 | -2.7% | -0.3 | no |
| total | home_goalie_gsax_pg mid | lead | over | 254 | +6.6 | +2.10 | 213 | -2.3 | 0.754 | 44 | +1.9 | -7.5% | -0.2 | no |
| total | sum_save_pg mid | lead | over | 254 | +6.3 | +2.00 | 166 | -3.3 | 0.801 | 30 | -6.7 | -9.6% | -0.3 | no |
| total | line_65 = 1 | lead | over | 244 | +6.2 | +1.93 | 172 | -2.4 | 0.739 | 57 | -2.8 | -8.2% | +0.2 | no |
| total | sum_l10_gf_pg mid | lead | over | 255 | +6.0 | +1.91 | 124 | +2.2 | 0.315 | 40 | -2.7 | +0.8% | +0.1 | no |
| total | away_road_trip low (<= 1) | lead | over | 295 | +5.5 | +1.88 | 170 | -0.8 | 0.582 | 44 | +6.7 | -4.8% | +0.1 | no |
| total | sum_ga_pg low & xg_total_minus_line low | lead | over | 57 | +12.4 | +1.87 | 14 | +9.1 | 0.248 | 2 | -49.2 | +15.2% | +0.8 | no |

Holdout and live edges are shown in the candidate's direction (positive = it kept working).

## 6. Strongest trend tests (does the gap grow with the feature?)

b = change in log-odds per 1 standard deviation of the feature, after the market price. Top 8 per market by discovery |z|.

| Market | Feature | Disc z | Holdout z (same sign = kept) | Live z | BH (disc) |
|---|---|--:|--:|--:|---|
| sog | model_minus_fair | +3.60 | +5.19 | +0.31 |  |
| sog | opp_b2b | +2.99 | +1.86 | +0.14 |  |
| sog | on_net | -2.83 | +0.25 | +0.49 |  |
| sog | D | +2.13 | -0.73 | -0.78 |  |
| sog | ev_toi | +2.04 | -0.65 | -0.17 |  |
| sog | toi_jump | +1.96 | +0.59 | +1.05 |  |
| sog | xg_edge | -1.91 | +1.74 | +0.95 |  |
| sog | pp_toi | -1.71 | -0.66 | +1.00 |  |
| home | diff_prev_xg_pct | -2.86 | +0.72 | +0.73 |  |
| home | home_fav | -2.80 | -0.60 | +0.61 |  |
| home | ml_home_fair | -2.30 | -0.01 | +1.07 |  |
| home | early_start | +2.19 | +0.29 | +0.37 |  |
| home | start_hour_et | -1.77 | -1.63 | -1.32 |  |
| home | away_b2b_only | +1.52 | +0.51 | +1.16 |  |
| home | diff_gd_pg | -1.34 | +0.23 | +1.06 |  |
| home | tot_line | +1.27 | -0.24 | +0.21 |  |
| pl_fav | division_game | -2.68 | +0.47 | -0.53 |  |
| pl_fav | tot_line | +2.09 | +0.55 | +0.53 |  |
| pl_fav | fav_xg_edge | +1.60 | +1.78 | +2.20 |  |
| pl_fav | season_gp | +1.44 | +0.38 | +0.43 |  |
| pl_fav | fav_b2b | -1.40 | -1.23 | +0.82 |  |
| pl_fav | early_start | -1.37 | -0.38 | -0.72 |  |
| pl_fav | fav_backup | +1.16 | +0.40 | +0.02 |  |
| pl_fav | fav_gd_edge | +1.10 | +1.10 | +1.84 |  |
| points | D | +2.15 | +1.47 | +1.46 |  |
| points | toi_std | +2.06 | +0.75 | +0.43 |  |
| points | fair_over | -1.91 | -1.08 | -0.53 |  |
| points | tot_line | +1.54 | +0.95 | +0.42 |  |
| points | opp_goalie_gsax_pg | -1.42 | -0.04 | -0.65 |  |
| points | pts_l10 | -1.34 | -1.51 | -0.70 |  |
| points | game_over_fair | +1.32 | +0.43 | -2.20 |  |
| points | goals_std | -1.16 | -2.16 | -0.21 |  |
| total | sum_pk_xga60 | -1.67 | +0.87 | +0.50 |  |
| total | both_b2b | -1.65 | -0.98 | +0.07 |  |
| total | home_b2b_only | -1.58 | -1.61 | -0.50 |  |
| total | line_whole | -1.51 | +0.48 | +0.36 |  |
| total | line_65 | +1.47 | -0.57 | -0.36 |  |
| total | away_tz_shift | +1.45 | -0.78 | -0.79 |  |
| total | sum_finish_pg | -1.44 | -1.81 | -0.88 |  |
| total | away_road_trip | -1.33 | -0.58 | -1.40 |  |

## 7. Goals distribution vs the market's implied Poisson

Each game's Poisson mean is solved from Pinnacle's line and over price (half-goal lines only, n = 671, all seasons). Chi-square goodness of fit of the goal counts: 111.8 on 11 df, p = 0.000. Mean actual 6.39 vs implied 6.38; variance of (actual - implied) 5.17 vs Poisson 6.38 (ratio 0.81; > 1 = more blowouts and shutouts than a Poisson market assumes).

| Goals | Games | Implied by price |
|--:|--:|--:|
| 0 | 0 | 1.3 |
| 1 | 10 | 7.8 |
| 2 | 10 | 24.1 |
| 3 | 52 | 50.2 |
| 4 | 40 | 78.6 |
| 5 | 149 | 99.2 |
| 6 | 83 | 104.9 |
| 7 | 152 | 95.6 |
| 8 | 52 | 76.6 |
| 9 | 67 | 54.8 |
| 10 | 18 | 35.4 |
| 11+ | 38 | 42.6 |

Odd totals (5, 7, 9) are far more common than even ones (4, 6, 8) because a game tied after regulation always gets one more goal (overtime or the shootout's +1). That is why a plain Poisson fails, and why a whole-number line such as 6.0 pushes less often than a naive model expects. Pinnacle's main-line prices already reflect it (section 2 shows no total bias), so it is a modelling fact, not an edge.

## 8. Patterns that kept the same direction everywhere

Same direction in discovery, holdout AND live (by chance alone about 1 in 4 candidates would do this):

| Market | Slice | Side | Edge disc / hold / live, pts | Lines or games disc / hold / live |
|---|---|---|---|---|
| home | away_goalie_gsax_pg mid | away | +8.4 / +0.3 / +11.3 | 260 / 222 / 39 |
| home | diff_finish_pg low & diff_rest high | home | +13.2 / +8.4 / +13.1 | 75 / 34 / 11 |
| home | home_fav = 1 | away | +4.8 / +2.3 / +5.0 | 507 / 276 / 64 |
| home | diff_finish_pg low & ml_home_fair high | away | +9.4 / +0.7 / +11.7 | 84 / 26 / 5 |
| pl_fav | fav_fair_pl mid | dog +1.5 | +7.7 / +3.4 / +3.7 | 260 / 146 / 33 |
| pl_fav | fav_xg_edge low (<= 0.0077) | dog +1.5 | +7.3 / +4.3 / +13.8 | 261 / 125 / 28 |
| pl_fav | early_start = 1 | dog +1.5 | +10.9 / +1.8 / +6.2 | 97 / 55 / 18 |
| points | D = 1 | over | +2.3 / +2.6 / +4.9 | 2764 / 1677 / 331 |
| points | tot_line > 6 | over | +2.6 / +2.0 / +2.5 | 3831 / 2954 / 765 |
| points | pts_l10 low (<= 0.5) | over | +1.8 / +1.5 / +0.6 | 4184 / 2628 / 458 |
| points | toi_std high (> 20.1) | over | +2.0 / +2.1 / +3.9 | 3955 / 2128 / 480 |
| points | pts_minus_line low (<= 0.0152) | over | +1.7 / +2.2 / +2.0 | 3958 / 2472 / 477 |
| points | goals_std low (<= 0.182) | over | +1.6 / +2.3 / +1.7 | 4020 / 2044 / 520 |
| points | fair_over low (<= 0.408) | over | +1.5 / +1.1 / +4.1 | 3962 / 2770 / 440 |
| points | points_std low (<= 0.545) | over | +1.4 / +1.8 / +2.0 | 3970 / 2561 / 455 |
| points | home = 1 | over | +1.3 / +0.8 / +1.4 | 6052 / 3570 / 789 |
| sog | opp_b2b = 1 | over | +3.5 / +1.4 / +2.4 | 1631 / 1116 / 180 |
| sog | model_minus_fair high (> 0.013) | over | +1.8 / +6.4 / +1.1 | 3380 / 788 / 371 |
| sog | opp_ga_pct mid | under | +1.5 / +2.4 / +0.7 | 3304 / 1840 / 394 |
| total | sum_gf_pg high & any_backup=1 | over | +12.1 / +2.3 / +14.7 | 83 / 62 / 26 |

20 of 50 candidates.

## 9. Shots model (M6 signal) by month

Trend test of the outcome on (shots model probability - Pinnacle fair), after Pinnacle's price, by month. 2025-26 uses the model fit on 2023-25 only (out of sample); 2026-27 uses the frozen live model. z > 2 = the model's disagreement with Pinnacle came true more than chance.

| Month | Lines | z |
|---|--:|--:|
| 2025-10 | 1,511 | +0.66 |
| 2025-11 | 2,786 | +1.46 |
| 2025-12 | 2,762 | +3.38 |
| 2026-01 | 3,082 | +1.69 |
| 2026-02 | 972 | +0.83 |
| 2026-03 | 3,413 | +3.55 |
| 2026-04 | 1,629 | +3.92 |
| 2026-10 | 51 | +0.33 |
| 2026-11 | 1,215 | +0.23 |

## 10. Player points overs by position and line (price check)

Best US-book cost exists for 2025-26 only (live props come from the shadow board).

| Sample | Line | Position | Lines | Hit | Pinnacle fair | Edge, pts | Best US-book cost | ROI best US book |
|---|--:|---|--:|--:|--:|--:|--:|--:|
| discovery | 0.5 | F | 8,492 | 49.8% | 49.8% | -0.0 | 52.3% | -5.1% |
| discovery | 0.5 | D | 2,719 | 44.4% | 41.8% | +2.6 | 45.2% | -2.2% |
| discovery | 1.5 | F | 618 | 40.6% | 37.8% | +2.8 | 41.6% | -2.6% |
| discovery | 1.5 | D | 45 | 17.8% | 32.6% | -14.8 | 37.2% | -50.7% |
| holdout | 0.5 | F | 4,813 | 49.3% | 48.3% | +1.0 | 51.1% | -4.0% |
| holdout | 0.5 | D | 1,641 | 42.8% | 40.2% | +2.7 | 43.7% | -2.6% |
| holdout | 1.5 | F | 412 | 36.9% | 38.4% | -1.5 | 42.2% | -11.5% |
| holdout | 1.5 | D | 36 | 33.3% | 32.8% | +0.6 | 37.2% | -8.1% |
| live | 0.5 | F | 1,115 | 50.8% | 50.4% | +0.4 | – | – |
| live | 0.5 | D | 323 | 49.5% | 44.9% | +4.7 | – | – |
| live | 1.5 | F | 99 | 44.4% | 38.8% | +5.7 | – | – |

## 11. Limits

- 2025-26 starters are projected by a rule (right 83% of the time); live uses DailyFaceoff. A wrong starter blurs goalie patterns.
- Injuries and line changes are not in the 2025-26 archive, so they can't be scanned yet.
- Live 2026-27 is small (a few hundred games), so a live miss is weak evidence either way.
- Closing prices for 2025-26 exist only where a snapshot was cached within 30 minutes of the start.
- Prop slices cluster by game; patterns among lines of the same game are not independent.

