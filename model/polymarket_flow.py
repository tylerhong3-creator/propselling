#!/usr/bin/env python3
"""Polymarket betting flow for NBA games: "public" tickets vs "whale" money.

For each NBA game event on Polymarket it pulls every trade on the moneyline and
spread markets placed before tip-off and summarizes who backed which side:

  public_ticket_home  share of small trades (< $100 notional) that backed the home team
                      (the closest analogue to a sportsbook's "bet %")
  money_home          share of all dollars that backed the home team ("money %")
  whale_net_home      net dollars from whale wallets backing home minus away, where a whale
                      is a wallet whose net position in that game is >= $1,000
  whale_share_home    whale_net / whale gross, in [-1, 1]
  pm_home_prob        last pre-game moneyline price for the home team

A trade backs the home team when it BUYS the home outcome or SELLS the away outcome.

  python3 model/polymarket_flow.py 2026-10-20 2026-11-28

Writes model/data/polymarket_flow.csv. Raw trades are cached in model/.pm_cache/.
"""
import csv
import datetime as dt
import gzip
import json
import os
import sys
import time
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".pm_cache")
OUT = os.path.join(HERE, "data", "polymarket_flow.csv")
GAMMA = "https://gamma-api.polymarket.com"
DATA = "https://data-api.polymarket.com/v2"
PUBLIC_MAX = 100.0   # $ notional: trades below this count as public tickets
WHALE_MIN = 1000.0   # $ net per wallet per game to count as a whale

# Polymarket slug abbreviation -> archive nickname
ABBR = {"atl": "Hawks", "bos": "Celtics", "bkn": "Nets", "cha": "Hornets", "chi": "Bulls", "cle": "Cavaliers",
        "dal": "Mavericks", "den": "Nuggets", "det": "Pistons", "gsw": "Warriors", "hou": "Rockets",
        "ind": "Pacers", "lac": "Clippers", "lal": "Lakers", "mem": "Grizzlies", "mia": "Heat", "mil": "Bucks",
        "min": "Timberwolves", "nop": "Pelicans", "nyk": "Knicks", "okc": "Thunder", "orl": "Magic",
        "phi": "Seventysixers", "phx": "Suns", "por": "Trailblazers", "sac": "Kings", "sas": "Spurs",
        "tor": "Raptors", "uta": "Jazz", "was": "Wizards"}


def canon(outcome):
    """Polymarket outcome label -> archive nickname."""
    o = outcome.strip()
    if o.endswith("76ers"):
        return "Seventysixers"
    if o.endswith("Trail Blazers") or o == "Blazers":
        return "Trailblazers"
    return o.split()[-1]


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip", "User-Agent": "propselling-model/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return json.loads(raw)
        except Exception as e:  # noqa: BLE001
            if i == tries - 1:
                print("failed", url, e, file=sys.stderr)
                return None
            time.sleep(2 * (i + 1))


def events(start, end):
    out, offset = [], 0
    for closed in ("true", "false"):
        offset = 0
        while True:
            d = get(f"{GAMMA}/events?tag_slug=nba&closed={closed}&start_date_min={start - dt.timedelta(30)}"
                    f"&limit=50&offset={offset}")
            if not d:
                break
            for e in d:
                p = e["slug"].split("-")
                if len(p) != 6 or p[0] != "nba" or p[1] not in ABBR or p[2] not in ABBR:
                    continue
                day = dt.date(int(p[3]), int(p[4]), int(p[5]))
                if start <= day <= end:
                    out.append(e)
            if len(d) < 50:
                break
            offset += 50
    return out


def trades(cid, final):
    path = os.path.join(CACHE, cid + ".json")
    if final and os.path.exists(path):
        return json.load(open(path))
    rows, cursor = [], None
    for _ in range(200):
        url = f"{DATA}/trades?conditionId={cid}&limit=1000" + (f"&cursor={cursor}" if cursor else "")
        d = get(url)
        if not d:
            break
        rows += d.get("data", [])
        pg = d.get("pagination", {})
        cursor = pg.get("next_cursor")
        if not pg.get("has_more") or not cursor:
            break
    keep = [dict(w=t["proxy_wallet"], side=t["side"], outcome=t["outcome"], size=t["size"], price=t["price"],
                 ts=t["timestamp"]) for t in rows]
    if final:
        os.makedirs(CACHE, exist_ok=True)
        json.dump(keep, open(path, "w"))
    return keep


def summarize(e):
    p = e["slug"].split("-")
    away, home = ABBR[p[1]], ABBR[p[2]]
    start = e.get("startTime") or e.get("endDate")
    tip = dt.datetime.fromisoformat(start.replace("Z", "+00:00")).timestamp() if start else 9e18
    final = bool(e.get("closed"))
    mkts = [m for m in e.get("markets", []) if m.get("sportsMarketType") in ("moneyline", "spreads")]
    tickets = defaultdict(int)
    money = defaultdict(float)
    wallet = defaultdict(float)
    last_ml = (0, None)
    n = 0
    for m in mkts:
        for t in trades(m["conditionId"], final):
            if t["ts"] >= tip:
                continue
            is_home = canon(t["outcome"]) == home
            if canon(t["outcome"]) not in (home, away):
                continue
            backs_home = is_home if t["side"] == "BUY" else not is_home
            usd = t["size"] * t["price"]
            n += 1
            money["home" if backs_home else "away"] += usd
            if usd < PUBLIC_MAX:
                tickets["home" if backs_home else "away"] += 1
            wallet[t["w"]] += usd if backs_home else -usd
            if m.get("sportsMarketType") == "moneyline" and t["ts"] > last_ml[0]:
                last_ml = (t["ts"], t["price"] if is_home else 1 - t["price"])
    whales = {w: v for w, v in wallet.items() if abs(v) >= WHALE_MIN}
    wn, wg = sum(whales.values()), sum(abs(v) for v in whales.values())
    tt = tickets["home"] + tickets["away"]
    mt = money["home"] + money["away"]
    return dict(slug=e["slug"], date=f"{p[3]}-{p[4]}-{p[5]}", home=home, away=away, final=int(final), trades=n,
                usd=round(mt), public_tickets=tt,
                public_ticket_home=round(tickets["home"] / tt, 3) if tt else "",
                money_home=round(money["home"] / mt, 3) if mt else "",
                whales=len(whales), whale_net_home=round(wn), whale_share_home=round(wn / wg, 3) if wg else "",
                pm_home_prob=last_ml[1] if last_ml[1] is not None else "")


def main(start, end):
    start, end = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    evs = events(start, end)
    print(len(evs), "Polymarket NBA game events", flush=True)
    with ThreadPoolExecutor(6) as ex:
        rows = list(ex.map(summarize, evs))
    rows.sort(key=lambda r: (r["date"], r["slug"]))
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", len(rows), "games to", OUT)


if __name__ == "__main__":
    main(*sys.argv[1:3])
