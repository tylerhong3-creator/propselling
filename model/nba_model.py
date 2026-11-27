#!/usr/bin/env python3
"""NBA point-spread model built on the 2011-12 to 2021-22 closing-odds archive,
with player availability (injuries, rest days, suspensions) from play-by-play.

How it works:

1. Two online team ratings on a points scale:
   - performance rating, updated from each game's actual margin;
   - market rating, updated from each game's closing spread.
   Both shrink toward 0 between seasons; update speeds are tuned on 2011-14 only.
   In the injury-aware version the ratings learn *full-strength* team quality:
   each game's target is corrected for the players who sat out.
2. Schedule features from the game dates: back-to-backs, rest difference, and
   an altitude flag for Denver and Utah at home.
3. Player availability (model/data/player_games.csv.gz, built from
   play-by-play by build_player_logs.py). For every player the model keeps a
   running, exponentially weighted estimate of minutes per game and Game Score
   per minute, using only past games. A rotation player (recent minutes >= 12,
   appeared in the team's last 10 games this season) who does not play is
   counted as absent. Absences are converted to points with weights fitted on
   the training seasons only.
4. A linear regression maps the features to the home margin, refit walk-forward
   (each test season is predicted from earlier seasons only).
5. Bets: when the predicted margin beats the line by the edge threshold, bet that
   side at -110, graded against the opening and the closing line.

Look-ahead caveat: "who did not play" is read from the game's own box score.
Most absences are known before the closing line (injury reports, rest days),
so tests against the close are fair. Tests against the *opening* line assume
you knew every absence when the line opened, which overstates a real bettor's
edge; treat them as an upper bound on reacting to news before the book does.

Usage:
  python3 model/nba_model.py backtest            # writes model/results/
  python3 model/nba_model.py predict games.csv   # rate upcoming games
"""
import csv
import datetime as dt
import gzip
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "nba_archive.json")
PLAYERS = os.path.join(HERE, "data", "player_games.csv.gz")
ESPN_GAMES = os.path.join(HERE, "data", "espn_games.csv")          # 2022-23 onward, from fetch_espn.py
ESPN_PLAYERS = os.path.join(HERE, "data", "espn_player_games.csv.gz")
OUT = os.path.join(HERE, "results")

TRAIN_SEASONS = (2011, 2012, 2013)  # used to tune ratings / injury weights and as first regression window
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
                          home=h, away=a, hpts=int(hs), apts=int(as_), margin=hs - as_,
                          close=cs, open=os_, total=tot, src="archive"))
    if os.path.exists(ESPN_GAMES):
        games += load_espn_games()
    games.sort(key=lambda g: (g["season"], g["date"]))
    return games


def load_espn_games(path=ESPN_GAMES):
    """2022-23 onward: DraftKings opening/closing spreads with real prices (via ESPN)."""
    out = []
    for r in csv.DictReader(open(path)):
        if not r["close_spread"]:
            continue
        num = lambda k: float(r[k]) if r[k] not in ("", "None") else None  # noqa: E731
        cs = num("close_spread")
        has_open = num("open_spread") is not None
        os_ = num("open_spread") if has_open else cs
        out.append(dict(season=int(r["season"]), date=dt.date.fromisoformat(r["date"]), home=r["home"],
                        away=r["away"], hpts=int(r["hpts"]), apts=int(r["apts"]),
                        margin=float(r["hpts"]) - float(r["apts"]), close=cs, open=os_,
                        total=num("total") or 0.0, src="draftkings", has_open=has_open,
                        price=dict(open_home=num("open_home_price"), open_away=num("open_away_price"),
                                   close_home=num("close_home_price"), close_away=num("close_away_price"))))
    return out


# ---------------------------------------------------------------- player availability
class Availability:
    """Running per-player minutes and Game Score per minute, using past games only."""

    def __init__(self, alpha=0.15, window=10, min_minutes=12.0, prior_rate=0.30, prior_min=40.0):
        self.alpha, self.window, self.min_minutes = alpha, window, min_minutes
        self.prior_rate, self.prior_min = prior_rate, prior_min
        self.p = {}                       # pid -> state
        self.team_games = defaultdict(int)  # team -> games played (all seasons)
        self.names = {}

    def rate(self, s):
        return (s["g"] + self.prior_rate * self.prior_min) / (s["m"] + self.prior_min)

    def roster(self, team, season):
        """Rotation players expected to be available for `team`."""
        n = self.team_games[team]
        return {pid: s for pid, s in self.p.items()
                if s["team"] == team and s["season"] == season and s["apps"] >= 3
                and n - s["last"] <= self.window and s["min"] >= self.min_minutes}

    def missing(self, team, season, played):
        out = [(pid, s) for pid, s in self.roster(team, season).items() if pid not in played]
        return dict(min=sum(s["min"] for _, s in out),
                    gs=sum(s["min"] * self.rate(s) for _, s in out),
                    names=[self.names[pid] for pid, _ in out])

    def missing_by_name(self, team, season, names):
        want = {n.strip().lower() for n in names if n.strip()}
        out = [(pid, s) for pid, s in self.p.items()
               if s["team"] == team and self.names[pid].lower() in want]
        unknown = want - {self.names[pid].lower() for pid, _ in out}
        return dict(min=sum(s["min"] for _, s in out),
                    gs=sum(s["min"] * self.rate(s) for _, s in out),
                    names=[self.names[pid] for pid, _ in out]), unknown

    def update(self, team, season, players):
        self.team_games[team] += 1
        n = self.team_games[team]
        a = self.alpha
        for r in players:
            pid, mins, gs = r["player_id"], r["minutes"], r["gmsc"]
            self.names[pid] = r["player"]
            s = self.p.get(pid)
            if s is None:
                s = self.p[pid] = dict(team=team, season=season, min=mins, g=0.0, m=0.0, apps=0, last=n)
            s["min"] = (1 - a) * s["min"] + a * mins if s["apps"] else mins
            s["g"] = (1 - a) * s["g"] + gs
            s["m"] = (1 - a) * s["m"] + mins
            s["team"], s["season"], s["last"] = team, season, n
            s["apps"] += 1


def load_player_games(path=PLAYERS):
    """Player rows grouped by game, in chronological order: play-by-play logs for
    2011-22 (ordered by game id) then ESPN box scores (ordered by date)."""
    games = defaultdict(list)
    paths = [path] + ([ESPN_PLAYERS] if path == PLAYERS and os.path.exists(ESPN_PLAYERS) else [])
    for f in paths:
        for r in csv.DictReader(gzip.open(f, "rt")):
            if float(r["minutes"]) <= 0:
                continue
            order = r.get("date") or ""
            games[(int(r["season"]), int(r["playoffs"]), order, str(r["game_id"]).zfill(12))].append(
                dict(player_id=r["player_id"], player=r["player"], team=r["team"],
                 minutes=float(r["minutes"]), gmsc=float(r["gmsc"]), home=r["home"], away=r["away"],
                     hpts=int(float(r["home_pts"])), apts=int(float(r["away_pts"]))))
    return games


def injury_features(path=PLAYERS):
    """Absence features for every play-by-play game, keyed by
    (season, home, away, home points, away points), plus the final player state."""
    av = Availability()
    feats = {}
    for (season, *_), rows in sorted(load_player_games(path).items()):
        h, a = rows[0]["home"], rows[0]["away"]
        key = (season, h, a, rows[0]["hpts"], rows[0]["apts"])
        played = {r["player_id"] for r in rows}
        mh, ma = av.missing(h, season, played), av.missing(a, season, played)
        feats[key] = dict(inj_min_h=mh["min"], inj_gs_h=mh["gs"], inj_min_a=ma["min"], inj_gs_a=ma["gs"],
                          out_h=mh["names"], out_a=ma["names"])
        av.update(h, season, [r for r in rows if r["team"] == h])
        av.update(a, season, [r for r in rows if r["team"] == a])
    return feats, av


def attach_injuries(games, feats):
    hit = 0
    for g in games:
        f = feats.get((g["season"], g["home"], g["away"], g["hpts"], g["apts"]))
        g["has_inj"] = f is not None
        hit += f is not None
        f = f or dict(inj_min_h=0, inj_gs_h=0, inj_min_a=0, inj_gs_a=0, out_h=[], out_a=[])
        g.update(f)
        # positive = the away side is missing more (good for home)
        g["inj_min_diff"] = g["inj_min_a"] - g["inj_min_h"]
        g["inj_gs_diff"] = g["inj_gs_a"] - g["inj_gs_h"]
    return hit


# -------------------------------------------------------------------------- ratings
class Ratings:
    """Online point ratings. perf learns from margins, mkt from closing spreads.
    If `inj_w` is given, each game's targets are corrected for absences so the
    ratings describe full-strength teams."""

    def __init__(self, k_perf=0.06, k_mkt=0.12, carry=0.6, k_hca=0.002, cap=25.0, inj_w=None):
        self.k_perf, self.k_mkt, self.carry, self.k_hca, self.cap = k_perf, k_mkt, carry, k_hca, cap
        self.inj_w = inj_w
        self.perf, self.mkt, self.last, self.played = {}, {}, {}, {}
        self.hca_perf = self.hca_mkt = 3.0
        self.season = None

    def new_season(self, season):
        for d in (self.perf, self.mkt):
            for t in d:
                d[t] *= self.carry
        self.last, self.played, self.season = {}, {}, season

    def inj_pts(self, g):
        if not self.inj_w:
            return 0.0
        return self.inj_w[0] * g.get("inj_min_diff", 0) + self.inj_w[1] * g.get("inj_gs_diff", 0)

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
            inj_pts=self.inj_pts(g),
            warm=min(self.played.get(h, 0), self.played.get(a, 0)),
            pred_perf=self.perf.get(h, 0) - self.perf.get(a, 0) + self.hca_perf,
            pred_mkt=self.mkt.get(h, 0) - self.mkt.get(a, 0) + self.hca_mkt,
        )

    def update(self, g, f):
        h, a = g["home"], g["away"]
        adj = f["inj_pts"]  # points the absences were worth to the home side
        m = max(min(g["margin"] - adj, self.cap), -self.cap)
        e = m - f["pred_perf"]
        self.perf[h] = self.perf.get(h, 0) + self.k_perf * e
        self.perf[a] = self.perf.get(a, 0) - self.k_perf * e
        self.hca_perf += self.k_hca * e
        e2 = -g["close"] - adj - f["pred_mkt"]
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


def fit_injury_weights(games, params, iters=4):
    """Points per missing minute / per missing Game Score, fitted on the training
    seasons only. Iterated because the ratings themselves depend on the weights."""
    train = [g for g in games if g["season"] in TRAIN_SEASONS]
    w = (0.0, 0.0)
    for _ in range(iters):
        feats, _ = run_ratings(train, **params, inj_w=w)
        rows = [{**g, **f} for g, f in zip(train, feats) if f["warm"] >= 5 and g["has_inj"]]
        cols = ["perf_diff", "mkt_diff", "b2b_home", "b2b_away", "rest_diff", "altitude",
                "inj_min_diff", "inj_gs_diff"]
        beta = fit(rows, cols, ridge=1.0)
        w = (float(beta[7]), float(beta[8]))  # intercept is column 0
    return w


# ------------------------------------------------------------------------ regression
BASE = ["perf_diff", "mkt_diff", "b2b_home", "b2b_away", "rest_diff", "altitude"]
MODELS = {
    "stats": (BASE, False),
    "blend": (BASE + ["open_line"], False),
    "stats+inj": (BASE + ["inj_pts"], True),
    "blend+inj": (BASE + ["inj_pts", "open_line"], True),
}
LOGGED = {("stats+inj", "close", 2): "bets_stats_inj_vs_close_edge2.csv",
          ("blend+inj", "open", 2): "bets_blend_inj_vs_open_edge2.csv"}
MODEL_NAMES = {
    "stats": "Stats only (no injuries)",
    "blend": "Stats + opening line (no injuries)",
    "stats+inj": "Stats + injuries",
    "blend+inj": "Stats + injuries + opening line",
}


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


def profit(res, price=None):
    """Units won on a 1-unit bet at American `price` (default -110)."""
    if res == 0:
        return 0.0
    if res < 0:
        return LOSS
    if not price:
        return WIN
    return 100 / -price if price < 0 else price / 100


def summarize(bets):
    n = len(bets)
    w = sum(b["res"] == 1 for b in bets)
    l = sum(b["res"] == -1 for b in bets)
    p = n - w - l
    units = sum(profit(b["res"], b.get("price")) for b in bets)
    dec = w + l
    pct_ = w / dec if dec else float("nan")
    z = (w - dec * BREAK_EVEN) / math.sqrt(dec * BREAK_EVEN * (1 - BREAK_EVEN)) if dec else float("nan")
    clv = sum(b.get("clv", 0) for b in bets) / n if n else float("nan")
    return dict(n=n, w=w, l=l, p=p, pct=pct_, units=units, roi=units / n if n else float("nan"), z=z, clv=clv)


def build_rows(games):
    """Feature rows for both rating runs (plain and injury-corrected)."""
    params = tune(games)
    inj_w = fit_injury_weights(games, params)
    plain, _ = run_ratings(games, **params)
    injr, _ = run_ratings(games, **params, inj_w=inj_w)
    rows = []
    for g, f0, f1 in zip(games, plain, injr):
        rows.append(dict(g=g, plain={**g, **f0, "open_line": -g["open"]},
                         inj={**g, **f1, "open_line": -g["open"]}, warm=f0["warm"]))
    return params, inj_w, rows


def backtest(games):
    params, inj_w, rows = build_rows(games)
    usable = [r for r in rows if r["warm"] >= 5]
    seasons = sorted({r["g"]["season"] for r in usable})
    test_seasons = [s for s in seasons if s not in TRAIN_SEASONS]

    preds = []
    coefs = defaultdict(dict)
    for s in test_seasons:
        train = [r for r in usable if r["g"]["season"] < s]
        test = [r for r in usable if r["g"]["season"] == s]
        out = [dict(r["inj"]) for r in test]
        for name, (cols, injured) in MODELS.items():
            key = "inj" if injured else "plain"
            beta = fit([r[key] for r in train], cols)
            coefs[s][name] = beta.round(3).tolist()
            p = design([r[key] for r in test], cols) @ beta
            for o, v in zip(out, p):
                o["pred_" + name] = float(v)
        preds += out

    def mae(key):
        return sum(abs(p["margin"] - key(p)) for p in preds) / len(preds)

    acc = {"closing line": mae(lambda p: -p["close"]), "opening line": mae(lambda p: -p["open"])}
    for name in MODELS:
        acc[MODEL_NAMES[name]] = mae(lambda p, n=name: p["pred_" + n])

    results = {}
    bet_log = defaultdict(list)
    for model in MODELS:
        for lk in ("open", "close"):
            for thr in (1, 2, 3, 4, 5):
                bets = []
                for p in preds:
                    if lk == "open" and not p.get("has_open", True):
                        continue  # no opening line recorded for this game
                    line = p[lk]  # home spread
                    edge = p["pred_" + model] + line  # >0: model likes home to cover
                    if abs(edge) < thr:
                        continue
                    side = 1 if edge > 0 else -1
                    b = dict(season=p["season"], date=str(p["date"]), home=p["home"], away=p["away"],
                             side="home" if side > 0 else "away", line=line, edge=round(edge, 2),
                             res=grade(p["margin"], line, side), inj_pts=round(p["inj_pts"], 2),
                             price=(p.get("price") or {}).get(f"{lk}_{'home' if side > 0 else 'away'}"),
                             src=p.get("src", "archive"))
                    if lk == "open":
                        b["clv"] = (p["open"] - p["close"]) * side  # points gained vs close
                        b["res_close"] = grade(p["margin"], p["close"], side)
                    bets.append(b)
                    if (model, lk, thr) in LOGGED:
                        bet_log[(model, lk, thr)].append({**b, "model": model, "pred_margin": round(p["pred_" + model], 2),
                                        "home_out": "; ".join(p["out_h"]), "away_out": "; ".join(p["out_a"])})
                results[(model, lk, thr)] = (summarize(bets), bets)
    return params, inj_w, dict(coefs), acc, results, bet_log, preds


def pct(x):
    return "—" if x != x else f"{100 * x:.1f}%"


def ols_t(X, y):
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    se = np.sqrt(np.diag(e @ e / (len(y) - X.shape[1]) * np.linalg.inv(X.T @ X)))
    return b, b / se


def situational_check(preds):
    names = ["home edge", "home on back-to-back", "away on back-to-back", "rest difference (days)",
             "altitude home", "injury points (model's absence value)"]
    X = np.array([[1, r["b2b_home"], r["b2b_away"], r["rest_diff"], r["altitude"], r["inj_pts"]] for r in preds])
    out = ["| Feature | vs opening line (pts) | t | vs closing line (pts) | t |", "|---|---|---|---|---|"]
    stats = [ols_t(X, np.array([r["margin"] + r[lk] for r in preds])) for lk in ("open", "close")]
    for i, n in enumerate(names):
        out.append(f"| {n} | {stats[0][0][i]:+.2f} | {stats[0][1][i]:+.2f} | {stats[1][0][i]:+.2f} | {stats[1][1][i]:+.2f} |")

    def ats(cond, side):
        w = l = 0
        for r in preds:
            if cond(r):
                v = (r["margin"] + r["close"]) * side
                w, l = w + (v > 0), l + (v < 0)
        return f"{w}-{l} ({pct(w / (w + l))})" if w + l else "—"

    out.append("\nClassic angles, graded at the closing line:\n")
    out.append("| Angle | Record |\n|---|---|")
    out.append(f"| Rested home team vs away team on a back-to-back | {ats(lambda r: r['b2b_away'] and not r['b2b_home'], 1)} |")
    out.append(f"| Rested away team vs home team on a back-to-back | {ats(lambda r: r['b2b_home'] and not r['b2b_away'], -1)} |")
    out.append(f"| Home underdog of 10+ points | {ats(lambda r: r['close'] >= 10, 1)} |")
    out.append(f"| Road favorite | {ats(lambda r: r['close'] > 0, -1)} |")
    out.append(f"| Team missing 4+ points more of players than opponent (bet the healthier side) | "
               f"{ats(lambda r: r['inj_pts'] >= 4, 1)} home / {ats(lambda r: r['inj_pts'] <= -4, -1)} away |")
    return "\n".join(out)


def line_move_check(preds):
    """How much of the absence value is already in the opening line, and how much
    is added between open and close?"""
    X = np.array([[1, r["inj_pts"]] for r in preds])
    b_open, t_open = ols_t(X, np.array([-r["open"] for r in preds]))
    b_move, t_move = ols_t(X, np.array([r["open"] - r["close"] for r in preds]))
    b_res, t_res = ols_t(X, np.array([r["margin"] + r["close"] for r in preds]))
    b_mar, t_mar = ols_t(X, np.array([r["margin"] for r in preds]))
    return ("| Outcome regressed on injury points | Slope | t |\n|---|---|---|\n"
            f"| Actual home margin | {b_mar[1]:.2f} | {t_mar[1]:.1f} |\n"
            f"| Opening line (home expected margin) | {b_open[1]:.2f} | {t_open[1]:.1f} |\n"
            f"| Line move, open to close (toward home) | {b_move[1]:.2f} | {t_move[1]:.1f} |\n"
            f"| Cover margin vs closing line | {b_res[1]:.2f} | {t_res[1]:.1f} |\n")


def write_report(games, params, inj_w, coefs, acc, results, bet_log, preds, hit):
    os.makedirs(OUT, exist_ok=True)
    seasons = sorted({p["season"] for p in preds})
    L = []
    L.append("# NBA spread model backtest\n")
    L.append(f"Archive: {len(games):,} games, seasons {games[0]['season']}-{games[-1]['season'] + 1 - 2000:02d}; "
             f"{hit:,} ({hit / len(games):.1%}) matched to play-by-play player data. "
             f"Ratings and injury weights tuned on {TRAIN_SEASONS[0]}-{TRAIN_SEASONS[-1] + 1 - 2000:02d}; "
             f"walk-forward test on {len(preds):,} games from {seasons[0]}-{seasons[-1] + 1 - 2000:02d}. "
             "All bets assumed at -110 (break-even 52.38%).\n")
    L.append("**Look-ahead caveat:** absences are read from each game's box score. Tests against the closing "
             "line are fair because injury news is almost always out before the close. Tests against the "
             "opening line assume you knew every absence at the open, so treat them as an upper bound.\n")
    L.append(f"Tuned rating parameters: {params}\n")
    L.append(f"Injury weights (points of home margin per unit, away minus home): "
             f"{inj_w[0]:+.3f} per missing rotation minute, {inj_w[1]:+.3f} per missing Game Score point\n")
    L.append("## Forecast accuracy (mean absolute error of home margin, test seasons)\n")
    L.append("| Forecast | MAE (points) |\n|---|---|")
    for k, v in acc.items():
        L.append(f"| {k} | {v:.2f} |")
    L.append("")
    L.append("## DraftKings era: 2022-23 to 2026-27, graded at actual DraftKings prices\n")
    L.append("Out-of-sample seasons not used in any earlier version of this model. Opening-line rows use only "
             "games where ESPN recorded a DraftKings opener.\n")
    L.append("| Model | Bet against | Min edge | Bets | Win % | Units | ROI | z vs 52.38% | Avg CLV (pts) |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for model in MODELS:
        for lk in ("open", "close"):
            for thr in (1, 2, 3):
                _, bets = results[(model, lk, thr)]
                x = summarize([b for b in bets if b.get("src") == "draftkings"])
                clv = f"{x['clv']:+.2f}" if lk == "open" else "—"
                L.append(f"| {MODEL_NAMES[model]} | {lk} | {thr} | {x['n']} | {pct(x['pct'])} | {x['units']:+.1f} | "
                         f"{100 * x['roi']:+.1f}% | {x['z']:+.2f} | {clv} |")
    L.append("")
    L.append("## Is injury news priced?\n")
    L.append(line_move_check(preds))
    for model in MODELS:
        L.append(f"## {MODEL_NAMES[model]}\n")
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
    L.append("## By season: stats + injuries vs closing line, edge ≥ 2\n")
    L.append("| Season | Bets | Win % | Units |\n|---|---|---|---|")
    _, bets = results[("stats+inj", "close", 2)]
    for s in seasons:
        sb = [b for b in bets if b["season"] == s]
        if sb:
            x = summarize(sb)
            L.append(f"| {s}-{s + 1 - 2000:02d} | {x['n']} | {pct(x['pct'])} | {x['units']:+.1f} |")
    L.append("")
    L.append("## Does the line already price the situation?\n")
    L.append("Regression of the cover margin (home margin + home spread) on situational features, "
             "test seasons. A coefficient near 0 means the line already accounts for that factor.\n")
    L.append(situational_check(preds))
    L.append("")
    L.append("## Regression coefficients by test season\n")
    for name, (cols, _) in MODELS.items():
        L.append(f"**{MODEL_NAMES[name]}**: intercept, " + ", ".join(cols) + "\n")
        L.append("| Season | Coefficients |\n|---|---|")
        for s, c in coefs.items():
            L.append(f"| {s} | {c[name]} |")
        L.append("")
    open(os.path.join(OUT, "backtest.md"), "w").write("\n".join(L) + "\n")

    for f in os.listdir(OUT):
        if f.startswith("bets_"):
            os.remove(os.path.join(OUT, f))
    for key, fname in LOGGED.items():
        rows = bet_log[key]
        with open(os.path.join(OUT, fname), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print("\n".join(L))


# --------------------------------------------------------------------------- predict
def predict(csv_path, extra=None):
    """Rate upcoming games. CSV columns: date (YYYY-MM-DD), home, away, open_spread
    (home team's spread, e.g. -4.5), and optionally home_out / away_out: players
    ruled out, separated by ';' (names as on NBA.com). Ratings come from every game in
    the archive (plus `extra`, a JSON file of newer results in the archive's format)."""
    games = load_games(extra=extra)
    feats, av = injury_features()
    attach_injuries(games, feats)
    params, inj_w, rows = build_rows(games)
    usable = [r["inj"] for r in rows if r["warm"] >= 5]
    cols = MODELS["blend+inj"][0]
    beta = fit(usable, cols)
    _, r = run_ratings(games, **params, inj_w=inj_w)
    print(f"Ratings current through {games[-1]['date']}. If that is not yesterday, results are stale.\n")
    print(f"{'date':<11}{'away':<15}{'home':<15}{'line':>6}{'model':>8}{'edge':>7}  pick / notes")
    for row in csv.DictReader(open(csv_path)):
        d = dt.date.fromisoformat(row["date"])
        season = d.year if d.month >= 10 else d.year - 1
        g = dict(season=season, date=d, home=row["home"], away=row["away"], open=float(row["open_spread"]))
        mh, uh = av.missing_by_name(g["home"], season, (row.get("home_out") or "").split(";"))
        ma, ua = av.missing_by_name(g["away"], season, (row.get("away_out") or "").split(";"))
        g["inj_min_diff"] = ma["min"] - mh["min"]
        g["inj_gs_diff"] = ma["gs"] - mh["gs"]
        f = r.features(g)
        x = {**f, "open_line": -g["open"]}
        pred = float((design([x], cols) @ beta)[0])
        edge = pred + g["open"]
        pick = ""
        if abs(edge) >= 2:
            pick = f"{g['home']} {g['open']:+g}" if edge > 0 else f"{g['away']} {-g['open']:+g}"
        notes = []
        if f["inj_pts"]:
            notes.append(f"injuries worth {f['inj_pts']:+.1f} to home")
        if uh or ua:
            notes.append("unknown players: " + ", ".join(sorted(uh | ua)))
        print(f"{row['date']:<11}{g['away']:<15}{g['home']:<15}{g['open']:>+6g}{-pred:>+8.1f}{edge:>+7.1f}  "
              + "  ".join(x for x in [pick] + notes if x))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "backtest"
    if cmd == "backtest":
        games = load_games()
        feats, _ = injury_features()
        hit = attach_injuries(games, feats)
        write_report(games, *backtest(games), hit)
    elif cmd == "predict":
        predict(sys.argv[2], extra=sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        sys.exit(__doc__)
