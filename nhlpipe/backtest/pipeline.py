"""2025-26 backtest of M1 sharp price, M3 xG model, M4 shots model.

pull START END   cache NHL days (season start..END), MoneyPuck game logs, and
                 the pick-time odds snapshot (13:50 ET: main markets for the
                 slate + SOG/points props per game) for START..END
run START END    for each date: point-in-time features -> candidates -> the
                 live methods (nhlpipe.methods, unchanged) -> closing snapshot
                 (pulled only for games / markets that were picked) -> grade
                 -> data/backtest/bets/<date>.csv, then report
report           data/backtest/report.md from every bets file

Venues: the bets are priced where they could be placed in the archive:
DraftKings, FanDuel, BetMGM, Caesars, BetRivers, ESPN BET (American odds ->
implied prob), Kalshi (+ taker fee), Underdog / PrizePicks (2-pick
breakeven, as live). Pinnacle is only the fair-price reference.
CLV vs Pinnacle = Pinnacle no-vig close - cost.
"""
import json
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from .. import fair, grade, methods, models
from ..candidates import describe, kalshi_fee
from ..methods import PICKEM_2_PAYOUT
from ..names import norm
from ..nhl_api import lookup_team, team_name_map
from ..odds_api import flatten
from ..pull_odds import american_to_prob
from . import mpdata, nhldata, oddshist
from .features import Season, results_dict

ET = ZoneInfo("America/New_York")
OUT = Path(__file__).resolve().parents[2] / "data" / "backtest"
VENUES = {"draftkings", "fanduel", "betmgm", "williamhill_us", "betrivers", "espnbet", "kalshi", "underdog", "prizepicks"}
PICKEM = {"underdog", "prizepicks"}
PICK_TIME = time(13, 50)
CLOSE_LEAD = timedelta(minutes=2)
PROP_BOOK_MARKETS = {"player_shots_on_goal": "player_sog", "player_points": "player_points"}
RUN = {"M1_sharp_price": methods.m1_sharp, "M3_xg_model": methods.m3_xg, "M4_shots_model": methods.m4_shots}


def _dates(start: str, end: str) -> list[date]:
    a, b = date.fromisoformat(start), date.fromisoformat(end)
    return [a + timedelta(days=i) for i in range((b - a).days + 1)]


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def pick_dt(d: date) -> datetime:
    return datetime.combine(d, PICK_TIME, ET)


def _slate_events(feat: dict, d: date, t_pick: datetime) -> list[dict]:
    """Archive events that start on ET date d, after the pick time."""
    out = []
    for ev in feat.get("data", []) or []:
        st = _utc(ev["commence_time"])
        if st.astimezone(ET).date() == d and st > t_pick:
            out.append(ev)
    return out


# ---------------------------------------------------------------- pull ----
def pull(start: str, end: str) -> None:
    days = _dates(start, end)
    nhldata.pull(nhldata.SEASON_START, days[-1])
    recs = nhldata.load_range(nhldata.SEASON_START, days[-1])
    mpdata.pull_teams()
    gids = {gl["pid"] for r in recs.values() for g in r["games"] for gl in g["goalies"]}
    mpdata.pull_goalies(sorted(gids))
    for d in days:
        t = pick_dt(d)
        try:
            feat = oddshist.featured(_iso(t))
            evs = _slate_events(feat, d, t)
            for ev in evs:
                oddshist.event_odds(ev["id"], _iso(t))
        except oddshist.BudgetExceeded as e:
            print(e)
            break
        print(f"odds {d}: {len(evs)} games at pick time  credits so far {oddshist.SPENT}")
    print("credits:", oddshist.SPENT, oddshist.LAST_HEADERS)


# ----------------------------------------------------------- odds frames --
def odds_frame(responses: list, tmap: dict) -> pd.DataFrame:
    """responses: archive responses, or (response, allowed event ids) pairs so a
    game is only read from the snapshot taken for it (a featured snapshot also
    lists later games, and mixing two snapshots of one market breaks the de-vig)."""
    rows = []
    for item in responses:
        resp, allowed = item if isinstance(item, tuple) else (item, None)
        data = resp.get("data")
        evs = data if isinstance(data, list) else ([data] if isinstance(data, dict) else [])
        for ev in evs:
            if allowed is not None and ev.get("id") not in allowed:
                continue
            for r in flatten(ev, resp.get("timestamp")):
                r["snap_ts"] = resp.get("timestamp")
                rows.append(r)
    od = pd.DataFrame(rows)
    if od.empty:
        return od
    od["home"] = od["home_name"].map(lambda n: lookup_team(n, tmap))
    od["away"] = od["away_name"].map(lambda n: lookup_team(n, tmap))
    od["implied_prob"] = od["price_american"].map(american_to_prob)
    return od


def candidates(od: pd.DataFrame, game_keys: set[str]) -> pd.DataFrame:
    out = []
    for r in od[od["book"].isin(VENUES)].to_dict("records"):
        gk = f"{r['away']}@{r['home']}"
        p = r["implied_prob"]
        if gk not in game_keys or p is None or pd.isna(p):
            continue
        teams = {r["home"], r["away"]}
        c = {"game_key": gk, "venue": r["book"], "ticker": None, "team": None, "player": None, "line": None,
             "american": r["price_american"], "event_id": r["event_id"], "commence_utc": r["commence_utc"],
             "snap_ts": r["snap_ts"]}
        m, pt = r["market"], r["point"]
        if m == "h2h":
            t = lookup_team(r["outcome"], {norm(r["home_name"]): r["home"], norm(r["away_name"]): r["away"]})
            if t not in teams:
                continue
            c.update(market="ml", team=t, side="yes")
        elif m == "spreads":
            t = lookup_team(r["outcome"], {norm(r["home_name"]): r["home"], norm(r["away_name"]): r["away"]})
            if t not in teams or pt is None or pd.isna(pt) or abs(pt) % 1 != 0.5:
                continue
            if pt < 0:
                c.update(market="spread", team=t, line=-pt, side="yes")
            else:  # "+1.5" = the other team does not win by 2+
                c.update(market="spread", team=(teams - {t}).pop(), line=pt, side="no")
        elif m == "totals":
            if pt is None or pd.isna(pt) or float(pt).is_integer():
                continue
            c.update(market="total", line=pt, side="yes" if str(r["outcome"]).lower() == "over" else "no")
        elif m in PROP_BOOK_MARKETS:
            if pt is None or pd.isna(pt) or float(pt).is_integer() or not isinstance(r["player"], str):
                continue
            c.update(market=PROP_BOOK_MARKETS[m], player=r["player"], line=pt,
                     side="yes" if str(r["outcome"]).lower() == "over" else "no")
        else:
            continue
        c["price"] = p
        c["cost"] = p + kalshi_fee(p) if r["book"] == "kalshi" else p
        out.append(c)
    df = pd.DataFrame(out)
    if df.empty:
        return df
    df["player_key"] = df["player"].map(lambda x: norm(x) if isinstance(x, str) else None)
    df["selection"] = [describe(r) for r in df.to_dict("records")]
    df["cand_id"] = [
        f"{r['venue']}|{r['game_key']}|{r['market']}|{r['team'] if isinstance(r['team'], str) else (r['player_key'] or '')}|{r['line']}|{r['side']}"
        for r in df.to_dict("records")
    ]
    return df.sort_values("cost").drop_duplicates("cand_id").reset_index(drop=True)


def _tables(od: pd.DataFrame) -> tuple[dict, dict]:
    """(fair table with consensus fallback, Pinnacle-only table)."""
    if od.empty:
        return {}, {}
    dv = fair.devig(od)
    return fair.lookup_table(dv), fair.lookup_table(dv[dv["book"] == fair.SHARP])


# ------------------------------------------------------------- grading ----
def _grade(pick: dict, legs: list[dict], res: dict) -> tuple[str, float | None, str, str]:
    stake = 1.0
    if not legs:
        result, detail = grade.grade_leg(pick, res)
        profit = {"win": 1 / pick["cost"] - 1, "loss": -1.0, "void": 0.0}.get(result)
        return result, profit, detail, ""
    gl = [grade.grade_leg(lg, res) for lg in legs]
    rs = [x[0] for x in gl]
    if "error" in rs:
        result = "error"
    elif "pending" in rs:
        result = "pending"
    elif "loss" in rs:
        result = "loss"
    elif all(x == "void" for x in rs):
        result = "void"
    else:
        result = "win"
    if result == "win":
        eff = float(np.prod([lg["cost"] for lg, x in zip(legs, rs) if x == "win"]))
        profit = stake * (1 / eff - 1)
    else:
        profit = {"loss": -stake, "void": 0.0}.get(result)
    return result, profit, " | ".join(d for _, d in gl), ",".join(x[0].upper() for x in rs)


# ----------------------------------------------------------------- run ----
def run(start: str, end: str) -> None:
    days = _dates(start, end)
    recs = nhldata.load_range(nhldata.SEASON_START, days[-1])
    names = nhldata.rosters()
    grade._rosters.clear()
    for pid, p in names.items():
        for t in p["teams"]:
            grade._rosters.setdefault(t, set()).add(norm(p["name"]))
    season = Season(recs, pd.read_csv(mpdata.ROOT / f"teams_{mpdata.SEASON}.csv.gz"),
                    pd.read_csv(mpdata.ROOT / f"goalies_{mpdata.SEASON}.csv.gz"))
    all_games = [g for r in recs.values() for g in r["games"]]
    tmap = team_name_map(all_games, [])
    goalie_acc = []
    for d in days:
        rec = recs.get(d.isoformat())
        if not rec or not rec["games"]:
            continue
        t_pick = pick_dt(d)
        sched = [g for g in rec["games"] if _utc(g["start_utc"]) > t_pick]
        if not sched:
            continue
        slate, mp_t, asof = season.slate(d, sched)
        if mp_t.empty or mp_t[mp_t["situation"] == "all"]["games_played"].min() < 3:
            print(f"{d}: skipped (fewer than 3 games of stats for some team)")
            continue
        # goalie projection accuracy (uses results; report only, after the slate is built)
        for g in sched:
            for side in ("home", "away"):
                proj = slate.loc[slate["game_id"] == g["game_id"], f"{side}_goalie_pid"].iloc[0]
                act = [x["pid"] for x in g["goalies"] if x["starter"] and x["team"] == g[side]]
                if act:
                    goalie_acc.append(proj == act[0])

        feat = oddshist.featured(_iso(t_pick))
        evs = _slate_events(feat, d, t_pick)
        props = [oddshist.event_odds(ev["id"], _iso(t_pick)) for ev in evs]
        od = odds_frame([feat] + props, tmap)
        gks = {f"{g['away']}@{g['home']}" for g in sched}
        c = candidates(od, gks)
        if c.empty:
            print(f"{d}: no candidates")
            continue
        table, _ = _tables(od)
        fp = [fair.fair_prob(r, table) for r in c.to_dict("records")]
        c["fair_prob"], c["fair_source"] = [p for p, _ in fp], [s for _, s in fp]
        lp = models.league_params(mp_t)
        sims = {}
        for i, g in enumerate(slate.to_dict("records")):
            lh, la = models.team_lambdas(pd.Series(g), lp)
            sims[f"{g['away']}@{g['home']}"] = (models.simulate(lh, la, seed=i), g["home"], g["away"])
        c["model_prob"] = [
            (lambda p: None if p is None else (p if r["side"] == "yes" else 1 - p))(
                models.game_prob(r, *sims[r["game_key"]]) if r["game_key"] in sims and r["market"] not in methods.PROP_MARKETS else None)
            for r in c.to_dict("records")
        ]
        sk = models.skater_table(season.skaters_asof(d), mp_t, lp)
        c["sog_prob"] = [models.sog_prob(r, sk) for r in c.to_dict("records")]

        picks = []
        for name, fn in RUN.items():
            res = fn(c, d)
            if res is None or res.empty:
                continue
            res = pd.concat([res, methods.parlays(res)], ignore_index=True)
            res["method"] = name
            res["pick_no"] = range(1, len(res) + 1)
            picks.append(res)
        if not picks:
            print(f"{d}: no picks")
            continue
        picks = pd.concat(picks, ignore_index=True)
        cidx = c.set_index("cand_id")

        # closing: pull only what was picked
        legs_all = set()
        for r in picks.to_dict("records"):
            legs_all |= set(str(r["legs"]).split("||")) if isinstance(r.get("legs"), str) else {r["cand_id"]}
        lc = cidx.loc[sorted(legs_all)]
        close_resp = []
        for ct, grp in lc.groupby("commence_utc"):
            t_close = _iso(_utc(ct) - CLOSE_LEAD)
            main_ev = set(grp.loc[~grp["market"].isin(methods.PROP_MARKETS), "event_id"])
            if main_ev:
                close_resp.append((oddshist.featured(t_close), main_ev))
            for eid in sorted(grp.loc[grp["market"].isin(methods.PROP_MARKETS), "event_id"].unique()):
                close_resp.append((oddshist.event_odds(eid, t_close), {eid}))
        cod = odds_frame(close_resp, tmap)
        ctab, ptab = _tables(cod)
        close_ts = {}
        if not cod.empty:
            close_ts = cod.groupby("event_id")["snap_ts"].max().to_dict()

        def closes(cid: str):
            r = cidx.loc[cid].to_dict() | {"cand_id": cid}
            return fair.fair_prob(r, ctab)[0] if ctab else None, fair.fair_prob(r, ptab)[0] if ptab else None

        res_d = results_dict(rec)
        rows = []
        for r in picks.to_dict("records"):
            legs = [cidx.loc[x].to_dict() | {"cand_id": x} for x in str(r["legs"]).split("||")] if isinstance(r.get("legs"), str) else []
            base = legs or [cidx.loc[r["cand_id"]].to_dict() | {"cand_id": r["cand_id"]}]
            cl = [closes(b["cand_id"]) for b in base]
            cf = None if any(x[0] is None for x in cl) else float(np.prod([x[0] for x in cl]))
            cp = None if any(x[1] is None for x in cl) else float(np.prod([x[1] for x in cl]))
            result, profit, detail, legs_res = _grade(r, legs, res_d)
            rows.append({
                "date": d.isoformat(), "method": r["method"], "pick_no": r["pick_no"],
                "bucket": "parlay" if legs else "single", "venue": r["venue"], "game_key": r["game_key"],
                "market": r["market"], "selection": r["selection"], "price": r["price"], "cost": r["cost"],
                "est_prob": r.get("est_prob"), "edge": r.get("edge"),
                "result": result, "profit": profit, "legs_result": legs_res, "detail": detail,
                "close_fair": cf, "clv_fair": None if cf is None else cf - r["cost"],
                "close_pinnacle": cp, "clv_pinnacle": None if cp is None else cp - r["cost"],
                "pick_snap_ts": max(b["snap_ts"] for b in base),
                "first_commence_utc": min(b["commence_utc"] for b in base),
                "close_snap_ts": max((close_ts.get(b["event_id"]) or "") for b in base) or None,
                "feat_mp_max": asof["mp_max_gamedate"], "feat_box_max": asof["box_max_date"],
                "feat_goalie_max": asof["goalie_max_gamedate"], "cand_id": r["cand_id"],
            })
        df = pd.DataFrame(rows)
        (OUT / "bets").mkdir(parents=True, exist_ok=True)
        df.to_csv(OUT / "bets" / f"{d.isoformat()}.csv", index=False)
        print(f"{d}: {len(sched)} games, {len(c)} candidates, {len(df)} bets "
              f"{df['result'].value_counts().to_dict()} units {df['profit'].sum():+.2f}  credits {oddshist.SPENT}")
    if goalie_acc:
        (OUT / "goalie_projection.json").write_text(json.dumps(
            {"dates": f"{start}..{end}", "team_games": len(goalie_acc), "correct": int(sum(goalie_acc))}))
        print(f"projected starter correct {sum(goalie_acc)}/{len(goalie_acc)}")
    print("credits:", oddshist.SPENT, oddshist.LAST_HEADERS)
    report()


# -------------------------------------------------------------- report ----
def _boot(df: pd.DataFrame, col: str, weight: str | None = None, n: int = 2000, seed: int = 7) -> tuple[float, float]:
    """95% CI of a mean, resampling whole dates (bets on one night are not independent)."""
    if df.empty:
        return (np.nan, np.nan)
    groups = [g for _, g in df.groupby("date")]
    rng = np.random.default_rng(seed)
    sums = np.array([g[col].sum() for g in groups])
    dens = np.array([(g[weight].sum() if weight else len(g)) for g in groups], dtype=float)
    idx = rng.integers(0, len(groups), size=(n, len(groups)))
    vals = sums[idx].sum(1) / np.maximum(dens[idx].sum(1), 1e-9)
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def summarize(b: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (bucket, m), g in b.groupby(["bucket", "method"]):
        s = g[g["result"].isin(["win", "loss"])]
        clv = g[g["result"].isin(["win", "loss", "void"])].dropna(subset=["clv_pinnacle"])
        roi_lo, roi_hi = _boot(s, "profit")
        clv_lo, clv_hi = _boot(clv, "clv_pinnacle")
        rows.append({
            "bucket": bucket, "method": m, "bets": len(s), "wins": int((s["result"] == "win").sum()),
            "voids": int((g["result"] == "void").sum()), "units": s["profit"].sum(),
            "roi": s["profit"].mean() if len(s) else np.nan, "roi_lo": roi_lo, "roi_hi": roi_hi,
            "n_clv": len(clv), "clv": clv["clv_pinnacle"].mean() if len(clv) else np.nan, "clv_lo": clv_lo, "clv_hi": clv_hi,
            "beat_close": (clv["clv_pinnacle"] > 0).mean() if len(clv) else np.nan,
            "avg_cost": s["cost"].mean() if len(s) else np.nan,
        })
    return pd.DataFrame(rows)


def _share(x) -> str:
    return "–" if pd.isna(x) else f"{x:.0%}"


def report(*_args) -> None:
    files = sorted((OUT / "bets").glob("*.csv"))
    if not files:
        print("no bets yet")
        return
    b = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    s = summarize(b)
    s.to_csv(OUT / "summary.csv", index=False)
    f = lambda x, d=1: "–" if pd.isna(x) else f"{x * 100:+.{d}f}%"  # noqa: E731
    md = [f"# Backtest 2025-26 · {b['date'].min()} – {b['date'].max()} ({b['date'].nunique()} slates)", "",
          "Flat 1 unit. ROI and CLV with 95% intervals from resampling whole slates. "
          "CLV = Pinnacle no-vig close − cost paid, in percentage points.", ""]
    for bucket, name in (("single", "Singles"), ("parlay", "3-leg parlays")):
        t = s[s["bucket"] == bucket]
        if t.empty:
            continue
        md += [f"## {name}", "", "| Method | Bets | W-L | Units | ROI (95% CI) | CLV vs Pinnacle (95% CI) | Beat close | n CLV | Void |",
               "|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
        for r in t.to_dict("records"):
            md.append(f"| {r['method']} | {r['bets']} | {r['wins']}-{r['bets'] - r['wins']} | {r['units']:+.2f} | "
                      f"{f(r['roi'])} ({f(r['roi_lo'])}, {f(r['roi_hi'])}) | "
                      f"{f(r['clv'], 2)} ({f(r['clv_lo'], 2)}, {f(r['clv_hi'], 2)}) | "
                      f"{_share(r['beat_close'])} | {r['n_clv']} | {r['voids']} |")
        md.append("")
    sg = b[b["bucket"] == "single"]
    md += ["## Singles by venue and market", "", "| Method | Venue | Market | Bets | Units | ROI | CLV |", "|---|---|---|--:|--:|--:|--:|"]
    for (m, v, mk), g in sg.groupby(["method", "venue", "market"]):
        st = g[g["result"].isin(["win", "loss"])]
        md.append(f"| {m} | {v} | {mk} | {len(st)} | {st['profit'].sum():+.2f} | {f(st['profit'].mean())} | {f(g['clv_pinnacle'].mean(), 2)} |")
    gp = OUT / "goalie_projection.json"
    if gp.exists():
        j = json.loads(gp.read_text())
        md += ["", f"Projected starting goalie matched the actual starter in {j['correct']}/{j['team_games']} team-games ({j['dates']})."]
    leak = leak_check(b)
    md += ["", "## Leak checks", ""] + [f"- {k}: {v}" for k, v in leak.items()]
    (OUT / "report.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


def leak_check(b: pd.DataFrame) -> dict:
    ts = pd.to_datetime(b["pick_snap_ts"], utc=True)
    st = pd.to_datetime(b["first_commence_utc"], utc=True)
    cs = pd.to_datetime(b["close_snap_ts"], utc=True)
    day = pd.to_datetime(b["date"])
    pick_lim = [pick_dt(d.date()).astimezone(timezone.utc) for d in day]
    return {
        "pick odds snapshot after 13:50 ET": int((ts > pd.Series(pick_lim, index=b.index)).sum()),
        "pick odds snapshot at/after first game start": int((ts >= st).sum()),
        "closing snapshot at/after game start": int((cs >= st).sum()),
        "bets with no closing snapshot": int(cs.isna().sum()),
        "MoneyPuck team data dated on/after pick date": int((b["feat_mp_max"].astype(str) >= b["date"].str.replace("-", "")).sum()),
        "goalie data dated on/after pick date": int((b["feat_goalie_max"].astype(str) >= b["date"].str.replace("-", "")).sum()),
        "box-score data dated on/after pick date": int((b["feat_box_max"].astype(str) >= b["date"]).sum()),
    }
