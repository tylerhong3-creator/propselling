# Polymarket flow vs. NBA spread results

268 completed 2026-27 games with Polymarket trades and a DraftKings closing spread. Public tickets = trades under $100; whales = wallets with a net position of $1,000+ in the game. Flow is measured on moneyline and spread markets before tip-off.

Median pre-game Polymarket volume per game: $478,994; games with at least one whale: 268.

## 1. Does flow anticipate the DraftKings line move?

Line move = opening spread − closing spread (positive = moved toward home). Slope per unit of the flow measure, with standard error.

| Flow measure | Games | Slope (pts) | SE | t |
|---|---|---|---|---|
| Whale share toward home (−1..1) | 268 | +1.96 | 0.34 | +5.77 |
| Early whale share (trades ≥ 6 h before tip) | 268 | +1.30 | 0.31 | +4.22 |
| Money share on home − 50% | 268 | +4.62 | 0.84 | +5.50 |
| Public ticket share on home − 50% | 268 | -0.55 | 1.70 | -0.32 |

## 2. Does flow predict covering the closing spread?

Cover margin = home margin + home closing spread. A real signal needs a slope clearly away from 0.

| Flow measure | Games | Slope (pts of cover margin) | SE | t |
|---|---|---|---|---|
| Whale share toward home | 268 | +0.21 | 1.74 | +0.12 |
| Early whale share (≥ 6 h before tip) | 268 | +0.84 | 1.54 | +0.54 |
| Money share on home − 50% | 268 | +0.86 | 4.28 | +0.20 |
| Public ticket share on home − 50% | 268 | +8.85 | 8.21 | +1.08 |

## 3. Strategies graded at DraftKings closing prices

| Strategy | Bets | W-L-P | Win % (95% CI) | Units | ROI |
|---|---|---|---|---|---|
| Follow whales (any whale money) | 268 | 133-135-0 | 49.6% ± 6.0 | -13.8 | -5.1% |
| Follow whales, whale share ≥ 0.5 one way | 109 | 52-57-0 | 47.7% ± 9.4 | -9.5 | -8.8% |
| Fade the public tickets (≥ 60% one side) | 95 | 45-50-0 | 47.4% ± 10.0 | -8.8 | -9.3% |
| Whales vs public: whales opposite a ≥ 60% public side | 45 | 17-28-0 | 37.8% ± 14.2 | -12.3 | -27.2% |
| Follow early whales (share ≥ 0.5, ≥ 6 h before tip) | 129 | 59-70-0 | 45.7% ± 8.6 | -16.3 | -12.6% |
| Bet every home team (baseline) | 268 | 129-139-0 | 48.1% ± 6.0 | -22.2 | -8.3% |

Break-even at −110 is 52.38%. With a few hundred games the 95% interval is about ±6–9 points, so only a very large effect would show up as significant this early in the season.

