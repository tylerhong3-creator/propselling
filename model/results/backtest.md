# NBA spread model backtest

Archive: 12,960 games, seasons 2011-22. Ratings tuned and regression first trained on 2011-14; walk-forward test on 8,788 games from 2014-22. All bets assumed at -110 (break-even 52.38%).

Tuned rating parameters: {'k_perf': 0.045, 'carry': 0.8, 'k_mkt': 0.2}

## Forecast accuracy (mean absolute error of home margin, test seasons)

| Forecast | MAE (points) |
|---|---|
| closing line | 9.76 |
| opening line | 9.85 |
| stats model | 9.98 |
| blend model | 9.85 |

## Stats-only model

| Bet against | Min edge | Bets | W-L-P | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) | Win % at close |
|---|---|---|---|---|---|---|---|---|---|
| open line | 1 | 5206 | 2632-2484-90 | 51.4% | -91.3 | -1.8% | -1.34 | +0.17 | 50.9% |
| open line | 2 | 2562 | 1252-1264-46 | 49.8% | -125.8 | -4.9% | -2.63 | +0.23 | 48.8% |
| open line | 3 | 1237 | 621-592-24 | 51.2% | -27.5 | -2.2% | -0.83 | +0.29 | 50.2% |
| open line | 4 | 604 | 302-291-11 | 50.9% | -16.5 | -2.7% | -0.71 | +0.32 | 50.5% |
| open line | 5 | 315 | 158-151-6 | 51.1% | -7.4 | -2.3% | -0.44 | +0.31 | 50.2% |
| close line | 1 | 5717 | 2827-2785-105 | 50.4% | -215.0 | -3.8% | -3.01 | — | — |
| close line | 2 | 3313 | 1630-1619-64 | 50.2% | -137.2 | -4.1% | -2.52 | — | — |
| close line | 3 | 1800 | 877-886-37 | 49.7% | -88.7 | -4.9% | -2.22 | — | — |
| close line | 4 | 956 | 464-474-18 | 49.5% | -52.2 | -5.5% | -1.79 | — | — |
| close line | 5 | 478 | 241-230-7 | 51.2% | -10.9 | -2.3% | -0.53 | — | — |

## Blend model (stats + opening line)

| Bet against | Min edge | Bets | W-L-P | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) | Win % at close |
|---|---|---|---|---|---|---|---|---|---|
| open line | 1 | 1403 | 707-671-25 | 51.3% | -28.3 | -2.0% | -0.80 | +0.40 | 49.3% |
| open line | 2 | 132 | 67-64-1 | 51.1% | -3.1 | -2.3% | -0.28 | +0.64 | 48.5% |
| open line | 3 | 19 | 11-8-0 | 57.9% | +2.0 | +10.5% | +0.48 | +2.53 | 52.6% |
| open line | 4 | 1 | 1-0-0 | 100.0% | +0.9 | +90.9% | +0.95 | +9.00 | 0.0% |
| open line | 5 | 1 | 1-0-0 | 100.0% | +0.9 | +90.9% | +0.95 | +9.00 | 0.0% |
| close line | 1 | 4156 | 2059-2014-83 | 50.6% | -142.2 | -3.4% | -2.34 | — | — |
| close line | 2 | 1572 | 758-782-32 | 49.2% | -92.9 | -5.9% | -2.48 | — | — |
| close line | 3 | 575 | 274-292-9 | 48.4% | -42.9 | -7.5% | -1.89 | — | — |
| close line | 4 | 234 | 108-123-3 | 46.8% | -24.8 | -10.6% | -1.71 | — | — |
| close line | 5 | 86 | 43-41-2 | 51.2% | -1.9 | -2.2% | -0.22 | — | — |

## By season: blend model vs opening line, edge ≥ 2

| Season | Bets | Win % | Units | Avg CLV |
|---|---|---|---|---|
| 2014-15 | 31 | 46.7% | -3.3 | -0.31 |
| 2015-16 | 12 | 66.7% | +3.3 | +1.21 |
| 2016-17 | 15 | 53.3% | +0.3 | +0.07 |
| 2017-18 | 11 | 36.4% | -3.4 | +0.41 |
| 2018-19 | 3 | 33.3% | -1.1 | -0.83 |
| 2019-20 | 21 | 57.1% | +1.9 | +1.14 |
| 2020-21 | 16 | 62.5% | +3.1 | +1.31 |
| 2021-22 | 23 | 43.5% | -3.9 | +1.35 |

## Does the line already price the situation?

Regression of the cover margin (home margin + home spread) on situational features, all games with at least 5 games played by each team (2011-22). A coefficient near 0 means the line already accounts for that factor.

| Feature | vs opening line (pts) | t | vs closing line (pts) | t |
|---|---|---|---|---|
| home edge | -0.22 | -1.62 | -0.19 | -1.39 |
| home on back-to-back | -0.33 | -0.81 | +0.14 | +0.35 |
| away on back-to-back | +0.41 | +1.20 | -0.11 | -0.32 |
| rest difference (days) | +0.12 | +0.86 | +0.10 | +0.67 |
| altitude home | +0.83 | +1.84 | +0.61 | +1.35 |

Classic angles, graded at the closing line:

| Angle | Record |
|---|---|
| Rested home team vs away team on a back-to-back | 1074-1123 (48.9%) |
| Rested away team vs home team on a back-to-back | 460-445 (50.8%) |
| Home underdog of 10+ points | 167-186 (47.3%) |
| Road favorite | 1951-1854 (51.3%) |

## Regression coefficients by test season

Columns: intercept (home edge), perf_diff, mkt_diff, b2b_home, b2b_away, rest_diff, altitude, open_line

| Season | Stats model | Blend model |
|---|---|---|
| 2014 | [2.381, 0.268, 0.769, -1.164, 2.113, -0.049, 0.941] | [0.337, 0.092, 0.262, -0.566, 1.471, -0.053, 0.581, 0.686] |
| 2015 | [2.503, 0.173, 0.847, -1.204, 1.298, 0.077, 1.097] | [0.429, -0.014, 0.318, -0.564, 0.619, 0.076, 0.652, 0.715] |
| 2016 | [2.621, 0.17, 0.849, -1.166, 1.126, 0.173, 1.047] | [0.659, -0.01, 0.338, -0.538, 0.471, 0.155, 0.749, 0.692] |
| 2017 | [2.648, 0.12, 0.878, -1.361, 1.262, 0.156, 0.857] | [0.642, -0.072, 0.363, -0.657, 0.568, 0.144, 0.594, 0.708] |
| 2018 | [2.526, 0.121, 0.869, -1.163, 1.335, 0.128, 1.083] | [0.415, -0.075, 0.304, -0.394, 0.56, 0.116, 0.858, 0.761] |
| 2019 | [2.534, 0.118, 0.873, -1.165, 1.342, 0.146, 1.29] | [0.483, -0.075, 0.315, -0.39, 0.547, 0.129, 1.08, 0.749] |
| 2020 | [2.437, 0.124, 0.866, -1.282, 1.648, 0.082, 0.996] | [0.488, -0.059, 0.315, -0.498, 0.796, 0.067, 0.809, 0.735] |
| 2021 | [2.308, 0.103, 0.891, -1.175, 1.582, 0.141, 1.23] | [0.391, -0.08, 0.323, -0.331, 0.699, 0.124, 1.062, 0.752] |
