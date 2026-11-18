# Kalshi resting-order paper test (H20)

Updated 2026-11-18 13:44 UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.

| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |
|---|--:|--:|--:|--:|--:|--:|--:|
| All | 1,486 | 21% | -9.2% | +0.4 | -0.7 | +0.2 | -7.2% |
| ml | 136 | 14% | -58.7% | -1.0 | -1.9 | +0.2 | -8.4% |
| p1_total | 68 | 38% | +4.2% | +0.8 | -0.3 | +0.1 | -4.2% |
| player_points | 1,136 | 22% | -8.6% | +0.5 | -0.6 | +0.2 | -7.1% |
| spread | 78 | 18% | +6.2% | -0.1 | -1.3 | +0.3 | -10.4% |
| total | 68 | 16% | +12.3% | -0.2 | -1.1 | +0.3 | -4.9% |

Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us (adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20).
