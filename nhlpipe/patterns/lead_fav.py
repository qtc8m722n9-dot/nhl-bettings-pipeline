"""The strong-favourite -1.5 + over lead (found after looking at 2025-26, so not yet evidence).

Checks, none using the seasons the lead came from:
  1. 2022-23..2024-25 results (no prices): chi-square test of independence between "favourite wins by 2+"
     and "total over 5.5 / 6.5", by favourite strength. Favourite strength = a point-in-time proxy for the
     moneyline fitted on 2025-26 (logit fair ~ xG share gap, goal-diff gap, last season's xG gap, home).
  2. Mechanism: how many favourite 2+ goal wins include an empty-net goal, by strength band (all seasons).
  3. Priced seasons (2025-26 + live): joint vs product of Pinnacle fair, by band, for reference.
python -m nhlpipe.patterns.lead_fav -> data/patterns/lead_fav_over.md
"""
from datetime import date

import numpy as np
import pandas as pd
from scipy import stats

from .data import DATA, OUT, team_asof
from ..shots2 import pull as spull

BANDS = [0.0, 0.55, 0.60, 0.67, 1.0]
LABELS = ["<55%", "55-60%", "60-67%", "67%+"]


def games_hist() -> pd.DataFrame:
    m = pd.read_csv(DATA / "shots2" / "mp_teams.csv.gz")
    a = m[(m["situation"] == "all") & (m["home_or_away"] == "HOME")].copy()
    a["date"] = pd.to_datetime(a["gameDate"].astype(str)).dt.date
    g = a.rename(columns={"team": "home", "opposingTeam": "away", "goalsFor": "hg", "goalsAgainst": "ag", "gameId": "game_id"})[
        ["game_id", "season", "date", "home", "away", "hg", "ag"]]
    # empty-net goals per team-game from NHL per-game skater stats
    eng = []
    for s in ("20222023", "20232024", "20242025", "20252026", "20262027"):
        st = spull.load_stats(s)
        eng.append(st.groupby(["gameId", "teamAbbrev"])["emptyNetGoals"].sum().reset_index())
    e = pd.concat(eng).rename(columns={"gameId": "game_id"})
    g = g.merge(e.rename(columns={"teamAbbrev": "home", "emptyNetGoals": "h_eng"}), on=["game_id", "home"], how="left")
    g = g.merge(e.rename(columns={"teamAbbrev": "away", "emptyNetGoals": "a_eng"}), on=["game_id", "away"], how="left")
    ta = team_asof(m, list(g["date"]))
    for s in ("home", "away"):
        x = ta[["team", "date", "xg_pct", "gd_pg", "prev_xg_pct", "gp"]].rename(columns={"team": s, "xg_pct": f"{s}_xg", "gd_pg": f"{s}_gd",
                                                                                     "prev_xg_pct": f"{s}_pxg", "gp": f"{s}_gp"})
        g = g.merge(x, on=[s, "date"], how="left")
    g["d_xg"], g["d_gd"], g["d_pxg"] = g["home_xg"] - g["away_xg"], g["home_gd"] - g["away_gd"], g["home_pxg"] - g["away_pxg"]
    g["tie"] = (g["hg"] == g["ag"]).astype(int)                 # MoneyPuck 'all' excludes the shootout goal
    g["total"] = g["hg"] + g["ag"] + g["tie"]                   # books' total: shootout winner +1
    return g[(g["home_gp"] >= 5) & (g["away_gp"] >= 5)]


def proxy_fit(g: pd.DataFrame) -> np.ndarray:
    pr = pd.read_csv(OUT / "games.csv.gz")
    pr = pr[pr["season"] == 2025][["game_id", "ml_home_fair"]]
    j = g.merge(pr, on="game_id")
    X = np.column_stack([np.ones(len(j)), j["d_xg"], j["d_gd"], j["d_pxg"].fillna(0)])
    yl = np.log(j["ml_home_fair"] / (1 - j["ml_home_fair"]))
    beta, *_ = np.linalg.lstsq(X, yl, rcond=None)
    pred = 1 / (1 + np.exp(-(X @ beta)))
    return beta, float(np.corrcoef(pred, j["ml_home_fair"])[0, 1])


def main() -> str:
    g = games_hist()
    beta, r = proxy_fit(g)
    X = np.column_stack([np.ones(len(g)), g["d_xg"], g["d_gd"], g["d_pxg"].fillna(0)])
    ph = 1 / (1 + np.exp(-(X @ beta)))
    g["fav_p"] = np.maximum(ph, 1 - ph)
    fh = ph >= 0.5
    g["margin"] = np.where(fh, g["hg"] - g["ag"], g["ag"] - g["hg"])
    g["fav_eng"] = np.where(fh, g["h_eng"], g["a_eng"])
    g["fav2"] = (g["margin"] >= 2).astype(int)
    g["band"] = pd.cut(g["fav_p"], BANDS, labels=LABELS)
    md = ["# Lead: strong favourite -1.5 + over", "",
          f"Run {date.today().isoformat()}. The lead (2025-26 + live): with favourites priced 60%+ to win, 'favourite by 2+ AND over' "
          "hit 2.7-4 points more than the product of the two fair prices. It was spotted after looking, so it needs data it did "
          "not come from.", "",
          f"Favourite strength for unpriced seasons = a proxy for Pinnacle's moneyline fitted on 2025-26 from point-in-time stats "
          f"(correlation with the real price r = {r:.2f}). Totals count the shootout goal as books do.", "",
          "## 1. Independence test on 2022-23 to 2024-25 (seasons the lead did not come from)", "",
          "Chi-square test of independence between 'favourite wins by 2+' and 'over'. Lift = P(both) / (P(fav 2+) x P(over)); "
          "1.00 = independent; > 1 = they go together, which is what makes the pair worth more than two separately priced legs.", "",
          "| Line | Favourite strength (proxy) | Games | P(fav by 2+) | P(over) | P(both) | Lift | Chi-square p |", "|---|---|--:|--:|--:|--:|--:|--:|"]
    old = g[g["season"].isin([2022, 2023, 2024])]
    for line in (5.5, 6.5):
        for b, q in old.groupby("band", observed=True):
            ov = (q["total"] > line).astype(int)
            both = (q["fav2"] & ov).mean()
            tab = pd.crosstab(q["fav2"], ov)
            p = stats.chi2_contingency(tab)[1] if tab.shape == (2, 2) else np.nan
            md.append(f"| {line} | {b} | {len(q):,} | {q['fav2'].mean():.1%} | {ov.mean():.1%} | {both:.1%} | {both / (q['fav2'].mean() * ov.mean()):.2f} | {p:.3f} |")
    md += ["", "## 2. Mechanism: empty-net goals (all seasons 2022-23 to 2026-27)", "",
           "| Favourite strength | Favourite 2+ goal wins | Share with a favourite ENG | Of those, share where the ENG made it 2+ (won by exactly 2) | Over 5.5 rate when fav scored an ENG | Over 5.5 rate otherwise |",
           "|---|--:|--:|--:|--:|--:|"]
    for b, q in g.groupby("band", observed=True):
        w = q[q["fav2"] == 1]
        e = w[w["fav_eng"] > 0]
        md.append(f"| {b} | {len(w):,} | {(w['fav_eng'] > 0).mean():.1%} | {(e['margin'] == 2).mean():.1%} | "
                  f"{(q.loc[q['fav_eng'] > 0, 'total'] > 5.5).mean():.1%} | {(q.loc[q['fav_eng'] == 0, 'total'] > 5.5).mean():.1%} |")
    md += ["", "ENG per game by season: " + ", ".join(f"{int(s)}-{str(int(s) + 1)[2:]} {((q['h_eng'] + q['a_eng']).mean()):.2f}"
                                                    for s, q in g.groupby("season")) + ".", ""]
    # 3. priced seasons
    G = pd.read_csv(OUT / "games.csv.gz")
    G = G[G["pl_fav"].notna() & G["y_over"].notna() & G["pl_fav_fair"].notna()].copy()
    G["fav_ml"] = np.maximum(G["ml_home_fair"], 1 - G["ml_home_fair"])
    G["band"] = pd.cut(G["fav_ml"], BANDS, labels=LABELS)
    md += ["## 3. Priced seasons (where the lead came from), for reference", "",
           "| Season | Favourite strength (Pinnacle) | Games | Both hit | Product of fair prices | Edge, pts | Lift |", "|---|---|--:|--:|--:|--:|--:|"]
    for (s, b), q in G.groupby(["season", "band"], observed=True):
        yb = (q["y_pl_fav"] * q["y_over"]).mean()
        pp = (q["pl_fav_fair"] * q["over_fair"]).mean()
        md.append(f"| {s}-{str(s + 1)[2:]} | {b} | {len(q)} | {yb:.1%} | {pp:.1%} | {100 * (yb - pp):+.1f} | {yb / pp:.2f} |")
    txt = "\n".join(md) + "\n"
    (OUT / "lead_fav_over.md").write_text(txt)
    return txt


if __name__ == "__main__":
    print(main())
