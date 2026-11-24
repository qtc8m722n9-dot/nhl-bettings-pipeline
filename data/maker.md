# Kalshi resting-order paper test (H20)

Updated 2026-11-24 17:13 UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.

| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |
|---|--:|--:|--:|--:|--:|--:|--:|
| All | 7,200 | 21% | -6.1% | +0.3 | -0.7 | +0.2 | -5.9% |
| ml | 668 | 16% | -22.3% | -0.9 | -1.9 | +0.4 | -5.0% |
| p1_total | 334 | 39% | -9.9% | +0.5 | -0.5 | +0.3 | -5.9% |
| player_points | 5,500 | 21% | -4.5% | +0.5 | -0.6 | +0.2 | -6.3% |
| spread | 364 | 18% | +0.3% | -0.1 | -1.0 | +0.2 | -4.6% |
| total | 334 | 18% | -6.7% | -0.6 | -1.6 | +0.3 | -4.0% |

Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us (adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20).
