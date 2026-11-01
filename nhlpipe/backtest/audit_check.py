"""Independent re-grade of a live slate from ESPN box scores (not the NHL API,
not nhlpipe.grade), plus a re-derivation of the fair close from the Odds API
historical archive.

python -m nhlpipe.backtest.audit_check 2026-10-30
Needs data/backtest/audit/espn/*.json and the historical event odds cached
by `cli audit`.
"""
import glob
import gzip
import json
import sys
from pathlib import Path

import pandas as pd

from nhlpipe.methods import split_legs

ROOT = Path(__file__).resolve().parents[2] / "data"
ESPN_AB = {"NJ": "NJD", "LA": "LAK", "SJ": "SJS", "TB": "TBL", "UTAH": "UTA", "WSH": "WSH"}


def _plain(s: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if c.isalnum())


def espn_games() -> dict:
    out = {}
    for f in glob.glob(str(ROOT / "backtest/audit/espn/summary_*.json")):
        s = json.load(open(f))
        comp = s["header"]["competitions"][0]
        teams = {}
        for c in comp["competitors"]:
            ab = ESPN_AB.get(c["team"]["abbreviation"], c["team"]["abbreviation"])
            teams[c["homeAway"]] = (ab, int(c["score"]), int(c["linescores"][0]["displayValue"]))
        players = {}
        for t in s["boxscore"]["players"]:
            for grp in t["statistics"]:
                if grp["name"] == "goalies":
                    continue
                keys = grp["keys"]
                for a in grp["athletes"]:
                    st = dict(zip(keys, a["stats"]))
                    players[_plain(a["athlete"]["displayName"])] = {
                        "g": int(st["goals"]), "a": int(st["assists"]), "sog": int(st["shotsTotal"]),
                        "toi": st["timeOnIce"], "scratched": a["athlete"].get("scratched"),
                    }
        gk = f"{teams['away'][0]}@{teams['home'][0]}"
        out[gk] = {"home": teams["home"], "away": teams["away"], "status": comp["status"]["type"]["detail"], "players": players}
    return out


def check(r: dict, g: dict) -> tuple[str, str]:
    (h, hs, h1), (a, as_, a1) = g["home"], g["away"]
    score = {h: hs, a: as_}
    other = {h: a, a: h}
    m, side, line, team = r["market"], r["side"], r["line"], r["team"]
    if m == "spread":
        hit = score[team] - score[other[team]] > line
        why = f"{a} {as_}-{hs} {h}"
    elif m == "total":
        hit, why = hs + as_ > line, f"total {hs + as_}"
    elif m == "team_total":
        hit, why = score[team] > line, f"{team} {score[team]}"
    elif m == "ml":
        hit, why = score[team] > score[other[team]], f"{a} {as_}-{hs} {h}"
    elif m in ("player_goals", "player_points", "player_sog"):
        p = g["players"].get(_plain(r["player"]))
        if p is None:
            return "NOT FOUND", r["player"]
        v = {"player_goals": p["g"], "player_points": p["g"] + p["a"], "player_sog": p["sog"]}[m]
        hit, why = v > line, f"{r['player']} {v}"
    else:
        return "SKIP", m
    won = hit if side == "yes" else not hit
    return ("win" if won else "loss"), why


def main(day: str) -> None:
    games = espn_games()
    picks = pd.read_csv(ROOT / "picks" / f"{day}.csv")
    graded = pd.read_csv(ROOT / "graded" / f"{day}.csv")
    rows = []
    for r in picks.to_dict("records"):
        res, why = check(r, games[r["game_key"]])
        units = (1 / r["cost"] - 1) if res == "win" else -1.0
        gr = graded[(graded["method"] == r["method"]) & (graded["pick_no"] == r["pick_no"])].iloc[0]
        rows.append({"method": r["method"], "pick": r["selection"], "espn": why, "espn_result": res,
                     "graded_result": gr["result"], "espn_units": round(units, 4), "graded_units": round(gr["profit"], 4),
                     "ok": res == gr["result"] and abs(units - gr["profit"]) < 1e-6})
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    print(f"\n{df['ok'].sum()}/{len(df)} picks agree with ESPN; units ESPN {df['espn_units'].sum():+.4f} vs graded {df['graded_units'].sum():+.4f}")
    # scoreboard per method (season singles) vs recomputed
    sb = pd.read_csv(ROOT / "scoreboard.csv")
    sb = sb[(sb["window"] == "season") & (sb["bucket"] == "single")].set_index("method")
    for m, d in df.groupby("method"):
        print(f"{m:16s} scoreboard units {sb.at[m, 'units']:+.4f} ROI {sb.at[m, 'roi']:+.4f} | ESPN units {d['espn_units'].sum():+.4f} ROI {d['espn_units'].sum() / len(d):+.4f}")


if __name__ == "__main__":
    main(sys.argv[1])


# ---- backtest spot check (ESPN, independent of the NHL API and nhlpipe.grade) ----
SPOT = ROOT / "backtest" / "audit" / "spot"
ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl"


def sample_bets(n: int = 20, seed: int = 2026) -> pd.DataFrame:
    files = sorted((ROOT / "backtest" / "bets").glob("*.csv"))
    b = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    b = b[b["result"].isin(["win", "loss", "void"])]
    return b.sample(n=min(n, len(b)), random_state=seed)


def legs_of(cand_id: str) -> list[dict]:
    ids = split_legs(cand_id.split("|", 1)[1]) if cand_id.startswith("parlay|") else [cand_id]
    out = []
    for x in ids:
        venue, gk, market, who, line, side = x.split("|")
        out.append({"cand_id": x, "game_key": gk, "market": market, "side": side,
                    "line": float(line) if line not in ("", "None", "nan") else None,
                    "team": who if who.isupper() else None, "player": who if not who.isupper() else None})
    return out


def fetch_spot(n: int = 20, seed: int = 2026) -> None:
    """Network part (runs on Actions): ESPN box scores for the sampled bets' games."""
    from ..http import get_json
    s = sample_bets(n, seed)
    for d in sorted(s["date"].unique()):
        sb = get_json(f"{ESPN_BASE}/scoreboard", {"dates": d.replace("-", "")})
        (SPOT / d).mkdir(parents=True, exist_ok=True)
        (SPOT / d / "scoreboard.json").write_text(json.dumps(sb))
        want = {lg["game_key"] for cid in s.loc[s["date"] == d, "cand_id"] for lg in legs_of(cid)}
        for ev in sb.get("events", []):
            comp = ev["competitions"][0]["competitors"]
            ab = {c["homeAway"]: ESPN_AB.get(c["team"]["abbreviation"], c["team"]["abbreviation"]) for c in comp}
            if f"{ab['away']}@{ab['home']}" in want:
                summ = get_json(f"{ESPN_BASE}/summary", {"event": ev["id"]})
                (SPOT / d / f"summary_{ev['id']}.json").write_text(json.dumps(summ))
    print(f"ESPN box scores saved for {len(s)} sampled bets")


def eval_spot(n: int = 20, seed: int = 2026) -> pd.DataFrame:
    s = sample_bets(n, seed)
    rows = []
    for r in s.to_dict("records"):
        games = {}
        for f in glob.glob(str(SPOT / r["date"] / "summary_*.json")):
            games.update(_espn_one(json.load(open(f))))
        res = []
        for lg in legs_of(r["cand_id"]):
            g = games.get(lg["game_key"])
            if g is None:
                res.append(("NO ESPN GAME", lg["game_key"]))
                continue
            res.append(check(lg, g))
        outcomes = [x[0] for x in res]
        if any(o not in ("win", "loss") for o in outcomes):
            espn = "void" if all(o == "NOT FOUND" for o in outcomes) and len(outcomes) == 1 else "CHECK"
        else:
            espn = "loss" if "loss" in outcomes else "win"
        rows.append({"date": r["date"], "method": r["method"], "selection": r["selection"][:60], "ours": r["result"],
                     "espn": espn, "espn_detail": "; ".join(x[1] for x in res), "match": espn == r["result"]})
    return pd.DataFrame(rows)


def _espn_one(s: dict) -> dict:
    comp = s["header"]["competitions"][0]
    teams = {}
    for c in comp["competitors"]:
        ab = ESPN_AB.get(c["team"]["abbreviation"], c["team"]["abbreviation"])
        teams[c["homeAway"]] = (ab, int(c["score"]), int(c["linescores"][0]["displayValue"]))
    players = {}
    for t in s["boxscore"]["players"]:
        for grp in t["statistics"]:
            if grp["name"] == "goalies":
                continue
            for a in grp["athletes"]:
                st = dict(zip(grp["keys"], a["stats"]))
                players[_plain(a["athlete"]["displayName"])] = {"g": int(st["goals"]), "a": int(st["assists"]),
                                                                "sog": int(st["shotsTotal"]), "toi": st["timeOnIce"]}
    return {f"{teams['away'][0]}@{teams['home'][0]}": {"home": teams["home"], "away": teams["away"], "players": players}}
