"""Independent audit of one live slate: ESPN box scores + Kalshi's own
settlements vs data/graded/<date>.csv (nothing from nhlpipe.grade is reused).

fetch (Actions):  python -m nhlpipe.backtest.cli live_audit YYYY-MM-DD
check (offline):  python -m nhlpipe.backtest.live_audit YYYY-MM-DD
"""
import glob
import json
import sys
from pathlib import Path

import pandas as pd

from ..methods import split_legs
from .audit_check import ESPN_AB, _plain

ROOT = Path(__file__).resolve().parents[2] / "data"
ESPN = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl"
KALSHI = "https://api.elections.kalshi.com/trade-api/v2"


def fetch(day: str) -> None:
    from ..http import get_json
    out = ROOT / "backtest" / "audit" / "live" / day
    out.mkdir(parents=True, exist_ok=True)
    sb = get_json(f"{ESPN}/scoreboard", {"dates": day.replace("-", "")})
    for ev in sb.get("events", []):
        (out / f"espn_{ev['id']}.json").write_text(json.dumps(get_json(f"{ESPN}/summary", {"event": ev["id"]})))
    cands = pd.read_csv(ROOT / "picks" / f"{day}_candidates.csv.gz")
    picks = pd.read_csv(ROOT / "picks" / f"{day}.csv")
    ids = set(picks["cand_id"])
    for legs in picks["legs"].dropna():
        ids |= set(split_legs(legs))
    tick = sorted(set(cands.loc[cands["cand_id"].isin(ids), "ticker"].dropna()))
    res = {}
    for t in tick:
        m = get_json(f"{KALSHI}/markets/{t}").get("market", {})
        res[t] = {"status": m.get("status"), "result": m.get("result")}
    (out / "kalshi.json").write_text(json.dumps(res, indent=1))
    print(f"{day}: {len(sb.get('events', []))} ESPN games, {len(res)} Kalshi markets")


def _games(day: str) -> dict:
    out = {}
    for f in glob.glob(str(ROOT / "backtest" / "audit" / "live" / day / "espn_*.json")):
        s = json.load(open(f))
        comp = s["header"]["competitions"][0]
        t = {}
        for c in comp["competitors"]:
            ab = ESPN_AB.get(c["team"]["abbreviation"], c["team"]["abbreviation"])
            t[c["homeAway"]] = (ab, int(c["score"]), int(c["linescores"][0]["displayValue"]))
        pl = {}
        for team in s["boxscore"]["players"]:
            for grp in team["statistics"]:
                if grp["name"] == "goalies":
                    continue
                for a in grp["athletes"]:
                    st = dict(zip(grp["keys"], a["stats"]))
                    pl[_plain(a["athlete"]["displayName"])] = (int(st["goals"]), int(st["assists"]), int(st["shotsTotal"]))
        out[f"{t['away'][0]}@{t['home'][0]}"] = (t, pl)
    return out


def leg_result(c: dict, games: dict, kal: dict) -> tuple[str, str, str]:
    """(ESPN result, Kalshi result or '', detail)."""
    t, pl = games[c["game_key"]]
    (h, hs, h1), (a, as_, a1) = t["home"], t["away"]
    sc, p1, opp = {h: hs, a: as_}, {h: h1, a: a1}, {h: a, a: h}
    m, line, team = c["market"], c.get("line"), c.get("team")
    if m == "ml":
        hit = sc[team] > sc[opp[team]]
    elif m == "spread":
        hit = sc[team] - sc[opp[team]] > line
    elif m == "total":
        hit = hs + as_ > line
    elif m == "team_total":
        hit = sc[team] > line
    elif m == "p1_total":
        hit = h1 + a1 > line
    elif m == "p1_result":
        hit = (h1 == a1) if team == "TIE" else p1[team] > p1[opp[team]]
    else:
        st = pl.get(_plain(c["player"]))
        if st is None:
            return "void?", "", f"{c['player']} not in ESPN box"
        v = {"player_goals": st[0], "player_points": st[0] + st[1], "player_sog": st[2]}[m]
        hit = v > line
    espn = "win" if (hit if c["side"] == "yes" else not hit) else "loss"
    k = ""
    if isinstance(c.get("ticker"), str) and c["ticker"] in kal and kal[c["ticker"]]["result"] in ("yes", "no"):
        k = "win" if kal[c["ticker"]]["result"] == c["side"] else "loss"
    return espn, k, f"{a} {as_}-{hs} {h}, 1P {a1}-{h1}"


def check(day: str) -> pd.DataFrame:
    games = _games(day)
    kal = json.loads((ROOT / "backtest" / "audit" / "live" / day / "kalshi.json").read_text())
    cands = pd.read_csv(ROOT / "picks" / f"{day}_candidates.csv.gz").set_index("cand_id")
    graded = pd.read_csv(ROOT / "graded" / f"{day}.csv")
    rows = []
    for r in graded.to_dict("records"):
        ids = split_legs(r["cand_id"].split("|", 1)[1]) if r["cand_id"].startswith(("parlay|", "entry|")) else [r["cand_id"]]
        legs = [cands.loc[i].to_dict() | {"cand_id": i} for i in ids]
        res = [leg_result(lg, games, kal) for lg in legs]
        espn = [x[0] for x in res]
        kres = [x[1] for x in res]
        ind = "loss" if "loss" in espn else ("win" if all(x == "win" for x in espn) else "CHECK")
        if ind == "win":
            prof = 1 / (r["cost"]) - 1 if len(legs) == 1 or r["cand_id"].startswith("parlay|") else 2.0
        else:
            prof = -1.0 if ind == "loss" else None
        kal_ok = all(k == "" or k == e for k, e in zip(kres, espn))
        rows.append({"method": r["method"], "pick": r["selection"][:55], "graded": r["result"], "espn": ind,
                     "units_graded": round(r["profit"], 4), "units_espn": None if prof is None else round(prof, 4),
                     "kalshi_agrees": kal_ok, "kalshi_legs": sum(1 for k in kres if k),
                     "ok": ind == r["result"] and prof is not None and abs(prof - r["profit"]) < 1e-6 and kal_ok})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    d = check(sys.argv[1])
    print(d.to_string(index=False))
    print(f"\n{d['ok'].sum()}/{len(d)} graded picks confirmed by ESPN"
          f" ({d['kalshi_legs'].sum()} Kalshi legs also checked against Kalshi settlements)")
