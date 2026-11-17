# NHL Game-State Mechanics: Empty Nets, Goalie Pulls, Score Effects, Overtime (linking margin, totals, late-game outcomes)

Research date: 2026-11-17. About 20 tool calls. Scope: late-game mechanics that set final margins and totals, for testing puck line (-1.5), totals and their combination. Wherever a number is my own derivation rather than something a source stated, it is marked **[derived]** or listed under Inferences.

## 1. Empty-net goal rates by season, the 1-goal to 2-goal conversion, and the trend toward earlier pulls

### Takeaway
Empty-net goals (ENGs) have roughly tripled as a share of scoring in 20 years. They went from about 2.4% of goals (2005-06) to about 7% (2024-25), and the 2024-25 rate was about 0.40-0.42 ENG per game. 2021-22 set a regular-season record of 477 ENGs (about 0.36 per game), and 2024-25 was described mid-season as on pace to break it. Theory (Asness & Brown, Beaudoin & Swartz) says to pull far earlier than coaches do: about 5-6 minutes left when down one, versus the observed average of about 1:04. So the trend toward earlier pulls has room to run. Any puck-line model built on pre-2018 margin distributions will understate how often a 1-goal lead becomes a 2-goal win.

### Cited Findings
**League ENG volume and rate**
- 2005-06: empty-netters were 2.4% of all goals (about 1 in 42). In the first quarter of 2024-25 they were 7.0% (about 1 in 14). The recent pace was 0.42 ENG per game. — [Daily Faceoff, "The rise of empty net goals"](https://dailyfaceoff.com/news/how-empty-net-goals-have-changed-the-nhl)
- 2024-25 through March 11, 2025: the league ENG rate had "dropped slightly" to 0.40 per game. The writer expected 2024-25 to set the all-time record for league ENGs ("The Year of the Empty Netter"). — [Daily Faceoff, stretch-drive storylines (Mar 12 2025)](https://dailyfaceoff.com/news/top-8-statistical-chase-nhl-stretch-drive-ovechkin-crosby-hellebuyck-makar)
- 2024-25 through about Jan 6, 2025: "One in 14 NHL goals… is scored into an empty net," triple the rate of 20 years earlier. Extra-attacker goals (scored by the team that pulled its goalie) were on pace for 240, versus 138 a decade earlier. — [Daily Faceoff, five statistical trends 2025](https://www.dailyfaceoff.com/news/five-statistical-trends-to-watch-in-2025)
- 2021-22 regular season: a record 477 ENGs in 1,312 games. The previous records were 408 (2018-19) and 368 (2015-16). The top 13 regular seasons for ENGs have all come since 2007-08. The 2022 playoffs set a postseason record of 41 ENGs in 76 games. — [ESPN (Kaplan/Wyshynski), 2022](https://www.espn.com/nhl/story/_/id/34020506/why-2022-stanley-cup-playoffs-set-new-empty-net-goals-record)
- Team ENG counts, 2023-24: league average 13.8 per team. Winnipeg had 24 (tying Dallas 2015-16 for the record), Tampa Bay 23, Florida 21, San Jose 4. — [Daily Faceoff](https://dailyfaceoff.com/news/how-empty-net-goals-have-changed-the-nhl)
- 2024-25: Colorado had 24 team ENGs by March 11, 2025, tying the record. Rantanen and Ovechkin had 8 ENGs each, against a record of 9. — [Daily Faceoff (Mar 2025)](https://dailyfaceoff.com/news/top-8-statistical-chase-nhl-stretch-drive-ovechkin-crosby-hellebuyck-makar)
- Player-level ENG effects are now material for props. Kucherov had 14 ENG points in 2023-24, out of 144 total. Without ENG points, MacKinnon (132 points without ENG) would have led him (130 without ENG) in the Art Ross race. — [Daily Faceoff](https://dailyfaceoff.com/news/how-empty-net-goals-have-changed-the-nhl)

**Effect on margin (1-goal wins becoming 2-goal wins)**
- ESPN Research defines "close games" as games decided by one goal, or by two or more after an empty-netter. In 2024-25, 74% of wins were close games, the highest rate in NHL history. — [ESPN, 2025-26 OT/shootout article](https://africa.espn.com/nhl/story/_/id/47210375/nhl-2025-26-games-shootout-theories-trends-stats-standings)
- Outcomes once the goalie is pulled (2013-14 to 2019-20 regular season): a team trailing by one ends in a regulation tie about 15% of the time, a team trailing by two about 1% (25 occurrences), and a team trailing by three never. About 6.5 goals per 60 for the attacking team at 6v5, about 12 per 60 at 6v4, and about 11 ENG per 60 against at 6v4. The 6v5 ENG-against rate is described as "particularly high", with no number given in the text. Teams averaged about 34 minutes per season with the goalie pulled. — [Hockey-Graphs, "The State of Goalie Pulling in the NHL" (2020)](https://hockey-graphs.com/2020/05/18/the-state-of-goalie-pulling-in-the-nhl/)

**Pull timing: theory and observed practice**
- Asness & Brown (2018, "Pulling the Goalie: Hockey and Investment Implications", SSRN): when down one, pull with about 6 minutes left; when down two or more, pull even earlier. Teams usually pull with less than 2 minutes left, often about 1 minute. Brown attributes the gap to coaches' incentives ("content to lose quietly and gracefully"), not to coaches misunderstanding the math. — [Newswise / NYU release](https://www.newswise.com/articles/when-to-pull-the-goalie-nyu-researcher-offers-risk-based-analysis)
- Observed averages from Stathletes data, as reported in 2022: when trailing by one, the goalie came out with 1:04 left in the regular season and 1:19 in the playoffs. When trailing by two, it came out with 1:44 left (regular season) and 1:56 (playoffs). A 2015 FiveThirtyEight model gave a 19-20% chance of tying when pulling with 2:30 left, versus 17% when waiting until 1:00. — [ESPN 2022](https://www.espn.com/nhl/story/_/id/34020506/why-2022-stanley-cup-playoffs-set-new-empty-net-goals-record)
- The average pull time when down one rose by about 30 seconds from 2013-14 to 2019-20. Pulls when down two show no clear trend. The author says "quite a lot of progress" remains relative to ThePullBot, MoneyPuck's model based on Beaudoin & Swartz. — [Hockey-Graphs 2020](https://hockey-graphs.com/2020/05/18/the-state-of-goalie-pulling-in-the-nhl/)
- Beaudoin & Swartz (2010) is referenced as the basis of MoneyPuck's ThePullBot. I could not retrieve the paper's own optimal-time figures in this session. — [Hockey-Graphs 2020](https://hockey-graphs.com/2020/05/18/the-state-of-goalie-pulling-in-the-nhl/)

### Inferences
- **[derived]** At about 0.40-0.42 ENG per game, a Poisson upper bound for the share of games with at least one ENG is 1 − e^-0.41 ≈ 34%. ENGs cluster, since a team can score several into an empty net in one game, so the true share is probably somewhat lower (perhaps about 28-32%). This needs to be measured directly from play-by-play.
- **[derived]** 2021-22 ran at 477 / 1,312 ≈ 0.36 ENG per game, and 2024-25 at about 0.40-0.42. At about 6.1 goals per game in 2005-06, 2.4% of goals implies about 0.15 ENG per game, so per-game ENG volume has risen roughly 2.5-3x.
- Combined with the ESPN "close games" figure (74% of 2024-25 wins), a large share of 2+ goal regulation wins are really 1-goal games plus an ENG. That makes favourite -1.5 cover rates more sensitive to pull aggressiveness than to team strength. My working hypothesis is that about 40-50% of 2-goal wins include an ENG. This is speculation and must be computed.
- ENGs add to totals, but only in games that are close late. Each trailing-by-one pull is a two-sided gamble: the trailing team scores about 6.5 per 60 at 6v5, and the empty-net goal rate against it is higher still. Either outcome adds a goal, so earlier pulls push totals up in close games and do almost nothing in blowouts.
- Theory says to pull about 4-5 minutes earlier than coaches do. Further drift toward earlier pulls is plausible, which would add ENG volume and keep pushing -1.5 cover rates up for 1-goal leaders. This is speculation about future coach behaviour.

### Gaps
- I found no official season-by-season ENG table (league totals and per-game rates) for 2015-16 through 2025-26. Only 2015-16 (368), 2018-19 (408), 2021-22 (477) and in-season 2024-25 rates (0.40-0.42 per game) are sourced here. I found no final 2024-25 total, nothing confirming whether the record was broken, and no 2025-26 or 2026-27 figures. NHL.com stats (team summary: ENG for/against) or the play-by-play can fill this.
- I found no source giving the share of games with an ENG, or the share of 2-goal wins that include an ENG, for any season.
- I could not read the full Asness & Brown SSRN paper (win probabilities, assumed scoring rates) or the Beaudoin & Swartz 2010 paper (Canadian Journal of Statistics / JQAS).
- I found no published average pull times by season after 2021-22.

## 2. Which coaches and teams pull earliest, whether it persists, and whether it can be measured from play-by-play

### Takeaway
Some teams are known to be aggressive (Toronto and Carolina 2013-20; Colorado under Patrick Roy in 2015-16; Seattle under Hakstol and Columbus are also discussed), and coaches describe pull timing as a "feel" decision. Extra-attacker shot rates repeat weakly from season to season (r ≈ 0.19-0.22). Extra-attacker goal rates do not repeat (r ≈ 0). The team or coach pull-time tendency itself is the most promising persistent input. Pull timing can be measured from public play-by-play: Hockey-Graphs did it from Evolving-Hockey's scraped data, using each team's first pull per game and excluding delayed penalties.

### Cited Findings
- Toronto and Carolina were "consistently more aggressive than average" from 2013-14 to 2019-20. The 2015-16 spike in pull times is partly attributed to Colorado (Roy), with Tampa Bay and Chicago also aggressive. Team offence (xGF/60 RAPM) shows no strong relationship with pull timing. — [Hockey-Graphs 2020](https://hockey-graphs.com/2020/05/18/the-state-of-goalie-pulling-in-the-nhl/)
- Repeatability, tested by splitting each team-season into odd and even games: extra-attacker goal scoring ≈ 0. Extra-attacker shot-attempt rate r = 0.22, or 0.19 when the split is repeated 1,000 times. Five-forward usage at 6v5 nearly doubled over the seven seasons studied, without a clear rise in 6v5 scoring. — [Hockey-Graphs 2020](https://hockey-graphs.com/2020/05/18/the-state-of-goalie-pulling-in-the-nhl/)
- Rod Brind'Amour (Carolina) calls pulling "a feel thing for me", not analytics. Gerard Gallant waits longer in high-scoring games and pulls sooner in 1-0 or 2-1 games. — [ESPN 2022](https://www.espn.com/nhl/story/_/id/34020506/why-2022-stanley-cup-playoffs-set-new-empty-net-goals-record)
- Seattle Kraken team analytics content discusses earlier pulls under Hakstol, and Columbus earlier pulls are also defended in the press. These pages turned up in search, but I did not open them, so no numbers are taken from them. — [NHL.com Kraken "Analytics with Alison"](https://www.nhl.com/kraken/news/analytics-with-alison-pulling-the-goaltender-327235290); [The Hockey News on Columbus](https://thehockeynews.com/nhl/columbus-blue-jackets/latest-news/yes-the-blue-jackets-should-keep-pulling-their-goalie)
- Hockey-Graphs' method used Evolving-Hockey play-by-play, the first pull per team per game, and removed delayed-penalty goalie pulls. — [Hockey-Graphs 2020](https://hockey-graphs.com/2020/05/18/the-state-of-goalie-pulling-in-the-nhl/)
- The NHL's current public endpoint for play-by-play is `/v1/gamecenter/{game-id}/play-by-play` (JSON), per the community API reference. That document does not describe the `situationCode` field. — [Zmalski NHL-API-Reference](https://uithub.com/Zmalski/NHL-API-Reference)

### Inferences
- **[unverified, from working knowledge, not sourced in this session]** In api-web.nhle.com play-by-play, each event carries a 4-digit `situationCode` read as [away goalie in net (1/0)][away skaters][home skaters][home goalie in net (1/0)]. So `1551` is 5v5 with both goalies in, `0651` is the away goalie pulled at 6v5, and `1560` is the home goalie pulled. Goal events also carry `details.goalieInNetId`, which is absent on empty-net goals. Pull time ≈ the first event in regulation, with game time remaining under about 5:00, where the trailing team's goalie digit = 0 and no delayed-penalty indicator is present. This is approximate, because events are discrete. Shift-chart data (`/stats/rest/en/shiftcharts?cayenneExp=gameId=…`) gives exact goalie off-ice times. Verify the decoding against a few known games before relying on it.
- Because the tendency is a coach decision, it should be keyed to coach, not team. Coaching changes should reset the prior. Given the "feel" quotes, partial persistence is plausible, but I found no published year-over-year correlation of average pull time by coach.
- Pairing a favourite's opponent (the trailing team's pull aggressiveness) with the favourite's ENG finishing is the relevant interaction for -1.5. An aggressive-pulling underdog raises the favourite's -1.5 cover probability when the favourite leads by one late, and also raises the underdog's chance of tying.

### Gaps
- I found no current (2022-2026) published ranking of coaches by average pull time, and no measure of how well it repeats. MoneyPuck and HockeyViz may publish this, but I did not retrieve it.
- I found no official NHL documentation of `situationCode`. The decoding above is unverified.

## 3. Score effects: shot and goal rates when leading or trailing, and how this relates to totals for heavy favourites versus even matchups

### Takeaway
Score effects are large for shot volume but small for goal rates. Trailing teams out-attempt leaders by a lot, but the adjustment weights for goals and xG stay within about ±7-9% of neutral. Teams also appear to be defending leads more conservatively lately: scoring chances in the final 10 minutes are down 5.57% since 2015. For totals this suggests that mismatched games do not get a big "garbage-time" boost at 5v5. The material late-game total effect comes from extra-attacker play and ENGs in close games.

### Cited Findings
- Evolving-Hockey score-adjustment weights at 5v5, using McCurdy's (HockeyViz) method, from the home team's perspective. Corsi weights reach 0.843 for the home side when down 3+ (away leaders 1.230), and 1.140 for the home side when up 3+ (away 0.891). Goal weights when the home team trails are 0.938 (away 1.071), and when it leads 0.988 (away 1.012). xG weights when trailing are 0.923 (away 1.091). In other words, shot-based effects are much larger than goal-based effects. — [Evolving-Hockey glossary: Score Adjustments](https://evolving-hockey.com/glossary/score-adjustments/)
- Scoring chances in the final 10 minutes of games are down 5.57% since 2015 (Meghan Chayka, Stathletes). Chayka argues teams defend leads more conservatively. 2025-26 third-period scoring was 2.14 goals per game through 850 games, in line with the four previous seasons, and third-period shooting was 12.0% versus 11.8%. — [ESPN 2025-26](https://africa.espn.com/nhl/story/_/id/47210375/nhl-2025-26-games-shootout-theories-trends-stats-standings)
- In 2024-25, 43% of games were comeback wins, the second-highest rate in NHL history. In 2025-26, 68 wins came after trailing in the third period at the time of writing, against 78 at the same point of 2023-24. — [ESPN 2025-26](https://africa.espn.com/nhl/story/_/id/47210375/nhl-2025-26-games-shootout-theories-trends-stats-standings)
- HockeyViz has a "Score Sequencing" explainer on modelling score-state dynamics (not opened). — [HockeyViz](https://www.hockeyviz.com/txt/scoreSeq)

### Inferences
- With heavy favourites, the favourite leads more often, and leads trigger defensive play and lower shot volume from the leader. Goal rates move little, so the totals effect at 5v5 is likely small. The most likely net effect is that heavy-favourite games end with somewhat fewer "extra" late goals than an even-strength Poisson implies, unless the game is within one goal late. This is speculation and needs testing by binning games by moneyline and comparing actual goals with the market total.
- Even matchups spend more time tied or within one goal late. That raises (a) overtime frequency and (b) extra-attacker time, which adds both 6v5 goals and ENGs. A heavier-tailed goal distribution in close games could make overs on 5.5 or 6 slightly more likely than an independent-Poisson model predicts. This is a hypothesis.
- Leading teams in close games concede extra-attacker goals at about 6.5 per 60 at 6v5, while the leader scores ENGs at a higher rate. The joint distribution of (margin, total) is therefore correlated in a structured way. A favourite -1.5 cover via ENG also adds a goal, so favourite -1.5 and over are positively correlated in game types with low totals. This matters for same-game parlays and "combination" pricing.

### Gaps
- I found no source giving raw goals per 60 by score state for recent seasons, or totals results (over/under hit rates) by favourite size. Both need to be computed from play-by-play and odds data.

## 4. Overtime frequency by season, how it varies with game closeness and total line, and implications for 6.0 and odd/even totals

### Takeaway
From 2016-17 to 2024-25 the share of games tied after regulation was stable at 20.5-23.5%. Early 2025-26 ran at 27.3%, which would be the highest of the shootout era (previous high 25% in 2013-14). The NHL counts an overtime or shootout winner as one extra goal, so every game that reaches overtime finishes with an odd total. A regulation tie at 2-2 becomes 5, and at 3-3 becomes 7. That gives totals of 5.5 and 6.0 a mechanical structure.

### Cited Findings
- Percentage of games tied after regulation: 2016-17 23.5%; 2017-18 23.3%; 2018-19 21.3%; 2019-20 23.1%; 2020-21 22.5%; 2021-22 22%; 2022-23 23%; 2023-24 20.7%; 2024-25 20.5%; 2025-26 27.3% through 425 games. That 27.3% would be the highest since 2005-06; the previous high was 25% in 2013-14. Some weeks in early 2025-26 hit 35% and 39%. 65.5% of 2025-26 overtimes ended in overtime rather than a shootout. — [ESPN 2025-26](https://africa.espn.com/nhl/story/_/id/47210375/nhl-2025-26-games-shootout-theories-trends-stats-standings)
- 2024-25 (through about Jan 2025): a record 77% of games tied after regulation ended in overtime, against 61% when 3-on-3 debuted. There were 30 shootouts in 639 games, a pace of 62 per season versus an average of 97 per season since 2015-16. — [Daily Faceoff 2025 trends](https://www.dailyfaceoff.com/news/five-statistical-trends-to-watch-in-2025)
- Playing for the tie: players and coaches (Jason Robertson, Sheldon Keefe) say teams ease off late in tied games to secure a point. Stathletes says the expected-score winner wins only 54% of the time. — [ESPN 2025-26](https://africa.espn.com/nhl/story/_/id/47210375/nhl-2025-26-games-shootout-theories-trends-stats-standings)
- 2022 playoffs: only 14% of games went to overtime through 76 games, against 32% the previous postseason, 22% (2019-20) and 20% (2018-19). — [ESPN 2022](https://www.espn.com/nhl/story/_/id/34020506/why-2022-stanley-cup-playoffs-set-new-empty-net-goals-record)
- Totals usually sit at 5.5 or 6, and shopping 5.5 against 6 changes expected value. This is unsourced editorial from a betting site. — [DeucesCracked 2026-27 guide](https://www.deucescracked.com/blog/nhl-2026-27-regular-season-betting-guide-puck-line-goalies)

### Inferences
- **[derived, NHL scoring convention]** Every overtime or shootout game finishes with an odd final total (2k+1 after a k-k regulation tie). On a 6.0 total, a 3-3 regulation tie lands on 7, so the over wins instead of a push. A 2-2 tie lands on 5, so the under wins. Only regulation finishes can push at 6. Pushes on 6.0 therefore require a regulation win with exactly 6 goals (4-2, 5-1, 6-0). Overtime games remove probability mass from even totals. A higher overtime rate (2025-26 at about 27%) shifts the distribution toward odd totals and reduces 6.0 push frequency. Even/odd total props should be priced with the overtime probability explicitly.
- If a market treats total goals as roughly Poisson with no overtime adjustment, it will overprice "even" in high-overtime environments. Overtime probability is highest in evenly matched, low-total games, and those are exactly the games where a 2-2 tie into overtime puts 5 on the board. Some under-5.5 bets in low-total even games can be lost to the overtime goal. This needs testing.
- The 2025-26 overtime spike may be regression noise: the 2016-25 range was 20.5-23.5%. A pipeline should use a shrunk estimate (perhaps about 23-24%) rather than the hot early-season rate. This is speculation.
- Overtime probability should be modelled as a function of closeness (moneyline near pick'em) and total. Lower totals mean more regulation ties. I found no published table of overtime rate by moneyline or total band. It must be computed.

### Gaps
- I found no source on overtime rate by total line or moneyline band, and no full-season 2025-26 or 2026-27 overtime figures.
- I found no published distribution of NHL final totals (frequency of exactly 5, 6, 7), or of push rates on 6.0.

## 5. Evidence that betting markets misprice puck lines for heavy favourites or totals in games with large favourites

### Takeaway
I found no rigorous, sourced, recent evidence, academic or otherwise, that NHL puck lines or totals are systematically mispriced for heavy favourites. What I found is unsourced betting-site figures (heavy favourites at -1.5 cover about 40-45%) and team-season ATS trend articles. The structural argument for a possible edge is that markets may lag the multi-year rise in ENGs, which mechanically raises favourite -1.5 cover rates in games led by one goal late. That remains a hypothesis to test.

### Cited Findings
- One betting guide claims, without naming a source or period, that favourites at -1.5 (moneyline under -120) cover about 45-48%, heavy favourites (-200 or steeper) cover about 40-45%, underdogs at +1.5 cover about 55-58%, and "about 24%" of games are decided by exactly one goal. The 24% one-goal figure looks inconsistent with ESPN's "74% of wins were close games", so treat these numbers as unreliable. — [Slapshot Diaries, puck line explained](https://www.slapshotdiaries.com/sports-betting-canada/guides/puck-line-explained.html); conflicts with [ESPN 2025-26](https://africa.espn.com/nhl/story/_/id/47210375/nhl-2025-26-games-shootout-theories-trends-stats-standings)
- Daily Faceoff publishes team-level profitability tables for 2024-25 (moneyline and puck line) but no structural analysis (not opened in detail). — [Daily Faceoff 2024-25 betting trends](https://dailyfaceoff.com/news/2024-25-nhl-betting-trends)
- ENGs "affect betting markets", but no numbers are given. — [Daily Faceoff](https://dailyfaceoff.com/news/how-empty-net-goals-have-changed-the-nhl)
- Stathletes: the expected-score winner wins only 54% of the time, which suggests high randomness. The ESPN 2025-26 article implies an increase in parity, with 28 of 32 teams at .500 or better at the time. — [ESPN 2025-26](https://africa.espn.com/nhl/story/_/id/47210375/nhl-2025-26-games-shootout-theories-trends-stats-standings)

### Inferences
- Testable hypotheses for the pipeline, all speculative:
  1. **Favourite -1.5 against the ENG regime.** Compare implied -1.5 probabilities with realised cover rates by season (2015-16 to 2025-26). If books calibrate on long windows, realised covers should exceed the implied rate in high-ENG seasons such as 2021-22 and 2024-25. Use the trailing team's pull aggressiveness (coach-level) and the favourite's ENG conversion as covariates.
  2. **Overtime-driven parity.** In seasons with high overtime rates (2025-26), +1.5 underdogs gain because every overtime loss covers +1.5. Combining the overtime rate with the ENG rate gives the net cover probability.
  3. **Totals for large favourites.** Score effects lower the leader's shot volume, while ENGs add goals only in close games. Heavy-favourite games may resolve as either blowouts (over) or controlled 1-goal games. Test whether the variance of the total exceeds a Poisson fit at the same market total.
  4. **Combination (favourite -1.5 and over).** These are positively correlated through ENGs. Check whether same-game-parlay pricing applies enough correlation, particularly at low totals (5.5) where an ENG is often the decisive sixth goal.
  5. **6.0 and odd/even totals.** Price pushes using a regulation-only distribution and route overtime probability mass to odd totals.

### Gaps
- I found no peer-reviewed or rigorous public study of NHL puck-line or totals market efficiency by favourite size, especially after 2018. Odds-history data (for example SBR archives, or the pipeline's own odds store) is needed.
- I found no sourced, recent cover-rate table for -1.5 by moneyline band.
