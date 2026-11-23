# Kalshi resting-order paper test (H20)

Updated 2026-11-23 13:31 UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.

| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |
|---|--:|--:|--:|--:|--:|--:|--:|
| All | 6,920 | 21% | -7.5% | +0.3 | -0.7 | +0.2 | -6.0% |
| ml | 640 | 17% | -23.3% | -0.9 | -1.9 | +0.4 | -4.8% |
| p1_total | 320 | 39% | -12.4% | +0.5 | -0.5 | +0.3 | -6.0% |
| player_points | 5,292 | 21% | -5.8% | +0.5 | -0.6 | +0.2 | -6.3% |
| spread | 348 | 18% | -1.8% | -0.1 | -1.0 | +0.2 | -4.4% |
| total | 320 | 18% | -8.3% | -0.5 | -1.6 | +0.3 | -3.9% |

Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us (adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20).
