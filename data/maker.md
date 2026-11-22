# Kalshi resting-order paper test (H20)

Updated 2026-11-22 16:58 UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.

| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |
|---|--:|--:|--:|--:|--:|--:|--:|
| All | 6,742 | 21% | -8.3% | +0.3 | -0.7 | +0.2 | -6.0% |
| ml | 620 | 17% | -25.6% | -0.9 | -1.9 | +0.4 | -4.8% |
| p1_total | 310 | 39% | -10.2% | +0.5 | -0.5 | +0.3 | -5.9% |
| player_points | 5,164 | 21% | -6.7% | +0.5 | -0.6 | +0.2 | -6.3% |
| spread | 338 | 19% | -3.1% | -0.1 | -1.1 | +0.2 | -4.7% |
| total | 310 | 18% | -6.7% | -0.6 | -1.7 | +0.4 | -3.9% |

Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us (adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20).
