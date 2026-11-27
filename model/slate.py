#!/usr/bin/env python3
"""Rank an NBA slate by calibrated spread-cover probability.

  python3 model/slate.py 2026-11-28

For every game on the date it combines:
  - the injury-aware model (ratings + rest + altitude + expected absences),
    trained on every game from 2011-12 through yesterday;
  - the market line: DraftKings via ESPN if posted, otherwise a spread implied by
    the Polymarket moneyline (flagged, much less reliable);
  - ESPN's injury report (Out = 1.0, Doubtful = 0.75, Questionable = 0.5,
    Day-To-Day = 0.35, Probable = 0.1 chance of missing);
  - back-to-backs from yesterday's schedule, including games not yet played;
  - Polymarket public-ticket and whale flow (shown, and used only if the
    flow analysis finds it significant).

Cover probabilities are *calibrated*: a logistic regression, fitted on the
walk-forward backtest, of "home covered the closing spread" on the model's
edge versus that spread. Because the closing line is close to efficient,
the calibration shrinks the model's opinion heavily toward 50%.

Writes model/results/slate_<date>.md
"""
import csv
import datetime as dt
import json
import math
import os
import sys
from statistics import NormalDist

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_espn as E  # noqa: E402
import nba_model as M  # noqa: E402
import polymarket_flow as P  # noqa: E402

STATUS_P = {"out": 1.0, "doubtful": 0.75, "questionable": 0.5, "day-to-day": 0.35, "probable": 0.1}
WHALE_MOVE = 1.96  # pts of DraftKings line move per unit of whale share (flow_analysis.md, t = 5.8)
ML_SIGMA = 11.6  # spread SD used to turn a moneyline probability into a spread (research report)


def logistic_fit(x, y, iters=50):
    X = np.column_stack([np.ones(len(x)), x])
    y = np.asarray(y, float)
    b = np.zeros(2)
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ b))
        W = p * (1 - p)
        H = X.T @ (X * W[:, None]) + 1e-6 * np.eye(2)
        b += np.linalg.solve(H, X.T @ (y - p))
    p = 1 / (1 + np.exp(-X @ b))
    cov = np.linalg.inv(X.T @ (X * (p * (1 - p))[:, None]))
    return b, np.sqrt(np.diag(cov))


def calibrate(preds, model):
    """P(home covers line L) as a function of the model's edge vs. L, fitted on the
    walk-forward backtest. 'open' uses DraftKings openers (2022-26): the honest
    benchmark for a line bet well before tip-off. 'close' uses closing lines."""
    out = {}
    dk = [p for p in preds if p.get("src") == "draftkings"]
    for label, rows, lk in (("open", [p for p in dk if p.get("has_open")], "open"), ("close", dk, "close"),
                            ("close_all", preds, "close")):
        rows = [p for p in rows if p["margin"] + p[lk] != 0]
        x = np.array([p["pred_" + model] + p[lk] for p in rows])
        y = np.array([p["margin"] + p[lk] > 0 for p in rows])
        b, se = logistic_fit(x, y)
        out[label] = dict(b=b.tolist(), se=se.tolist(), n=len(rows))
    return out


def cover_p(b, edge):
    return 1 / (1 + math.exp(-(b[0] + b[1] * edge)))


def espn_injuries(summary, team_abbr_to_nick):
    out = {}
    for t in summary.get("injuries", []):
        nick = E.nick(t["team"]) if "shortDisplayName" in t["team"] else team_abbr_to_nick.get(t["team"]["abbreviation"])
        for i in t.get("injuries", []):
            st = (i.get("status") or "").lower()
            out.setdefault(nick, []).append((i["athlete"]["displayName"], i.get("status"), STATUS_P.get(st, 0.0)))
    return out


def dk_line(eid):
    d = E.get(f"{E.CORE}/events/{eid}/competitions/{eid}/odds", None)
    o = E.parse_odds(d)
    cur = None
    if d and d.get("items"):
        cur = d["items"][0].get("spread")
    line = o.get("close_spread") if o.get("close_spread") is not None else cur
    return line, o


def main(date):
    day = dt.date.fromisoformat(date)
    season = E.season_of(day)
    games = M.load_games()
    feats, av = M.injury_features()
    M.attach_injuries(games, feats)
    games = [g for g in games if g["date"] < day]
    print(f"training on {len(games):,} games through {games[-1]['date']}", flush=True)
    params, inj_w, coefs, acc, results, bet_log, preds = M.backtest(games)
    cal = calibrate(preds, "stats+inj")
    _, _, rows = M.build_rows(games)
    usable = [r["inj"] for r in rows if r["warm"] >= 5]
    cols = M.MODELS["stats+inj"][0]
    beta = M.fit(usable, cols)
    _, R = M.run_ratings(games, **params, inj_w=inj_w)

    # residual SD of the model in the most recent seasons, for the uncalibrated view
    recent = [p for p in preds if p["season"] >= season - 2]
    sd = float(np.std([p["margin"] - p["pred_stats+inj"] for p in recent]))

    board = E.get(f"{E.SITE}/scoreboard?dates={day:%Y%m%d}", None)
    prev = E.get(f"{E.SITE}/scoreboard?dates={day - dt.timedelta(1):%Y%m%d}", None)
    played_yesterday = set()
    for e in (prev or {}).get("events", []):
        for c in e["competitions"][0]["competitors"]:
            played_yesterday.add(E.nick(c["team"]))

    flow_rows = {}
    if os.path.exists(P.OUT):
        for r in csv.DictReader(open(P.OUT)):
            flow_rows[(r["date"], r["home"], r["away"])] = r

    out = []
    for e in board.get("events", []):
        c = e["competitions"][0]
        teams = {x["homeAway"]: x["team"] for x in c["competitors"]}
        home, away = E.nick(teams["home"]), E.nick(teams["away"])
        summ = E.get(f"{E.SITE}/summary?event={e['id']}", None) or {}
        abbr = {teams["home"]["abbreviation"]: home, teams["away"]["abbreviation"]: away}
        inj = espn_injuries(summ, abbr)

        g = dict(season=season, date=day, home=home, away=away, open=0.0, close=0.0)
        for t in (home, away):
            if t in played_yesterday:
                R.last[t] = day - dt.timedelta(1)
        exp_min = {"h": 0.0, "a": 0.0}
        exp_gs = {"h": 0.0, "a": 0.0}
        notes = {home: [], away: []}
        for side, t in (("h", home), ("a", away)):
            roster = av.roster(t, season)
            by_name = {av.names[pid].lower(): s for pid, s in roster.items()}
            for name, status, p_out in inj.get(t, []):
                s = by_name.get(name.lower())
                if s is None or p_out == 0:
                    continue
                exp_min[side] += p_out * s["min"]
                exp_gs[side] += p_out * s["min"] * av.rate(s)
                pts = p_out * (inj_w[0] * s["min"] + inj_w[1] * s["min"] * av.rate(s))
                notes[t].append(f"{name} ({status}, {s['min']:.0f} mpg, ≈{pts:.1f} pts)")
        g["inj_min_diff"] = exp_min["a"] - exp_min["h"]
        g["inj_gs_diff"] = exp_gs["a"] - exp_gs["h"]
        f = R.features(g)
        pred = float((M.design([f], cols) @ beta)[0])

        line, odds = dk_line(e["id"])
        src = "DraftKings"
        slug = f"nba-{P_ABBR[away]}-{P_ABBR[home]}-{date}"
        fl = flow_rows.get((date, home, away))
        live = None
        if fl is None:
            ev = P.get(f"{P.GAMMA}/events?slug={slug}")
            if ev:
                live = P.summarize(ev[0])
                fl = {k: str(v) for k, v in live.items()}
        if line is None and fl and fl.get("pm_home_prob"):
            ph = float(fl["pm_home_prob"])
            if 0.02 < ph < 0.98:
                line = -ML_SIGMA * NormalDist().inv_cdf(ph)
                line = round(line * 2) / 2
                src = "Polymarket moneyline (implied)"
        row = dict(away=away, home=home, tip=e["date"], pred=pred, fair=-pred, line=line, src=src,
                   b2b_home=f["b2b_home"], b2b_away=f["b2b_away"], inj_pts=f["inj_pts"], notes=notes,
                   flow=fl, odds=odds)
        if line is not None:
            edge = pred + line
            # intercept dropped: home/away bias is already in the model; keep only the edge slope
            p_home = cover_p([0, cal["open"]["b"][1]], edge)
            p_close = cover_p([0, max(cal["close"]["b"][1], 0.0)], edge)
            p_raw = NormalDist().cdf(edge / sd)
            row.update(edge=edge, p_home=p_home, p_close=p_close, p_raw=p_raw)
        if fl and fl.get("whale_share_home") not in (None, "", "None"):
            # flow analysis: whale share of +1 preceded a 1.96-pt DraftKings move toward that side
            row["whale_move"] = WHALE_MOVE * float(fl["whale_share_home"])
        out.append(row)

    write(date, out, cal, sd, inj_w, games[-1]["date"])


P_ABBR = {v: k for k, v in P.ABBR.items()}


def write(date, out, cal, sd, inj_w, through):
    sides = []
    for r in out:
        if r["line"] is None:
            continue
        sides.append((r["p_home"], r["p_close"], r["p_raw"], f"{r['home']} {r['line']:+g}", r, 1))
        sides.append((1 - r["p_home"], 1 - r["p_close"], 1 - r["p_raw"], f"{r['away']} {-r['line']:+g}", r, -1))
    sides.sort(key=lambda s: -s[0])
    bo, bc = cal["open"], cal["close"]
    L = [f"# NBA slate {date}: spread cover probabilities\n"]
    L.append(f"Model trained on every game from 2011-12 through {through}. "
             f"Injury weights: {inj_w[0]:+.3f} pts per missing rotation minute, {inj_w[1]:+.3f} per missing Game Score point.\n")
    L.append("**Cover % (bet now)** is calibrated on 2022-26 DraftKings *opening* lines: a logistic fit of real "
             f"outcomes on the model's edge (slope {bo['b'][1]:+.4f} ± {1.96 * bo['se'][1]:.4f} per point, "
             f"n = {bo['n']:,}). It is the right benchmark for betting an early line, but the backtest knew each "
             "game's absences, so it is optimistic. **Cover % (at close)** uses the closing-line fit "
             f"(slope {bc['b'][1]:+.4f} ± {1.96 * bc['se'][1]:.4f}, n = {bc['n']:,}, floored at 0): once the line "
             "has absorbed the news the model has no measurable edge, so every side is ≈ 50%. "
             f"**Raw model %** assumes the model is exactly right with normal errors (SD {sd:.1f} pts) and "
             "overstates confidence; it is shown for reference only.\n")
    L.append("**Whale move** is the DraftKings line move toward that side that this season's Polymarket whale flow "
             "has historically preceded (1.96 pts per unit of whale share, t = 5.8). Whale flow did *not* predict "
             "covers against the closing line, so it is not in the cover %.\n")
    L.append("## Ranked sides\n")
    L.append("| Rank | Side | Line source | Cover % (bet now) | Cover % (at close) | Raw model % | Model fair line | Edge (pts) | Whale move (pts) |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for i, (p, pc, praw, label, r, sgn) in enumerate(sides, 1):
        edge = sgn * r["edge"]
        wm = f"{sgn * r['whale_move']:+.1f}" if r.get("whale_move") is not None else "—"
        L.append(f"| {i} | **{label}** | {r['src']} | {100 * p:.1f}% | {100 * pc:.1f}% | {100 * praw:.1f}% | "
                 f"{r['home']} {r['fair']:+.1f} | {edge:+.1f} | {wm} |")
    missing = [r for r in out if r["line"] is None]
    if missing:
        L.append("\nNo line available yet for: " + ", ".join(f"{r['away']} @ {r['home']}" for r in missing))
    L.append("\n## Game detail\n")
    for r in out:
        L.append(f"### {r['away']} @ {r['home']}\n")
        ln = f"{r['home']} {r['line']:+g} ({r['src']})" if r["line"] is not None else "not posted"
        L.append(f"- Market line: {ln}; model fair line: {r['home']} {r['fair']:+.1f}")
        if r["odds"].get("open_spread") is not None:
            L.append(f"- DraftKings open: {r['home']} {r['odds']['open_spread']:+g}")
        b2b = [t for t, flag in ((r["home"], r["b2b_home"]), (r["away"], r["b2b_away"])) if flag]
        L.append(f"- Back-to-back: {', '.join(b2b) if b2b else 'neither'}")
        L.append(f"- Injury adjustment: {r['inj_pts']:+.1f} pts to {r['home']} (positive = helps home)")
        for t in (r["away"], r["home"]):
            if r["notes"][t]:
                L.append(f"  - {t}: " + "; ".join(r["notes"][t]))
        fl = r["flow"]
        if fl:
            def pc(k):
                v = fl.get(k)
                return f"{100 * float(v):.0f}%" if v not in (None, "", "None") else "—"
            L.append(f"- Polymarket flow (pre-game so far): ${float(fl.get('usd') or 0):,.0f} traded, "
                     f"{fl.get('public_tickets')} public tickets ({pc('public_ticket_home')} on {r['home']}), "
                     f"money {pc('money_home')} on {r['home']}, {fl.get('whales')} whale wallets, "
                     f"whale net ${float(fl.get('whale_net_home') or 0):+,.0f} toward {r['home']}")
        L.append("")
    path = os.path.join(M.OUT, f"slate_{date}.md")
    open(path, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1])
