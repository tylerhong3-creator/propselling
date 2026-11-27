#!/usr/bin/env python3
"""Does Polymarket betting flow predict NBA spread results?

Joins model/data/polymarket_flow.csv (public tickets, money share, whale flow per
game) with DraftKings opening/closing spreads and final scores
(model/data/espn_games.csv) and tests, for completed games:

  1. Does whale flow anticipate DraftKings line movement (open -> close)?
  2. Does whale flow, money share, or public ticket share predict covering the
     closing spread? ("follow the whales", "fade the public")
  3. Simple strategies graded at the DraftKings closing price.

  python3 model/flow_analysis.py      # writes model/results/flow_analysis.md
"""
import csv
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FLOW = os.path.join(HERE, "data", "polymarket_flow.csv")
GAMES = os.path.join(HERE, "data", "espn_games.csv")
OUT = os.path.join(HERE, "results", "flow_analysis.md")


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load():
    games = {(r["date"], r["home"], r["away"]): r for r in csv.DictReader(open(GAMES))}
    rows = []
    for r in csv.DictReader(open(FLOW)):
        g = games.get((r["date"], r["home"], r["away"]))
        if not g or not g["close_spread"] or not r["final"] == "1":
            continue
        close, opn = f(g["close_spread"]), f(g["open_spread"])
        margin = int(g["hpts"]) - int(g["apts"])
        rows.append(dict(
            date=r["date"], home=r["home"], away=r["away"], usd=f(r["usd"]) or 0,
            tickets=f(r["public_tickets"]) or 0,
            pub=f(r["public_ticket_home"]), money=f(r["money_home"]),
            whale=f(r["whale_share_home"]), whale_net=f(r["whale_net_home"]) or 0, whales=int(r["whales"]),
            close=close, open=opn if opn is not None else close, cover=margin + close,
            ph=f(g["close_home_price"]), pa=f(g["close_away_price"])))
    return rows


def ols(X, y):
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    se = np.sqrt(np.diag(e @ e / max(len(y) - X.shape[1], 1) * np.linalg.pinv(X.T @ X)))
    return b, se


def profit(res, price):
    if res == 0:
        return 0.0
    if res < 0:
        return -1.0
    price = price or -110
    return 100 / -price if price < 0 else price / 100


def strategy(rows, pick):
    """pick(r) -> +1 home, -1 away, 0 no bet. Graded at the DraftKings close."""
    w = l = p = 0
    units = 0.0
    for r in rows:
        s = pick(r)
        if not s:
            continue
        v = r["cover"] * s
        res = (v > 0) - (v < 0)
        w, l, p = w + (res > 0), l + (res < 0), p + (res == 0)
        units += profit(res, r["ph"] if s > 0 else r["pa"])
    n = w + l + p
    pct = w / (w + l) if w + l else float("nan")
    se = math.sqrt(pct * (1 - pct) / (w + l)) if w + l else float("nan")
    return f"| {n} | {w}-{l}-{p} | {100 * pct:.1f}% ± {196 * se:.1f} | {units:+.1f} | {100 * units / n if n else 0:+.1f}% |"


def main():
    rows = load()
    L = ["# Polymarket flow vs. NBA spread results\n"]
    L.append(f"{len(rows)} completed 2026-27 games with Polymarket trades and a DraftKings closing spread. "
             "Public tickets = trades under $100; whales = wallets with a net position of $1,000+ in the game. "
             "Flow is measured on moneyline and spread markets before tip-off.\n")
    if len(rows) < 30:
        L.append("Not enough games to test.\n")
        open(OUT, "w").write("\n".join(L))
        print("\n".join(L))
        return
    usd = sorted(r["usd"] for r in rows)
    L.append(f"Median pre-game Polymarket volume per game: ${usd[len(usd) // 2]:,.0f}; "
             f"games with at least one whale: {sum(r['whales'] > 0 for r in rows)}.\n")

    L.append("## 1. Does flow anticipate the DraftKings line move?\n")
    L.append("Line move = opening spread − closing spread (positive = moved toward home). "
             "Slope per unit of the flow measure, with standard error.\n")
    L.append("| Flow measure | Games | Slope (pts) | SE | t |\n|---|---|---|---|---|")
    for name, key, center in (("Whale share toward home (−1..1)", "whale", 0), ("Money share on home − 50%", "money", .5),
                              ("Public ticket share on home − 50%", "pub", .5)):
        sub = [r for r in rows if r[key] is not None]
        X = [[1, r[key] - center] for r in sub]
        b, se = ols(X, [r["open"] - r["close"] for r in sub])
        L.append(f"| {name} | {len(sub)} | {b[1]:+.2f} | {se[1]:.2f} | {b[1] / se[1]:+.2f} |")
    L.append("")

    L.append("## 2. Does flow predict covering the closing spread?\n")
    L.append("Cover margin = home margin + home closing spread. A real signal needs a slope clearly away from 0.\n")
    L.append("| Flow measure | Games | Slope (pts of cover margin) | SE | t |\n|---|---|---|---|---|")
    for name, key, center in (("Whale share toward home", "whale", 0), ("Money share on home − 50%", "money", .5),
                              ("Public ticket share on home − 50%", "pub", .5)):
        sub = [r for r in rows if r[key] is not None]
        b, se = ols([[1, r[key] - center] for r in sub], [r["cover"] for r in sub])
        L.append(f"| {name} | {len(sub)} | {b[1]:+.2f} | {se[1]:.2f} | {b[1] / se[1]:+.2f} |")
    L.append("")

    L.append("## 3. Strategies graded at DraftKings closing prices\n")
    L.append("| Strategy | Bets | W-L-P | Win % (95% CI) | Units | ROI |\n|---|---|---|---|---|---|")
    sgn = lambda x: (x > 0) - (x < 0)  # noqa: E731
    L.append("| Follow whales (any whale money) " + strategy(rows, lambda r: sgn(r["whale_net"]) if r["whales"] else 0))
    L.append("| Follow whales, whale share ≥ 0.5 one way " + strategy(
        rows, lambda r: sgn(r["whale"]) if r["whale"] is not None and abs(r["whale"]) >= .5 else 0))
    L.append("| Fade the public tickets (≥ 60% one side) " + strategy(
        rows, lambda r: -sgn(r["pub"] - .5) if r["pub"] is not None and abs(r["pub"] - .5) >= .1 else 0))
    L.append("| Whales vs public: whales opposite a ≥ 60% public side " + strategy(
        rows, lambda r: sgn(r["whale_net"]) if r["whales"] and r["pub"] is not None and abs(r["pub"] - .5) >= .1
        and sgn(r["whale_net"]) == -sgn(r["pub"] - .5) else 0))
    L.append("| Bet every home team (baseline) " + strategy(rows, lambda r: 1))
    L.append("")
    L.append("Break-even at −110 is 52.38%. With a few hundred games the 95% interval is about ±6–9 points, "
             "so only a very large effect would show up as significant this early in the season.\n")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
