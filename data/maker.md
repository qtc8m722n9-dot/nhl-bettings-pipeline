# Kalshi resting-order paper test (H20)

Updated 2026-11-21 13:00 UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.

| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |
|---|--:|--:|--:|--:|--:|--:|--:|
| All | 6,152 | 21% | -7.4% | +0.3 | -0.7 | +0.2 | -6.0% |
| ml | 564 | 16% | -25.1% | -1.0 | -2.0 | +0.4 | -5.0% |
| p1_total | 282 | 40% | -4.6% | +0.5 | -0.5 | +0.3 | -5.5% |
| player_points | 4,714 | 21% | -6.4% | +0.5 | -0.6 | +0.2 | -6.4% |
| spread | 310 | 19% | -3.5% | -0.1 | -1.0 | +0.2 | -3.9% |
| total | 282 | 19% | -7.1% | -0.6 | -1.7 | +0.4 | -4.1% |

Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us (adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20).
