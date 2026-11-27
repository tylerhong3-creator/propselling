# NBA spread model

A walk-forward point-spread model built on 12,960 NBA games with opening and closing lines (2011-12 to 2021-22, SportsbookReviewsOnline archive). It adds player availability (injuries, rest days, suspensions) reconstructed from stats.nba.com play-by-play. Requires Python 3 and numpy.

```bash
python3 model/nba_model.py backtest
```

```bash
python3 model/nba_model.py predict model/example_games.csv
```

`backtest` writes `results/backtest.md` (all tables) and two bet logs:
- `results/bets_stats_inj_vs_close_edge2.csv`
- `results/bets_blend_inj_vs_open_edge2.csv`

Each bet in the logs lists the players who were out.

## Data

| File | What it is |
|---|---|
| `data/nba_archive.json` | Scores, opening and closing spreads and totals. |
| `data/player_games.csv.gz` | One row per player per game, 13,888 games from 2011-22 including playoffs: minutes (rebuilt from substitutions), Game Score and plus-minus. It matches 99.8% of archive games. Check: team minutes sum to 240, player points sum to the final score in 98% of games, and LeBron's 2015-16 line comes out at 76 games and 35.6 mpg, which is correct. |
| `build_player_logs.py` | Rebuilds the player file from the `nbastats_YYYY.tar.xz` / `nbastats_po_YYYY.tar.xz` play-by-play files at [github.com/shufinskiy/nba_data](https://github.com/shufinskiy/nba_data). |

## How it works

1. **Team ratings, on a points scale, updated after each game.**
   - A *performance* rating comes from margins; a *market* rating comes from past closing spreads.
   - In the injury-aware version, each game's target is corrected for who sat out, so the ratings describe the full-strength team.
2. **Schedule features.** Back-to-backs, rest difference, and altitude (Denver, Utah).
3. **Player availability.** Using past games only, each player carries a running estimate of minutes per game and Game Score per minute. A rotation player who doesn't play counts as absent: 12+ recent minutes, and appeared in the team's last 10 games this season. Absences become points via weights fitted on 2011-14 only: −0.074 per missing minute and +0.311 per missing Game Score point. Sitting LeBron James and Anthony Davis together comes out at about 7.8 points.
4. **Regression to home margin.** Refit each season using only earlier seasons. There are four versions: stats, stats + opening line, and each of those plus injuries.
5. **Bets.** When the prediction beats the line by the edge threshold, bet that side at −110. Bets are graded against both the opening and the closing line.

## Results (2014-15 to 2021-22, 8,788 test games)

### 1. Injuries matter, and the market prices them completely by the close

| Regressed on the model's injury points | Slope | t |
|---|---|---|
| Actual home margin | 0.84 | 11.9 |
| Opening line | 0.53 | 16.1 |
| Line move from open to close | 0.31 | 44.6 |
| Cover margin vs the closing line | **−0.00** | −0.0 |

Roughly 60% of an absence's value is already in the opening line, and the rest arrives as the line moves before tip-off. After the close there is nothing left to exploit.

### 2. Against the closing line, adding injuries doesn't help

| Configuration | Bets | Win % | ROI |
|---|---|---|---|
| Stats + injuries vs close, edge ≥ 1 | 5,157 | 50.1% | −4.3% |
| Stats + injuries vs close, edge ≥ 2 | 2,543 | 48.6% | −7.0% |
| Stats + injuries + open line vs close, edge ≥ 2 | 1,124 | 48.5% | −7.3% |

Break-even is 52.38%. When the model disagrees with a close that already prices injuries, it is usually the model that's wrong.

### 3. Against the opening line, injury information is a real edge, but only if you're early

| Configuration | Bets | Win % | ROI | z | Avg closing line value |
|---|---|---|---|---|---|
| Stats + injuries vs open, edge ≥ 2 | 2,765 | 52.9% | +1.0% | +0.6 | +1.10 pts |
| Stats + injuries vs open, edge ≥ 4 | 578 | 56.5% | +7.8% | +2.0 | +2.03 pts |
| **Stats + injuries + open line vs open, edge ≥ 2** | **714** | **58.2%** | **+10.9%** | **+3.1** | **+2.18 pts** |

The same 714 bets graded at the closing number win only 50.2%. The whole edge comes from getting the number before the market reacted to the absence, not from out-predicting the market.

**This is an upper bound.** Absences are read from each game's box score, so the backtest assumes you knew every absence when the line opened. In reality much injury news comes out after the open, and sharp books move within minutes of it. The realistic version of this edge is a news-speed strategy:
- watch injury reports;
- run the model the moment a player is ruled out;
- bet any book that hasn't moved yet.

Measure success by closing line value, not by win rate.

### 4. Other findings

- **Rest, back-to-backs and altitude are fully priced at the close.** All |t| < 1.4.
- **Classic angles lose at the close:**

  | Angle | Win % |
  |---|---|
  | Rested home team vs away team on a back-to-back | 49.0% |
  | Home underdogs of 10+ points | 47.0% |
  | Betting the healthier side when the injury gap is 4+ points | 47–52% |

## Predicting games

`predict` takes a CSV with these columns:

| Column | Notes |
|---|---|
| `date` | |
| `home` | Archive nickname, e.g. `Seventysixers`, `Trailblazers` |
| `away` | Same naming as `home` |
| `open_spread` | The home team's spread |
| `home_out` | Players ruled out, separated by `;`, named as on NBA.com |
| `away_out` | Same format as `home_out` |

It prints the model's line, the edge and the injury adjustment. Unknown player names are flagged. Ratings and player values are frozen at June 2022. To use it this season, two things need adding:
- recent results in the archive's JSON format, passed as the third argument;
- the matching play-by-play, by rerunning `build_player_logs.py` with newer season files from the same repository.

Without them the output is stale. `example_games.csv` uses made-up lines and only shows the input format.

## Limits

- **No spread prices.** Every bet is assumed at −110.
- **The "open" timestamp is unknown.** The archive doesn't say when the opening line was posted.
- **No questionable/probable statuses.** Players are either in or out.
- **Late scratches and minutes restrictions** are only partly captured.
- **Thresholds were not tuned on a holdout.** The tables show every threshold, but the best-looking row is still the best of several.

Treat output as leans unless you track closing line value live over hundreds of bets.
