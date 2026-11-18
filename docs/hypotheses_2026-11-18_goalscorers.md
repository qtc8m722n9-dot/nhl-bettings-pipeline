# H21 Goalscorer models: price-driven vs price-blind (registered 2026-11-18, before any data below was looked at; Evan approved)

Question: can we estimate P(player scores >= 1 goal) well enough to beat the price on single legs, and then build
small 3-4 leg parlays only from legs that beat their price? Two models are built so they can be compared.

## Model P (price-driven)
- Team expected goals from Pinnacle at pick time: total mean solved from the main total line and its no-vig over
  price (Poisson), split between the teams so that P(home wins, ties split 50/50) matches Pinnacle's no-vig moneyline.
- Player share = player's goal rate / his team's goal rate, both season to date before the pick date:
  player rate = (projected shots per game, shots model baseline mu_base) x (shooting %, his last two seasons shrunk to
  the position rate with 223 shots); team rate = goals for per game (shrunk to the league with 10 games).
- P(score) = 1 - exp(-team expected goals x share).

## Model B (price-blind: no betting prices anywhere)
- Poisson regression of goals per skater-game, offset log(player rate as above), fitted on 2022-23..2024-25 with
  these factors (all point-in-time): EV and PP minutes, defenceman flag, home, own back-to-back, opponent
  back-to-back, opponent expected goals against per game, opponent goaltending (goals saved above expected per game,
  team level), own team expected goals for per game, opponent penalties taken, games played (log).
- P(score) = 1 - exp(-lambda). Coefficients and a factor-drop table (log-loss change on 2025-26 when each factor is
  removed) are reported, so the strongest factors are visible.

## Evaluation (fixed now)
- Samples: 2025-26 full season (Pinnacle + sportsbook anytime-goal prices at 13:50 ET, bought for this test) and
  2026-27 live (Pinnacle, books, Kalshi player-goal markets).
- Accuracy: log loss and calibration of Model P, Model B, and Pinnacle's no-vig price on the same player-games.
- Betting (paper): a single leg = YES when model P(score) - cost >= 3 pts (cost = best US-book price; Kalshi ask + fee
  live). Report ROI, hit rate, and edge vs Pinnacle fair for each model.
- Parlays (paper): each night, the 3 legs with the largest model edge from different games, priced as the product of
  the legs (separate markets). Report hit rate and ROI.
- Primary comparison: which model's single legs beat Pinnacle's no-vig price (mean(hit - Pinnacle fair)) on 2025-26,
  one-sided p < 0.05; the winner is then judged live from 2026-11-19 on (300 legs).
