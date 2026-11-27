# NBA spread model backtest

Archive: 12,960 games, seasons 2011-22; 12,932 (99.8%) matched to play-by-play player data. Ratings and injury weights tuned on 2011-14; walk-forward test on 8,788 games from 2014-22. All bets assumed at -110 (break-even 52.38%).

**Look-ahead caveat:** absences are read from each game's box score. Tests against the closing line are fair because injury news is almost always out before the close. Tests against the opening line assume you knew every absence at the open, so treat them as an upper bound.

Tuned rating parameters: {'k_perf': 0.045, 'carry': 0.8, 'k_mkt': 0.2}

Injury weights (points of home margin per unit, away minus home): -0.074 per missing rotation minute, +0.311 per missing Game Score point

## Forecast accuracy (mean absolute error of home margin, test seasons)

| Forecast | MAE (points) |
|---|---|
| closing line | 9.76 |
| opening line | 9.85 |
| Stats only (no injuries) | 9.98 |
| Stats + opening line (no injuries) | 9.85 |
| Stats + injuries | 9.92 |
| Stats + injuries + opening line | 9.84 |

## Is injury news priced?

| Outcome regressed on injury points | Slope | t |
|---|---|---|
| Actual home margin | 0.84 | 11.9 |
| Opening line (home expected margin) | 0.53 | 16.1 |
| Line move, open to close (toward home) | 0.31 | 44.6 |
| Cover margin vs closing line | -0.00 | -0.0 |

## Stats only (no injuries)

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

## Stats + opening line (no injuries)

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

## Stats + injuries

| Bet against | Min edge | Bets | W-L-P | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) | Win % at close |
|---|---|---|---|---|---|---|---|---|---|
| open line | 1 | 5274 | 2686-2497-91 | 51.8% | -55.2 | -1.0% | -0.80 | +0.76 | 49.1% |
| open line | 2 | 2765 | 1441-1282-42 | 52.9% | +28.0 | +1.0% | +0.56 | +1.10 | 49.3% |
| open line | 3 | 1329 | 702-606-21 | 53.7% | +32.2 | +2.4% | +0.93 | +1.49 | 48.7% |
| open line | 4 | 578 | 321-247-10 | 56.5% | +44.8 | +7.8% | +1.97 | +2.03 | 49.9% |
| open line | 5 | 264 | 148-110-6 | 57.4% | +24.5 | +9.3% | +1.60 | +2.66 | 46.7% |
| close line | 1 | 5157 | 2534-2526-97 | 50.1% | -222.4 | -4.3% | -3.28 | — | — |
| close line | 2 | 2543 | 1213-1281-49 | 48.6% | -178.3 | -7.0% | -3.74 | — | — |
| close line | 3 | 1053 | 487-549-17 | 47.0% | -106.3 | -10.1% | -3.46 | — | — |
| close line | 4 | 414 | 193-213-8 | 47.5% | -37.5 | -9.1% | -1.95 | — | — |
| close line | 5 | 170 | 72-93-5 | 43.6% | -27.5 | -16.2% | -2.25 | — | — |

## Stats + injuries + opening line

| Bet against | Min edge | Bets | W-L-P | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) | Win % at close |
|---|---|---|---|---|---|---|---|---|---|
| open line | 1 | 2980 | 1545-1383-52 | 52.8% | +21.5 | +0.7% | +0.42 | +1.19 | 48.9% |
| open line | 2 | 714 | 406-291-17 | 58.2% | +78.1 | +10.9% | +3.10 | +2.18 | 50.2% |
| open line | 3 | 151 | 86-62-3 | 58.1% | +16.2 | +10.7% | +1.40 | +3.57 | 42.3% |
| open line | 4 | 43 | 30-11-2 | 73.2% | +16.3 | +37.8% | +2.67 | +4.26 | 45.2% |
| open line | 5 | 13 | 10-3-0 | 76.9% | +6.1 | +46.9% | +1.77 | +5.50 | 50.0% |
| close line | 1 | 3748 | 1802-1871-75 | 49.1% | -232.8 | -6.2% | -4.03 | — | — |
| close line | 2 | 1124 | 535-568-21 | 48.5% | -81.6 | -7.3% | -2.58 | — | — |
| close line | 3 | 281 | 131-145-5 | 47.5% | -25.9 | -9.2% | -1.64 | — | — |
| close line | 4 | 77 | 37-38-2 | 49.3% | -4.4 | -5.7% | -0.53 | — | — |
| close line | 5 | 24 | 14-9-1 | 60.9% | +3.7 | +15.5% | +0.82 | — | — |

## By season: stats + injuries vs closing line, edge ≥ 2

| Season | Bets | Win % | Units |
|---|---|---|---|
| 2014-15 | 346 | 48.8% | -23.0 |
| 2015-16 | 282 | 52.9% | +2.6 |
| 2016-17 | 272 | 52.4% | +0.3 |
| 2017-18 | 296 | 44.3% | -44.5 |
| 2018-19 | 308 | 46.7% | -33.0 |
| 2019-20 | 302 | 48.5% | -22.0 |
| 2020-21 | 409 | 48.5% | -29.8 |
| 2021-22 | 328 | 47.6% | -28.8 |

## Does the line already price the situation?

Regression of the cover margin (home margin + home spread) on situational features, test seasons. A coefficient near 0 means the line already accounts for that factor.

| Feature | vs opening line (pts) | t | vs closing line (pts) | t |
|---|---|---|---|---|
| home edge | -0.13 | -0.80 | -0.08 | -0.47 |
| home on back-to-back | -0.30 | -0.61 | +0.09 | +0.19 |
| away on back-to-back | +0.02 | +0.06 | -0.43 | -1.04 |
| rest difference (days) | +0.18 | +1.09 | +0.16 | +0.93 |
| altitude home | +0.91 | +1.72 | +0.71 | +1.34 |
| injury points (model's absence value) | +0.31 | +4.80 | -0.00 | -0.02 |

Classic angles, graded at the closing line:

| Angle | Record |
|---|---|
| Rested home team vs away team on a back-to-back | 726-757 (49.0%) |
| Rested away team vs home team on a back-to-back | 329-335 (49.5%) |
| Home underdog of 10+ points | 142-160 (47.0%) |
| Road favorite | 1462-1396 (51.2%) |
| Team missing 4+ points more of players than opponent (bet the healthier side) | 176-197 (47.2%) home / 139-129 (51.9%) away |

## Regression coefficients by test season

**Stats only (no injuries)**: intercept, perf_diff, mkt_diff, b2b_home, b2b_away, rest_diff, altitude

| Season | Coefficients |
|---|---|
| 2014 | [2.381, 0.268, 0.769, -1.164, 2.113, -0.049, 0.941] |
| 2015 | [2.503, 0.173, 0.847, -1.204, 1.298, 0.077, 1.097] |
| 2016 | [2.621, 0.17, 0.849, -1.166, 1.126, 0.173, 1.047] |
| 2017 | [2.648, 0.12, 0.878, -1.361, 1.262, 0.156, 0.857] |
| 2018 | [2.526, 0.121, 0.869, -1.163, 1.335, 0.128, 1.083] |
| 2019 | [2.534, 0.118, 0.873, -1.165, 1.342, 0.146, 1.29] |
| 2020 | [2.437, 0.124, 0.866, -1.282, 1.648, 0.082, 0.996] |
| 2021 | [2.308, 0.103, 0.891, -1.175, 1.582, 0.141, 1.23] |

**Stats + opening line (no injuries)**: intercept, perf_diff, mkt_diff, b2b_home, b2b_away, rest_diff, altitude, open_line

| Season | Coefficients |
|---|---|
| 2014 | [0.337, 0.092, 0.262, -0.566, 1.471, -0.053, 0.581, 0.686] |
| 2015 | [0.429, -0.014, 0.318, -0.564, 0.619, 0.076, 0.652, 0.715] |
| 2016 | [0.659, -0.01, 0.338, -0.538, 0.471, 0.155, 0.749, 0.692] |
| 2017 | [0.642, -0.072, 0.363, -0.657, 0.568, 0.144, 0.594, 0.708] |
| 2018 | [0.415, -0.075, 0.304, -0.394, 0.56, 0.116, 0.858, 0.761] |
| 2019 | [0.483, -0.075, 0.315, -0.39, 0.547, 0.129, 1.08, 0.749] |
| 2020 | [0.488, -0.059, 0.315, -0.498, 0.796, 0.067, 0.809, 0.735] |
| 2021 | [0.391, -0.08, 0.323, -0.331, 0.699, 0.124, 1.062, 0.752] |

**Stats + injuries**: intercept, perf_diff, mkt_diff, b2b_home, b2b_away, rest_diff, altitude, inj_pts

| Season | Coefficients |
|---|---|
| 2014 | [2.345, 0.292, 0.753, -1.266, 2.089, -0.114, 1.025, 1.005] |
| 2015 | [2.428, 0.194, 0.832, -1.202, 1.272, 0.016, 1.19, 1.014] |
| 2016 | [2.544, 0.192, 0.831, -1.116, 1.063, 0.11, 1.099, 1.001] |
| 2017 | [2.541, 0.15, 0.854, -1.278, 1.182, 0.117, 0.946, 1.022] |
| 2018 | [2.42, 0.149, 0.845, -1.106, 1.26, 0.088, 1.158, 0.991] |
| 2019 | [2.433, 0.147, 0.848, -1.106, 1.247, 0.103, 1.357, 0.987] |
| 2020 | [2.347, 0.138, 0.855, -1.195, 1.537, 0.047, 1.025, 0.903] |
| 2021 | [2.226, 0.115, 0.881, -1.055, 1.418, 0.112, 1.269, 0.899] |

**Stats + injuries + opening line**: intercept, perf_diff, mkt_diff, b2b_home, b2b_away, rest_diff, altitude, inj_pts, open_line

| Season | Coefficients |
|---|---|
| 2014 | [0.769, 0.157, 0.357, -0.758, 1.603, -0.092, 0.712, 0.613, 0.533] |
| 2015 | [0.809, 0.047, 0.409, -0.687, 0.739, 0.042, 0.785, 0.593, 0.569] |
| 2016 | [1.035, 0.051, 0.43, -0.641, 0.571, 0.121, 0.837, 0.6, 0.544] |
| 2017 | [1.073, 0.007, 0.466, -0.777, 0.685, 0.122, 0.721, 0.652, 0.532] |
| 2018 | [0.794, -0.003, 0.396, -0.521, 0.676, 0.095, 0.949, 0.573, 0.602] |
| 2019 | [0.875, -0.001, 0.411, -0.521, 0.658, 0.109, 1.157, 0.6, 0.585] |
| 2020 | [0.817, -0.003, 0.405, -0.599, 0.895, 0.051, 0.847, 0.507, 0.593] |
| 2021 | [0.688, -0.032, 0.41, -0.414, 0.762, 0.112, 1.097, 0.497, 0.619] |

