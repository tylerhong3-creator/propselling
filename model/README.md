# NBA spread model

A walk-forward point-spread model built on 12,960 NBA games with opening and closing lines (2011-12 to 2021-22, SportsbookReviewsOnline archive). It only needs Python 3 and numpy.

```bash
python3 model/nba_model.py backtest
```

```bash
python3 model/nba_model.py predict model/example_games.csv
```

`backtest` rebuilds everything from `data/nba_archive.json` and writes `results/backtest.md` (full tables) and `results/bets_blend_open_edge2.csv` (every bet the main configuration would have placed).

## How it works

Every input is something you would know before tip-off.

1. **Two team ratings on a points scale**, updated after each game:
   - a *performance* rating from actual margins (capped at ±25);
   - a *market* rating from each past game's closing spread, i.e. how the market rated the team.

   Both shrink 20% toward average between seasons. Update speeds are tuned on 2011-14 only.
2. **Schedule features** from the game dates: back-to-backs, rest difference, and an altitude flag for Denver and Utah at home.
3. **Linear regression** to the home margin, refit walk-forward: each test season uses only earlier seasons. There are two versions:
   - **Stats:** ratings + schedule.
   - **Blend:** stats + the opening line.
4. **Bets.** When the predicted margin beats the line by the edge threshold, bet that side at −110. Bets are graded against the opening line, which is the realistic early number, and against the closing line.

## What the backtest shows (2014-15 to 2021-22, 8,788 test games)

**The model does not beat the vig.** That matches the research report (`reports/NBA spread betting expertise.md`).

| Forecast | Mean absolute error |
|---|---|
| Closing line | **9.76** |
| Opening line | 9.85 |
| Blend model | 9.85 |
| Stats model | 9.98 |

| Configuration | Bets | Win % | ROI |
|---|---|---|---|
| Stats model vs opening line, edge ≥ 1 | 5,206 | 51.4% | −1.8% |
| Stats model vs closing line, edge ≥ 2 | 3,313 | 50.2% | −4.1% |
| Blend model vs opening line, edge ≥ 1 | 1,403 | 51.3% | −2.0% |
| Blend model vs closing line, edge ≥ 2 | 1,572 | 49.2% | −5.9% |

Break-even at −110 is 52.38%.

**The model does have one real skill: it predicts which way the line will move.**
- Bets placed at the opening line got positive closing line value: +0.2 to +0.3 points for the stats model, and +0.4 to +0.6 for the blend.
- That is roughly half a point to a point short of what −110 pricing requires.
- At reduced juice (−105, break-even 51.2%), the stats model at edge ≥ 1 (51.4%) would be about break-even.

**Closing lines already price the situation.**
- Back-to-backs and rest have essentially zero effect on covering at the close (all |t| < 1).
- Altitude is the largest leftover at about +0.6 points, but it is not significant.
- Classic angles lose at the close:

| Angle | Win % at close |
|---|---|
| Rested home team vs away team on a back-to-back | 48.9% |
| Home underdog of 10+ points | 47.3% (the old Paul & Weinbach anomaly is gone) |

## Limits

- **No spread prices in the archive.** Every bet is assumed at −110. Real prices vary, and shopping for −105 changes the conclusions more than any feature here.
- **No injury or lineup data.** Most of the market's information edge comes from late injury news, so it is the missing input most likely to matter.
- **Data ends June 2022.** To predict today's games, append the newer results to a JSON file in the archive's format and pass it as the third argument:

  ```bash
  python3 model/nba_model.py predict games.csv newer_results.json
  ```

  Without that, ratings are frozen at the end of 2021-22 and the output is stale.
- `example_games.csv` uses made-up lines to show the input format only.

Treat any pick from this model as a lean, not an edge, unless you track its closing line value live and it holds up over hundreds of bets.
