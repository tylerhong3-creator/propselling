# Quantitative Mathematics of NBA Point-Spread Betting (Vig, No-Vig, CLV, Margin Distribution, Conversions, Correlation, Kelly, Sample Size, Teasers)

**Method note (read first).** Network access in this session was restricted: most publisher sites (Pinnacle, JSTOR, Berkeley, eScholarship, CRAN, Basketball-Reference) could not be fetched, so literature claims below rest on search-result abstracts and secondary sources, flagged where relevant. To compensate, I downloaded a public NBA closing-odds archive (SportsbookReviewsOnline data re-hosted on GitHub, `nba_archive_10Y.json`, seasons 2011-12 through 2021-22) and computed the NBA-specific numbers myself in Python — [Dataset](https://raw.githubusercontent.com/flancast90/sportsbookreview-scraper/main/data/nba_archive_10Y.json). After dropping rows with corrupt or implausible lines (|spread| > 25, or total outside 150–280), **12,956 games** remained (947 dropped). The archive gives closing spreads and totals **without the spread prices**, so every ATS calculation assumes −110. Its moneylines carry a 3.2–4.5% two-way overround, so they are a retail/consensus market, not Pinnacle. Formulas are standard; numbers marked "computed" are my own calculations. The scripts are in the session scratchpad, which is temporary: `/tmp/claude-0/-home-user-propselling/09043879-ee60-5599-b1e1-d93c9775dfc5/scratchpad/an.py`, `calc.py` and `t.py`.

---

## 1. Vig, break-even, hold, and removing the vig (multiplicative, additive, power, Shin)

### Takeaway
At −110 you must win 52.38% to break even; the two-way −110/−110 market has 4.76% overround, which is a 4.55% theoretical hold. For a two-outcome market like a spread, Shin's method gives the same answer as the additive method. Štrumbelj (2014) found Shin-based probabilities more accurate than plain normalization, but on a −110/−110 spread every method gives 50/50, so the choice only matters for moneylines and lopsided prices.

### Cited Findings

**Formulas (standard; numbers computed):**
- Decimal odds from American: D = 1 + 100/|A| for A < 0; D = 1 + A/100 for A > 0. Break-even win probability = 1/D, which is |A|/(|A|+100) for favorites and 100/(A+100) for underdogs. (Computed.)
- Break-even table (computed):

| Price | Decimal | Break-even |
|---|---|---|
| −100 (even) | 2.000 | 50.00% |
| −102 | 1.980 | 50.50% |
| −104 | 1.962 | 50.98% |
| −105 (reduced juice) | 1.952 | 51.22% |
| −107 | 1.935 | 51.69% |
| −108 | 1.926 | 51.92% |
| **−110 (standard)** | **1.909** | **52.38%** |
| −112 | 1.893 | 52.83% |
| −115 | 1.870 | 53.49% |
| −120 | 1.833 | 54.55% |
| −125 | 1.800 | 55.56% |
| −130 | 1.769 | 56.52% |

- **Overround (booksum):** B = Σ 1/D_i. **Theoretical hold** (the book's margin when the action is balanced in proportion to fair probabilities) = 1 − 1/B. (Computed.)

| Two-way market | Booksum | Overround | Hold |
|---|---|---|---|
| −110 / −110 | 1.0476 | 4.76% | **4.55%** |
| −108 / −108 | 1.0385 | 3.85% | 3.70% |
| −105 / −105 | 1.0244 | 2.44% | 2.38% |
| −102 / −102 | 1.0099 | 0.99% | 0.98% |
| −115 / −105 | 1.0471 | 4.71% | 4.50% |
| −112 / −108 | 1.0475 | 4.75% | 4.54% |

- Expected loss per $1 bet on a −110 coin flip is 0.5×0.9091 − 0.5 = −4.55%, which equals the hold. (Computed.)
- In the archive, NBA closing moneylines had a median two-way overround of 3.2–4.5% depending on the spread band. Hold is highest on near-pick'em games (≈4.5%) and on big favorites (≈4.1–4.2%). (Computed from the [Dataset](https://raw.githubusercontent.com/flancast90/sportsbookreview-scraper/main/data/nba_archive_10Y.json).)

**De-vig methods.** Notation: r_i = 1/D_i are the raw implied probabilities, B = Σ r_i, and the goal is fair probabilities p_i.
- **Basic / multiplicative (normalization):** p_i = r_i / B. It is the default in the `implied` R package — [implied vignette (GitHub source of CRAN vignette)](https://raw.githubusercontent.com/opisthokonta/implied/master/vignettes/introduction.Rmd)
- **Additive:** p_i = r_i − (B − 1)/n, which subtracts an equal share of the margin from each outcome. It can produce negative probabilities for longshots in many-outcome markets (example from Clarke, Kovalchik & Ingram 2017). The vignette states: **"If there are only two outcomes, the additive method and Shin's method are equivalent."** — [implied vignette](https://raw.githubusercontent.com/opisthokonta/implied/master/vignettes/introduction.Rmd)
- **Power:** p_i = r_i^k, with k chosen so that Σ p_i = 1 (called the "logarithmic" method in the "Wisdom of the Crowds" document) — [implied vignette](https://raw.githubusercontent.com/opisthokonta/implied/master/vignettes/introduction.Rmd)
- **Odds ratio** (Cheung 2015): the bookmaker probabilities are an odds-ratio transform of the true probabilities, with the OR chosen so the probabilities sum to 1 — [implied vignette](https://raw.githubusercontent.com/opisthokonta/implied/master/vignettes/introduction.Rmd)
- **Shin:** assumes a fraction z of bettors are insiders and the bookmaker sets prices to maximize profit given z. Closed form (as in Jullien & Salanié 1994 and Štrumbelj 2014; I reproduced this formula from standard references, and the vignette describes the model but its formula text was not extracted):
  p_i = [ √(z² + 4(1−z)·r_i²/B) − z ] / [ 2(1−z) ], with z solved numerically so that Σ p_i = 1.
  Sources: Shin, H.S. (1993), "Measuring the Incidence of Insider Trading in a Market for State-Contingent Claims," *Economic Journal* 103(420):1141–53 — [IDEAS/RePEc](https://ideas.repec.org/a/ecj/econjl/v103y1993i420p1141-53.html); Shin (1992) "Prices of State Contingent Claims with Insider Traders, and the Favourite-Longshot Bias" and Jullien & Salanié (1994) comment are listed in [implied vignette references](https://raw.githubusercontent.com/opisthokonta/implied/master/vignettes/introduction.Rmd). The prompt's "Shin 1991" is probably Shin (1991), "Optimal betting odds against insider traders," *Economic Journal* 101; this is from memory and not verified here.
- **Štrumbelj (2014)**, "On determining probability forecasts from betting odds," *International Journal of Forecasting* 30(4):934–943: probabilities from Shin's model were more accurate than basic normalization — [pypi `shin` package citing it](https://pypi.org/project/shin/0.1.0/); summarized as "the Shin method is the most accurate of the approaches compared" in later literature — [Springer Annals of OR 2022](https://link.springer.com/article/10.1007/s10479-022-04722-3). A follow-up by Štrumbelj says basic normalization produces biased probabilities (search summary of that follow-up; not fetched).

**Worked example (computed), moneyline −150 / +130:** raw 0.6000 / 0.4348, B = 1.0348.

| Method | Favorite | Underdog |
|---|---|---|
| Multiplicative | 0.5798 | 0.4202 |
| Additive | 0.5826 | 0.4174 |
| Power (k = 1.053) | 0.5840 | 0.4160 |
| Shin (z = 0.0348) | 0.5826 | 0.4174 (= additive, as expected for 2 outcomes) |

Three-way example with decimal odds 1.5 / 4.2 / 7.0: multiplicative gives 0.636/0.227/0.136; Shin (z = 0.024) gives 0.647/0.223/0.130. Shin moves probability from the longshot to the favorite, which corrects for the favorite–longshot bias. (Computed.)

### Inferences
- For NBA **spreads** at −110/−110, all methods give 50.00%. The method only matters for skewed prices (e.g., −120/+100 or a −115/−105 spread) and for moneylines. On a two-way market, multiplicative assigns a little more of the margin to the favorite than additive/Shin. The differences are about 0.3 percentage points at −150/+130 and grow with the price gap.
- Hold should be judged per market. Reduced juice (−105) roughly halves the bettor's handicap, cutting break-even by 1.16 points (52.38% → 51.22%), which is worth more than most handicapping edges.

### Gaps
- I could not open the Štrumbelj 2014 full text, so its accuracy metrics (Brier/log-loss deltas) and sports covered are unverified. The Shin closed form is reproduced from standard references, not extracted from the papers.
- No Pinnacle-specific NBA spread hold data was available; widely quoted figures of about 2–2.5% are unverified here.

---

## 2. Closing Line Value (CLV): definition, measurement, and evidence

### Takeaway
CLV compares the price you took with the market's closing price. The best-documented support is that efficient closing prices (Pinnacle's is the usual benchmark) are the best available estimate of true probability. In this NBA archive, betting the opening number in the direction the line later moved won 54.0% overall and 60.7% when the move was ≥2 points. Taking the same sides at the closing number won only 49.6%. So the closing line absorbs the information that the opener lacked.

### Cited Findings
- **Definitions / measurement (standard; computed):**
  - *Spread CLV in points* = (your line − closing line), from your side. For example, taking −4 when it closes −5.5 is +1.5 points.
  - *Price CLV %* = (your decimal odds / closing no-vig fair decimal odds) − 1, which is your expected ROI if the close is the true probability. Example: you bet +105 (D = 2.05) and the close is −120/+100 (no-vig, multiplicative: 54.35%/45.65%). Your side's fair D = 1/0.4565 = 2.190, so CLV = 2.05/2.190 − 1 = −6.4%. Had you bet the −120 side at −105 (D = 1.952) vs fair 1/0.5435 = 1.840, CLV = +6.1%. (Computed.)
  - To convert point CLV into probability on a spread, use the margin density near the number (see Section 3). Each half-point near the center is worth roughly f(0)·0.5 ≈ 0.5/(12.6·√(2π)) ≈ **1.6 percentage points** of cover probability under the normal model. Landing on 3, 5, 6 or 7 adds about 1.6–2.3 points per half-point (half the landing probability). (Computed.)
- Buchdahl's framework (secondary summary): "if you are beating the closing no-vig price, your bets should hold expected value," and Pinnacle's closing odds are "widely accepted as providing the most accurate numbers" — [secondary summary of Buchdahl](https://pod-d614f9k2t-pod-team.vercel.app/blog/closing-line-value--clv-demystified-by-expert-joseph-buchdahl). The same summary attributes to Buchdahl the claim that proving profit from results alone can take "several thousand bets," while a consistent ~5% CLV edge "might only need 50 bets to demonstrate significance." This is secondary; verify against Buchdahl's books (*Squares & Sharps, Suckers & Sharks*, 2016; *Fixed Odds Sports Betting*, 2003).
- Caveat from Buchdahl (per search summary): he wrote that Pinnacle's closing odds had stopped being a reliable predictor of outcomes in Europe's main soccer leagues, attributing part of this to arbitrage bettors pushing closing odds the wrong way — [search summary; secondary](https://pod-d614f9k2t-pod-team.vercel.app/blog/closing-line-value--clv-demystified-by-expert-joseph-buchdahl). This could not be verified at the primary source.
- Betting guides describe the close at sharp books as "the most reliable estimate of true probabilities" and CLV as an early indicator of edge before results are statistically meaningful — [TheLines](https://www.thelines.com/betting/guides/closing-line-value/); [TheSpread](https://www.thespread.com/?p=550721). The origin story (a Pinnacle-affiliated writer found CLV predicted future results better than W/L) appears only in a forum post — [SBR forum](https://www.sportsbookreview.com/forum/handicapper-think-tank/475316-the-misunderstanding-of-beating-the-closing-line); unverified. A forum thread also cites a Pinnacle article saying you need to beat the close about 75% of the time; that article could not be located — [SBR forum](https://www.sportsbookreview.com/forum/handicapper-think-tank/1788273-information-opening-line-vs-closing-line-calculating-average-clv).
- Some practitioners argue the benchmark should be a consensus of several sharp books rather than Pinnacle alone — [SBR forum](https://www.sportsbookreview.com/forum/handicapper-think-tank/506237-beating-pinny-s-line-guarantee-profit).
- **NBA test, opener vs close (computed from the [Dataset](https://raw.githubusercontent.com/flancast90/sportsbookreview-scraper/main/data/nba_archive_10Y.json), 2011-12 to 2021-22).** Bet the side the spread moved toward, at the opening number, assuming −110:

| Opening→close move | Bets | ATS win% at opening number |
|---|---|---|
| ≥ 0.5 pt | 10,550 | **54.0%** |
| ≥ 1.0 pt | 6,767 | 55.6% |
| ≥ 1.5 pt | 3,936 | 58.1% |
| ≥ 2.0 pt | 2,219 | 60.7% |
| ≥ 3.0 pt | 715 | 64.6% |
| Same sides at the **closing** number | 10,567 | **49.6%** |

  Overall closing-line ATS results were also unbiased: home teams covered 49.3% and favorites 50.0% (computed).

### Inferences
- The table shows directly that NBA closing spreads are more informative than openers. Beating the close by about 1–2 points matched a 55–61% win rate at the opener, and the edge disappears at the closing number. That is the mechanism behind CLV.
- This is a look-ahead test (you cannot know the move in advance). It shows the close is the better estimate; it does not show any strategy is profitable. Opening limits are also low, so real fill sizes are small.
- In practice: track the % of bets that beat the close, average point CLV, and average price CLV against a no-vig sharp close. CLV variance per bet is much smaller than W/L variance, so CLV becomes significant far sooner than ROI (see Section 7).

### Gaps
- I could not access Pinnacle's own articles or an academic paper that directly regresses bettor profit on CLV. One independent study of 12,437 bets from 213 bettors was surfaced by search, but its findings are unverified — [sharpery](https://sharpery.vercel.app/research/clv-long-term-profitability) (low-quality source).
- The archive has no spread prices or Pinnacle closes, so price-based CLV could not be computed.

---

## 3. NBA final-margin distribution relative to the spread; key numbers; half-point values vs NFL

### Takeaway
The NBA margin minus the closing spread is close to normal with **SD ≈ 12.6** over 2011-22. The SD has risen over time, from about 12.0 in 2011-15 to 13.6–13.8 in 2020-22. The distribution is more peaked and fatter-tailed than normal (excess kurtosis ≈ 2.6). NBA "key numbers" are weak. The most common margins are 7, 5, 6, 8 and 3, each at roughly 6% of games. Landing on an exact closing integer spread happens about 3.35% of the time, against roughly 9% at NFL −3. Half-points matter far less in the NBA.

### Cited Findings (all NBA numbers computed from the [Dataset](https://raw.githubusercontent.com/flancast90/sportsbookreview-scraper/main/data/nba_archive_10Y.json), n = 12,956, unless otherwise cited)
- Home margin: mean +2.68, SD 14.20. Mean closing home spread −2.88.
- **Residual (margin + home closing spread): mean −0.20, SD 12.61.** Within ±1 SD: 70.0% (normal 68.3%). Within ±2 SD: 95.3% (normal 95.4%). **Excess kurtosis +2.63** (peaked center, heavy tails). OT share (tied after 4 quarters) ≈ 5.8%.
- Residual SD by season: 2011-12 12.07, 2012-13 12.19, 2013-14 12.00, 2014-15 11.61, 2015-16 12.07, 2016-17 13.12, 2017-18 12.25, 2018-19 13.19, 2019-20 12.72, 2020-21 13.78, 2021-22 13.59.
- Residual SD by |spread|: 0–2.5: 13.97; 3–5.5: 12.24; 6–8.5: 12.58; 9–11.5: 12.20; ≥12: 12.10.
- Residual SD by closing total: 180s 12.24; 190s 12.08; 200s 12.14; 210s 12.78; 220s 13.16; 230s 14.11. **SD rises with the total** (see Section 5).
- **Absolute final margin frequency** (% of all games): 1: 3.94, 2: 5.10, 3: 5.74, 4: 5.58, 5: 6.20, 6: 6.16, **7: 6.49 (mode)**, 8: 6.03, 9: 5.46, 10: 4.84, 11: 4.35, 12: 4.07, 13: 3.58, 14: 3.35, 15: 3.23.
- Favorite-perspective (favorite wins by exactly k, % of games): 1: 2.05, 2: 2.76, 3: 3.28, 4: 3.22, 5: 3.76, 6: 4.04, **7: 4.31**, 8: 3.89, 9: 3.68, 10: 3.33, 11: 3.05, 12: 2.98.
- **Landing probability near the number:** P(favorite wins by exactly k | |spread| within ±2 of k): k=1 2.36%, 2 3.13%, **3 3.80%**, 4 3.28%, **5 3.94%, 6 4.28%, 7 4.64%**, 8 4.20%, 9 3.68%, 10 3.78%, 11 3.05%, 12 3.82%.
- **Push rate at integer closing spreads:** |1| 2.68% (n=299), 2 3.35%, **3 4.09%**, 4 2.57%, 5 3.67%, **6 4.08%, 7 4.50%**, 8 2.50%, 9 2.90%, 10 3.10%, 11 1.85%, 12 3.68% (n=190); **all integer spreads 3.35%** (n=6,538). Per-number samples are small (SE ≈ 0.7–1.3 points).
- Practitioners also say 5 and 7 are the most common NBA margins; those claims come from informal forum posts without data — [SBR forum](https://www.sportsbookreview.com/forum/players-talk/210446-how-to-gamble-on-sports-key-numbers-occur-in-the-nba); [SBR forum on 7](https://www.sportsbookreview.com/forum/handicapper-think-tank/131028-7-a-key-number-in-nba). My computation supports 7 as the mode, with 5, 6 and 8 close behind.
- **NFL comparison:** 3 is the final margin in 15.12% of games (1,100/7,276, 1999–2025) and 7 in 9.03%. Pushes at a closing −3 occur 9.0% of the time and at −7 6.5% — [DeucesCracked NFL margin data](https://www.deucescracked.com/blog/nfl-margin-of-victory-data-1999-2025); Action Network gives about 15% at 3 since 2003 — [Action Network](https://www.actionnetwork.com/nfl/nfl-key-betting-numbers-spread-margins-of-victory-line-value).
- Literature: Stern (1994) modeled the score difference as Brownian motion on t ∈ (0,1) with drift μ (home edge) and variance σ², and found a good fit to 493 NBA games from 1991-92 — [JASA 89(427):1128–1134, DOI 10.1080/01621459.1994.10476851](https://informahealthcare.com/doi/abs/10.1080/01621459.1994.10476851). The paper's estimates of μ and σ could not be extracted (PDF host blocked). Stern (1991, *American Statistician*), on NFL margins being about N(spread, ≈13.9²), is from memory and not verified in this session.

### Inferences
- **Value of a half-point:** about P(land)/2 in cover probability. In the NBA a half-point near 7 is worth about 2.3 points of win probability, and around 1.2–2.0 points near 1–4. In the NFL a half-point through 3 is worth about 4.5 points. The NBA lacks the scoring-quantum structure that creates NFL key numbers, so its half-points are spread more evenly. The modest bumps at 3 and 5–7 likely reflect end-game fouling and possession math (inference).
- For modeling, use a normal with σ ≈ 12.5–13.5 for the current era, or better, the empirical residual distribution: the excess kurtosis means a normal overstates mid-range outcomes and understates both exact-number pushes and blowouts.

### Gaps
- Margins could not be checked against Basketball-Reference for 2022-23 onward (blocked). Recent seasons (higher totals, more 3-pointers) may have SD of 13.5+, and that trend is unverified past 2021-22.
- Per-number push samples are small. A multi-decade dataset (e.g., Covers 1990–2009 numbers referenced on SBR) could not be retrieved.

---

## 4. Converting a point spread to win probability / moneyline

### Takeaway
The classic conversion is P(fav wins) = Φ(|spread|/σ). With σ = 12.6 (the residual SD), it gives a −7 favorite 71.1% (fair about −246). Market moneylines are not consistent with a single σ, though. The implied σ falls from about 15–18 for 2–3 point favorites to about 10.5 for 12–14 point favorites. A single fitted probit gives σ ≈ 11.6, so use a spread-dependent mapping or an empirical table.

### Cited Findings
- Model: final margin ~ N(spread-implied mean, σ²), so P(win) = Φ(μ/σ). Polson & Stern (2015), "The implied volatility of a sports game," *JQAS* 11(3):145–153, back out σ from the spread plus moneyline. Their example (an NFL Super Bowl) uses spread −4 and σ = 10.6 — [De Gruyter](https://www.degruyterbrill.com/document/doi/10.1515/jqas-2014-0095/html); [RePEc](https://econpapers.repec.org/RePEc:bpj:jqsprt:v:11:y:2015:i:3:p:145-153:n:4). (Details from search summary.)
- **Normal-model table (computed), P(favorite wins outright):**

| Fav spread | σ=11.5 | σ=12.0 | σ=12.6 | σ=13.5 | Fair ML at σ=12.6 |
|---|---|---|---|---|---|
| 1 | .535 | .533 | .532 | .530 | −114 |
| 2 | .569 | .566 | .563 | .559 | −129 |
| 3 | .603 | .599 | .594 | .588 | −146 |
| 4 | .636 | .631 | .625 | .616 | −166 |
| 5 | .668 | .662 | .654 | .644 | −189 |
| 6 | .699 | .691 | .683 | .672 | −215 |
| 7 | .729 | .720 | .711 | .698 | −246 |
| 8 | .757 | .748 | .737 | .723 | −281 |
| 9 | .783 | .773 | .762 | .748 | −321 |
| 10 | .808 | .798 | .786 | .771 | −368 |
| 12 | .852 | .841 | .830 | .813 | −487 |
| 14 | .888 | .878 | .867 | .850 | −650 |

- **Market-implied mapping (computed from archive closing MLs, multiplicative no-vig, median by closing spread):**

| Home closing spread | n | No-vig home win prob | Empirical SU win | Implied σ = |s|/Φ⁻¹(p) |
|---|---|---|---|---|
| −1 / −0.5 | 180 | .517 | .494 | — |
| −2 / −1.5 | 576 | .543 | .562 | 18.4 (|s| 1.5–2, all games) |
| −3 / −2.5 | 789 | .571 | .546 | 14.9 |
| −4 / −3.5 | 846 | .612 | .569 | 13.3 |
| −5 / −4.5 | 902 | .643 | .673 | 12.9 |
| −6 / −5.5 | 869 | .679 | .674 | 12.3 |
| −7 / −6.5 | 886 | .715 | .730 | 11.8 |
| −8 / −7.5 | 817 | .752 | .723 | 11.4 |
| −9 / −8.5 | 646 | .786 | .782 | 11.2 |
| −10 / −9.5 | 527 | .816 | .784 | 10.9 |
| −11 / −10.5 | 457 | .840 | .845 | 10.8 |
| −12 / −11.5 | 377 | .865 | .844 | 10.6 |
| −13 / −12.5 | 277 | .887 | .917 | 10.5 |
| −14 / −13.5 | 226 | .904 | .898 | 10.5 |

  (The implied-σ column pools home and away favorites at that |spread|; the other columns are home-favorite only.) Maximum-likelihood probit σ for the outright result given the closing spread: **11.6** (computed).

### Inferences
- The falling implied σ matches the excess kurtosis in Section 3. The residual distribution is peaked, so outright win probability rises faster with the spread than a σ ≈ 12.6 normal predicts. Large favorites win more often than Φ(s/12.6) suggests; at −13 the empirical rate was 91.7% against a normal 84.4%. A professional should convert spreads to moneylines with an empirical or market-calibrated table (or a fatter-tailed or mixture model), not a single σ.
- The empirical SU column is noisy (SE ≈ 1.5–3 points per row), and the market no-vig column is the smoother estimate.

### Gaps
- No public, current Pinnacle NBA spread→ML conversion table was retrievable. Unabated/Pinnacle articles were blocked.

---

## 5. Spread–total correlation (same-game parlays) and how the total affects margin variance

### Takeaway
For full-game NBA sides and totals the outcome correlation is essentially zero: correlation(favorite covers, over) = −0.014, and P(favorite & over) = 24.5% against 24.8% if independent. A favorite-plus-over parlay has no exploitable positive correlation. The total does change variance: the margin-vs-spread SD rises from about 12.1 at totals near 190–210 to 14.1 at 230+.

### Cited Findings (computed from the [Dataset](https://raw.githubusercontent.com/flancast90/sportsbookreview-scraper/main/data/nba_archive_10Y.json))
- Excluding pushes, n = 12,440: favorites covered 50.0%, overs hit 49.7%, corr(fav cover, over) = **−0.014**. P(fav cover & over) = 0.245 vs 0.248 independent; P(dog cover & under) = 0.248 vs 0.252.
- Big favorites (|spread| ≥ 10, n = 2,214): corr = −0.033, P(fav & over) = 0.239 vs 0.247 independent. Small spreads (≤ 3): corr −0.014.
- Continuous residuals: corr(favorite margin − spread, points − total) = **−0.005**.
- Total residual (points − closing total): mean +0.32, SD **17.92**.
- Margin residual SD by closing total: 180s 12.24 → 190s 12.08 → 200s 12.14 → 210s 12.78 → 220s 13.16 → 230s 14.11.

### Inferences
- At the full-game level, a same-game parlay of an NBA favorite and the over is priced near fairly by a book that assumes independence (and books usually price SGPs with extra margin). There is no structural edge like the one in NFL favorite+under or underdog+under spots (inference; not tested for NFL here).
- Correlations may exist in sub-markets not tested here: first-half lines, player props with team totals, and large-spread blowouts with bench minutes. The slight negative correlation for big favorites (−0.033) fits the idea that a blowout's garbage time can lower scoring, but it is small and not significant at n = 2,214 (SE ≈ 0.021).
- Variance scales with game pace: σ_margin ≈ 0.058–0.060 × total in this sample (12.2/205 ≈ 0.059; 14.1/235 ≈ 0.060). That is consistent with a Brownian/possession model where variance grows with the number of possessions. For high totals, use a larger σ when converting spread to moneyline, which helps the underdog's outright chance (inference).

### Gaps
- No academic source was found quantifying NBA spread/total correlation. Results are only from this dataset and use closing (not opening) lines.

---

## 6. Kelly criterion, fractional Kelly, simultaneous bets, risk of ruin, estimate uncertainty

### Takeaway
At −110 with true win rate p, full Kelly stakes f* = (bp − q)/b with b = 0.9091: 1.3% of bankroll at 53%, 3.4% at 54%, 5.5% at 55%. Half Kelly keeps 75% of the growth rate. It cuts the chance of ever halving the bankroll from 50% to 12.5% and raises P(double before halve) from 67% to 89%. Betting 2× Kelly gives zero growth. Because p is estimated with error, professionals bet 1/4 to 1/2 Kelly.

### Cited Findings
- Kelly (1956), "A New Interpretation of Information Rate," *Bell System Technical Journal* 35(4):917–926. The bibliographic details are from memory and the paper was not fetched.
- MacLean, Thorp & Ziemba (2010), "Long-term capital growth: the good and bad properties of the Kelly and fractional Kelly capital growth criteria," *Quantitative Finance* 10(7). Good: maximizing E[log X] asymptotically maximizes the growth rate. Bad: Kelly "can be very volatile," with extremely large bets in short-term favorable situations. Their figure (blackjack, 2% edge, from MacLean & Ziemba 1999) shows P(double before halve) ≈ 0.67 at full Kelly — [IDEAS/RePEc chapter](https://ideas.repec.org/h/wsi/wschap/9789814293501_0039.html); [Good/Bad Kelly PDF (Berkeley)](https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf) (content via search summary; the PDF host was blocked). This book chapter is in MacLean, Thorp & Ziemba (eds.), *The Kelly Capital Growth Investment Criterion* (World Scientific, 2011), the same ISBN series 9789814293501 — [RePEc](https://econpapers.repec.org/RePEc:wsi:wschap:9789814293501_0030).
- **Formulas (standard; computed):**
  - Kelly for a binary bet at net odds b: f* = (bp − q)/b = p − q/b. Growth per bet: G(f) = p·ln(1+bf) + q·ln(1−f).
  - Continuous (Brownian) approximation with fraction c of Kelly. Relative growth = c(2 − c), so 0.5 → 0.75 and 2 → 0. P(ever falling to fraction x of the starting bankroll) = x^(2/c − 1). P(double before halve) = 1/(1 + 2^(−(2−c)/c)). At c = 1 this gives 0.667, matching MacLean–Thorp–Ziemba's 0.67, which is a check on the formula.

| Kelly fraction c | Growth vs full | P(double before halve) | P(ever down 50%) | P(ever down 75%) |
|---|---|---|---|---|
| 0.25 | 0.44 | 0.992 | 0.8% | 0.01% |
| 0.50 | 0.75 | 0.889 | 12.5% | 1.6% |
| 0.75 | 0.94 | 0.760 | 31.5% | 9.9% |
| 1.00 | 1.00 | 0.667 | 50.0% | 25.0% |
| 1.50 | 0.75 | 0.558 | 79.4% | 63.0% |
| 2.00 | 0.00 | 0.500 | 100% | 100% |

  - **Stakes and edge at −110 / −105 (computed):**

| True p | Price | EV per $1 | Full Kelly | Log growth/bet (full) |
|---|---|---|---|---|
| 0.53 | −110 | +1.18% | 1.30% | 0.000077 |
| 0.54 | −110 | +3.09% | 3.40% | 0.000526 |
| 0.55 | −110 | +5.00% | 5.50% | 0.001378 |
| 0.56 | −110 | +6.91% | 7.60% | 0.002634 |
| 0.58 | −110 | +10.73% | 11.80% | 0.006365 |
| 0.53 | −105 | +3.48% | 3.65% | 0.000635 |
| 0.55 | −105 | +7.38% | 7.75% | 0.002866 |

  At 55%, moving from −110 to −105 roughly doubles log growth (0.00138 → 0.00287).
- **Estimate uncertainty (inference from the formulas):** growth falls to zero at 2× Kelly. If your estimated p of 0.55 is really 0.5375, true full Kelly is 2.75%. Betting 5.5% is then 2× Kelly, which means zero growth. That asymmetry is why fractional Kelly is standard.
- **Simultaneous bets (inference / standard result):** the Kelly fractions for independent simultaneous bets should be solved jointly (maximize E[log] over all outcomes). For small edges the joint solution is close to the individual f*, slightly reduced. For correlated bets (e.g., the same side at several books, or a side plus a correlated prop), treat them as one position. A practical rule is to cap total exposure on one slate.

### Gaps
- I could not open Thorp's papers (e.g., "The Kelly criterion in blackjack, sports betting and the stock market," 1997/2006) to quote his sports examples. The simultaneous-Kelly worked solution is not sourced.

---

## 7. Expected value, variance over N bets, and sample size to separate skill from luck

### Takeaway
At −110 the win-rate standard error is about 50%/√N: ±3.2 points at 250 bets, ±1.6 at 1,000. A true 55% bettor needs about **1,400 bets** to expect to show significance at the 5% level (two-sided z = 1.96) against 52.38%. A true 54% bettor needs about 3,700, and a true 53% bettor about 25,000. A 50% (no-skill) bettor hits ≥55% over 250 bets 5.7% of the time.

### Cited Findings (computed; standard binomial math)
- Per-bet outcome at −110 risking 1: win +0.9091 with probability p, lose −1 with probability q. Per-bet SD ≈ 0.95 units. Over N bets: E = N·(1.9091p − 1), SD ≈ 0.95√N units.

| True p | N | Win% SD | E[units] | SD units | P(net loss) |
|---|---|---|---|---|---|
| 0.53 | 1,000 | 1.6% | +11.8 | 30.1 | 34.7% |
| 0.53 | 5,000 | 0.7% | +59.1 | 67.4 | 19.0% |
| 0.54 | 500 | 2.2% | +15.5 | 21.3 | 23.4% |
| 0.54 | 1,000 | 1.6% | +30.9 | 30.1 | 15.2% |
| 0.54 | 2,500 | 1.0% | +77.3 | 47.6 | 5.2% |
| 0.55 | 250 | 3.1% | +12.5 | 15.0 | 20.3% |
| 0.55 | 500 | 2.2% | +25.0 | 21.2 | 12.0% |
| 0.55 | 1,000 | 1.6% | +50.0 | 30.0 | 4.8% |
| 0.55 | 2,500 | 1.0% | +125.0 | 47.5 | 0.4% |

- N for the expected z-statistic against 52.38% to reach the threshold: N = (z·√(0.5238·0.4762)/(p − 0.5238))².

| True p | z = 1.645 | z = 1.96 | z = 2.576 |
|---|---|---|---|
| 0.53 | 17,615 | 25,007 | 43,195 |
| 0.54 | 2,576 | 3,656 | 6,315 |
| 0.55 | 985 | 1,397 | 2,414 |

  This is the N at which the *expected* result crosses the threshold, so roughly 50% power. 80% power needs about 2× as many bets.
- Luck: P(a 50% bettor shows ≥55%) = 15.9% at N=100, 5.7% at 250, 1.3% at 500, 0.08% at 1,000.
- A secondary summary of Buchdahl's view: thousands of bets to prove skill from results, versus far fewer using CLV — [secondary summary](https://pod-d614f9k2t-pod-team.vercel.app/blog/closing-line-value--clv-demystified-by-expert-joseph-buchdahl). This is consistent with the numbers above.

### Inferences
- A typical NBA season offers about 1,230 games. Even a strong 55% bettor who bets every game would be only about 2σ above break-even after a full season. Results-based evaluation is slow, so CLV (lower variance per bet; Section 2) is the practical skill metric.
- Multiple-testing caution: among many touts, some will show 55%+ over hundreds of picks by chance alone.

### Gaps
- There is no sourced formula for the variance of CLV per bet in the NBA. It could be estimated from the archive's open→close movement (SD of line moves), but this was not done.

---

## 8. Teasers, alternate spreads, buying points in the NBA — ever +EV?

### Takeaway
Basic NBA 6-point teaser legs won **70.35%** in 2011-22. Break-even is 72.37% for a 2-team at −110 and 72.72% for a 3-team at +160. Teasers are −EV on average, and no segment cleared break-even by a significant margin. The Wong-teaser logic (teasing through 3 and 7) does not carry over to the NBA, which lacks key numbers. Buying a half-point onto a number for 10 cents (−110 → −120) pays only if the landing probability exceeds **3.6%**. NBA landing rates are 3.3–4.6% near 3 and 5–7 and lower elsewhere, so buying is roughly break-even at best and only at 6–7.

### Cited Findings (computed from the [Dataset](https://raw.githubusercontent.com/flancast90/sportsbookreview-scraper/main/data/nba_archive_10Y.json); pushes excluded)
- Teaser break-even per leg = (1/D)^(1/legs): 2-team −110: **72.37%**; 2-team −120: 73.85%; 3-team +160: 72.72%; 3-team +140: 74.69%; 4-team +250: 73.11%.
- Leg win rates, all sides (n = 25,680 legs): 4-point 64.49%, **6-point 70.35%**, 7-point 73.14%. 7-point teasers usually carry worse payouts, which were not available.
- 6-point leg win rate by segment:

| Segment (closing line) | Legs | Win% |
|---|---|---|
| Fav −1 to −3 → +5 to +3 | 2,583 | 65.4% |
| Fav −3.5 to −6 | 4,198 | 66.2% |
| Fav −6.5 to −9 | 3,293 | 72.4% |
| Fav −9.5 or more | 2,608 | 71.4% |
| Dog +1 to +3 | 2,597 | 70.7% |
| Dog +3.5 to +6 | 4,177 | 72.9% |
| Dog +6.5 to +9 | 3,279 | 71.8% |
| Dog +9.5 or more | 2,627 | 71.9% |

  Every segment is at or below the 72.4% break-even, within about 1 SE (≈0.7 points) for the best ones.
- The NFL basis for Wong teasers is 3 and 7 being the dominant margins (15% and 9% of games) — [DeucesCracked](https://www.deucescracked.com/blog/nfl-margin-of-victory-data-1999-2025). In the NBA no margin exceeds 6.5% of games (computed; Section 3). Stanford Wong's *Sharp Sports Betting* is the usual citation for Wong teasers; not fetched or verified here.
- **Buying points (computed, assuming the −k line is fair).** Comparing −k.5 at −110 with −k at a higher price, buying pays when the landing probability h exceeds 1.9% for −115, **3.6% for −120**, and 5.2% for −125. NBA landing probability near the number is 2.4% (k=1), 3.1% (2), 3.8% (3), 3.3% (4), 3.9% (5), 4.3% (6), **4.6% (7)**, 4.2% (8), 3.7% (9). So:
  - Buying on or off 7 or 6 for 10 cents is marginally +EV relative to not buying, but both bets are −EV unless you have an edge.
  - Buying for 5 cents (−115) is worthwhile at almost every NBA number.
  - Buying for 15 cents (−125) is never worthwhile in the NBA.
  - In the NFL (h ≈ 9% at 3), buying onto or off 3 for 10–20 cents can be justified (inference from the NFL rates above).
- **Alternate spreads:** price them with the empirical residual distribution. The cover probability at alternate line L is P(residual > L − closing spread), using the fat-tailed empirical CDF rather than Φ with σ = 12.6. The peaked distribution means alternates near the closing number are worth slightly more per point than a normal implies, and distant alternates slightly less until the tails (inference from the kurtosis finding).

### Inferences
- NBA teasers are −EV structurally: teaser prices are set for a margin density the NBA doesn't have. Only a bettor with a real side edge or stale-line advantage (e.g., teasing an opener that will move) could make them +EV.
- If buying at all, buy half-points only at about 5 cents per half-point, or at 10 cents only onto or through 6 and 7.

### Gaps
- Teaser analysis uses closing lines at assumed −110 and pooled 2011-22 data. It does not cover 2022+ scoring or a book's actual teaser and alternate-line prices, which could not be retrieved.
- No academic study of NBA teasers was found.
