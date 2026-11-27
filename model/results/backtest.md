# NBA spread model backtest

Archive: 18,510 games, seasons 2011-27; 18,478 (99.8%) matched to play-by-play player data. Ratings and injury weights tuned on 2011-14; walk-forward test on 13,943 games from 2014-27. All bets assumed at -110 (break-even 52.38%).

**Look-ahead caveat:** absences are read from each game's box score. Tests against the closing line are fair because injury news is almost always out before the close. Tests against the opening line assume you knew every absence at the open, so treat them as an upper bound.

Tuned rating parameters: {'k_perf': 0.045, 'carry': 0.8, 'k_mkt': 0.2}

Injury weights (points of home margin per unit, away minus home): -0.074 per missing rotation minute, +0.311 per missing Game Score point

## Forecast accuracy (mean absolute error of home margin, test seasons)

| Forecast | MAE (points) |
|---|---|
| closing line | 10.06 |
| opening line | 10.17 |
| Stats only (no injuries) | 10.29 |
| Stats + opening line (no injuries) | 10.17 |
| Stats + injuries | 10.22 |
| Stats + injuries + opening line | 10.15 |

## DraftKings era: 2022-23 to 2026-27, graded at actual DraftKings prices

Out-of-sample seasons not used in any earlier version of this model. Opening-line rows use only games where ESPN recorded a DraftKings opener.

| Model | Bet against | Min edge | Bets | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) |
|---|---|---|---|---|---|---|---|---|
| Stats only (no injuries) | open | 1 | 2548 | 51.9% | -50.3 | -2.0% | -0.51 | +0.63 |
| Stats only (no injuries) | open | 2 | 1487 | 52.9% | -13.7 | -0.9% | +0.38 | +0.95 |
| Stats only (no injuries) | open | 3 | 789 | 52.3% | -27.0 | -3.4% | -0.05 | +1.37 |
| Stats only (no injuries) | close | 1 | 3583 | 49.4% | -201.7 | -5.6% | -3.51 | — |
| Stats only (no injuries) | close | 2 | 2287 | 49.6% | -119.9 | -5.2% | -2.61 | — |
| Stats only (no injuries) | close | 3 | 1391 | 50.3% | -57.3 | -4.1% | -1.58 | — |
| Stats + opening line (no injuries) | open | 1 | 689 | 54.3% | +1.3 | +0.2% | +1.00 | +1.44 |
| Stats + opening line (no injuries) | open | 2 | 100 | 59.0% | -1.2 | -1.2% | +1.33 | +4.57 |
| Stats + opening line (no injuries) | open | 3 | 19 | 68.4% | +1.6 | +8.6% | +1.40 | +10.66 |
| Stats + opening line (no injuries) | close | 1 | 2422 | 49.8% | -123.2 | -5.1% | -2.54 | — |
| Stats + opening line (no injuries) | close | 2 | 1097 | 48.8% | -75.8 | -6.9% | -2.36 | — |
| Stats + opening line (no injuries) | close | 3 | 584 | 50.3% | -24.4 | -4.2% | -1.03 | — |
| Stats + injuries | open | 1 | 2617 | 54.1% | +59.8 | +2.3% | +1.77 | +1.50 |
| Stats + injuries | open | 2 | 1632 | 55.4% | +66.7 | +4.1% | +2.46 | +2.03 |
| Stats + injuries | open | 3 | 933 | 55.9% | +36.2 | +3.9% | +2.13 | +2.73 |
| Stats + injuries | close | 1 | 3114 | 49.1% | -196.1 | -6.3% | -3.61 | — |
| Stats + injuries | close | 2 | 1564 | 48.5% | -117.5 | -7.5% | -3.05 | — |
| Stats + injuries | close | 3 | 676 | 48.4% | -53.5 | -7.9% | -2.09 | — |
| Stats + injuries + opening line | open | 1 | 1681 | 56.4% | +103.0 | +6.1% | +3.32 | +2.09 |
| Stats + injuries + opening line | open | 2 | 570 | 56.8% | +25.2 | +4.4% | +2.10 | +3.67 |
| Stats + injuries + opening line | open | 3 | 189 | 61.7% | +14.5 | +7.7% | +2.56 | +5.85 |
| Stats + injuries + opening line | close | 1 | 2232 | 48.4% | -175.1 | -7.8% | -3.78 | — |
| Stats + injuries + opening line | close | 2 | 810 | 49.4% | -48.4 | -6.0% | -1.67 | — |
| Stats + injuries + opening line | close | 3 | 288 | 49.7% | -15.9 | -5.5% | -0.93 | — |

## Is injury news priced?

| Outcome regressed on injury points | Slope | t |
|---|---|---|
| Actual home margin | 1.00 | 20.1 |
| Opening line (home expected margin) | 0.67 | 29.3 |
| Line move, open to close (toward home) | 0.29 | 50.9 |
| Cover margin vs closing line | 0.05 | 1.1 |

## Stats only (no injuries)

| Bet against | Min edge | Bets | W-L-P | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) | Win % at close |
|---|---|---|---|---|---|---|---|---|---|
| open line | 1 | 7754 | 3947-3704-103 | 51.6% | -141.5 | -1.8% | -1.39 | +0.32 | 50.8% |
| open line | 2 | 4049 | 2034-1961-54 | 50.9% | -139.6 | -3.4% | -1.86 | +0.50 | 49.7% |
| open line | 3 | 2026 | 1031-966-29 | 51.6% | -54.5 | -2.7% | -0.67 | +0.71 | 50.0% |
| open line | 4 | 1029 | 522-493-14 | 51.4% | -41.7 | -4.1% | -0.61 | +0.99 | 49.8% |
| open line | 5 | 561 | 289-264-8 | 52.3% | -21.7 | -3.9% | -0.06 | +1.36 | 50.0% |
| close line | 1 | 9300 | 4585-4583-132 | 50.0% | -416.7 | -4.5% | -4.54 | — | — |
| close line | 2 | 5600 | 2759-2764-77 | 50.0% | -257.1 | -4.6% | -3.61 | — | — |
| close line | 3 | 3191 | 1571-1573-47 | 50.0% | -146.0 | -4.6% | -2.71 | — | — |
| close line | 4 | 1772 | 880-865-27 | 50.4% | -65.4 | -3.7% | -1.63 | — | — |
| close line | 5 | 947 | 477-459-11 | 51.0% | -25.5 | -2.7% | -0.87 | — | — |

## Stats + opening line (no injuries)

| Bet against | Min edge | Bets | W-L-P | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) | Win % at close |
|---|---|---|---|---|---|---|---|---|---|
| open line | 1 | 2092 | 1080-985-27 | 52.3% | -27.0 | -1.3% | -0.07 | +0.74 | 49.9% |
| open line | 2 | 232 | 126-105-1 | 54.5% | -4.3 | -1.8% | +0.66 | +2.33 | 48.3% |
| open line | 3 | 38 | 24-14-0 | 63.2% | +3.6 | +9.6% | +1.33 | +6.59 | 42.1% |
| open line | 4 | 3 | 2-1-0 | 66.7% | +0.8 | +27.3% | +0.50 | +16.67 | 0.0% |
| open line | 5 | 2 | 2-0-0 | 100.0% | +1.8 | +90.9% | +1.35 | +17.00 | 0.0% |
| close line | 1 | 6578 | 3259-3224-95 | 50.3% | -265.4 | -4.0% | -3.40 | — | — |
| close line | 2 | 2669 | 1292-1342-35 | 49.1% | -168.7 | -6.3% | -3.42 | — | — |
| close line | 3 | 1159 | 567-582-10 | 49.3% | -67.3 | -5.8% | -2.06 | — | — |
| close line | 4 | 520 | 256-261-3 | 49.5% | -28.9 | -5.6% | -1.30 | — | — |
| close line | 5 | 240 | 127-111-2 | 53.4% | +3.9 | +1.6% | +0.30 | — | — |

## Stats + injuries

| Bet against | Min edge | Bets | W-L-P | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) | Win % at close |
|---|---|---|---|---|---|---|---|---|---|
| open line | 1 | 7891 | 4094-3691-106 | 52.6% | +4.6 | +0.1% | +0.37 | +1.01 | 49.2% |
| open line | 2 | 4397 | 2339-2004-54 | 53.9% | +94.7 | +2.2% | +1.95 | +1.45 | 49.2% |
| open line | 3 | 2262 | 1220-1015-27 | 54.6% | +68.4 | +3.0% | +2.09 | +2.00 | 48.8% |
| open line | 4 | 1072 | 592-467-13 | 55.9% | +46.7 | +4.4% | +2.29 | +2.74 | 48.5% |
| open line | 5 | 545 | 304-233-8 | 56.6% | +20.3 | +3.7% | +1.96 | +3.76 | 46.1% |
| close line | 1 | 8271 | 4054-4099-118 | 49.7% | -418.4 | -5.1% | -4.80 | — | — |
| close line | 2 | 4107 | 1967-2081-59 | 48.6% | -295.7 | -7.2% | -4.83 | — | — |
| close line | 3 | 1729 | 812-896-21 | 47.5% | -159.8 | -9.2% | -4.01 | — | — |
| close line | 4 | 703 | 332-362-9 | 47.8% | -61.7 | -8.8% | -2.40 | — | — |
| close line | 5 | 296 | 142-149-5 | 48.8% | -21.1 | -7.1% | -1.22 | — | — |

## Stats + injuries + opening line

| Bet against | Min edge | Bets | W-L-P | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) | Win % at close |
|---|---|---|---|---|---|---|---|---|---|
| open line | 1 | 4661 | 2488-2111-62 | 54.1% | +124.5 | +2.7% | +2.33 | +1.51 | 49.3% |
| open line | 2 | 1284 | 728-536-20 | 57.6% | +103.3 | +8.0% | +3.71 | +2.84 | 48.8% |
| open line | 3 | 340 | 202-134-4 | 60.1% | +30.7 | +9.0% | +2.84 | +4.84 | 45.6% |
| open line | 4 | 108 | 79-27-2 | 74.5% | +30.3 | +28.0% | +4.57 | +7.14 | 52.3% |
| open line | 5 | 38 | 31-7-0 | 81.6% | +15.1 | +39.9% | +3.60 | +9.41 | 45.9% |
| close line | 1 | 5980 | 2876-3017-87 | 48.8% | -407.9 | -6.8% | -5.50 | — | — |
| close line | 2 | 1934 | 934-976-24 | 48.9% | -130.0 | -6.7% | -3.05 | — | — |
| close line | 3 | 569 | 274-290-5 | 48.6% | -41.8 | -7.3% | -1.81 | — | — |
| close line | 4 | 185 | 96-87-2 | 52.5% | -0.3 | -0.2% | +0.02 | — | — |
| close line | 5 | 77 | 43-33-1 | 56.6% | +6.0 | +7.7% | +0.73 | — | — |

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
| 2022-23 | 333 | 53.0% | +4.1 |
| 2023-24 | 326 | 46.4% | -37.4 |
| 2024-25 | 388 | 46.9% | -40.6 |
| 2025-26 | 448 | 48.2% | -37.2 |
| 2026-27 | 69 | 47.8% | -6.4 |

## Does the line already price the situation?

Regression of the cover margin (home margin + home spread) on situational features, test seasons. A coefficient near 0 means the line already accounts for that factor.

| Feature | vs opening line (pts) | t | vs closing line (pts) | t |
|---|---|---|---|---|
| home edge | -0.11 | -0.80 | -0.05 | -0.42 |
| home on back-to-back | -0.43 | -1.09 | -0.08 | -0.20 |
| away on back-to-back | +0.20 | +0.58 | -0.16 | -0.47 |
| rest difference (days) | +0.15 | +1.01 | +0.11 | +0.76 |
| altitude home | +0.77 | +1.75 | +0.67 | +1.55 |
| injury points (model's absence value) | +0.32 | +7.24 | +0.04 | +1.02 |

Classic angles, graded at the closing line:

| Angle | Record |
|---|---|
| Rested home team vs away team on a back-to-back | 1051-1067 (49.6%) |
| Rested away team vs home team on a back-to-back | 600-595 (50.2%) |
| Home underdog of 10+ points | 302-320 (48.6%) |
| Road favorite | 2427-2384 (50.4%) |
| Team missing 4+ points more of players than opponent (bet the healthier side) | 421-422 (49.9%) home / 348-304 (53.4%) away |

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
| 2022 | [2.275, 0.1, 0.893, -1.451, 1.598, 0.14, 1.054] |
| 2023 | [2.261, 0.1, 0.885, -1.368, 1.684, 0.15, 1.132] |
| 2024 | [2.271, 0.103, 0.888, -1.542, 1.71, 0.157, 1.147] |
| 2025 | [2.239, 0.113, 0.888, -1.731, 1.845, 0.16, 1.099] |
| 2026 | [2.21, 0.13, 0.881, -1.802, 1.832, 0.152, 1.004] |

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
| 2022 | [0.349, -0.087, 0.312, -0.582, 0.686, 0.129, 0.881, 0.77] |
| 2023 | [0.331, -0.09, 0.293, -0.437, 0.681, 0.131, 0.923, 0.783] |
| 2024 | [0.371, -0.081, 0.297, -0.6, 0.69, 0.131, 0.944, 0.78] |
| 2025 | [0.488, -0.062, 0.341, -0.82, 0.873, 0.137, 0.911, 0.727] |
| 2026 | [0.466, -0.051, 0.33, -0.868, 0.853, 0.124, 0.814, 0.733] |

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
| 2022 | [2.193, 0.119, 0.877, -1.296, 1.401, 0.116, 1.076, 0.939] |
| 2023 | [2.177, 0.104, 0.885, -1.187, 1.428, 0.123, 1.156, 0.928] |
| 2024 | [2.182, 0.11, 0.882, -1.344, 1.447, 0.122, 1.191, 0.937] |
| 2025 | [2.147, 0.131, 0.87, -1.507, 1.565, 0.124, 1.139, 0.952] |
| 2026 | [2.121, 0.154, 0.856, -1.564, 1.516, 0.111, 1.023, 0.989] |

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
| 2022 | [0.694, -0.025, 0.41, -0.668, 0.756, 0.117, 0.9, 0.547, 0.613] |
| 2023 | [0.733, -0.035, 0.423, -0.553, 0.772, 0.121, 0.965, 0.506, 0.602] |
| 2024 | [0.75, -0.025, 0.416, -0.697, 0.77, 0.117, 0.99, 0.529, 0.604] |
| 2025 | [0.828, 0.002, 0.437, -0.886, 0.919, 0.121, 0.962, 0.577, 0.564] |
| 2026 | [0.84, 0.022, 0.432, -0.947, 0.892, 0.106, 0.871, 0.622, 0.553] |

