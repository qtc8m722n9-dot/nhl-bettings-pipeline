# Bullseye: game-winner component (2026-11-03)

Purpose: a moneyline input for the combined model (STATUS step 2). Every factor that research says moves NHL win probability, combined into one P(home wins), then checked against Pinnacle.
Code: `nhlpipe/bullseye.py` (factors, model), `nhlpipe/backtest/bullseye_bt.py` (build, market, fit, test). Full test tables: `report_results.md`.

## Research: what moves NHL win probability

| Factor | Evidence | In Bullseye as |
|---|---|---|
| Team strength from scoring chances | MoneyPuck's pre-game model puts 54% of its weight here (xG, shot attempts, by manpower situation) | 5v5 xG diff/game, non-5v5 xG diff/game |
| Results / finishing | MoneyPuck 17% (win %, recency-weighted). Old research: PDO (luck) doesn't help single-game prediction | goals minus xG per game, shrunk hard (prior worth 80 games) |
| Goaltending | MoneyPuck 29% (multi-season GSAx/60, sv%) | today's projected starter vs the team's usual (GSAx/game, M3's shrinkage) |
| Home ice | home teams win ~54%, partly referee bias (MoneyPuck) | intercept |
| Rest | back-to-back: win rate 45% vs 51% on one day's rest, worse on the road (42%), cap era 2005-25 (nhlscraper). MoneyPuck: about -4 pts when only one side is tired | b2b each side, 3 games in 4 nights, rest-day difference |
| Travel / time zones | teams travelling west to east win more than the reverse (AASM, NFL/NBA/NHL pooled; no NHL-only numbers) | away team's time-zone shift and km since its last game |
| Injuries | GAR-based injury cost is real but measured at season level (Hockey Graphs) | share of regular TOI missing from the team's last game (live: injury list) |
| Market biases | reverse favourite-longshot bias reported in older NHL moneyline studies; totals market inefficient (Woodland & Woodland 2011) | tested on Pinnacle below |
| Ceiling | public models get about 60-61% of games right, log loss ~0.66 (MoneyPuck 2020-25); ~38% of standings is luck (Weissbock et al. 2013) | - |

## Model

Logistic regression on 12 factors (home minus away). Recency weighting, prior weight and regression to the mean were tuned on 2023-24 only, then confirmed on 2024-25. Coefficients were refit on 2023-25 and frozen before 2025-26 was touched. The goalie term isn't fit (no goalie logs cached before 2025-26). It enters in goal units.

Fitted weights that matter: 5v5 xG diff 0.81/goal, non-5v5 0.67, finishing 0.61, away b2b +0.34, home 3-in-4 -0.34, home intercept +0.16. Season-to-date with no recency weighting won the tuning (half-life 20 and 40 games were worse).

## Results

| Test | Bullseye | Benchmark |
|---|--:|--:|
| 2024-25, out of sample (log loss) | 0.660 | MoneyPuck 0.658, home rate only 0.686 |
| 2026-27 to Nov 2, 217 games (results only) | 0.651, favourite won 62.7% | home rate only 0.688 |
| 2025-26 vs Pinnacle, 1205 games | 0.689 | Pinnacle 0.683, M3 raw 0.683 |
| Blend weight on Bullseye next to Pinnacle (2025-26) | 0.20 (95% CI -0.18 to 0.60) | M3: 0.46 |
| Walk-forward blend (fit Oct-Dec, test Jan-Apr) | -0.0003 vs Pinnacle (CI -0.008 to +0.007) | M3: -0.0009 |

## Conclusions

1. **Bullseye is about as good as a public model, but it doesn't beat Pinnacle.** Its blend weight isn't clearly above zero. With M3 in the blend too, Bullseye's weight drops to 0.08: both are xG-based team ratings, and M3 already carries most of that information. Bullseye is not a standalone betting method.
2. **Two leads where the market looks slow** (2025-26; 12 factors tested, so roughly one false hit is expected):
   - **Away team on a back-to-back:** home won 60.6% vs Pinnacle's 56.3% (254 games). The size matches Bullseye's coefficient from 2023-25. But most of the gap comes from October and February (about 20 games each); other months are 0 to +4 pts.
   - **xG vs actual goals:** the market under-weights 5v5 xG difference (lower CI just above 0) and leans on actual goals (CI just touches 0). That's the classic "market chases luck" pattern, but it's borderline.
   - Rest days, 3-in-4, travel, time zones, special teams and the lineup proxy all look priced in.
3. **Fitting a residual model on one season of odds overfits.** Pinnacle plus all 12 factors, fit on Oct-Dec, was worse than Pinnacle alone on Jan-Apr (0.685-0.705 vs 0.680). Corrections to the market need more than one season of data.
4. Pinnacle's 2025-26 moneyline was over-confident (calibration slope 0.74; home favourites at 55-65% won 55%). This is one season and no past-season odds are cached, so it's not a rule.

## Recommendation (needs Evan's approval; nothing live changed)

- Feed Bullseye into the combined model (step 2) as an input: its probability plus the raw `a_b2b`, `ev_xgd` and `fin` factors. The combined model decides their weight out of sample. Bullseye can be rebuilt for any date from data the pipeline already pulls daily (MoneyPuck team logs, NHL box scores, schedule; projected starters from the daily goalie pull), so no new live job is needed.
- Pre-register the away-back-to-back hypothesis for the 2026-27 shadow board: on games where only the away team is on a back-to-back, the home side beats the Pinnacle/Kalshi fair price. Judge it on CLV and results at the 2026-12-31 review.

## Sources

- MoneyPuck, pre-game prediction model: https://moneypuck.com/about.htm
- nhlscraper vignette, "How Costly Are Back-to-Backs in the Salary-Cap Era?": https://ftp2.uib.no/cran/web/packages/nhlscraper/vignettes/back-to-back-tax.html
- Weissbock, Viktor & Inkpen (2013), ML for NHL game outcomes, ECML PKDD: https://www.eecs.uottawa.ca/~diana/publications/ECML_PKDD___2013.pdf
- AASM, teams travelling west are at a disadvantage: https://aasm.org/nfl-nba-and-nhl-teams-have-a-disadvantage-when-traveling-west
- Hockey Graphs, GAR to measure injury impact: https://hockey-graphs.com/2017/04/21/fqg-using-goals-above-replacement-to-measure-injury-impact/
- Woodland & Woodland (2011), NHL betting market efficiency: https://commons.emich.edu/accfin_facsch/91
