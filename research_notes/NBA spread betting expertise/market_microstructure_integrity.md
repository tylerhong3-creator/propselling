# NBA Spread Betting: Market Microstructure, Bookmaker Behavior, the US Legal Market, and Integrity

Research method note: compiled 2026-11-26 from web searches. Full-text fetches were **blocked** in this session for justice.gov, deseret.com, stat.berkeley.edu and nbcsports.com, so several findings rest on search-result summaries of those pages, not on a direct reading of the primary document. Each such case is marked. Before publication, verify DOJ/NBA facts against justice.gov (EDNY press releases) and nba.com.

## 1. Line origination: market-making vs. market-following books, opening vs. closing lines, limits

### Takeaway
Practitioner sources consistently describe a two-tier market. Low-margin, high-limit "market makers" (Pinnacle is the canonical example; Circa and Asian books are commonly named) post opening lines at low limits, let sharp action shape the price, and raise limits as the line converges toward a closing number. Retail books largely follow those prices and manage risk by profiling customers. Peer-reviewed evidence (mostly from soccer) agrees that prices become more efficient as the event nears. I found no academic source documenting NBA-specific line release timing.

### Cited Findings
- Practitioner sources describe Pinnacle as a market maker that earns its profit through volume and low margins, aims for the most accurate prices, and uses sharp action to improve pricing. That is the opposite of books that limit sharp customers. — [Complete Sports, "How Pinnacle sets the sharpest lines"](https://www.completesports.com/how-pinnacle-sets-the-sharpest-lines/) (practitioner/secondary; low-to-moderate reliability)
- Pinnacle posts opening lines with smaller limits. This "allows Pinnacle to shape their lines according to the betting activity of 'sharp' bettors without exposing the book." — [Wikipedia: Pinnacle Sports](https://en.wikipedia.com/wiki/Pinnacle_Sports) (secondary)
- A third-party guide says Pinnacle limits often start at about 25% of their maximum when a market opens and rise to full value near game time. It also argues that a higher limit signals more bookmaker confidence in the price. **Pinnacle has not confirmed the 25% figure.** — [Limit and vig: the two confidence proxies (third-party guide)](https://pod-mu.vercel.app/guides/market-limits-and-vigs-what-are-they-and-why-are-they-important); anecdotal corroboration in a [Sportsbook Review forum thread](https://www.sportsbookreview.com/forum/players-talk/1605591-pinnacle-limit-winners)
- Pinnacle's closing odds are widely used as the benchmark for "closing line value" (CLV) and for finding mispriced lines at other books. — [Action Network: Closing line value](https://www.actionnetwork.com/education/closing-line-value-definition-importance-sports-betting) (practitioner)
- Academic evidence (soccer) finds that prices closer to kickoff predict outcomes better than prices 24 hours earlier. This supports the idea that the market converges as informed money arrives. — [Angelini, De Angelis & Singleton, information-efficiency working paper (Univ. of Reading/Bologna)](https://cris.unibo.it/retrieve/8c5e3d3d-d36f-4279-b566-da91767d1a5c/information_efficiency_angelini_de_angelis_singleton.pdf)
- Retail books classify bettors mainly by CLV analysis. — [third-party site](https://bet88com-run.pages.dev/betting-limits-line-movement.html) (**low-quality source**). It is indirectly corroborated by the Massachusetts regulator's request for closing-line-value data from operators (see Section 4).

### Inferences
- For NBA spreads, the "true" market price is best approximated by a low-vig, high-limit book's closing number. A line that moves early, at low limits, carries more information per dollar than one that moves late.
- Retail US books (DraftKings, FanDuel, etc.) behave as market followers on sides and totals. Their edge comes from hold, parlays and customer selection rather than from originating the price. This is inferred from the practitioner evidence and the limiting data in Section 4. I found no direct primary source for it.

### Gaps
- I found no credible (non-forum) source on **when NBA lines are released**. Practitioner lore says lines for the next day's games are often posted the previous evening, with low limits, and get injury-adjusted on game day. This is unverified.
- I found no primary Pinnacle or Circa documentation (Pinnacle's own "Betting Resources" pages did not surface). I also found no source on Circa's or Asian books' role specifically in NBA pricing.
- I found no academic paper measuring NBA opening-to-closing line efficiency in the search window. The Moskowitz (2021) paper below is the closest.
- Buchdahl's books (e.g., *Squares & Sharps, Suckers & Sharks*) were not checked directly.

## 2. Bookmaker behavior: balanced book vs. position-taking (Levitt, Paul & Weinbach, Humphreys et al.)

### Takeaway
The academic consensus since Levitt (2004) rejects the strict balanced-book hypothesis. Bettors predictably over-bet favorites (and overs), and books often accept lopsided action and shade prices against those biases. Paul & Weinbach confirmed this for the NBA using real sportsbook betting-percentage data from the 2004-05 to 2006-07 seasons.

### Cited Findings
- **Levitt, S. (2004). "Why are gambling markets organised so differently from financial markets?" *Economic Journal* 114(495): 223–246.**
  - Bookmakers announce a price and then adjust it only slightly and rarely. They act as position-takers, not as market makers who match buyers and sellers. — [IDEAS/RePEc](https://ideas.repec.org/a/ecj/econjl/v114y2004i495p223-246.html)
  - Bookmakers are better than bettors at predicting games and set prices that deviate from market clearing to exploit bettor biases. — [IDEAS/RePEc](https://ideas.repec.org/a/ecj/econjl/v114y2004i495p223-246.html); [AcaWiki summary](https://acawiki.org/Why_are_Gambling_Markets_Organised_So_Differently_from_Financial_Markets%3F)
  - Data: about 20,000 NFL wagers by 285 bettors at an online sportsbook (a betting tournament). — [IDEAS/RePEc](https://ideas.repec.org/a/ecj/econjl/v114y2004i495p223-246.html); NBER WP version: [w9422](https://www.nber.org/papers/w9422)
  - A secondary summary reports that position-taking raises bookmaker gross profit from 5.0% to 6.16%, about 23% higher than under balancing. — [AcaWiki summary](https://acawiki.org/Why_are_Gambling_Markets_Organised_So_Differently_from_Financial_Markets%3F) (**not verified against the paper; fetching the full text was blocked**)
- **Paul, R. & Weinbach, A. (2008). "Price Setting in the NBA Gambling Market: Tests of the Levitt Model of Sportsbook Behavior." *International Journal of Sport Finance* 3(3): 137–145.** The paper uses betting-percentage data from four sportsbooks for the 2004-05 to 2006-07 NBA seasons. Favorites receive a disproportionate share of point-spread bets, so betting volumes are not balanced. — [EconPapers](https://econpapers.repec.org/RePEc:jsf:intjsf:v:3:y:2008:i:3:p:137-145); [IDEAS](https://ideas.repec.org:443/a/jsf/intjsf/v3y2008i3p137-145.html); [PDF copy](https://kylewoodward.com/blog-data/pdfs/references/paul+weinbach-international-journal-of-sport-finance-2008A.pdf); cited as "unbalanced betting volumes on NBA games" in [Humphreys, U. Alberta WP 2010-05](https://sites.ualberta.ca/~econwps/2010/wp2010-05.pdf)
- **Paul, R. & Weinbach, A. (2005). "Bettor Misperceptions in the NBA: The Overbetting of Large Favorites and the 'Hot Hand'." *Journal of Sports Economics* 6(4): 390–400.** This covers NBA point spreads from 1995-96 to 2001-02. Bettors over-bet favorites. A strategy of betting big underdogs rejects the null of a fair bet, and betting big home underdogs rejects the null of no profitability. — [EconPapers](https://econpapers.repec.org/RePEc:sae:jospec:v:6:y:2005:i:4:p:390-400)
- **Paul, R. & Weinbach, A. (2011). "NFL bettor biases and price setting: further tests of the Levitt hypothesis of sportsbook behaviour." *Applied Economics Letters* 18(2): 193–197.** Using actual sportsbook betting percentages on sides and totals, the paper supports Levitt: books set prices to maximize profit rather than to clear the market. — [IDEAS](https://ideas.repec.org/a/taf/apeclt/v18y2011i2p193-197.html)
- **Paul, Weinbach & Humphreys (2011), *Journal of Gambling Business and Economics* 5(2): 42–56 (NBA "hot hand").** The paper notes that recent evidence suggests bookmakers do not set spreads to balance action. — [EconPapers](https://econpapers.repec.org/RePEc:buc:jgbeco:v:5:y:2011:i:2:p:42-56)
- **Correction to the assignment's citation:** I found no 2013 paper titled "Bettor biases and price setting by sportsbooks" in *JEBO*. The 2013 Humphreys–Paul–Weinbach paper is **"Bettor Biases and the Home-Underdog Bias in the NFL," *International Journal of Sport Finance* 8(4): 294–311.** It covers the NFL only. Bettors predictably favor the best teams, books do not behave as the balanced-book hypothesis predicts, and the paper offers an alternative explanation for the home-underdog bias, challenging Dare & Dennis (2011). — [IDEAS](https://ideas.repec.org/a/jsf/intjsf/v8y2013i4p294-311.html); [EconPapers](https://econpapers.repec.org/RePEc:jsf:intjsf:v:8:y:2013:i:4:p:294-311)
- Humphreys's 2010 working paper (U. Alberta WP 2010-05) reviews this literature and summarizes the evidence for unbalanced NBA volumes. — [PDF](https://sites.ualberta.ca/~econwps/2010/wp2010-05.pdf)

### Inferences
- In the NBA the "public" side is typically the favorite, especially popular or large favorites. Paul & Weinbach's evidence implies books shade spreads toward favorites rather than balancing, which is why big underdogs historically performed better than a fair bet would predict.
- These datasets predate legal US mobile betting (2004–2007 sportsbook percentages). Whether the effect survives in the post-2018, parlay-heavy market is not established by these sources.

### Gaps
- **Kuypers (2000)**, "Information and efficiency: an empirical study of a fixed odds betting market," *Applied Economics* 32(11), is the theoretical precursor showing that bookmakers can profit by not balancing. This citation is from background knowledge and was **not verified** in this session.
- I found no NBA-specific balanced-book test using post-2018 US legal data.
- Levitt's exact quantitative results (e.g., the share of bets on favorites and the home-underdog win rate) could not be extracted because the full-text fetch was blocked.

## 3. Sharp vs. public money: reverse line movement, steam, betting percentages, and momentum/value (Moskowitz)

### Takeaway
Academic evidence says the profitability of fading the public in the NBA is small at best. Historic biases (big underdogs) were modest, and Moskowitz (2021) finds that return predictability from line movement, including momentum, is real but too small to beat transaction costs (the vig). Reverse line movement and "steam" are practitioner concepts with little peer-reviewed validation. Retail "betting percentage" data are of uncertain provenance.

### Cited Findings
- **Moskowitz, T. J. (2021). "Asset Pricing and Sports Betting." *Journal of Finance* 76(6): 3153–3209.**
  - The paper uses betting contracts as a laboratory for asset-pricing theory, with about 120,000 contracts: 18,681 NBA, 7,035 NFL, 23,986 MLB and 9,890 NHL games. — [EconPapers](https://econpapers.repec.org/RePEc:bla:jfinan:v:76:y:2021:i:6:p:3153-3209); [NBER conference draft](https://conference.nber.org/conf_papers/f92072/f92072.pdf)
  - **Momentum** (line movement from open to close continuing in the same direction) is the strongest effect. It fits delayed overreaction and is inconsistent with underreaction or rational pricing. **Value** effects are weaker, and size effects are mixed. — [IDEAS](https://ideas.repec.Org/a/bla/jfinan/v76y2021i6p3153-3209.html); [Yale Insights](https://insights.som.yale.edu/insights/what-sports-betting-teaches-us-about-financial-markets)
  - Return predictability is a fraction of what is seen in financial markets and **fails to overcome transaction costs**, so arbitrage cannot eliminate it. — [Alpha Architect summary](https://alphaarchitect.com/value-momentum-sports-betting/); [BFI/UChicago](https://bfi.uchicago.edu/news/what-losing-50-on-a-football-game-can-teach-us-about-financial-markets/)
  - Moskowitz himself describes statistical significance as "slight." — [Alpha Architect](https://alphaarchitect.com/value-momentum-sports-betting/)
  - The sample period is described as "almost three decades" in the NBER draft and "two decades" in a secondary summary. Prefer the journal or NBER version. — [NBER draft](https://conference.nber.org/conf_papers/f92072/f92072.pdf)
- Paul & Weinbach (2005, JSE): fading the public on big NBA underdogs, especially home underdogs, rejected the fair-bet null in the 1995–2002 data. — [EconPapers](https://econpapers.repec.org/RePEc:sae:jospec:v:6:y:2005:i:4:p:390-400)
- A podcast summary claims positive-CLV bets returned +7.7% ROI vs. –8.38% for negative-CLV bets. **This could not be verified against a primary source.** — [Smart Betting Club podcast episode](https://www.buzzsprout.com/1340614/episodes/17827110-sports-strategy-edges-steam-moves-sharp-betting-unpacked-with-dylan-from-pinnacle-odds-dropper)
- Practitioner explanations of reverse line movement and steam: [Covers, "What line moves can tell us"](https://www.covers.com/guides/what-line-moves-can-tell-us); [PFF](https://pff.com/news/nfl-betting-101-sharp-signs-for-bettors-red-flags-to-avoid) (practitioner; definitional only)

### Inferences
- Moskowitz's momentum finding argues against "fading steam." Line moves tend to persist slightly, which is consistent with sharp/informed money moving the line rather than noise.
- Public "bet %/money %" figures from media sites are not audited. The academic studies used actual sportsbook data (e.g., four books in Paul & Weinbach 2008), so the published percentages common today should not be assumed to match that quality.

### Gaps
- I found no peer-reviewed test of reverse-line-movement strategies in the NBA.
- I found no audit of the reliability of commercial betting-percentage feeds (Action Network, VSiN/DraftKings splits, etc.).
- The NBA-specific momentum coefficients in Moskowitz were not extracted (full text was not fetched).

## 4. Limiting and banning winning bettors in US legal books

### Takeaway
The best regulatory data come from Massachusetts. As of December 10, 2024, 0.64% of sportsbook accounts were limited. Most limited accounts were cut to under 25% of the default maximum, and limits correlated with winning. Massachusetts then moved to require operators to notify limited bettors.

### Cited Findings
- On November 21, 2024 the Massachusetts Gaming Commission (MGC) approved a staff proposal to collect limiting data. The Sports Wagering Division sent a data request (covering stakes and closing-line value) to all licensed operators on December 10, 2024, and all seven responded. — [Covers, Nov 2024](https://www.covers.com/industry/massachusetts-data-collection-sports-bettor-limiting-mgc-november-2024); [MGC meeting materials 9/30/25](https://massgaming.com/wp-content/uploads/Meeting-Materials-9.30.25-OPEN.pdf)
- **0.64% of player accounts were limited** as of December 10, 2024. The count is of accounts, not people, since one person can be limited at several books. Of the limited accounts, **about 12.7% were capped below 1% of the default maximum stake and 57.6% at 1–24%.** — [MGC meeting materials 9/30/25](https://massgaming.com/wp-content/uploads/Meeting-Materials-9.30.25-OPEN.pdf); [CasinoBeats, Oct 1 2025](https://casinobeats.com/2025/10/01/massachusetts-gaming-commission-sportsbooks-notify-bettors-limited/)
- Regulators found that winning bettors were more likely to be limited, while the overall share stayed small. — [Covers, Sept 2025](https://www.covers.com/industry/massachusetts-limiting-sports-betting-prediction-markets-exchanges-sharps-box-september-2025)
- The MGC moved toward rules requiring operators to notify limited bettors and explain why. One report says the rule was approved in December 2025 with an effective date of June 1 (2026). **This date is unconfirmed; check MGC materials.** — [Covers, Dec 18 2025](https://www.covers.com/industry/massachusetts-bettors-could-soon-have-wagerning-limitations-explained-dec-18-2025)

### Inferences
- With sharp accounts limited at retail books, sharp information reaches US retail prices mostly *indirectly*, through market-maker prices that retail books copy. This fits the two-tier structure in Section 1.
- For a bettor, CLV against the market-maker close is both the best measure of skill and the variable retail books use to flag accounts.

### Gaps
- I found no equivalent limiting statistics from other states (NJ, NY, etc.).
- The Covers September 2025 piece mentions exchanges and prediction markets as alternatives for limited bettors, but I did not verify details.

## 5. Information and injury news: speed of market reaction

### Takeaway
High-quality evidence (from soccer betting exchanges) shows that prices incorporate major news swiftly and fully. I found no peer-reviewed study of NBA spread reaction to injury announcements. The 2025 federal indictments show, however, that non-public NBA injury and availability information was itself the asset being traded.

### Cited Findings
- **Croxson, K. & Reade, J. J. (2014). "Information and Efficiency: Goal Arrival in Soccer Betting." *Economic Journal* 124(575): 62–91.** The paper uses goals scored just before half-time, about 53 matches in the later literature's description, to separate major news from in-play noise. On a betting exchange, prices update "swiftly and fully" after a goal, with no drift during the break. That is consistent with semi-strong efficiency. — [EconPapers](https://econpapers.repec.org/RePEc:wly:econjl:v:124:y:2014:i:575:p:62-91); [Univ. of Reading repository](https://centaur.reading.ac.uk/34884/); [Birmingham research portal](https://research.birmingham.ac.uk/en/publications/information-and-efficiency-goal-arrival-in-soccer-betting/)
- Later work (Angelini, De Angelis & Singleton) finds more noise around information events than Croxson & Reade. — [working paper](https://cris.unibo.it/retrieve/8c5e3d3d-d36f-4279-b566-da91767d1a5c/information_efficiency_angelini_de_angelis_singleton.pdf)
- In the October 2025 EDNY case, Damon Jones allegedly sold non-public information about a Lakers player's injury or availability to bettors. He later pleaded guilty, admitting he passed on injury information about LeBron James and Anthony Davis in 2023 (Section 7). — [NBC News live blog](https://www.nbcnews.com/news/amp/live-blog/rcna239312?page=2); [NBC Sports](https://www.nbcsports.com/nba/news/damon-jones-pleads-guilty-in-federal-gambling-probe-terry-rozier-to-face-additional-charges)

### Inferences
- Because the market reacts quickly to *public* news, any edge from injury information depends on obtaining it before the public announcement. That is precisely what the 2025 indictments allege was being monetized, and it is why NBA injury-reporting rules double as integrity rules.

### Gaps
- I found no academic study of NBA line response to injury reports or lineup releases.
- I did not research the NBA's injury-report rules (timing requirements, fines) in this session.

## 6. The post-PASPA US market: handle, hold, NBA share, same-game parlays

### Takeaway
After *Murphy v. NCAA* (May 2018), US legal sports betting reached a record **$16.96B revenue on $166.94B handle in 2025** (AGA). Implied hold rose to about 10.2%, driven by parlay mix. Handle growth stalled in early 2026 as prediction markets drew volume. I could not obtain an NBA-specific share of national handle or Nevada's annual basketball hold.

### Cited Findings
- **2025 (AGA):** sports betting revenue about **$16.96B (+22.8%)** on **$166.94B handle (+11%)**. State-regulated books paid **$3.71B in taxes (+32.4%)**. Total commercial gaming revenue was a record $78.7B. — [AGA press release](https://www.americangaming.org/commercial-gaming-revenue-hits-78-7-billion-in-2025-driving-record-18-1-billion/); [ESPN](https://www.espn.com/espn/betting/story/_/id/48045855/sports-betting-hits-record-1696-billion-revenue-2025)
- AGA's *State of the States 2026* puts commercial sports betting revenue at $16.89B (+22.6%), a figure that excludes tribal books including Florida. — [Legal Sports Report](https://www.legalsportsreport.com/263300/sportsbooks-make-more-money-from-slower-sports-betting-growth-in-2025/); [AGA State of the States 2026](https://www.americangaming.org/research/state-of-the-states-2026/)
- **Implied national hold:** about 10.2% in 2025, vs. 9.2% in 2024 and 6.9% in 2019. This is LSR's calculation from AGA data, not an AGA-stated figure. — [Legal Sports Report](https://www.legalsportsreport.com/263300/sportsbooks-make-more-money-from-slower-sports-betting-growth-in-2025/)
- Commercial handle fell about 2% in Q1 2026, the first quarterly decline on record per LSR. The AGA estimates that sports event contracts on prediction markets have diverted more than $500M in potential tax revenue. — [Legal Sports Report](https://www.legalsportsreport.com/263300/sportsbooks-make-more-money-from-slower-sports-betting-growth-in-2025/); [ESPN](https://www.espn.com/espn/betting/story/_/id/48045855/sports-betting-hits-record-1696-billion-revenue-2025); [Covers, Feb 2026](https://www.covers.com/industry/aga-state-of-the-industry-sports-betting-prediction-markets-records-february-2026)
- Nevada basketball data points (monthly, from media summaries of NGCB reports): basketball revenue was $11.1M in June 2026, up 34.4% year over year. A Covers table for March 2026 lists basketball at $36.8M. — [Covers, July 31 2026](https://www.covers.com/industry/nevada-sportsbooks-see-significant-handle-revenue-increases-in-june-july-31-2026); [Covers, Apr 30 2026](https://www.covers.com/industry/nevada-sports-betting-handle-drops-again-in-march-april-30-2026) (**the meaning of the table figures is unclear; verify against NGCB monthly reports**)

### Inferences
- Rising hold with slower handle growth fits a shift in mix toward parlays and same-game parlays, which carry much higher hold than straight spreads (about 4.5% theoretical at -110). This inference is consistent with LSR's analysis, but I did not find a direct parlay-share citation.
- For NBA spread markets specifically, the relevant hold is the straight-bet margin, not the blended 10% figure.

### Gaps
- I found no NBA share of US handle. Several states break out basketball, but NBA vs. college is often combined.
- I did not obtain New Jersey DGE parlay or basketball hold figures or Nevada's annual basketball win %; NGCB monthly "Gaming Revenue Report" PDFs are the primary source.
- I found no same-game-parlay share data from a regulator.

## 7. Integrity: point-shaving research, the Donaghy scandal, Jontay Porter, the 2025 federal indictments, and NBA prop restrictions

### Takeaway
The academic "forensic" evidence for widespread point shaving (Wolfers 2006) was seriously challenged. The same asymmetries appear in the NBA and NFL, and they are explained by late-game strategy. Proven NBA cases have instead involved insiders (a referee in 2007, a two-way player in 2024, and players and an ex-coach in the 2025 EDNY indictments) exploiting **player props and inside information**. That led the NBA and its partner sportsbooks to restrict specific prop markets in 2024–2026.

### Cited Findings

**Point-shaving research**
- **Wolfers, J. (2006). "Point Shaving: Corruption in NCAA Basketball." *American Economic Review* 96(2): 279–283 (Papers & Proceedings).** Strong favorites (e.g., 14-point favorites) were about 6% more likely to win but fail to cover than to cover. That implied about 1% of games, roughly 500 NCAA games from 1989 to 2005, may have involved point shaving. Wolfers noted this holds only if the market fails to price in point shaving. — [Berkeley course copy](https://www.stat.berkeley.edu/~aldous/157/Papers/PointShaving.pdf); [University of Washington news, Mar 2006](https://washington.edu/news/2006/03/14/basketball-badness); summarized in [J. Sports Analytics review (2015)](https://doi.org/10.3233%2FJSA-150011)
- **Borghesi (2008)** found the same patterns in the **NBA and NFL**, which makes point shaving an unlikely cause. **Borghesi & Dare** attribute the excess "win but don't cover" outcomes to coaches and players optimizing late in blowouts. **Borghesi, Paul & Weinbach** question Wolfers's assumption that outcomes are symmetric around the spread. — [J. Sports Analytics review, "The debate on widespread point shaving"](https://doi.org/10.3233%2FJSA-150011)
- **Bernhardt & Heston (2010, *Economic Inquiry*, "Point shaving in college basketball: a cautionary tale for forensic economics")** imputed spreads using Sagarin ratings for games with no Vegas line. The same patterns appeared where no betting market existed, which they attribute to late-game strategy. — [Univ. of Illinois news](https://news.illinois.edu/researchers-dispute-study-pointing-to-college-basketball-point-shaving/); [Illinois LAS news](https://las.illinois.edu/news/2006-09-01/no-foul)
- **Diemer & Leeds** found the patterns absent in NCAA tournament games. **Berkowitz** argues that point shaving is impractical and so not widespread. — [J. Sports Analytics review](https://doi.org/10.3233%2FJSA-150011); [UNC Charlotte WP 2016-012](https://belkcollegeofbusiness.charlotte.edu/economic-working-papers/wp-content/uploads/sites/850/2012/10/wp2016-012.pdf)
- **Paul & Weinbach (2011), *Journal of Sports Economics* 12(4): 432–447** used actual sportsbook betting percentages, rejected the balanced book, and then tested for NCAA corruption. — [EconPapers](https://econpapers.repec.org/RePEc:sae:jospec:v:12:y:2011:i:4:p:432-447)

**Tim Donaghy (2007–2008)**
- He pleaded guilty on August 15, 2007 and was sentenced on July 29, 2008 to **15 months** by Judge Carol Amon, below the 33 months he had faced. One NPR report says 13 months, which conflicts with the other sources. — [ESPN](https://www.espn.co.uk/nba/news/story?id=3509440); [CBS News](https://www.cbsnews.com/news/donaghys-surprising-sentence-15-months); [NPR](https://www.npr.org/transcripts/93041356)
- The **Pedowitz Report** (October 2008, 116 pages), commissioned by the NBA, concluded that Donaghy acted alone and found no evidence his calls affected outcomes. It cleared referee Scott Foster. — [Washington Times, Oct 2 2008](https://m.washingtontimes.com/news/2008/oct/2/report-donaghy-acted-alone/)

**Jontay Porter (2024)**
- He was banned for life by the NBA on **April 17, 2024**. He pleaded guilty in July 2024 in EDNY (Brooklyn) to one count of wire-fraud conspiracy, admitting he rigged games, through early exits that hit "under" props, to pay gambling debts. The guidelines range was 41–51 months. — [PBS NewsHour](https://www.pbs.org/newshour/nation/jontay-porter-pleads-guilty-in-case-tied-to-gambling-scandal-that-tanked-his-nba-career); [ESPN](https://africa.espn.com/nba/story/_/id/40534530/jontay-porter-pleads-guilty-case-tied-nba-betting-scandal)
- His sentencing has been repeatedly postponed, most recently with no new date set according to reporting dated around January 2026. I found no source tying the delay to cooperation. Co-defendant Timothy McCormack was sentenced to 24 months. — [Covers, Mar 2025](https://www.covers.com/industry/former-nba-player-jontay-porter-sentencing-delayed-until-december-march-7-2025); [Philly Daily, Oct 23 2025](https://phillydaily.com/news/2025/oct/23/montco-man-involved-in-jontay-porter-nba-betting-s)

**October 23, 2025 federal indictments (EDNY)**
- There were two separate indictments: (1) a sports-betting and inside-information case naming **Terry Rozier** (Heat; the only active player charged) and ex-player/assistant coach **Damon Jones**; (2) a mob-linked rigged-poker case naming **Chauncey Billups** (Trail Blazers head coach). In total **34 people were charged** across 11 states. Rozier and Billups were placed on leave. Prosecutors say Jontay Porter was involved in the betting operation. — [PBS NewsHour](https://www.pbs.org/newshour/nation/miami-heats-rozier-trail-blazers-billups-arrested-in-federal-gambling-probe-sources-say); [NBC News](https://www.nbcnews.com/news/us-news/illegal-gambling-nba-poker-betting-chauncey-billups-terry-rozier-rcna239497); [CBS News](https://www.cbsnews.com/news/terry-rozier-chauncey-billups-nba-gambling-poker-indicted-names); [Axios](https://www.axios.com/2025/10/23/sports-gambling-nba-rozier-billups)
- Key Rozier allegation: on a **March 2023** Hornets game he told an associate he would leave early with a purported injury, and associates bet his unders. The indictment outlines **8 NBA games** in total. — [PBS NewsHour](https://www.pbs.org/newshour/nation/miami-heats-rozier-trail-blazers-billups-arrested-in-federal-gambling-probe-sources-say); [AOL/Reuters-style piece, "U.S. prosecutors outline 8 NBA games"](https://www.aol.com/articles/u-prosecutors-outline-8-nba-205736458.html)
- Jones allegedly sold non-public Lakers injury information. — [NBC News](https://www.nbcnews.com/news/amp/live-blog/rcna239312?page=2)
- **Subsequent developments (2026):**
  - Rozier pleaded not guilty and was released on a $3M bond. — [CBS News](https://www.cbsnews.com/news/terry-rozier-nba-pleads-not-guilty-gambling-case); [Courthouse News](https://www.courthousenews.com/terry-rozier-pleads-not-guilty-to-rigging-nba-bets-out-on-3-million-bond/)
  - **Damon Jones pleaded guilty (April 2026)** to wire-fraud conspiracy, the first plea in the case, admitting he passed on injury information about LeBron James and Anthony Davis in 2023. His sentencing is set for January 2027. — [NBC Sports](https://www.nbcsports.com/nba/news/damon-jones-pleads-guilty-in-federal-gambling-probe-terry-rozier-to-face-additional-charges); [Defector](https://defector.com/prosecutors-got-a-guilty-plea-in-the-nba-gambling-case)
  - A superseding indictment adds **bribery in sporting contests** and honest-services wire-fraud conspiracy, alleging Rozier accepted a **$100,000 bribe** to leave a 2023 game early. Rozier pleaded not guilty, and **trial is set for February 8, 2027** (Covers, June 11, 2026). He is not being paid his NBA salary. — [Covers](https://www.covers.com/industry/terry-rozier-pleads-not-guilty-to-bribery-charges-awaits-february-trial); [TSN](https://www.tsn.ca/nba/article/prosecutors-plan-to-file-new-charges-against-rozier-n1-48613917/)
  - The EDNY U.S. Attorney called the investigations "very much ongoing" at the October 2025 announcement. — [Covers, Mar 2025 / later update](https://www.covers.com/industry/former-nba-player-jontay-porter-sentencing-delayed-until-december-march-7-2025); see also [NBC Sports explainer](https://www.nbcsports.com/nba/news/what-to-know-about-terry-rozier-chauncey-billups-indictments-amid-sprawling-fbi-investigations)
  - **Verification caveat:** the DOJ EDNY press release could not be fetched (justice.gov is blocked in this session). Facts above come from multiple major outlets. Billups's case is about poker, not NBA betting.

**NBA and sportsbook prop-bet restrictions**
- **2024 (after Porter):** the NBA asked partner sportsbooks to stop offering unders on props for players on two-way contracts. — [ESPN](https://africa.espn.com/nba/story/_/id/40140497/jontay-porter-scandal-nba-leagues-betting-risks)
- **2025-26 season baseline:** partner books (most of the legal US market) dropped props on players on 10-day or two-way contracts and restricted props on turnovers, fouls and missed free throws. — [NBC News, "How the NBA took on prop bets"](https://www.nbcnews.com/sports/sports-gambling/nba-mlb-microbets-sports-betting-gambling-rcna224412?rand=14095); [NBC New York](https://www.nbcnewyork.com/news/sports/nba/nba-microbets-mlb-blueprint-betting-scandals/)
- **October 2026 (reported by ESPN, carried by Deseret News Oct 16, 2026):** new voluntary restrictions cover parlays combining unders on multiple statistics for the same player, "first of" bets (e.g., first basket), and unders on players expected to average fewer than 12 minutes per game. The NBA and the players' union back "reasonable limitations." An NBA spokesperson said: "Protecting the integrity of our game is paramount, and we believe reasonable limitations on certain prop bets should be given due consideration." — [Deseret News, Oct 16 2026](https://www.deseret.com/sports/2026/10/16/nba-sportsbooks-agree-to-ban-several-types-of-player-prop-bets-amid-gambling-concerns/) (full text was not fetched; based on a search summary); [ESPN, NBA/union back bet limits](https://africa.espn.com/nba/story/_/id/45987377/nba-union-back-bet-limits-curb-manipulation-athlete-abuse); [NBC Sports](https://www.nbcsports.com/nba/news/nba-works-with-sportsbook-partners-to-remove-specific-wagers-prop-bet-parlays-on-games)
- The AGA's Joe Maloney argued that sweeping bans reduce the integrity-monitoring visibility that legal books provide. — [NBC News](https://www.nbcnews.com/sports/sports-gambling/nba-mlb-microbets-sports-betting-gambling-rcna224412?rand=14095)
- CBS Sports analysis of options for the league's prop-bet problem. — [CBS Sports](https://www.cbssports.com/nba/news/how-can-nba-address-prop-betting-problem-three-possible-solutions-as-league-faces-another-gambling-scandal)
- Related: the NGCB announced an arrest in an NCAA illegal-wagering case on June 11, 2026. — [NGCB press release](https://www.gaming.nv.gov/siteassets/content/about/press-release/ngcb-arrests-suspect-involved-in-ncaa-illegal-sports-wagering-activity--6.11.26.pdf)

### Inferences
- Modern NBA manipulation risk is concentrated in **low-salary players' individual props** and in **non-public availability information**, not in full-game spreads. A single player can control his own minutes and stats far more easily than a final margin. The restrictions target exactly those markets (unders, low-minute players, "first of").
- The academic lesson from the Wolfers debate is that point-spread distribution asymmetries alone are weak evidence of fixing. Integrity monitoring relies instead on account-level betting patterns, as in the Porter case, which was flagged through unusual prop action.

### Gaps
- No primary DOJ text was read, because justice.gov was blocked. The exact indictment counts, the full game list and the dollar amounts should be verified against the EDNY press release and indictment.
- I found no outcome for Porter's sentencing as of late 2026, and no outcome for Billups's poker case.
- The exact list of sportsbooks party to the October 2026 agreement, and whether its effective date was the 2026-27 season, are unverified.
- I found no "under-25" age-based prop restriction (it may not exist).
- I found no evidence on whether there was any NBA spread (not prop) manipulation in the 2025 case.
