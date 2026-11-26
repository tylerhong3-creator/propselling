# Statistical and ML Methods for Predicting NBA Game Margins and Beating Point Spreads

Research constraint note: In this session, direct page fetches were blocked by the network (fivethirtyeight.com, stat.berkeley.edu, ida.fel.cvut.cz and github.io hosts failed to resolve). All findings below come from search-result abstracts and snippets, such as RePEc/EconPapers abstracts, journal landing pages, and Basketball-Reference glossary text. Figures marked "unverified" were not checked against full text. Source-type labels: **[PR]** = peer-reviewed journal; **[WP]** = working paper / preprint / thesis; **[PRAC]** = practitioner / non-peer-reviewed (blogs, sites, forums).

## Rating systems (Elo, SRS, net rating, least squares/Massey, Bradley-Terry, Glicko, Four Factors, player-based models)

### Takeaway
Most usable NBA team ratings are margin-based linear or Elo-type systems. Elo with a margin-of-victory (MOV) multiplier, SRS (MOV adjusted for schedule), and least-squares/Massey ratings all reduce to "rating difference + home-court advantage = expected margin." Player-based plus-minus metrics (RAPM, EPM, DARKO, LEBRON, RAPTOR) let you adjust a team rating for roster and injury changes, but I found no published head-to-head test of their game-level predictive accuracy.

### Cited Findings
**FiveThirtyEight NBA Elo [PRAC, archived methodology]**
- Home-court advantage is set at 100 Elo points, which FiveThirtyEight equates to about 3.5 NBA points. A time-varying home-court rating made almost no difference, so they kept the constant. — [FiveThirtyEight, "How We Calculate NBA Elo Ratings"](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings) (content via search snippet)
- The optimal K-factor for the NBA was 20. Teams always gain Elo after wins and lose it after losses, but the size of the change grows with the margin of victory. — [FiveThirtyEight NBA Elo](https://fivethirtyeight.com/features/how-we-calculate-nba-Elo-ratings/)
- Between seasons, teams keep three-quarters of their rating; the rest reverts toward the mean. — [FiveThirtyEight NBA Elo](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings)
- MOV multiplier: ((MOV+3)^0.8) / (7.5 + 0.006 × Elo difference of the winner). This exact wording appears on FiveThirtyEight's **WNBA** methodology page. A third-party blog gives the NBA update as K = 20·(MOV+3)^0.8 / (7.5 + 0.006·ED) and says it matches FiveThirtyEight's NBA system. — [FiveThirtyEight WNBA methodology](https://fivethirtyeight.com/methodology/how-our-wnba-predictions-work/); [luke-lite blog, "How to build an NBA Elo rating system"](https://luke-lite.github.io/blog/how-to-build-an-NBA-Elo-rating-system) [PRAC]
- The later CARM-Elo version (2015-16) used a home bonus of about 92 CARM-Elo points plus an extra altitude bonus for Denver and Utah. — [FiveThirtyEight, "How Our 2015-16 NBA Predictions Work"](https://fivethirtyeight.com/features/how-our-2015-16-nba-predictions-work)
- FiveThirtyEight's historical NBA Elo dataset (game-by-game ratings and probabilities, no betting lines) is publicly mirrored. — [datahub.io fivethirtyeight/nba-elo](https://datahub.io/fivethirtyeight/nba-elo)
- Recent academic work argues that Elo should be updated on margin relative to expectation rather than on win/loss. — [arXiv 2506.00348, "Beyond Winning: Margin of Victory Relative to Expectation Unlocks Accurate Skill Ratings"](https://arxiv.org/abs/2506.00348) [WP]

**SRS / least squares / Massey / Harville**
- Basketball-Reference defines SRS as a rating that combines average point differential and strength of schedule, in points above or below average (0 = average). Sports-Reference says adjusted MOV is the same thing as SRS. — [Basketball-Reference glossary](https://www.basketballreference.com/about/glossary.html); [Sports-Reference Blog, SRS calculation details](https://www.sports-reference.com/blog/2015/03/srs-calculation-details/) [PRAC]
- Basketball-Reference has also written up a maximum-likelihood alternative to its team rankings. — [BBR blog, "Alternatives to the BBR Rankings: The Maximum Likelihood Method"](https://aws.basketball-reference.com/blog/indexc39a.html?p=4398) [PRAC]
- Harville (1980), JASA 75:516–524, used mixed linear models on past score differences. For 1,320 **NFL** games from 1971–1977, his predictions had a mean absolute error of 10.68 points, against 10.49 for bookmaker lines. This is the classic early benchmark showing that a least-squares-type rating gets close to, but stays worse than, the market. — [JASA, Harville 1980](https://informahealthcare.com/doi/full/10.1080/01621459.1980.10477504) [PR]
- Kenneth Massey's 1997 thesis/notes cover linear regression and least-squares ratings, the basis of "Massey ratings." — [Massey, "Statistical Models Applied to the Rating of Sports Teams"](https://masseyratings.com/theory/massey97.pdf) [WP]
- A survey frames team ratings as parameters in linear models that predict game outcomes. It credits Harville (2003) with a modified least-squares approach that removes the influence of margin of victory. — [West, review of rating methods (UMich)](https://public.websites.umich.edu/~bwest/inpress_063008.pdf) [WP]
- An alternative to least squares is least absolute errors ("Robust Sports Ratings Based on Least Absolute Errors"). — [OUCI record](https://ouci.dntb.gov.ua/works/4KgnMJN4) [PR, details unverified]

**Four Factors (Dean Oliver, *Basketball on Paper*)**
- Approximate NBA weights: shooting (eFG%) 40%, turnovers (TOV%) 25%, offensive rebounding (ORB%) 20%, free throw rate (FT/FGA) 15%. Formulas: eFG% = (FG + 0.5·3P)/FGA; TOV% = TOV/(FGA + 0.44·FTA + TOV); ORB% = ORB/(ORB + Opp DRB); FT rate = FT/FGA. — [Basketball-Reference, Four Factors](https://basketball-reference.com/about/factors.html) [PRAC]; [Atlanta Hawks, The Four Factors](https://www.nba.com/hawks/four-factors) [PRAC]
- KenPom says the ordering holds for the NBA, but free throw rate matters slightly more in college. — [kenpom.com, four factors](https://kenpom.com/blog/four-factors/) [PRAC]
- A recent arXiv paper decomposes team efficiency into the Four Factors using Shapley values. — [arXiv 2305.13032](https://arxiv.org/pdf/2305.13032) [WP]

**Player-based models (RAPM, EPM, DARKO, LEBRON, RAPTOR)**
- In an informal forum comment, DARKO and EPM are described as ML-derived, with a model stage followed by a time-decay stage. EPM uses play-by-play data and DARKO uses box-score data. The commenter says DARKO, EPM and LEBRON usually produce similar player values. — [r/NBAanalytics thread (mirror)](https://redlib.hyperreal.coffee/r/NBAanalytics/comments/1im3u2n/difference_between_darko_plus_minus_and/mc1n9h9/?context=3) [PRAC, low reliability]
- Recent RAPM methodology work exists, such as "Dummy RAPM," which handles low-minute players in regularized adjusted plus-minus. — [arXiv 2608.19454](https://arxiv.org/pdf/2608.19454) [WP]

### Inferences
- From FiveThirtyEight's 100 Elo ≈ 3.5 pts, the Elo-to-spread conversion is about 28–29 Elo points per point of margin. An Elo difference of D (including home advantage) therefore implies a spread of about D/28. This is derived, not quoted, so check it against the archived FiveThirtyEight page.
- Elo, SRS and Massey are all close relatives: each is a linear or quasi-linear estimate of team strength from margins. Their differences lie mainly in recency weighting (Elo is implicitly exponential via K; SRS weights the whole season equally), handling of blowouts (Elo dampens via (MOV+3)^0.8), and priors (Elo's 75% carryover).
- Bradley-Terry is the win/loss (logistic) analogue of least squares, and Glicko adds rating uncertainty to Elo. For spread work, margin-based ratings dominate because the target is a margin.
- Player-based team ratings (sum of player metric × projected minutes) are the main route to adjusting for injuries and rest. Their edge depends on minutes projection quality.

### Gaps
- I could not fetch the FiveThirtyEight NBA Elo page to confirm that the NBA MOV multiplier constants are identical to the WNBA ones, or to confirm the exact Elo-to-spread divisor.
- I found no published comparison of out-of-sample game-margin accuracy for RAPTOR, EPM, LEBRON, DARKO or BPM. I also found no peer-reviewed NBA comparison of Bradley-Terry or Glicko against margin-based ratings.
- I could not retrieve Massey's or Sagarin's NBA-specific accuracy figures, or Winston/Nestler/Pelechrinis *Mathletics* content.

## Academic forecasting papers and their accuracy versus the betting market

### Takeaway
The peer-reviewed literature consistently finds that NBA betting lines are the best single forecast. Statistical models (Stern, Harville-style ratings, Manner's state-space model, Štrumbelj & Vračar's Markov model, neural nets) come close but do not beat them. The main peer-reviewed claim of profitability (Hubáček et al. 2019) works by *decorrelating* the model from the bookmaker, not by being more accurate, and it used bookmaker odds rather than a verified sharp closing line.

### Cited Findings
- **Stern (1994), JASA 89(427):1128–1134 [PR].** Models the home-minus-away score difference as Brownian motion on t ∈ (0,1) with drift μ (home edge) and variance σ². This gives a simple formula for in-game win probability from the current lead. It fits 493 NBA games from 1991-92 well. — [JASA via informahealthcare](https://informahealthcare.com/doi/abs/10.1080/01621459.1994.10476851); [PDF at Berkeley](https://www.stat.berkeley.edu/users/aldous/157/Papers/stern.pdf)
- Polson & Stern (2015) extend the framework to back out market-implied volatility from point spreads and moneylines. — [De Gruyter, JQAS 2015](https://www.degruyterbrill.com/document/doi/10.1515/jqas-2014-0095/html) [PR]
- **Harville (1980) [PR]:** NFL MAE of 10.68 for the model against 10.49 for the bookmaker. — [JASA](https://informahealthcare.com/doi/full/10.1080/01621459.1980.10477504)
- **Loeffelholz, Bednar & Bauer (2009), JQAS 5(1) [PR].** The authors trained feed-forward, radial-basis, probabilistic and generalized-regression neural networks on 620 NBA games, fused them with Bayesian belief networks, and compared them with human experts. Reported accuracies conflict across secondary sources. One review reports 74.33% correct winners against 68.67% for experts; another summary reports about 72% against about 69%. Either way, this is straight-up *winner* accuracy against experts, **not** a test against the spread. — [EconPapers](https://econpapers.repec.org/RePEc:bpj:jqsprt:v:5:y:2009:i:1:n:7); [De Gruyter](https://www.degruyterbrill.com/document/doi/10.2202/1559-0410.1156/html); [Bohrium summary](https://www.bohrium.com/paper-details/predicting-nba-games-using-neural-networks/811873926836649986-17077)
- **Štrumbelj & Vračar (2012), IJF 28(2):532–542 [PR].** A possession-based Markov model with transitions estimated from play-by-play data (2007-08 and 2008-09) and from team summary statistics. Its forecast quality was comparable to logit regression and latent-strength ratings, but "consistent with previous studies, bookmaker odds were the best probabilistic forecasts." — [EconPapers](https://econpapers.repec.org/RePEc:eee:intfor:v:28:y:2012:i:2:p:532-542); [WSC 2017 paper describing data](https://www.informs-sim.org/wsc17papers/includes/files/062.pdf)
- **Manner (2016), JQAS 12(1):31–41 [PR].** Extends the benchmark linear margin model with heteroscedasticity and a dynamic state-space model of team strength, plus home-court and back-to-back effects. Uses eight NBA seasons. Evidence for heteroscedasticity was weak, and persistent time variation appeared only when several seasons were pooled. Compared with betting point spreads, "the market is hard to beat"; combining model forecasts with betting odds gave "slight improvements." — [EconPapers](https://econpapers.repec.org/RePEc:bpj:jqsprt:v:12:y:2016:i:1:p:31-41:n:4); [working-paper PDF](https://static.uni-graz.at/fileadmin/_Persoenliche_Webseite/manner_hans/Publikationen/NBA_revision2.pdf)
- **Hubáček, Šourek & Železný (2019), IJF 35(2):783–796 [PR].** Convolutional neural networks on player-level statistics predict match outcomes. The models are trained to also *reduce correlation with bookmaker-implied probabilities*, and modern portfolio theory is used to size bets. The authors report "consistently positive cumulative profits" on NBA data for seasons 2007–2014, compared with the alternative methods they tested. The abstract does not state that they beat a sharp closing line. — [EconPapers](https://econpapers.repec.org/RePEc:eee:intfor:v:35:y:2019:i:2:p:783-796); [IDEAS](https://ideas.repec.org/a/eee/intfor/v35y2019i2p783-796.html)
- Follow-up: Hubáček & Šourek (2023), "Beating the market with a bad predictive model," IJF 39(2):691–719, extends the decorrelation idea. Hubáček's 2024 CTU PhD thesis concludes that "decorrelation is an effective way to achieve profits." — [IDA/CTU page](https://ida.fel.cvut.cz/papers/hubacek2019exploiting.html); [Hubáček thesis](https://dspace.cvut.cz/bitstream/handle/10467/114141/F3-D-2024-Hubacek-Ondrej-hubacek_thesis.pdf) [WP]
- **Walsh & Joshi (2024), *Machine Learning with Applications* 16:100539 [PR].** On NBA data, selecting models by calibration rather than accuracy produced higher betting returns. The arXiv preprint reports average ROI of +34.69% for calibration-selected models against −35.17% for accuracy-selected ones. These magnitudes are unverified against the final paper and look implausibly large for a real market, which suggests small samples or soft odds. — [Bath research portal](https://researchportal.bath.ac.uk/en/publications/machine-learning-for-sports-betting-should-model-selection-be-bas/); [arXiv 2303.06021 summary](https://aitopics.org/doc/arxivorg:7A1B8F22)
- A 2017 study covering NCAAB, NBA and NFL found that "high accuracy does not automatically equal high pay-out." — [arXiv 1702.05982](https://ar5iv.arxiv.org/html/1702.05982) [WP]
- A 2025/26 MDPI paper notes that profitability in NBA markets is limited unless models include informative features that bookmakers have not fully priced in. — [MDPI *Information* 17(1):56](https://www.mdpi.com/2078-2489/17/1/56) [PR, MDPI]
- A 2024 systematic review of ML in sports betting is available for broader context. — [arXiv 2410.21484](https://arxiv.org/html/2410.21484v1) [WP]
- A cross-league paper reports that NBA and NFL games are more predictable than MLB and NHL games, and that the betting market outperforms statistical models and human experts in prior studies. — [Predictability paper (2026 preprint)](https://davidxia3.github.io/docs/predictability_paper.pdf) [WP]
- **Song et al.:** I could not locate the specific "Song et al." paper that compares models against the NBA betting market (searches returned other papers).

### Inferences
- The Harville (NFL), Štrumbelj & Vračar, and Manner results fit a consistent pattern. A well-specified rating model gets within a few percent of market error but does not beat closing lines. Its best use is as a component in a combination with the market, or as a filter for line discrepancies.
- The Hubáček result suggests the realistic edge comes from *information the market under-weights*, so a model that just reproduces the market adds nothing. This argues for features orthogonal to public power ratings, such as player-level and lineup information.

### Gaps
- I could not confirm Stern's (1994) estimated NBA σ (the SD of the final margin) or the home drift μ, because the PDF fetch was blocked.
- I could not identify the "Song et al." paper.
- For Hubáček et al., I could not determine the exact ROI, the odds source (opening vs. closing; which bookmaker), or whether they report results against Pinnacle closing lines.
- The underlying literature (e.g., Sauer; Gandar et al.; Paul & Weinbach) on NBA closing-spread efficiency was not retrieved in detail; see the market-efficiency findings in the next section.

## Accuracy of Vegas closing lines versus models, and whether any model consistently beats closing NBA spreads

### Takeaway
Closing NBA spreads have a mean absolute error of roughly 9 points. That figure comes from practitioner sources, not peer-reviewed ones. At standard −110 pricing, a bettor needs a 52.38% ATS win rate to break even. Peer-reviewed studies find the NBA point-spread market largely efficient, with small, mostly transient anomalies. I found no published model that has been shown to *consistently* beat closing NBA spreads out of sample in a verified way.

### Cited Findings
- A Sportsbook Review forum post reports an average absolute error of 9.32 points for NBA opening lines and 9.29 for closing lines (circa 2008 data). — [SBR forum, "1 point lines in American sports"](https://www.sportsbookreview.com/forum/handicapper-think-tank/59267-1-point-lines-in-american-sports) [PRAC, forum, unverified]
- Another forum comment recalls that the SD of (actual margin − spread) is "around 9 or so" in the NBA. This is anecdotal. — [SBR forum, "NBA modeling"](https://www.sportsbookreview.com/forum/handicapper-think-tank/566389-nba-modeling) [PRAC, low reliability]
- For comparison, a 2024 Reddit thread cites a closing **totals** MAE of about 13. — [r/algobetting](https://lr.eu.psf.lt/r/algobetting/comments/1hbezkg/nba_total_score_predicting/m1vqwdi/?context=3) [PRAC]
- Bookmaker odds were the best probabilistic forecasts in Štrumbelj & Vračar (2012), and Manner (2016) found the spread market "hard to beat." — [EconPapers IJF 2012](https://econpapers.repec.org/RePEc:eee:intfor:v:28:y:2012:i:2:p:532-542); [EconPapers JQAS 2016](https://econpapers.repec.org/RePEc:bpj:jqsprt:v:12:y:2016:i:1:p:31-41:n:4) [PR]
- For NBA point spreads from 2000–2008, a likelihood-ratio test (Even & Noble) strongly supports efficiency. The one exception was home underdogs of 10 or more points, which were profitable. — [The Sport Journal, "NBA Gambling Inefficiencies: A Second Look"](https://thesportjournal.org/article/nba-gambling-inefficiencies-a-second-look/) [PR, lower-tier journal]
- **Early-season bias:** NBA *totals* lines were significantly biased early in the season, and a simple strategy against closing totals won 56.72%. *Point-spread* lines showed no similar bias. Line movement from open to close goes in the correct direction but does not fully remove the totals bias. — [ETSU, "Learning, Price Formation and the Early Season Bias in the NBA"](https://dc.etsu.edu/etsu-works/17780) [PR]
- NBA **preseason** spreads (2005–2014) were too large, making underdogs profitable. This was not seen in the regular season. — [Applied Economics 2016, DOI 10.1080/00036846.2016.1213367](https://informahealthcare.com/doi/full/10.1080/00036846.2016.1213367) [PR]
- A Stanford thesis proposes point shaving as one explanation for persistent anomalies in NBA spreads. — [Stanford thesis](https://purl.stanford.edu/nh108vv2047) [WP]
- Hubáček et al. (2019) reported profits on 2007–2014 NBA data through decorrelation. — [EconPapers](https://econpapers.repec.org/RePEc:eee:intfor:v:35:y:2019:i:2:p:783-796) [PR]

### Inferences
- The 52.38% break-even figure is arithmetic: risking 110 to win 100 means 110/210 = 0.5238. No source in these results stated it.
- If the closing spread has an MAE of about 9.3, then assuming roughly normal residuals, the SD of (margin − spread) is about MAE × 1.25 ≈ 11.6 points. That fits the commonly quoted "RMSE ~12" in the brief better than the forum's "SD ~9." This is a derivation, not a sourced measurement. A model's MAE should be compared with about 9.3 on the same games. A model with MAE of 9.6–10 is typical of good public ratings and is not good enough to bet blindly.
- Documented NBA inefficiencies are niche and time-limited: preseason games, early-season totals, and large home underdogs in the 2000s. Any edge should be expected to decay once published.

### Gaps
- I found no peer-reviewed, recent (post-2015) measurement of NBA closing-spread MAE or RMSE. Computing it directly from a historical odds dataset is recommended.
- I found no peer-reviewed paper documenting a model that consistently beats **Pinnacle or market-close** NBA spreads out of sample.

## Regression to the mean, early-season priors, Bayesian updating, recency weighting, and luck adjustments

### Takeaway
Best practice is to start each season from a prior that partially reverts to the mean, then update with new results. FiveThirtyEight kept 75% of the previous rating, and preseason win totals or player-based projections can serve as the prior. Results that are mostly noise should be shrunk: opponent 3P%, and opponent FT% in some practitioner work. Within-season time variation in team strength is weaker than often assumed (Manner 2016), so heavy recency weighting is risky.

### Cited Findings
- FiveThirtyEight NBA Elo reverts 25% toward the mean between seasons, so teams keep three-quarters of their rating. — [FiveThirtyEight](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings) [PRAC]
- Manner (2016) found persistent time variation in team strength only when pooling several seasons, not within single seasons. This argues against overweighting recent games. — [EconPapers](https://econpapers.repec.org/RePEc:bpj:jqsprt:v:12:y:2016:i:1:p:31-41:n:4) [PR]
- Early-season NBA totals lines are biased while spread lines are not. The market learns over the season, so priors matter most early. — [ETSU](https://dc.etsu.edu/etsu-works/17780) [PR]
- Opponent 3P% is largely noise. It was unstable from one season to the next and across 10-game subsets, and Nylon Calculus shrinks it toward an expected value weighted by stabilization attempts. — [Nylon Calculus/FanSided, "Measuring skill vs. luck in NBA defense"](https://fansided.com/2015/12/21/measuring-skill-vs-luck-in-nba-defense); [Nylon Calculus, 3-point team defense](https://fansided.com/2018/01/29/nylon-calculus-3-point-team-defense-closure) [PRAC]
- In one season's split, opponent 3P% over a team's first 25 games correlated just 0.24 with its rate over the next 57 games. The corresponding figures were 0.66 for opponent 2P% and 0.74 for opponent 3PA rate. — [The Ringer, "NBA make/miss 3-point shooting" (2021)](https://www.theringer.com/nba/2021/2/12/22279459/nba-make-miss-3-point-shooting) [PRAC]
- KenPom (college data) finds that defenses have little control over opponents' 3P%. — [kenpom.com](https://kenpom.com/blog/defense-has-little-control-over-opponents-3p/) [PRAC]
- Analysts argue that accounting for randomness in opponent 3P% and opponent FT% improves prediction of future defensive performance. NBA.com's betting section has used "lucky team" analysis for win totals. — [numberFire](https://www.numberfire.com/nba/news/12065/which-nba-defenses-have-been-the-unluckiest-this-season); [NBA.com, "Beware of these five lucky NBA teams"](https://www.nba.com/nbabet/beware-of-these-five-lucky-nba-teams-win-totals) [PRAC]
- Shot-trajectory work in the *Journal of Sports Analytics* examines defensive impact on shot quality. — [JSA](https://content.iospress.com/articles/journal-of-sports-analytics/jsa200400) [PR]

### Inferences
- A practical luck-adjusted net rating can be built by replacing actual opponent 3P% and FT% with league-average or shrunk expected values, then recomputing points allowed per 100 possessions. A similar adjustment can be applied to a team's own 3P% using a shooter-skill prior.
- Preseason market win totals can be converted to an expected per-game margin and used as a Bayesian prior with an effective sample size of roughly one to two dozen games. The exact weight is not documented in the sources found and should be tuned in backtests.

### Gaps
- I found no peer-reviewed source giving an optimal prior weight for preseason win totals, or an optimal recency half-life, for NBA spread prediction.
- I found no Cleaning the Glass methodology text on its luck-adjusted ratings. The site is paywalled and was not retrievable.

## Practical feature engineering, overfitting and look-ahead bias, backtesting, and evaluation metrics

### Takeaway
The core features are opponent-adjusted efficiency, home court, rest and back-to-backs, travel and altitude, and injuries priced via player value × projected minutes. Home-court advantage has fallen and vanished in the no-travel 2020 bubble, so it should be estimated over time rather than fixed. Model selection should favor calibration and log-loss over raw accuracy. Validation should use walk-forward backtests against historical **closing** lines, with ATS win% compared with 52.38% and closing line value (CLV) as the process metric.

### Cited Findings
- Manner (2016) models home-court advantage and back-to-back games explicitly. — [EconPapers](https://econpapers.repec.org/RePEc:bpj:jqsprt:v:12:y:2016:i:1:p:31-41:n:4) [PR]
- FiveThirtyEight CARM-Elo added an altitude bonus for Denver and Utah. — [FiveThirtyEight 2015-16](https://fivethirtyeight.com/features/how-our-2015-16-nba-predictions-work) [PRAC]
- Bubble evidence: in the 2020 bubble, with designated home teams but no travel and no crowd, there was no home advantage (Scientific Reports study, as covered by the BPS). Price & Yan found the 2020 bubble playoffs favored away teams more than in 2017–2019. Huo's 89-game sample showed home 116.87 vs. away 115.24 points per game. — [BPS Research Digest](https://www.bps.org.uk/research-digest/why-do-basketball-teams-have-home-court-advantage-natural-experiment-during) [PRAC coverage of PR]; [arXiv 2103.02832](https://arxiv.org/pdf/2103.02832) [WP]; [SUU working paper](https://suu.edu/business/economics/working-paper-series/pdf/2021/huo-under-the-bubble-does-home-court-advantage-still-exist.pdf) [WP]
- Calibration-based model selection beats accuracy-based selection for betting returns. — [Walsh & Joshi 2024](https://researchportal.bath.ac.uk/en/publications/machine-learning-for-sports-betting-should-model-selection-be-bas/) [PR]
- High accuracy ≠ high payout. — [arXiv 1702.05982](https://ar5iv.arxiv.org/html/1702.05982) [WP]
- Decorrelating from bookmaker probabilities and sizing bets with portfolio methods improved profit in Hubáček et al. — [IDEAS](https://ideas.repec.org/a/eee/intfor/v35y2019i2p783-796.html) [PR]
- Combining model forecasts with market odds gives slight improvements. — [Manner 2016](https://econpapers.repec.org/RePEc:bpj:jqsprt:v:12:y:2016:i:1:p:31-41:n:4) [PR]
- CLV is widely promoted by practitioners as the best leading indicator of long-run profit, with Pinnacle closing odds as the benchmark. No peer-reviewed validation was found, and skeptics exist: Karl Whelan's essay and a Substack piece questioning Pinnacle-close reliability in European soccer. — [Action Network](https://actionnetwork.com/how-to-bet-on-sports/general/closing-line-value-definition-importance-sports-betting); [Karl Whelan, "The Truth about Closing Line Value"](https://www.karlwhelan.com/?p=2595); [Networked Substack](https://networked.substack.com/p/a-view-from-the-pinnacle) [all PRAC]
- An evaluation framework for real-time probabilistic NBA forecasts (in-game win probability) is available. — [arXiv 2010.00781](https://arxiv.org/pdf/2010.00781) [WP]

### Inferences
- Look-ahead-bias checklist:
  - Compute every rating and feature using only games before the tip-off date.
  - Use injury and availability information as it was known *before* the line closed, not box-score minutes.
  - Use player metrics as of that date, not end-of-season versions. Many public RAPM/EPM/RAPTOR values are retrospective and fit on future data.
  - Tune hyperparameters (K, reversion, priors, HCA) only on training seasons.
- Recommended metrics:
  - Margin MAE/RMSE against the closing spread's MAE on the same games.
  - Log loss and Brier score for cover probabilities.
  - ATS win% with a binomial confidence interval. At 52.4% break-even, separating a 54% bettor from break-even at roughly 2 SE takes on the order of 1,000+ bets (0.5/√n ≈ 0.008 → n ≈ 4,000 for 1 SE; derived, not sourced).
  - CLV in points or implied probability.

### Gaps
- I found no sourced quantitative estimates of NBA rest/back-to-back effects, travel/time-zone effects, or the current (post-2021) home-court advantage in points.
- I found no peer-reviewed study of injury-adjusted, player-based team ratings against spreads.

## Data sources and reliability

### Takeaway
Basketball-Reference and the NBA Stats API cover box scores, play-by-play and advanced stats. For historical lines, the best free option found is Princeton's Historical Sports Odds Database (NBA 2006–2023 with opening and closing spreads and totals). The SBR (SportsbookReviewsOnline) archive is widely used but unverified here. Commercial vendors (SportsDataIO, others) sell cleaner odds.

### Cited Findings
- **Princeton DSS Historical Sports Odds Database:** NBA 2006–2023 with dates, scores, and opening and closing spreads and totals. — [Princeton DSS](https://dss.princeton.edu/catalog/resource6741)
- An R package (`bettingtools`) ships NBA moneyline datasets for 2017-18 through 2019-20, sourced from the SBR NBA odds archive. It covers opening and closing moneylines only. — [rdrr.io bettingtools nba_data](https://rdrr.io/github/pwu97/bettingtools/src/R/nba_data.R); [nba_odds_2020](https://rdrr.io/github/pwu97/bettingtools/man/nba_odds_2020.html)
- Covers maintains Sports Odds History, and TeamRankings publishes NBA odds history and ATS data. — [Covers Sports Odds History](https://www.covers.com/sportsoddshistory/?p=505); [TeamRankings NBA spread odds history](https://www.teamrankings.com/nba/odds-history/spread/) [PRAC]
- Commercial: SportsDataIO historical odds. A Whop seller offers opening and closing odds from 9 US books plus Pinnacle for 10,323 NBA games (2018–2026), with a free 20-game Kaggle sample. — [SportsDataIO](https://sportsdata.io/historical-odds); [Whop listing](https://whop.com/oliviersportsdata/nba-opening-closing-odds-9-us-books-pinnacle-2018-2026/) [commercial, unverified quality]
- FiveThirtyEight NBA Elo history is freely available but has no betting lines. — [datahub.io](https://datahub.io/fivethirtyeight/nba-elo)
- Basketball-Reference provides SRS, Four Factors, team and player advanced stats. — [Basketball-Reference Four Factors](https://basketball-reference.com/about/factors.html); [glossary](https://www.basketballreference.com/about/glossary.html)

### Inferences
- For a spread backtest, closing lines should ideally come from a sharp book such as Pinnacle, or a consensus close. Datasets mixing books or using "opening" lines will overstate model edge. Cross-checking two sources (e.g., Princeton against SBR) catches sign errors, pick'em handling, and neutral-site and date mismatches.

### Gaps
- I could not verify the SBR archive's current availability, format, or coverage, or confirm a Kaggle mirror.
- I could not assess NBA Stats API rate limits or reliability. The API is unofficial, undocumented and known for blocking, but no source was retrieved.
