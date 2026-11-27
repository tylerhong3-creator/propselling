#!/usr/bin/env python3
"""Turn NBA play-by-play into one row per player per game.

Source: stats.nba.com play-by-play as packaged by github.com/shufinskiy/nba_data
(files nbastats_YYYY.tar.xz and nbastats_po_YYYY.tar.xz, YYYY = season start year).

For every player who appears in a game it reconstructs:
  minutes  - from substitutions and period starters
  gmsc     - Hollinger Game Score from the play-by-play box score
  pm       - on-court plus-minus
Players are identified by the stats.nba.com player id.

Usage:
  python3 model/build_player_logs.py DIR_WITH_TAR_XZ_FILES
writes model/data/player_games.csv.gz
"""
import csv
import gzip
import io
import lzma
import os
import sys
import tarfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "player_games.csv.gz")
SEASONS = range(2011, 2022)

# stats.nba.com team id -> nickname used in the odds archive (current franchise names)
TEAM = {
    1610612737: "Hawks", 1610612738: "Celtics", 1610612739: "Cavaliers", 1610612740: "Pelicans",
    1610612741: "Bulls", 1610612742: "Mavericks", 1610612743: "Nuggets", 1610612744: "Warriors",
    1610612745: "Rockets", 1610612746: "Clippers", 1610612747: "Lakers", 1610612748: "Heat",
    1610612749: "Bucks", 1610612750: "Timberwolves", 1610612751: "Nets", 1610612752: "Knicks",
    1610612753: "Magic", 1610612754: "Pacers", 1610612755: "Seventysixers", 1610612756: "Suns",
    1610612757: "Trailblazers", 1610612758: "Kings", 1610612759: "Spurs", 1610612760: "Thunder",
    1610612761: "Raptors", 1610612762: "Jazz", 1610612763: "Grizzlies", 1610612764: "Wizards",
    1610612765: "Pistons", 1610612766: "Hornets",
}
TECHNICAL = {11, 12, 13, 16, 18, 19, 25, 30}  # foul action types that can hit bench players


def clock(s):
    m, sec = s.split(":")
    return int(m) * 60 + int(sec)


def period_len(p):
    return 720 if p <= 4 else 300


def process_game(rows):
    """rows: list of dicts for one game in file order. Returns (meta, players)."""
    home_id = away_id = None
    for r in rows:
        if r["PERSON1TYPE"] == "4" and r["PLAYER1_TEAM_ID"]:
            home_id = int(r["PLAYER1_TEAM_ID"])
        if r["PERSON1TYPE"] == "5" and r["PLAYER1_TEAM_ID"]:
            away_id = int(r["PLAYER1_TEAM_ID"])
        if home_id and away_id:
            break
    if not (home_id and away_id):
        return None

    stat = defaultdict(lambda: defaultdict(float))
    team_of, name_of = {}, {}

    def who(r, i):
        pid, tid = r[f"PLAYER{i}_ID"], r[f"PLAYER{i}_TEAM_ID"]
        if not pid or pid == "0" or not tid or r[f"PERSON{i}TYPE"] not in ("4", "5"):
            return None
        pid = int(pid)
        team_of[pid] = int(tid)
        name_of[pid] = r[f"PLAYER{i}_NAME"]
        return pid

    by_period = defaultdict(list)
    for r in rows:
        by_period[int(r["PERIOD"])].append(r)

    home_score = away_score = 0
    last_shot_team = None
    for p in sorted(by_period):
        evs = by_period[p]
        # starters: players whose first appearance in the period is not a sub-in
        seen, starters = set(), set()
        for r in evs:
            t, a = int(r["EVENTMSGTYPE"]), int(r["EVENTMSGACTIONTYPE"] or 0)
            if t in (9, 12, 13, 18) or (t == 6 and a in TECHNICAL) or t == 11:
                continue
            for i in (1, 2, 3):
                pid = who(r, i)
                if pid is None or pid in seen:
                    continue
                seen.add(pid)
                if not (t == 8 and i == 2):
                    starters.add(pid)
        on = {}  # pid -> clock when they came on
        start = period_len(p)
        for pid in starters:
            on[pid] = start
        for r in evs:
            t = int(r["EVENTMSGTYPE"])
            a = int(r["EVENTMSGACTIONTYPE"] or 0)
            now = clock(r["PCTIMESTRING"])
            desc = (r["HOMEDESCRIPTION"] or "") + " " + (r["VISITORDESCRIPTION"] or "")
            p1, p2, p3 = who(r, 1), who(r, 2), who(r, 3)
            if t == 8 and p1 is not None and p2 is not None:
                if p1 in on:
                    stat[p1]["sec"] += on.pop(p1) - now
                on[p2] = now
                continue
            if t == 1 and p1 is not None:
                pts = 3 if "3PT" in desc else 2
                stat[p1]["pts"] += pts
                stat[p1]["fg"] += 1
                stat[p1]["fga"] += 1
                if p2 is not None:
                    stat[p2]["ast"] += 1
                last_shot_team = team_of[p1]
            elif t == 2 and p1 is not None:
                stat[p1]["fga"] += 1
                if p3 is not None and "BLOCK" in desc:
                    stat[p3]["blk"] += 1
                last_shot_team = team_of[p1]
            elif t == 3 and p1 is not None:
                stat[p1]["fta"] += 1
                if "MISS" not in desc:
                    stat[p1]["pts"] += 1
                    stat[p1]["ft"] += 1
                last_shot_team = team_of[p1]
            elif t == 4 and p1 is not None:
                key = "orb" if team_of[p1] == last_shot_team else "drb"
                stat[p1][key] += 1
            elif t == 5 and p1 is not None:
                stat[p1]["tov"] += 1
                if p2 is not None and "STEAL" in desc:
                    stat[p2]["stl"] += 1
            elif t == 6 and p1 is not None and a not in TECHNICAL:
                stat[p1]["pf"] += 1
            if r["SCORE"]:
                v, h = (int(x) for x in r["SCORE"].split(" - "))
                dh, dv = h - home_score, v - away_score
                if dh or dv:
                    for pid in on:
                        sign = 1 if team_of.get(pid) == home_id else -1
                        stat[pid]["pm"] += sign * (dh - dv)
                home_score, away_score = h, v
        for pid, t0 in on.items():
            stat[pid]["sec"] += t0  # played to the end of the period

    meta = dict(home=TEAM.get(home_id), away=TEAM.get(away_id), home_pts=home_score, away_pts=away_score)
    players = []
    for pid, s in stat.items():
        gmsc = (s["pts"] + 0.4 * s["fg"] - 0.7 * s["fga"] - 0.4 * (s["fta"] - s["ft"]) + 0.7 * s["orb"]
                + 0.3 * s["drb"] + s["stl"] + 0.7 * s["ast"] + 0.7 * s["blk"] - 0.4 * s["pf"] - s["tov"])
        players.append(dict(player_id=pid, player=name_of[pid], team=TEAM.get(team_of[pid]),
                            minutes=round(s["sec"] / 60, 2), gmsc=round(gmsc, 2), pm=int(s["pm"]),
                            pts=int(s["pts"])))
    return meta, players


def read_season(path):
    with lzma.open(path) as xz, tarfile.open(fileobj=xz) as tar:
        member = next(m for m in tar.getmembers() if m.name.endswith(".csv"))
        text = io.TextIOWrapper(tar.extractfile(member), encoding="utf-8")
        game, rows = None, []
        for r in csv.DictReader(text):
            if r["GAME_ID"] != game:
                if rows:
                    yield game, rows
                game, rows = r["GAME_ID"], []
            rows.append(r)
        if rows:
            yield game, rows


def main(src):
    fields = ["season", "playoffs", "game_id", "home", "away", "home_pts", "away_pts",
              "player_id", "player", "team", "minutes", "gmsc", "pm", "pts"]
    n_games = bad = 0
    with gzip.open(OUT, "wt", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for season in SEASONS:
            for po in (0, 1):
                path = os.path.join(src, f"nbastats_{'po_' if po else ''}{season}.tar.xz")
                if not os.path.exists(path):
                    print("missing", path)
                    continue
                for gid, rows in read_season(path):
                    out = process_game(rows)
                    if out is None or not out[0]["home"]:
                        bad += 1
                        continue
                    meta, players = out
                    n_games += 1
                    for pl in players:
                        w.writerow(dict(season=season, playoffs=po, game_id=gid, **meta, **pl))
                print(season, "playoffs" if po else "regular", "done", n_games, flush=True)
    print("games", n_games, "skipped", bad)


if __name__ == "__main__":
    main(sys.argv[1])
