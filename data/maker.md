# Kalshi resting-order paper test (H20)

Updated 2026-11-19 17:31 UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.

| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |
|---|--:|--:|--:|--:|--:|--:|--:|
| All | 5,602 | 21% | -7.2% | +0.3 | -0.7 | +0.2 | -6.1% |
| ml | 516 | 16% | -24.5% | -1.3 | -2.3 | +0.4 | -5.4% |
| p1_total | 258 | 40% | -4.2% | +0.5 | -0.5 | +0.3 | -5.6% |
| player_points | 4,286 | 21% | -6.0% | +0.5 | -0.6 | +0.2 | -6.4% |
| spread | 284 | 19% | -3.4% | -0.2 | -1.1 | +0.3 | -4.5% |
| total | 258 | 18% | -11.8% | -0.7 | -1.7 | +0.4 | -4.1% |

Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us (adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20).
