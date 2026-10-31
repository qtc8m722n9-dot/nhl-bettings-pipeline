import json, os, time, datetime as dt
import pandas as pd, requests
os.makedirs("probe_out", exist_ok=True)
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0 research"
def g(u, **p):
    r = S.get(u, params=p, timeout=30); time.sleep(0.5); return r.status_code, (r.json() if r.ok else r.text[:500])
def dump(name, obj): json.dump(obj, open(f"probe_out/{name}.json", "w"), indent=1)
N = "https://api-web.nhle.com/v1"
sc, score = g(f"{N}/score/2026-10-30"); dump("score", score)
for gm in score.get("games", [])[:3]:
    gid = gm["id"]
    for kind in ("boxscore", "play-by-play", "landing"):
        dump(f"{gid}_{kind}", g(f"{N}/gamecenter/{gid}/{kind}")[1])
K = "https://api.elections.kalshi.com/trade-api/v2"
picks = pd.read_csv("data/picks/2026-10-30.csv")
tick = sorted(set(picks["ticker"].dropna()))
out = {}
for t in tick:
    out[t] = g(f"{K}/markets/{t}")[1]
dump("kalshi_markets", out)
t = "KXNHLSPREAD-26OCT30WPGFLA-FLA2"
st = int(dt.datetime(2026,10,30,22,30,tzinfo=dt.timezone.utc).timestamp())
dump("candles", {"series": g(f"{K}/series/KXNHLSPREAD/markets/{t}/candlesticks", start_ts=st, end_ts=st+3600, period_interval=1),
                 "hist": g(f"{K}/historical/markets/{t}/candlesticks", start_ts=st, end_ts=st+3600, period_interval=1)})
# one player goal market rules + a game market
