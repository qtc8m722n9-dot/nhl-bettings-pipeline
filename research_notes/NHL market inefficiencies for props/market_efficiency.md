# NHL Betting Market Inefficiencies (Game Lines and Props): What Has Been Documented

Research conducted 2026-11-17. IMPORTANT CAVEAT FOR THE REPORT WRITER: Most primary academic PDFs (ResearchGate, Wiley, Syracuse SURFACE, WVU repository, CORE, Academia.edu) returned fetch errors. Only one full-text NHL efficiency study (Robbins 2023) was read. For the others, only bibliographic details were confirmed. Findings I recall from background knowledge but could not verify this session are listed under Gaps and are clearly marked UNVERIFIED. Do not present them as confirmed.

## 1. Academic evidence on NHL game-line efficiency (favourite-longshot, home/away, puck line, totals, popular teams)

### Takeaway
The most recent full-sample study I could read (Robbins 2023: 19,456 NHL games, 2007-08 to 2022-23) found NHL moneylines to be the most efficient of the sports it tested. It found no significant favourite-longshot or reverse favourite-longshot bias, and no odds bin earned a positive return. Older papers (Woodland & Woodland 2001; Gandar et al. 2004; Paul & Weinbach 2012) exist and are cited for a favourite/longshot effect and for bettor-bias pricing in the NHL, but I could not retrieve their numbers. Overall, simple bias strategies on NHL moneylines look arbitraged away.

### Cited Findings
- **Robbins (2023), "Weak Form Efficiency in Sports Betting Markets," *American Journal of Management* 23(2).** Covers NHL seasons 2007-08 to 2022-23 (games dated 2007-09-29 to 2023-01-09): 19,456 contests and 33 teams. The average booksum was 3.40% and the margin 3.28%. The bookmaker source is not specified in the text I extracted, so it is unclear whether these are sharp or soft prices. A 3.3% margin is consistent with market-average or consensus closing odds rather than Pinnacle's roughly 2% NHL margin, but that is my inference. — [Robbins 2023 PDF](https://myweb.ecu.edu/robbinst/PDFs/Weak%20Form%20Efficiency%20in%20Sports%20Betting%20Markets.pdf)
  - Favourite-longshot test. The longshot bin (+190 to +505) returned -4.13%. The heavy-favourite bin (-700 to -219) returned -2.91%. The difference is not significant (p = .546). The next bins in (bin 2 at -2.19% vs bin 19 at -3.28%) show a nominal *reverse* longshot bias that is also not significant. — [Robbins 2023](https://myweb.ecu.edu/robbinst/PDFs/Weak%20Form%20Efficiency%20in%20Sports%20Betting%20Markets.pdf)
  - All odds bins had negative returns. The best bin (+130 to +139 dogs) returned -0.003%, roughly break-even before any line shopping. An ANOVA for equal returns across bins gave p = .905. Overall returns were not different from the hold (p = .938). — [Robbins 2023](https://myweb.ecu.edu/robbinst/PDFs/Weak%20Form%20Efficiency%20in%20Sports%20Betting%20Markets.pdf)
  - Calibration. The slope of actual wins regressed on implied probability has a 95% CI of [0.934, 1.01], which includes 1. The author concludes NHL odds "appear to be the most efficient of the odds set we have examined." — [Robbins 2023](https://myweb.ecu.edu/robbinst/PDFs/Weak%20Form%20Efficiency%20in%20Sports%20Betting%20Markets.pdf)
  - Home bias was not tested for the NHL. — [Robbins 2023](https://myweb.ecu.edu/robbinst/PDFs/Weak%20Form%20Efficiency%20in%20Sports%20Betting%20Markets.pdf)
- **Woodland & Woodland (2001), "Market Efficiency and Profitable Wagering in the National Hockey League: Can Bettors Score on Longshots?" *Southern Economic Journal* 67: 983–995.** A 2021 literature review in *Risks* cites it as evidence of "favorite bias ... in ice hockey," meaning a reverse favourite-longshot pattern in which favourites are underbet relative to the classic bias. The review gives no numbers. — [Risks 2021 literature review (MDPI)](https://www.mdpi.com/2227-9091/9/1/22); [Wiley listing](https://onlinelibrary.wiley.com/doi/10.1002/j.2325-8012.2001.tb00385.x)
- **Gandar, Zuber & Johnson (2004), "A Reexamination of the Efficiency of the Betting Market on National Hockey League Games," *Journal of Sports Economics* 5: 152–168.** A re-test of the Woodland & Woodland result. Robbins cites it without giving numbers, and I could not retrieve the findings. — [cited in Robbins 2023](https://myweb.ecu.edu/robbinst/PDFs/Weak%20Form%20Efficiency%20in%20Sports%20Betting%20Markets.pdf)
- **Paul & Weinbach (2012), "Sportsbook pricing and the behavioral biases of bettors in the NHL," *Journal of Economics and Finance* 36(1): 123–135 (DOI 10.1007/s12197-009-9112-4).** Uses betting-percentage data to study bettor biases and how books price them. RePEc lists no abstract, and the full text (Syracuse SURFACE) failed to load. — [RePEc](https://ideas.repec.org/a/spr/jecfin/v36y2012i1p123-135.html)
- **Paul & Weinbach, "Market Efficiency and the NHL totals betting market: Is there an under bias?"** The title confirms that a totals over/under test exists. The full text could not be fetched (ResearchGate/Academia errors). — [ResearchGate listing](https://www.researchgate.net/publication/227410468_Market_Efficiency_and_the_NHL_totals_betting_market_Is_there_an_under_bias)
- **Buttrey (2016), "Beating the market betting on NHL hockey games," *Journal of Quantitative Analysis in Sports* 12(2): 87–98.** Builds a model of goal scoring, goal yielding and penalties, combined through a Markov computation and simulation. It bets moneylines where the model differs "substantially" from market probabilities and reports a return that is "both positive and statistically significant." I could not retrieve the sample, seasons, ROI size, or whether the test was against closing or sharp prices. — [RePEc abstract](https://ideas.repec.Org/a/bpj/jqsprt/v12y2016i2p87-98n1.html)

### Inferences
- The broad, recent evidence (Robbins: 16 seasons, about 19k games) suggests NHL moneylines are well calibrated, with no exploitable favourite-longshot pattern in either direction. Older reverse-FLB claims appear to have been arbitraged away or were sample-specific.
- Any edge in NHL game lines is likely to come from better models (Buttrey-style) or timing and news, not from simple structural biases.

### Gaps
- UNVERIFIED (background recollection only): Woodland & Woodland (2001) reportedly found betting underdogs in the NHL to be roughly break-even or slightly profitable in some sub-samples, a reverse FLB. Gandar et al. (2004) reportedly found that this weakened or disappeared in an extended sample. I could not confirm effect sizes or seasons.
- UNVERIFIED: The direction and size of the Paul & Weinbach under bias, including whether unders cleared the roughly 52.4% break-even, and the seasons covered.
- I found no study testing **puck line vs moneyline** relative pricing, **home/away bias**, or a **popular/big-market team bias** with numbers I could verify. Paul & Weinbach (2012) is the likely source for the popular-team question but could not be read.
- I found no study explicitly testing against **Pinnacle closing lines** for the NHL.

## 2. Player prop markets (shots on goal, points, goals, saves, anytime goal)

### Takeaway
I found **no peer-reviewed or serious practitioner study with quantified results** on NHL player prop efficiency. That covers over/under bias, defencemen points, 0.5-line bias, and closing-line efficiency. Search results were dominated by tout and affiliate content with no data.

### Cited Findings
- Searches for NHL prop efficiency returned only marketing and how-to guides (e.g. NHL Betting Pro, BetSmart, Core Sports Betting, Sports Gambling Reviews), with no sample sizes or tests. — [NHL Betting Pro](https://nhlbettingpro.com/nhl-props-betting-guide/); [Core Sports Betting](https://www.coresportsbetting.com/nhl-player-shots-on-goal-prop-betting-strategy/)
- A vendor (PuckAPI) advertises historical NHL player prop line data. This is a possible data source for testing, not evidence. — [PuckAPI](https://puckapi.com/data/player-props)
- A public GitHub repo ("nhl-betting-lab") has a PR on shots-on-goal "own-games spread, measured under a fixed rule." I did not review it, and its quality is unknown. — [GitHub PR](https://github.com/cooperross399/nhl-betting-lab/pull/452)

### Inferences
- SPECULATIVE: Props carry higher hold and lower limits, and closing prices on props are less tested than game lines. That makes them the most plausible place for a residual edge. But no documented NHL evidence supports any specific bias, such as "unders hit more" on 0.5 lines or defencemen points being mispriced.
- The project would need to build its own tests (e.g. hit rate vs de-vigged implied probability by line and position, and CLV vs a sharp prop source) rather than rely on literature.

### Gaps
- No quantified study found on NHL props for: over/under bias, position bias, 0.5-line bias, anytime goalscorer overround, or closing-line efficiency.

## 3. Same-game / correlated markets (puck line + total, ML + total)

### Takeaway
I found no academic or quantified practitioner analysis of NHL same-game parlay correlation pricing. The only substantive sources are sportsbook patents describing correlated-prop pricing methods.

### Cited Findings
- Several US patents titled "Sportsbook odds optimization and correlated proposition bet analysis" describe systems for pricing correlated proposition bets. They are not hockey-specific, and I did not read their contents. — [USPTO 11657680](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11657680); [USPTO 12080130](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12080130)
- Other results (e.g. SGP explainers) are general and unquantified. — [Sharp Football Analysis SGP page](https://www.sharpfootballanalysis.com/sportsbook/same-game-parlay-sites/)

### Inferences
- SPECULATIVE: Puck line -1.5 is structurally correlated with the over (a two-goal win needs goals) and with empty-net goals. Whether books under-adjust for this in NHL SGPs is untested in what I found.

### Gaps
- No measured SGP hold or correlation-adjustment data for the NHL.

## 4. Line reaction to news (starting goalies, line-ups) and closing-line efficiency for props

### Takeaway
I found no quantified, credible study of how fast NHL lines move on goalie confirmation or line-up news. The available material is non-quantitative explainer content from sportsbooks and affiliates.

### Cited Findings
- Explainer pages from sportsbooks and affiliates assert that goalie confirmations move NHL lines but give no measured effect sizes or timing. — [MyBookie goalie confirmations](https://www.mybookie.ag/sports-betting-guide/goalie-confirmations-and-line-movement/); [odds.guru](https://www.odds.guru/learn/hockey/nhl-starting-goalies-betting); [ESPN goaltending factor](https://global.espn.com/espn/betting/story/_/id/42470775/nhl-odds-betting-goaltending-factor)
- Daily Faceoff publishes daily starting-goalie confirmations, a likely news-timing source for a pipeline. — [Daily Faceoff starting goalies](https://www.dailyfaceoff.com/starting-goalies/2026-01-22)

### Inferences
- SPECULATIVE: The window between morning skate or goalie confirmation and book adjustment (especially for soft-book saves props) is the most commonly claimed edge. It is undocumented in rigorous work, so it would need to be measured from timestamped odds.

### Gaps
- No timestamped study of NHL line reaction to goalie or line-up news.
- No study of closing-line efficiency for NHL props.

## 5. Recent (2020–2026) analytics-writer work

### Takeaway
I found no relevant 2020–2026 quantified NHL market-efficiency pieces from Evolving-Hockey, MoneyPuck, HockeyViz, The Athletic, Pinnacle Betting Resources or Unabated within the search budget. The only recent quantified item is Robbins (2023, above). A September 2026 arXiv paper on bettor bias (Dmochowski) covers MLB only.

### Cited Findings
- Dmochowski (arXiv 2609.06739, Sep 2026) studies 1,139 MLB run-line games from one book (DraftKings splits). Its only hockey content is a citation of Paul & Weinbach (2012). It is not usable as NHL evidence. — [arXiv](https://arxiv.org/pdf/2609.06739)

### Gaps
- Pinnacle Betting Resources hockey articles, Unabated NHL prop content, and analytics conference papers (RIT, OTTHAC, Sloan) were not reached within the tool budget. A targeted follow-up is recommended.
