# Kalshi resting-order paper test (H20)

Updated 2026-11-18 17:30 UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.

| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |
|---|--:|--:|--:|--:|--:|--:|--:|
| All | 2,870 | 21% | -10.2% | +0.4 | -0.6 | +0.2 | -7.1% |
| ml | 264 | 11% | -39.9% | -1.1 | -2.2 | +0.2 | -9.8% |
| p1_total | 132 | 39% | -16.1% | +0.8 | -0.3 | +0.2 | -6.6% |
| player_points | 2,190 | 22% | -8.7% | +0.5 | -0.5 | +0.1 | -7.1% |
| spread | 152 | 17% | -0.1% | -0.2 | -1.1 | +0.2 | -6.8% |
| total | 132 | 17% | -4.4% | -0.6 | -1.6 | +0.3 | -4.2% |

Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us (adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20).
