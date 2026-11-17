# Player-Level and Context Stats for NHL Props (SOG, Points, Saves)

Scope note: I searched about 17 times and fetched about 12 pages. Formal published stabilisation work on *game-level* skater shot volume is sparse. Most rigorous public work is from 2014 to 2017 (Hockey-Graphs, blogs) and uses season-level samples. Most current practitioner "prop" content is promotional and untested. Statements in "Inferences" are my reasoning, not sourced facts.

## 1. Shot generation: which inputs predict next-game SOG, and how fast they stabilise

### Takeaway
Volume (attempts x TOI x on-net share) carries most of the repeatable signal. Shooting % is mostly noise: a skater needs about 223 shots (roughly a full season for most players) before his shooting % is 50% signal. I found no reliable public games-to-stabilise figures for iCF, SOG/60, on-net share, rush shots or zone entries at game level. That is the biggest evidence gap.

### Cited Findings
- **Individual shooting % stabilisation.** Reliability reaches r = 0.707 (50% signal) at about **223 shots**. Signal share at other sample sizes: about 10% at 50 shots, 24% at 100, 46% at 200, 58% at 300 and 80% at 500. Only about 40 players (around 6% of the league, 2013-14) took more than 223 shots in a season. Even Ovechkin's 386 shots gave only about 65% signal. — [Don't Tell Me About Heart (2014)](https://donttellmeaboutheart.blogspot.com/2014/12/how-long-does-it-take-for-forwards.html)
- **5v5 individual shooting % regresses hard.** Over more than 2,000 consecutive-season pairs of forwards, only about **4 of 37** players who shot 15% or better at 5v5 were expected to repeat. Example: Zibanejad's 15.5% was projected to about 11.2%, and Pavelski's 5.9% to about 8.8% (simple Year-2 on Year-1 linear regression). — [JFresh, "Percentage Luck in Hockey, Explained"](https://jfresh.substack.com/p/percentage-luck-in-hockey-explained)
- **On-net share (SOG / attempts) moves a lot between seasons, even for established shooters.** Filip Forsberg's even-strength on-net share went 55% to 52% to 50.1% to 41.4% while his attempt rate held steady. Dylan Guenther went from 53% to 37.1%. The author expects a fall in SOG with a stable attempt rate to rebound (Forsberg: 3.53 SOG/game vs about 4.23 the prior year). No correlation or stabilisation figure is given. — [DobberHockey, Geek of the Week (Dec 2024)](https://dobberhockey.com/2024/12/22/geek-of-the-week-shot-attempts-shots-on-goal-and-shots-per-60/)
- **Shots/60 is the role-independent rate. SOG/game is shots/60 x TOI.** Example: Skinner at 10.36 shots/60 on a fourth-line role gives 2.3 SOG/game. — [DobberHockey (Dec 2024)](https://dobberhockey.com/2024/12/22/geek-of-the-week-shot-attempts-shots-on-goal-and-shots-per-60/)
- **Corsi-type (attempt-based) measures stabilise faster than chance-based measures because they have more events.** In a team-level model, CF% + Sh% + Sv% explained about 95% of goal share. Swapping in scoring chances (SCF%) dropped R² to about 82.6%, which the author attributes to Corsi's larger sample. Self-reported. — [Betstamp, "How I Built the NHL Betting Model…"](https://www.betstamp.com/education/How-I-Built-The-NHL-Betting-Model-That-Beat-The-Books)
- **Defencemen, 5v5 stats vs next-season production (2023-24, 2024-25).** ixG/60 correlated about 0.20 to 0.25 with next-season points (top 10 of 18 stats in both seasons). It was the best predictor of next-season goals (≥ 0.25 in one season) and beat goal rate. **Individual shot rate was inconsistent**: good in one season, poor in the other. Zone carries had a moderate, consistent link to goals. Rush contributions predicted points better than cycle/forecheck contributions. For forwards, ixG vs next-season points was below 0.1, while forward "chance contributions" were about 0.27. The author's wording ("r-squared, or correlation") leaves it unclear which statistic is reported. — [DobberHockey Ramblings (Aug 2026)](https://dobberhockey.com/2026/08/07/ramblings-finding-useful-stats-for-predicting-future-goal-and-point-production-among-defencemen/)
- **Zone-entry creation** is a Hockey-Graphs line of research on individual entry importance. The result page I found did not give repeatability or SOG predictive figures. — [Hockey-Graphs (2017)](https://hockey-graphs.com/2017/08/10/measuring-the-importance-of-individual-player-zone-entry-creation/)
- **Practitioner caveat.** A widely circulated "what stats matter for SOG props" guide admits: "We have not tested which NHL stats predict a result after accounting for the posted line." It is marketing for a picks service. — [Steezanomics (promotional)](https://steezanomics.com/learn/stats-for-nhl-shots-on-goal-props/)

### Inferences
- For next-game SOG, the most defensible structure is: projected TOI (especially PP TOI) x regressed attempts/60 (iCF/60) x regressed on-net share, with opponent and score-state adjustments. Attempt rates (iCF) pool more events than SOG, so they should stabilise faster than SOG/60. Shooting % should be ignored for SOG. This follows from the event-count logic in the Betstamp and shooting % sources, but I found no published games-to-stabilise number for iCF/60.
- On-net share looks like a "noisy skill." Big single-season drops with a stable attempt rate look like regression candidates (Dobber examples). If books price off recent SOG rather than attempts, a player whose SOG has fallen while attempts held steady is a candidate *over*. This is speculative.
- For defencemen, shot volume is a weaker forward-looking signal than ixG or carries, and much of D SOG comes from low-danger point shots that are often blocked. Blocked-shot share is likely a key gap between iCF and SOG for D (not quantified in sources).

### Gaps
- No public, citable split-half or games-to-stabilise figures for iCF/60, SOG/60, on-net %, rebound or rush shot rates, or offensive-zone start % at game level. Commonly quoted folklore figures (e.g. "shot rate stabilises in about 10 to 20 games") could not be sourced.
- No sourced quantification of how offensive-zone starts move individual shot volume (most modern analysis treats the zone-start effect as small, but I could not verify a number).
- No sourced correlation of PP1 vs PP2 status with SOG/game.

## 2. Points: on-ice Sh%, IPP, PDO, PP1 role, linemates; regression of PPG outliers

### Takeaway
Points depend heavily on on-ice shooting %, and on-ice shooting % barely repeats. About 3.6% of skaters with on-ice Sh% above 11% repeat it, and for defencemen on-ice Sh% is essentially unrepeatable. So points-per-game outliers driven by on-ice Sh% or PDO should be regressed hard. Defencemen points depend heavily on PP1 share, and changes in PP1 role produce immediate production swings.

### Cited Findings
- **On-ice Sh% repeat rates.** Of 138 skater-seasons with on-ice Sh% above 11% over a decade, only **5 (3.6%)** repeated above 11% the next season. The repeat rate is 15.1% at a 10% threshold and 26.5% at 9%. — [JFresh](https://jfresh.substack.com/p/percentage-luck-in-hockey-explained)
- **PDO repeatability is "extremely low" year to year, with a small talent component.** Tampa Bay had PDO above 100 in 8 of 10 seasons. Within a season, PDO regresses toward 100 over about 41 games, versus 82 games year to year. — [JFresh](https://jfresh.substack.com/p/percentage-luck-in-hockey-explained)
- **On-ice Sh% by position** (1,000+ minutes, 150+ GP, 2007-15). League average is about 7.5%. The recommendation is to regress about **67% toward the mean** over three-year windows (an 11% observed rate becomes about 9.2%). By position, the share of variance explained is: **defencemen about 0%**, wingers "weak", **centres about 40%**. — [TSN / Travis Yost](https://www.tsn.ca/examining-on-ice-shooting-percentage-by-position-1.338499)
- **Best predictors of next-season points for defencemen.** 5v5 points rate was one of only 2 of 18 stats with a correlation of at least 0.2 in both seasons; ixG/60 was about 0.20 to 0.25. For forwards, "chance contributions" (own chances plus assists on teammates' chances) were about 0.27. — [DobberHockey (Aug 2026)](https://dobberhockey.com/2026/08/07/ramblings-finding-useful-stats-for-predicting-future-goal-and-point-production-among-defencemen/)
- **PP share for defencemen is highly concentrated.** Spurgeon, Bouchard, Q. Hughes and Makar each had about **80%** of team PP time (Spurgeon peaked at 93.5%). Only 27 D cleared 55% of team PP time, covering 26 teams, and 6 teams had no such defenceman. — [DobberHockey Frozen Tool Forensics (Dec 2024)](https://dobberhockey.com/2024/12/13/frozen-tool-forensics-power-play-defencemen-and-changing-roles-for-spurgeon-ekblad-dunn-and-others)
- **Changes in PP1 role move D production right away.** Examples:
  - Chychrun took over PP1 (Nov 21) and had 5 points in 7 games.
  - Hutson was promoted when Matheson was injured and had 3 PP points in 4 games.
  - Vlasic was promoted with Seth Jones out and had 4 points in 5 games.
  - Counterexample: Dunn held more than 60% PP share, but the *other* unit (Montour/Wright) produced. TOI share does not guarantee points.
  - [DobberHockey (Dec 2024)](https://dobberhockey.com/2024/12/13/frozen-tool-forensics-power-play-defencemen-and-changing-roles-for-spurgeon-ekblad-dunn-and-others)
- **Assists props backtest (self-reported, public GitHub PR, not independently verified).** A Poisson model betting **unders only** at an EV cut of at least 10% at the best available price returned +10.9% on 1,063 bets over 2023-24 to 2025-26 (95% CI +4.7% to +17.2%). Returns were stable by season (+11.0%, +11.3%, +10.6%). The author notes that design choices were made on the same seasons used for the results. — [MJACode/betting-model PR #860](https://github.com/MJACode/betting-model/pull/860)

### Inferences
- Point props are a function of PP1 status, linemate quality and on-ice Sh%, and only the first two repeat. A player on a points heater with high on-ice Sh% or IPP and an unchanged role is a fade/under candidate. A promotion to PP1, especially for a D-man taking over an injured QB's slot, is an over candidate if the book's line still reflects season-long averages. The Dobber examples are anecdotes, not a controlled test.
- Under-side edges on assists and points are plausible structurally. Outcomes are low-count and right-skewed (most games end at 0 points), and books' margin appears to sit on the overs (see Section 5).
- Primary assists are generally considered more repeatable than secondary assists. I found no current citable figure for this (see Gaps).

### Gaps
- No sourced figure for primary vs secondary assist repeatability, or for IPP repeatability.
- No sourced quantification of "share of D points from PP" league-wide. The Dobber piece gives TOI shares, not points shares.
- No sourced measure of linemate-quality effects on individual points (WOWY results not found in this pass).

## 3. Goalie saves props: shots-against vs Sv%, score effects, back-to-backs

### Takeaway
Saves = shots against x Sv%. For a given starter, game-to-game spread in shots against is wide, and Sv% binomial noise is about ±1.5 saves, so shot volume (opponent, score state, pace) is the main controllable driver. The market sets near-identical numbers across books (95% identical) with a bias of about +0.8 saves above realised saves. Blind unders roughly break even, and modelled unders have reportedly been profitable.

### Cited Findings
- **Market structure for saves (3,516 observations, 2023-24 to 2025-26):**
  - Median number 25.5 (most fall in 21.5 to 29.5); median price −115 each side; median margin 6.48%.
  - **94.63%** of 2,982 multi-book goalie-games had the *same* number at every book. Books compete on price, not number.
  - Mean posted number **25.35** vs mean realised saves **24.51**, a gap of **0.84 saves**.
  - Unders hit **53.75%** overall (54.42%, 55.66%, 51.40% by season) vs a 53.49% break-even at −115, which is within noise (SE 0.84 pp).
  - Only **23.21%** of results landed within ±2 saves of the number, and **46.70%** were more than 5 saves away.
  - The site states it publishes no picks but links its own tools (mildly promotional).
  - [Nebula Insights](https://nebulainsights.net/blog/nhl-goalie-saves-props.html)
- **Saves model backtest (self-reported).** Unders only, EV ≥ 10%, best price: **+7.8% on 1,755 bets** (95% CI +3.2% to +12.5%; by season +7.3%, +10.1%, +4.7%). The model is over-confident: it predicts 63% and delivers 57%. The early-season return was +3.8% on 251 bets. — [MJACode PR #860](https://github.com/MJACode/betting-model/pull/860)
- **Back-to-back effect (about 40,000 games since 1987).** On the second night, Sv% fell from .905 to .897 (**−0.008**), shots against rose from 28.9 to 29.7 (**+0.8**), and win% fell from .498 to .421.
  - At 2 days' rest Sv% changed by −0.007, at 3 days by −0.005, at 4 days by −0.001 and at 5 days by +0.007.
  - Confounders: most back-to-backs are on the road, there is backup selection bias, and there is no adjustment for season or opponent.
  - [Hockey-Graphs, "Goaltender Performance vs Rest" (2014)](https://hockey-graphs.com/2014/12/01/goaltender-performance-vs-rest/)
- **Score effects on shot volume.** Evolving-Hockey 5v5 SOG score-adjustment weights:
  - **Home team:** 0.862 when trailing by 3 or more, 0.890 at −2, 0.915 at −1, 0.972 tied, 1.037 at +1, 1.077 at +2, 1.104 at +3 or more.
  - **Away team, trailing by 3 or more:** 1.191.
  - Trailing teams' shot counts are deflated in the adjustment (and leading teams' inflated) because trailing teams outshoot. Weights are smaller at 4v4 and 3v3. The method follows Micah McCurdy.
  - [Evolving-Hockey glossary](https://evolving-hockey.com/glossary/score-adjustments/)
- **Goalie Sv% is treated as a goalie trait, weighted over 3 seasons and regressed for small samples.** One model-builder calls weighted Sv% the "weakest link." — [Betstamp](https://www.betstamp.com/education/How-I-Built-The-NHL-Betting-Model-That-Beat-The-Books)

### Inferences
- **Variance decomposition (my calculation).** At 28 shots and .905 Sv%, the binomial SD of saves given shots is sqrt(28 x .905 x .095) ≈ **1.55 saves**. Nebula reports 46.7% of results more than 5 saves from the line, which implies a total SD of roughly 6 to 7 saves around the number. So most saves variance comes from shots-against volume (and pulled or early-hook starts), not Sv% skill. Projecting shots against (opponent shot generation, own team's shot suppression, expected game script) matters far more than goalie quality for saves props.
- **Score-effect inference.** A goalie on a heavy favourite should face fewer shots early but more late as the trailing opponent pushes. The Evolving-Hockey weights imply roughly 10 to 20% more shot volume for a trailing side. The net effect on a favourite's goalie depends on how long the game spends in each score state (not quantified here). An underdog goalie trailing late faces fewer shots, which is consistent with unders on underdog goalies.
- A goalie starting the second night of a back-to-back faces about 0.8 more shots, while Sv% drops about 0.008. Expected saves are roughly flat to slightly up (≈ +0.5), but pull risk is higher. Net direction for saves props is ambiguous.
- The persistent bias of about +0.84 between posted and realised saves (the line sits above realised saves) is consistent with books shading toward overs (public preference). It also matches the under-only edge in the PR backtest.

### Gaps
- No sourced game-level variance decomposition of saves into shots-against and Sv%.
- No sourced estimate of how often starters are pulled and its effect on saves-prop outcomes.
- No current (post-2020) back-to-back Sv% study found. The 2014 study's confounders are unresolved.

## 4. Opponent and context effects: shots allowed, PP opportunities, pace, travel and back-to-backs

### Takeaway
Score state is well quantified, with shot multipliers of about 0.86 to 1.19 by lead. Back-to-back teams allow about 0.8 more shots. Team-level shots-allowed rates are widely published, but how they spread across individual players is not well studied. I found no solid public quantification of PK-frequency or travel effects on individual SOG.

### Cited Findings
- Score-state shot weights by lead: see Section 3. — [Evolving-Hockey](https://evolving-hockey.com/glossary/score-adjustments/)
- Back-to-back second game: about **+0.8 shots against** for the tired team's goalie (28.9 to 29.7). — [Hockey-Graphs (2014)](https://hockey-graphs.com/2014/12/01/goaltender-performance-vs-rest/)
- A team's SOG-allowed rate "does not tell you how its shots against will be distributed" by position or player. Practitioner tools (defence-vs-position) exist but are untested. — [Steezanomics (promotional)](https://steezanomics.com/learn/stats-for-nhl-shots-on-goal-props/)
- Special-teams play adds noise to team-strength models, so one model-builder used 5v5 only. — [Betstamp](https://www.betstamp.com/education/How-I-Built-The-NHL-Betting-Model-That-Beat-The-Books)

### Inferences
- An opponent's penalty rate drives the player's team's PP minutes, and PP minutes drive shot rate for PP1 players. This is a plausible channel that is likely only partly priced, but I have no sourced effect size.
- Opponent shot suppression (CA/60) should be applied to a player's projected attempts after regression. The usual multiplicative approach is opponent CA/60 ÷ league CA/60.

### Gaps
- No sourced quantification of opponent penalty frequency → PP TOI → SOG.
- No sourced effect of travel or time zones on skater shot volume.
- No sourced "pace" metric with demonstrated predictive value for individual props.

## 5. How books set NHL prop lines and where they are slow

### Takeaway
Hard evidence is thin. The best data shows saves numbers are nearly identical across books (consensus or copy pricing), with the margin and bias sitting on the overs. Price shopping is worth about 2.4 percentage points of ROI on SOG unders. A public backtest reports positive under-only ROI in saves, SOG and assists over three seasons. I found no rigorous public study showing *how fast* books react to line or PP changes; claims that books are "slow" on deployment changes are practitioner lore.

### Cited Findings
- **Saves numbers are 94.63% identical across books, and books compete on price** (median margin 6.48%). Posted numbers average 0.84 saves above realised saves. — [Nebula Insights](https://nebulainsights.net/blog/nhl-goalie-saves-props.html)
- **SOG unders backtest (self-reported):** **+5.7% on 4,707 bets** (95% CI +2.8% to +8.7%; by season +8.2%, +4.6%, +4.8%), and +7.2% on 796 bets in the opening weeks. ROI was only +3.3% at DraftKings alone vs +5.7% at the best price; 58% of bets were placed at non-DraftKings books. — [MJACode PR #860](https://github.com/MJACode/betting-model/pull/860)
- **Margin sits on overs.** Blind overs at DraftKings lost 9 to 12%; blind unders lost 0 to 3.5%. — [MJACode PR #860](https://github.com/MJACode/betting-model/pull/860)
- **Total goals showed no edge in the same framework.** Overs lost 4.0% and unders lost 4.4%. — [MJACode PR #860](https://github.com/MJACode/betting-model/pull/860)
- **The team-side market has become efficient.** A modeller who reported 2016-17 results of +11.7% ROI on 341 bets, beating the close 87.4% of the time, says that same model would not win today because those edges are now priced. Self-reported. — [Betstamp](https://www.betstamp.com/education/How-I-Built-The-NHL-Betting-Model-That-Beat-The-Books)
- Most search-ranked "NHL prop strategy" pages (oddstrader, propsoptimizer, sportbotai, coresportsbetting, sportsgamblingreviews and similar) are affiliate or promotional pieces with no tested numbers. I excluded them as evidence. I found no Pinnacle or Unabated page on NHL prop line setting in this pass; search results for Pinnacle were spam or mirror domains.

### Inferences
- Consensus numbers plus margin on overs implies the structural opportunity is (a) the unders side, (b) shopping for price, and (c) spots where the consensus number is stale: PP1 promotions or demotions, line-combination changes, a key teammate's injury redistributing PP time, and confirmed-starter or backup swaps for saves. This is consistent with the evidence above, but how slowly books reprice is not demonstrated in any source I found.
- Early-season SOG returns (+7.2%) were at least as good as the full sample. This weakly suggests books lean on prior-season averages while role changes go unpriced. It is speculative, and the sample is small.

### Gaps
- No source quantifies how quickly NHL prop lines move after line-rush or PP-unit news, or the closing line value from betting at open vs close for props. The PR mentions CLV but reports no figure.
- No first-hand sportsbook or trader account of NHL prop line inputs (season average vs recency weighting) was found. The common claim that "books use season averages with minimal adjustment" remains unsourced.
- Bet limits on NHL props (which cap how much these edges are worth) were not found.
