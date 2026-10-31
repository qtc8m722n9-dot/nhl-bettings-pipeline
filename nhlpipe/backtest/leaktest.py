"""Empirical leak test: re-run picks for sample dates with every byte of data
dated on/after the pick date removed (that night's scores and box scores
blanked, later days dropped, MoneyPuck rows on/after the date dropped) and
check the picks, prices and model probabilities are unchanged.

python -m nhlpipe.backtest.leaktest [N] [seed]    (offline: cached data only)
"""
import copy
import random
import shutil
import sys
from datetime import date

import pandas as pd

from . import nhldata, oddshist
from . import pipeline as PP

KEY = ["method", "pick_no", "market", "selection", "cost", "est_prob", "close_pinnacle"]


def main(n: int = 8, seed: int = 11) -> None:
    orig_load, orig_read, out = nhldata.load_range, pd.read_csv, PP.OUT
    oddshist.get = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("leak test is offline"))
    files = sorted((out / "bets").glob("*.csv"))
    random.seed(seed)
    ok = 0
    for f in sorted(random.sample(files, min(n, len(files)))):
        d = date.fromisoformat(f.stem)

        def load(start, end, fix_names=True, d=d):
            res = {}
            for k, v in orig_load(start, end, fix_names).items():
                if k > d.isoformat():
                    continue
                if k == d.isoformat():
                    v = copy.deepcopy(v)
                    for g in v["games"]:
                        g.update(home_score=None, away_score=None, state="FUT", skaters=[], goalies=[],
                                 p1_home=0, p1_away=0, last_period=None)
                res[k] = v
            return res

        def read(path, *a, d=d, **k):
            df = orig_read(path, *a, **k)
            return df[df["gameDate"] < int(d.strftime("%Y%m%d"))] if "gameDate" in df.columns else df

        PP.nhldata.load_range, PP.pd.read_csv = load, read
        PP.OUT, PP.report = out.parent / "backtest_local", (lambda *a: None)
        try:
            PP.run(d.isoformat(), d.isoformat())
        finally:
            PP.nhldata.load_range, PP.pd.read_csv, PP.OUT = orig_load, orig_read, out
        a = orig_read(f)[KEY].sort_values(["method", "pick_no"]).round(9).reset_index(drop=True)
        b = orig_read(out.parent / "backtest_local" / "bets" / f.name)[KEY].sort_values(["method", "pick_no"]).round(9).reset_index(drop=True)
        same = a.fillna("-").astype(str).equals(b.fillna("-").astype(str))
        ok += same
        print(f"LEAK TEST {d}: {len(a)} picks, identical with all later data removed: {same}")
    shutil.rmtree(out.parent / "backtest_local", ignore_errors=True)
    print(f"{ok}/{min(n, len(files))} dates identical")


if __name__ == "__main__":
    main(*map(int, sys.argv[1:]))
