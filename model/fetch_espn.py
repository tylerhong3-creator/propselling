#!/usr/bin/env python3
"""Fetch NBA results, DraftKings opening/closing spreads and box scores from ESPN's
public JSON endpoints, and write them in the formats nba_model.py reads.

  python3 model/fetch_espn.py 2022-10-01 2026-11-26

Writes
  model/data/espn_games.csv          one row per game (scores, open/close spread + prices, total)
  model/data/espn_player_games.csv.gz one row per player per game (minutes, Game Score, +/-)

Raw responses are cached under model/.espn_cache/ (git-ignored) so reruns only
fetch new dates. Regular season, play-in and playoffs only.
"""
import csv
import datetime as dt
import gzip
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".espn_cache")
GAMES_OUT = os.path.join(HERE, "data", "espn_games.csv")
PLAYERS_OUT = os.path.join(HERE, "data", "espn_player_games.csv.gz")
SITE = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
CORE = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba"

# ESPN short display names -> nicknames used in the odds archive
NICK = {"76ers": "Seventysixers", "Trail Blazers": "Trailblazers"}


def get(url, path, refresh=False, tries=4):
    if path and os.path.exists(path) and not refresh:
        return json.load(open(path))
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "propselling-model/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            if path:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                json.dump(d, open(path, "w"))
            return d
        except Exception as e:  # noqa: BLE001 - retry any network error
            if i == tries - 1:
                print("failed", url, e, file=sys.stderr)
                return None
            time.sleep(2 * (i + 1))


def season_of(d):
    return d.year if d.month >= 8 else d.year - 1


def nick(team):
    n = team.get("shortDisplayName") or team["displayName"].split()[-1]
    return NICK.get(n, n)


def scoreboard(day, today):
    path = os.path.join(CACHE, "scoreboard", day.strftime("%Y%m%d") + ".json")
    return get(f"{SITE}/scoreboard?dates={day:%Y%m%d}", path, refresh=(today - day).days < 2)


def american(x):
    try:
        return float(str(x).replace("+", ""))
    except (TypeError, ValueError):
        return None


def game_detail(eid):
    summ = get(f"{SITE}/summary?event={eid}", os.path.join(CACHE, "summary", f"{eid}.json"))
    odds = get(f"{CORE}/events/{eid}/competitions/{eid}/odds", os.path.join(CACHE, "odds", f"{eid}.json"))
    return summ, odds


def parse_odds(odds):
    """DraftKings (or first provider) open/close home spread, prices and total."""
    if not odds or not odds.get("items"):
        return {}
    items = sorted(odds["items"], key=lambda i: (i.get("provider", {}).get("name") != "DraftKings",
                                                  i.get("provider", {}).get("priority", 99)))
    i = items[0]
    h, a = i.get("homeTeamOdds", {}), i.get("awayTeamOdds", {})
    out = dict(book=i.get("provider", {}).get("name"), total=i.get("overUnder"))
    for k in ("open", "close"):
        hp = h.get(k, {}).get("pointSpread", {}).get("american")
        out[f"{k}_spread"] = american(hp)
        out[f"{k}_home_price"] = american(h.get(k, {}).get("spread", {}).get("american"))
        out[f"{k}_away_price"] = american(a.get(k, {}).get("spread", {}).get("american"))
    if out.get("close_spread") is None and i.get("spread") is not None:
        # "spread" is the home line in ESPN's feed
        out["close_spread"] = float(i["spread"])
    return out


def parse_box(summ):
    rows = []
    for team in summ.get("boxscore", {}).get("players", []):
        tname = nick(team["team"])
        st = team["statistics"][0]
        lab = st["labels"]
        for a in st["athletes"]:
            if a.get("didNotPlay") or not a.get("stats"):
                rows.append(dict(team=tname, player_id="espn:" + a["athlete"]["id"],
                                 player=a["athlete"]["displayName"], minutes=0, gmsc=0, pm=0, pts=0,
                                 dnp_reason=a.get("reason") or ""))
                continue
            s = dict(zip(lab, a["stats"]))

            def num(k):
                try:
                    return float(str(s.get(k, "0")).replace("+", "") or 0)
                except ValueError:
                    return 0.0

            def pair(k):
                try:
                    m, n = s.get(k, "0-0").split("-")
                    return float(m), float(n)
                except ValueError:
                    return 0.0, 0.0

            fg, fga = pair("FG")
            ft, fta = pair("FT")
            pts = num("PTS")
            gmsc = (pts + 0.4 * fg - 0.7 * fga - 0.4 * (fta - ft) + 0.7 * num("OREB") + 0.3 * num("DREB")
                    + num("STL") + 0.7 * num("AST") + 0.7 * num("BLK") - 0.4 * num("PF") - num("TO"))
            rows.append(dict(team=tname, player_id="espn:" + a["athlete"]["id"], player=a["athlete"]["displayName"],
                             minutes=num("MIN"), gmsc=round(gmsc, 2), pm=int(num("+/-")), pts=int(pts),
                             dnp_reason=""))
    return rows


def main(start, end):
    start, end = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    today = dt.date.today()
    days = [start + dt.timedelta(n) for n in range((end - start).days + 1)]
    with ThreadPoolExecutor(6) as ex:
        boards = list(ex.map(lambda d: (d, scoreboard(d, today)), days))
    events = []
    for day, sb in boards:
        for e in (sb or {}).get("events", []):
            stype = e.get("season", {}).get("type")
            c = e["competitions"][0]
            if stype not in (2, 3, 5) or c["status"]["type"]["name"] != "STATUS_FINAL":
                continue
            teams = {x["homeAway"]: x for x in c["competitors"]}
            events.append(dict(id=e["id"], date=day, stype=stype, neutral=c.get("neutralSite", False),
                               home=nick(teams["home"]["team"]), away=nick(teams["away"]["team"]),
                               hpts=int(teams["home"]["score"]), apts=int(teams["away"]["score"])))
    print(f"{len(events)} final games; fetching details", flush=True)
    with ThreadPoolExecutor(6) as ex:
        details = list(ex.map(lambda ev: game_detail(ev["id"]), events))

    gcols = ["season", "date", "espn_id", "playoffs", "neutral", "home", "away", "hpts", "apts", "book",
             "open_spread", "close_spread", "open_home_price", "open_away_price", "close_home_price",
             "close_away_price", "total"]
    pcols = ["season", "playoffs", "game_id", "date", "home", "away", "home_pts", "away_pts", "player_id",
             "player", "team", "minutes", "gmsc", "pm", "pts", "dnp_reason"]
    n_lines = 0
    with open(GAMES_OUT, "w", newline="") as gf, gzip.open(PLAYERS_OUT, "wt", newline="") as pf:
        gw, pw = csv.DictWriter(gf, gcols), csv.DictWriter(pf, pcols)
        gw.writeheader()
        pw.writeheader()
        for ev, (summ, odds) in zip(events, details):
            o = parse_odds(odds)
            n_lines += o.get("close_spread") is not None
            season = season_of(ev["date"])
            gw.writerow(dict(season=season, date=ev["date"].isoformat(), espn_id=ev["id"],
                             playoffs=int(ev["stype"] == 3), neutral=int(ev["neutral"]), home=ev["home"],
                             away=ev["away"], hpts=ev["hpts"], apts=ev["apts"],
                             **{k: o.get(k) for k in gcols[9:]}))
            for r in parse_box(summ or {}):
                pw.writerow(dict(season=season, playoffs=int(ev["stype"] == 3), game_id=ev["id"],
                                 date=ev["date"].isoformat(), home=ev["home"], away=ev["away"],
                                 home_pts=ev["hpts"], away_pts=ev["apts"], **r))
    print(f"wrote {len(events)} games ({n_lines} with lines) to {GAMES_OUT}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
