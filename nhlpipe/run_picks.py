"""Generate tonight's paper picks for every method (the 'pick lock').

Usage: python -m nhlpipe.run_picks [YYYY-MM-DD] [--force]
Reads:  data/slates/<date>.csv, latest data/odds/<date>/<HHMM>/, data/raw/<date>/mp_*.csv.gz
Writes: data/picks/<date>.csv              locked picks (never overwritten without --force)
        data/picks/<date>_candidates.csv.gz every candidate with fair/model probs
        data/picks/<date>_games.csv         model expected goals per game
"""
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from . import candidates, fair, methods, models
from .names import norm

ET = ZoneInfo("America/New_York")
DATA = Path(__file__).resolve().parent.parent / "data"

PICK_COLS = [
    "date", "method", "pick_no", "created_et", "odds_snapshot", "venue", "game_key", "market",
    "selection", "side", "line", "team", "player", "ticker", "price", "cost", "american",
    "est_prob", "est_source", "edge", "stake", "legs", "cand_id",
]


def _latest_odds_dir(day: date) -> Path | None:
    d = DATA / "odds" / day.isoformat()
    snaps = sorted(p for p in d.glob("*") if p.is_dir()) if d.exists() else []
    return snaps[-1] if snaps else None


def backup_games(slate: pd.DataFrame, mp_goalies: pd.DataFrame) -> set[str]:
    """Games where a team starts someone other than its #1 goalie (most ice time)."""
    g = mp_goalies[mp_goalies["situation"] == "all"]
    number1 = g.sort_values("icetime", ascending=False).groupby("team")["name"].first().map(norm).to_dict()
    out = set()
    for r in slate.to_dict("records"):
        for side in ("home", "away"):
            starter = norm(r.get(f"{side}_goalie"))
            status = str(r.get(f"{side}_goalie_status") or "")
            if starter and status in ("Confirmed", "Likely") and starter != number1.get(r[side]):
                out.add(f"{r['away']}@{r['home']}")
    return out


def run(day: date, force: bool = False) -> pd.DataFrame:
    out_dir = DATA / "picks"
    out_dir.mkdir(parents=True, exist_ok=True)
    picks_path = out_dir / f"{day.isoformat()}.csv"
    if picks_path.exists() and not force:
        print(f"Picks for {day} already locked: {picks_path}")
        return pd.read_csv(picks_path)

    slate = pd.read_csv(DATA / "slates" / f"{day.isoformat()}.csv")
    odir = _latest_odds_dir(day)
    if odir is None:
        raise SystemExit(f"No odds snapshot for {day}")
    odds = pd.read_csv(odir / "odds_long.csv") if (odir / "odds_long.csv").exists() else pd.DataFrame()
    km = pd.read_csv(odir / "kalshi.csv") if (odir / "kalshi.csv").exists() else pd.DataFrame()
    raw = DATA / "raw" / day.isoformat()
    mp_t = pd.read_csv(raw / "mp_teams.csv.gz")
    mp_g = pd.read_csv(raw / "mp_goalies.csv.gz")
    mp_s = pd.read_csv(raw / "mp_skaters.csv.gz")

    # only games that haven't started
    slate = slate[slate["game_state"].isin(["FUT", "PRE"])].copy()
    c = candidates.build(slate, odds, km, day)
    if c.empty:
        raise SystemExit("No candidates (no odds for tonight's games?)")

    # fair prices
    table = fair.lookup_table(fair.devig(odds)) if not odds.empty else {}
    fp = [fair.fair_prob(r, table) for r in c.to_dict("records")]
    c["fair_prob"] = [p for p, _ in fp]
    c["fair_source"] = [s for _, s in fp]

    # M3 game model
    lp = models.league_params(mp_t)
    sims, game_rows = {}, []
    for i, g in enumerate(slate.to_dict("records")):
        lh, la = models.team_lambdas(pd.Series(g), lp)
        gk = f"{g['away']}@{g['home']}"
        sims[gk] = (models.simulate(lh, la, seed=i), g["home"], g["away"])
        s = sims[gk][0]
        game_rows.append(
            {"game_key": gk, "lam_home": lh, "lam_away": la,
             "p_home_win": float((s["hf"] > s["af"]).mean()), "exp_total": lh + la}
        )
    c["model_prob"] = [
        (lambda p: None if p is None else (p if r["side"] == "yes" else 1 - p))(
            models.game_prob(r, *sims[r["game_key"]]) if r["game_key"] in sims and r["venue"] == "kalshi" else None
        )
        for r in c.to_dict("records")
    ]

    # M4 shots model
    sk = models.skater_table(mp_s, mp_t, lp)
    c["sog_prob"] = [models.sog_prob(r, sk) for r in c.to_dict("records")]

    bgames = backup_games(slate, mp_g)
    now = datetime.now(ET).isoformat(timespec="seconds")
    frames = []
    for name, fn in methods.METHODS.items():
        res = fn(c, day, bgames) if name == "M2_goalie_news" else fn(c, day)
        if res is None or res.empty:
            continue
        res = res.copy()
        if name != "M5_pickem_entries":  # entries already are 2-pick parlays
            res = pd.concat([res, methods.parlays(res)], ignore_index=True)
        res["method"] = name
        res["pick_no"] = range(1, len(res) + 1)
        frames.append(res)
    picks = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=PICK_COLS)
    picks["date"] = day.isoformat()
    picks["created_et"] = now
    picks["odds_snapshot"] = odir.name
    picks["stake"] = 1.0
    for col in PICK_COLS:
        if col not in picks:
            picks[col] = None
    picks = picks[PICK_COLS]
    picks.to_csv(picks_path, index=False)
    c.to_csv(out_dir / f"{day.isoformat()}_candidates.csv.gz", index=False, compression="gzip")
    pd.DataFrame(game_rows).to_csv(out_dir / f"{day.isoformat()}_games.csv", index=False)

    print(f"{len(c)} candidates, backup-goalie games: {sorted(bgames) or 'none'}")
    for m in methods.METHODS:
        sub = picks[picks["method"] == m]
        print(f"\n{m}: {len(sub)} pick(s)")
        for r in sub.itertuples():
            e = f"edge {r.edge:+.1%}" if pd.notna(r.edge) else ""
            print(f"  {r.venue:10s} {r.game_key:10s} {r.selection:45s} cost {r.cost:.3f} {e}")
    return picks


if __name__ == "__main__":
    args = sys.argv[1:]
    d = next((date.fromisoformat(a) for a in args if a[:2] == "20"), datetime.now(ET).date())
    run(d, force="--force" in args)
