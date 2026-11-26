#!/usr/bin/env python3
"""NBA point-spread model built on the 2011-12 to 2021-22 closing-odds archive.

How it works (all features are computed from information available before tip-off):

1. Two online team ratings, both on a points scale:
   - performance rating: updated from each game's actual margin;
   - market rating: updated from each game's *closing spread*, i.e. how the
     market rated the team in its past games.
   Both shrink toward 0 between seasons. The update speeds are tuned only on
   the training seasons.
2. Schedule features: days of rest for each side and back-to-backs, built from
   the game dates. Denver and Utah get an altitude flag at home.
3. A linear regression maps those features to the home team's margin. It is
   refit walk-forward: to predict season S it is trained only on seasons < S.
   Two versions are fit:
     - "stats":  ratings + schedule only (no betting line as input)
     - "blend":  stats features + the opening spread
4. Bets: when the predicted margin differs from the line by at least the edge
   threshold, bet that side at -110. Results are graded against both the
   opening line (the number you could have bet early) and the closing line.

Usage:
  python3 model/nba_model.py backtest            # writes model/results/
  python3 model/nba_model.py predict games.csv   # rate upcoming games

The archive has no spread prices, so every bet is assumed to be at -110.
"""
import csv
import datetime as dt
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "nba_archive.json")
OUT = os.path.join(HERE, "results")

TRAIN_SEASONS = (2011, 2012, 2013)  # used to tune ratings and as first regression window
WIN, LOSS = 100 / 110, -1.0          # profit per unit at -110
BREAK_EVEN = 110 / 210
ALTITUDE = {"Nuggets", "Jazz"}
NAME_FIX = {"NewJersey": "Nets", "Golden State": "Warriors"}


# ----------------------------------------------------------------------------- data
def game_date(season, raw):
    """The archive's year field is unreliable (e.g. the 2020 bubble is stamped
    2019), so rebuild the year from the season and the month."""
    raw = int(raw)
    month, day = raw // 100 % 100, raw % 100
    year = season if month >= 10 else season + 1
    if season == 2019 and (month in (8, 9) or (month == 10 and day <= 15)):
        year = 2020  # bubble restart and 2020 Finals
    return dt.date(year, month, day)


def load_games(path=DATA, extra=None):
    rows = json.load(open(path))
    if extra:
        rows += json.load(open(extra))
    games = []
    for r in rows:
        h = NAME_FIX.get(str(r["home_team"]), str(r["home_team"]))
        a = NAME_FIX.get(str(r["away_team"]), str(r["away_team"]))
        if h == "0" or a == "0":
            continue
        try:
            hs, as_ = float(r["home_final"]), float(r["away_final"])
            cs, os_ = float(r["home_close_spread"]), float(r["home_open_spread"])
            tot = float(r["close_over_under"])
        except (TypeError, ValueError):
            continue
        # drop rows where a total or moneyline leaked into the spread column
        if abs(cs) > 25 or abs(os_) > 25 or not 150 <= tot <= 280:
            continue
        games.append(dict(season=int(r["season"]), date=game_date(int(r["season"]), r["date"]),
                          home=h, away=a, margin=hs - as_, close=cs, open=os_, total=tot))
    games.sort(key=lambda g: (g["season"], g["date"]))
    return games


# -------------------------------------------------------------------------- ratings
class Ratings:
    """Online point ratings. perf learns from margins, mkt from closing spreads."""

    def __init__(self, k_perf=0.06, k_mkt=0.12, carry=0.6, k_hca=0.002, cap=25.0):
        self.k_perf, self.k_mkt, self.carry, self.k_hca, self.cap = k_perf, k_mkt, carry, k_hca, cap
        self.perf, self.mkt, self.last, self.played = {}, {}, {}, {}
        self.hca_perf = self.hca_mkt = 3.0
        self.season = None

    def new_season(self, season):
        for d in (self.perf, self.mkt):
            for t in d:
                d[t] *= self.carry
        self.last, self.played, self.season = {}, {}, season

    def features(self, g):
        if g["season"] != self.season:
            self.new_season(g["season"])
        h, a = g["home"], g["away"]

        def rest(t):
            if t not in self.last:
                return 3
            return min(max((g["date"] - self.last[t]).days - 1, 0), 3)

        rh, ra = rest(h), rest(a)
        return dict(
            perf_diff=self.perf.get(h, 0) - self.perf.get(a, 0),
            mkt_diff=self.mkt.get(h, 0) - self.mkt.get(a, 0),
            b2b_home=float(rh == 0), b2b_away=float(ra == 0),
            rest_diff=float(rh - ra),
            altitude=float(h in ALTITUDE),
            warm=min(self.played.get(h, 0), self.played.get(a, 0)),
            pred_perf=self.perf.get(h, 0) - self.perf.get(a, 0) + self.hca_perf,
            pred_mkt=self.mkt.get(h, 0) - self.mkt.get(a, 0) + self.hca_mkt,
        )

    def update(self, g, f):
        h, a = g["home"], g["away"]
        m = max(min(g["margin"], self.cap), -self.cap)
        e = m - f["pred_perf"]
        self.perf[h] = self.perf.get(h, 0) + self.k_perf * e
        self.perf[a] = self.perf.get(a, 0) - self.k_perf * e
        self.hca_perf += self.k_hca * e
        e2 = -g["close"] - f["pred_mkt"]
        self.mkt[h] = self.mkt.get(h, 0) + self.k_mkt * e2
        self.mkt[a] = self.mkt.get(a, 0) - self.k_mkt * e2
        self.hca_mkt += self.k_hca * e2
        for t in (h, a):
            self.last[t] = g["date"]
            self.played[t] = self.played.get(t, 0) + 1


def run_ratings(games, **params):
    r = Ratings(**params)
    feats = []
    for g in games:
        f = r.features(g)
        feats.append(f)
        r.update(g, f)
    return feats, r


def tune(games):
    """Grid-search rating speeds on the training seasons only (squared error of
    the rating's own margin / closing-spread forecasts)."""
    train = [g for g in games if g["season"] in TRAIN_SEASONS]
    best_p = best_m = None
    for kp in (0.03, 0.045, 0.06, 0.08, 0.1):
        for carry in (0.4, 0.6, 0.8):
            feats, _ = run_ratings(train, k_perf=kp, carry=carry)
            sse = sum((g["margin"] - f["pred_perf"]) ** 2 for g, f in zip(train, feats) if f["warm"] >= 5)
            if best_p is None or sse < best_p[0]:
                best_p = (sse, kp, carry)
    for km in (0.06, 0.1, 0.15, 0.2, 0.3):
        feats, _ = run_ratings(train, k_perf=best_p[1], carry=best_p[2], k_mkt=km)
        sse = sum((-g["close"] - f["pred_mkt"]) ** 2 for g, f in zip(train, feats) if f["warm"] >= 5)
        if best_m is None or sse < best_m[0]:
            best_m = (sse, km)
    return dict(k_perf=best_p[1], carry=best_p[2], k_mkt=best_m[1])


# ------------------------------------------------------------------------ regression
STATS_COLS = ["perf_diff", "mkt_diff", "b2b_home", "b2b_away", "rest_diff", "altitude"]
BLEND_COLS = STATS_COLS + ["open_line"]


def design(rows, cols):
    return np.array([[1.0] + [r[c] for c in cols] for r in rows])


def fit(rows, cols, ridge=1.0):
    X, y = design(rows, cols), np.array([r["margin"] for r in rows])
    reg = ridge * np.eye(X.shape[1])
    reg[0, 0] = 0
    return np.linalg.solve(X.T @ X + reg, X.T @ y)


# -------------------------------------------------------------------------- backtest
def grade(margin, line, side):
    """side=+1 bets home at home line `line`, -1 bets away. Returns +1/0/-1."""
    v = (margin + line) * side
    return (v > 0) - (v < 0)


def summarize(bets):
    n = len(bets)
    w = sum(b["res"] == 1 for b in bets)
    l = sum(b["res"] == -1 for b in bets)
    p = n - w - l
    units = w * WIN + l * LOSS
    dec = w + l
    pct = w / dec if dec else float("nan")
    z = (w - dec * BREAK_EVEN) / math.sqrt(dec * BREAK_EVEN * (1 - BREAK_EVEN)) if dec else float("nan")
    clv = sum(b.get("clv", 0) for b in bets) / n if n else float("nan")
    return dict(n=n, w=w, l=l, p=p, pct=pct, units=units, roi=units / n if n else float("nan"), z=z, clv=clv)


def backtest(games):
    params = tune(games)
    feats, _ = run_ratings(games, **params)
    rows = []
    for g, f in zip(games, feats):
        rows.append({**g, **f, "open_line": -g["open"]})
    usable = [r for r in rows if r["warm"] >= 5]
    seasons = sorted({r["season"] for r in usable})
    test_seasons = [s for s in seasons if s not in TRAIN_SEASONS]

    preds = []
    coefs = {}
    for s in test_seasons:
        train = [r for r in usable if r["season"] < s]
        test = [r for r in usable if r["season"] == s]
        bs, bb = fit(train, STATS_COLS), fit(train, BLEND_COLS)
        coefs[s] = dict(stats=bs.round(3).tolist(), blend=bb.round(3).tolist())
        ps, pb = design(test, STATS_COLS) @ bs, design(test, BLEND_COLS) @ bb
        for r, a, b in zip(test, ps, pb):
            preds.append({**r, "pred_stats": float(a), "pred_blend": float(b)})

    # forecast accuracy
    def mae(key):
        return sum(abs(p["margin"] - key(p)) for p in preds) / len(preds)

    acc = {
        "closing line": mae(lambda p: -p["close"]),
        "opening line": mae(lambda p: -p["open"]),
        "stats model": mae(lambda p: p["pred_stats"]),
        "blend model": mae(lambda p: p["pred_blend"]),
    }

    # betting simulations
    results = {}
    bet_log = []
    for model in ("stats", "blend"):
        for lk in ("open", "close"):
            for thr in (1, 2, 3, 4, 5):
                bets = []
                for p in preds:
                    line = p[lk]  # home spread
                    edge = p["pred_" + model] + line  # >0: model likes home to cover
                    if abs(edge) < thr:
                        continue
                    side = 1 if edge > 0 else -1
                    b = dict(season=p["season"], date=str(p["date"]), home=p["home"], away=p["away"],
                             side="home" if side > 0 else "away", line=line, edge=round(edge, 2),
                             res=grade(p["margin"], line, side))
                    if lk == "open":
                        b["clv"] = (p["open"] - p["close"]) * side  # points gained vs close
                        b["res_close"] = grade(p["margin"], p["close"], side)
                    bets.append(b)
                    if model == "blend" and lk == "open" and thr == 2:
                        bet_log.append({**b, "model": model, "pred_margin": round(p["pred_blend"], 2)})
                results[(model, lk, thr)] = (summarize(bets), bets)
    return params, coefs, acc, results, bet_log, preds


def situational_check(games):
    feats, _ = run_ratings(games, **tune(games))
    rows = [{**g, **f} for g, f in zip(games, feats) if f["warm"] >= 5]
    names = ["home edge", "home on back-to-back", "away on back-to-back", "rest difference (days)", "altitude home"]
    X = np.array([[1, r["b2b_home"], r["b2b_away"], r["rest_diff"], r["altitude"]] for r in rows])
    out = ["| Feature | vs opening line (pts) | t | vs closing line (pts) | t |", "|---|---|---|---|---|"]
    stats = []
    for lk in ("open", "close"):
        y = np.array([r["margin"] + r[lk] for r in rows])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        se = np.sqrt(np.diag(e @ e / (len(y) - X.shape[1]) * np.linalg.inv(X.T @ X)))
        stats.append((b, b / se))
    for i, n in enumerate(names):
        out.append(f"| {n} | {stats[0][0][i]:+.2f} | {stats[0][1][i]:+.2f} | {stats[1][0][i]:+.2f} | {stats[1][1][i]:+.2f} |")

    def ats(cond, side):
        w = l = 0
        for r in rows:
            if cond(r):
                v = (r["margin"] + r["close"]) * side
                w, l = w + (v > 0), l + (v < 0)
        return f"{w}-{l} ({pct(w / (w + l))})"

    out.append("\nClassic angles, graded at the closing line:\n")
    out.append("| Angle | Record |\n|---|---|")
    out.append(f"| Rested home team vs away team on a back-to-back | {ats(lambda r: r['b2b_away'] and not r['b2b_home'], 1)} |")
    out.append(f"| Rested away team vs home team on a back-to-back | {ats(lambda r: r['b2b_home'] and not r['b2b_away'], -1)} |")
    out.append(f"| Home underdog of 10+ points | {ats(lambda r: r['close'] >= 10, 1)} |")
    out.append(f"| Road favorite | {ats(lambda r: r['close'] > 0, -1)} |")
    return "\n".join(out)


def pct(x):
    return "—" if x != x else f"{100 * x:.1f}%"


def write_report(games, params, coefs, acc, results, bet_log, preds):
    os.makedirs(OUT, exist_ok=True)
    seasons = sorted({p["season"] for p in preds})
    L = []
    L.append("# NBA spread model backtest\n")
    L.append(f"Archive: {len(games):,} games, seasons {games[0]['season']}-{games[-1]['season'] + 1 - 2000:02d}. "
             f"Ratings tuned and regression first trained on {TRAIN_SEASONS[0]}-{TRAIN_SEASONS[-1] + 1 - 2000:02d}; "
             f"walk-forward test on {len(preds):,} games from {seasons[0]}-{seasons[-1] + 1 - 2000:02d}. "
             "All bets assumed at -110 (break-even 52.38%).\n")
    L.append(f"Tuned rating parameters: {params}\n")
    L.append("## Forecast accuracy (mean absolute error of home margin, test seasons)\n")
    L.append("| Forecast | MAE (points) |\n|---|---|")
    for k, v in acc.items():
        L.append(f"| {k} | {v:.2f} |")
    L.append("")
    for model in ("stats", "blend"):
        name = "Stats-only model" if model == "stats" else "Blend model (stats + opening line)"
        L.append(f"## {name}\n")
        L.append("| Bet against | Min edge | Bets | W-L-P | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) | Win % at close |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for lk in ("open", "close"):
            for thr in (1, 2, 3, 4, 5):
                s, bets = results[(model, lk, thr)]
                if lk == "open":
                    sc = summarize([{**b, "res": b["res_close"]} for b in bets])
                    clv, atc = f"{s['clv']:+.2f}", pct(sc["pct"])
                else:
                    clv = atc = "—"
                L.append(f"| {lk} line | {thr} | {s['n']} | {s['w']}-{s['l']}-{s['p']} | {pct(s['pct'])} | "
                         f"{s['units']:+.1f} | {100 * s['roi']:+.1f}% | {s['z']:+.2f} | {clv} | {atc} |")
        L.append("")
    L.append("## By season: blend model vs opening line, edge ≥ 2\n")
    L.append("| Season | Bets | Win % | Units | Avg CLV |\n|---|---|---|---|---|")
    _, bets = results[("blend", "open", 2)]
    for s in seasons:
        sb = [b for b in bets if b["season"] == s]
        if sb:
            x = summarize(sb)
            L.append(f"| {s}-{s + 1 - 2000:02d} | {x['n']} | {pct(x['pct'])} | {x['units']:+.1f} | {x['clv']:+.2f} |")
    L.append("")
    L.append("## Does the line already price the situation?\n")
    L.append("Regression of the cover margin (home margin + home spread) on situational features, all "
             "games with at least 5 games played by each team (2011-22). A coefficient near 0 means the "
             "line already accounts for that factor.\n")
    L.append(situational_check(games))
    L.append("")
    L.append("## Regression coefficients by test season\n")
    L.append("Columns: intercept (home edge), " + ", ".join(BLEND_COLS) + "\n")
    L.append("| Season | Stats model | Blend model |\n|---|---|---|")
    for s, c in coefs.items():
        L.append(f"| {s} | {c['stats']} | {c['blend']} |")
    open(os.path.join(OUT, "backtest.md"), "w").write("\n".join(L) + "\n")

    with open(os.path.join(OUT, "bets_blend_open_edge2.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(bet_log[0].keys()))
        w.writeheader()
        w.writerows(bet_log)
    print("\n".join(L))


# --------------------------------------------------------------------------- predict
def predict(csv_path, extra=None):
    """Rate upcoming games. CSV columns: date (YYYY-MM-DD), home, away, open_spread
    (home team's spread, e.g. -4.5). Ratings come from every game in the archive
    (plus `extra`, a JSON file of newer results in the archive's format)."""
    games = load_games(extra=extra)
    params = tune(games)
    feats, r = run_ratings(games, **params)
    rows = [{**g, **f, "open_line": -g["open"]} for g, f in zip(games, feats) if f["warm"] >= 5]
    beta = fit(rows, BLEND_COLS)
    last = games[-1]["date"]
    print(f"Ratings current through {last}. If that is not yesterday, results are stale.\n")
    print(f"{'date':<11}{'away':<15}{'home':<15}{'line':>6}{'model':>8}{'edge':>7}  pick")
    for row in csv.DictReader(open(csv_path)):
        d = dt.date.fromisoformat(row["date"])
        g = dict(season=d.year if d.month >= 10 else d.year - 1, date=d, home=row["home"],
                 away=row["away"], open=float(row["open_spread"]))
        f = r.features(g)
        x = {**f, "open_line": -g["open"]}
        pred = float((design([x], BLEND_COLS) @ beta)[0])
        edge = pred + g["open"]
        pick = ""
        if abs(edge) >= 2:
            pick = f"{g['home']} {g['open']:+g}" if edge > 0 else f"{g['away']} {-g['open']:+g}"
        print(f"{row['date']:<11}{g['away']:<15}{g['home']:<15}{g['open']:>+6g}{-pred:>+8.1f}{edge:>+7.1f}  {pick}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "backtest"
    if cmd == "backtest":
        games = load_games()
        write_report(games, *backtest(games))
    elif cmd == "predict":
        predict(sys.argv[2], extra=sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        sys.exit(__doc__)
