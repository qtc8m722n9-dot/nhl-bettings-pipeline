# Pre-registered hypotheses H2-H5 (registered 2026-11-17, Evan approved)

Written and committed BEFORE any test below was run. Do not edit a registered spec; add a new
version with a new date instead. Research only: none of these is a betting method yet. A
hypothesis is promoted to a paper method only with Evan's approval after it passes.

Common rules (same as `nhlpipe/patterns/scan.py`):
- Expected = Pinnacle no-vig probability at pick time; observed = the result as books settle it.
- 2025-26: DISCOVERY 2025-10-15..2026-01-31, HOLDOUT 2026-02-01..2026-04-16. 2026-27 live = 2026-10-30 on.
- Inputs use only games played before the pick date.
- Test statistic: z = (hits - expected hits) / sqrt(sum p(1-p)), clustered by game for props.
- No Odds API credits are spent on any of these.

## H2 Rink scorekeeper effect on shots-on-goal props
- Rink factor for arena A on date D = (SOG recorded for both teams in A's home games) /
  (SOG the same two teams recorded in their games NOT at A), using the previous full season plus
  the current season before D, shrunk toward 1 with 20 games of prior weight. MoneyPuck team logs.
- Population: every Pinnacle SOG line in the 2025-26 archive (`data/shots2/lines.csv`) and the live shadow board.
- Primary metric: trend of (over hit - Pinnacle fair) on log(rink factor) (logistic, offset logit(fair)).
- Prediction: positive (overs hit more than priced in generous rinks, unders in stingy ones).
- Passes if: discovery z > 0 AND holdout one-sided p < 0.05. Secondary: top vs bottom quartile
  of rink factor edge in points; whether multiplying the M6 projection by the rink factor improves
  M6's log loss vs Pinnacle on the holdout.

## H3 Morning line promotions (shots and points props)
- Data: DailyFaceoff line combinations, scraped daily from 2026-11-18 (no history exists).
- Promotion = a skater listed today on the 1st forward line / 1st D pair or the 1st power-play unit
  who was NOT there in that team's previous snapshot (and the mirror case, demotion).
- Primary metric: edge (hit - Pinnacle fair) on SOG and points overs for promoted players, demoted
  players as the mirror test.
- Prediction: promoted overs beat the price, demoted unders beat the price.
- First look once there are 150 promoted lines; verdict at 400 (one-sided p < 0.05).

## H4 Favourite -1.5 and the over together (correlation)
- Population: every game with a Pinnacle -1.5 price and a main total.
- Primary metric: observed rate of (favourite wins by 2+ AND total over) vs the product of the two
  Pinnacle fair probabilities (what a venue pricing the legs as independent would charge).
- Prediction: joint rate > product (empty-net goals tie the two together). Also reported: the other
  three corners (fav -1.5 & under, dog +1.5 & over, dog +1.5 & under; the dog/under corner should be the
  mirror) and the favourite-moneyline + over pair.
- Passes if: discovery and holdout both show joint > product, holdout one-sided p < 0.05.
- Bettable only where the two legs can be bought separately at near-fair prices (Kalshi spread +
  total markets) - a sportsbook same-game parlay already prices the correlation.

## H5 Popular-team premium on Kalshi
- Popular teams (fixed now): TOR, MTL, EDM, NYR, BOS. Secondary set: all 7 Canadian teams.
- Population: every Kalshi NHL game-winner market at the live pick lock with a Pinnacle fair price
  (2026-27 shadow board) and Kalshi player-prop markets (goals, points) for those teams' players.
- Primary metric: premium = Kalshi mid - Pinnacle fair on the popular team's YES side, compared
  with the same quantity for all other teams (difference in points, 95% bootstrap CI by slate).
- Prediction: popular teams' YES trades above fair by more than other teams'.
- Secondary: ROI of buying the popular team's NO side at the Kalshi ask (paper).
- Interim look now (small sample); verdict once 300 popular-team markets are logged.

# H7-H9 (registered 2026-11-17, later the same day, before any test below was run)

Drawn from outside research (`reports/NHL market inefficiencies for props.md`) plus what the scan found. Same common
rules and splits as above. Each has ONE primary metric; everything else is secondary.

## H7 Trailing coach's goalie-pull aggressiveness -> favourite -1.5
- Pull proxy for a team on date D = empty-net goals it conceded per regulation loss, previous season + current season
  before D (NHL per-game skater stats `emptyNetGoals` of the opponent; regulation losses from MoneyPuck team logs),
  shrunk with 20 losses at the league rate.
- Population: games with a Pinnacle -1.5 price. The underdog's pull proxy is the feature.
- Primary metric: trend of (favourite covered -1.5 - Pinnacle fair) on the underdog's pull proxy. Prediction: positive
  (earlier pulls -> more empty-net goals -> more 2-goal wins than priced). Secondary: the over.
- Passes if discovery z > 0 and holdout one-sided p < 0.05.

## H8 Power-play role change -> player points and SOG overs
- PP share = player PP time / team 5-on-4 + 5-on-3 time, per game. Shift = mean share over the player's last 3 games
  minus his mean share over the 17 games before those (needs >= 8 of them). Only games before D.
- Primary metric: trend of (points over hit - Pinnacle fair) on the shift. Prediction: positive (books price
  season usage, not the new role). Secondary: the same for SOG overs; defencemen only.
- Passes if discovery z > 0 and holdout one-sided p < 0.05.

## H9 Shooting-luck regression in points props
- Finishing luck = (season-to-date goals - season-to-date shots x expected shooting %) per game, where expected
  shooting % = the player's previous-season shooting % shrunk to the position league rate with 223 shots
  (half-signal point from the research). Only games before D.
- Primary metric: trend of (points over hit - Pinnacle fair) on finishing luck. Prediction: negative (hot finishers'
  points are overpriced).
- Passes if discovery z < 0 and holdout one-sided p < 0.05 (in that direction).

# H10-H18: shots model patterns and shot factors (registered 2026-11-17, before the 2024-25 data was pulled)

Evan approved buying 2024-25 Pinnacle SOG props and game lines (pick time 13:50 ET) as a fresh, never-seen season.
All tests are on Pinnacle SOG overs: residual = over hit - Pinnacle no-vig fair at pick time.

Common rules
- PRIMARY sample = 2024-25 (fresh). Supporting = 2025-26 and 2026-27 live (partly seen for H12-H13; reported, not used to decide).
  H11 needs closing prices, which 2024-25 won't have: its primary sample is 2025-26 (this question was never looked at there).
- Shots model for 2024-25 = the v2 GLM refit on 2022-23 + 2023-24 only (out of sample for 2024-25).
  dm = logit(model P(over)) - logit(Pinnacle fair).
- Multiple testing: Benjamini-Hochberg at q = 0.10 over the 9 primary p-values (one-sided, in the predicted direction).
  A hypothesis passes if it survives BH AND 2025-26 has the same sign. Passing = worth a paper method, not proof.
- Player features use only games before the pick date.

| ID | Factor | Feature (primary) | Prediction |
|---|---|---|---|
| H10 | Model sharpens with games played | interaction dm x log(1 + player's games this season) in logistic y ~ offset(logit fair) + a + b1 dm + b2 dm x log(1+gp) | b2 > 0 |
| H11 | Model beats quiet lines | interaction dm x quiet, quiet = Pinnacle fair moved < 0.5 pts pick -> close (2025-26) | interaction > 0 |
| H12 | Tired opponent | opponent played yesterday (flag) | over residual > 0 |
| H13 | Game script | player's team Pinnacle moneyline fair (trend) | negative (underdogs' players shoot more than priced) |
| H14 | Returning from absence (early exit / limited minutes risk) | player missed his team's previous game (flag) | over residual < 0 |
| H15 | Opponent shot blocking | opponent's blocked shots per game, season to date (prev season before 10 games) (trend) | negative |
| H16 | Overtime chance | closeness = 1 - abs(2 x team win fair - 1), among players in the top third of projected EV ice time (trend) | positive |
| H17 | Blowout benching | team win fair >= 0.67 AND top-third EV ice time (flag) | over residual < 0 |
| H18 | Power-play opportunities | opponent penalties taken per game, among players in the top third of PP time (trend) | positive |

Not testable yet: line changes / linemates (collecting since 2026-11-17); referee crews (no data); teammates out
(already in the model as missing_toi; the scan found nothing).

# H19-H20 (registered 2026-11-17 ~19:40 ET, Evan approved; live from the 2026-11-18 pick lock)

## H19 Shots model strong unders on players early in their season (paper method M7_shots_under_early)
- Lead found AFTER H10-H18 were registered (2024-25 +8.2 pts z 5.3; 2025-26 +5.3 z 2.5; 2026-27 to date -0.5, n 184),
  so it is judged ONLY on picks from the 2026-11-18 lock on.
- Rule (nhlpipe/shots2/live.py): raw model P(over) at least 5 pts below Pinnacle's no-vig P(over), player has < 20 games
  this season before the pick date -> Under at the best sportsbook price; one bet per player, up to 3 per game
  (largest gaps first). Sportsbook prices are a paper benchmark (not usable from Quebec).
- Primary: mean(under hit - Pinnacle fair under) over M7 picks; one-sided p < 0.05 at 300 settled picks.
  Secondary: ROI at the book price, CLV vs Pinnacle close.

## H20 Kalshi resting orders (nhlpipe/maker.py, run each morning)
- Every Kalshi market side with a Pinnacle fair price at the lock: virtual bid at fair - 1 cent; filled only if the
  market traded/was offered strictly through the bid before the start; cost = bid + maker fee.
- Primary: ROI and CLV of filled orders (back-filled from 2026-10-31, then forward). Verdict at 300 fills:
  passes if fills' mean CLV vs Pinnacle close > 0 (95% CI by slate) and ROI beats buying the same sides at the ask.
