# Kalshi resting-order paper test (H20)

Updated 2026-11-28 13:22 UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.

| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |
|---|--:|--:|--:|--:|--:|--:|--:|
| All | 8,462 | 21% | -7.2% | +0.3 | -0.7 | +0.2 | -5.6% |
| ml | 788 | 17% | -23.5% | -0.9 | -1.9 | +0.4 | -4.1% |
| p1_total | 394 | 37% | -7.8% | +0.5 | -0.5 | +0.3 | -5.2% |
| player_points | 6,462 | 20% | -5.6% | +0.5 | -0.6 | +0.1 | -5.9% |
| spread | 424 | 17% | +0.3% | -0.1 | -1.0 | +0.2 | -4.4% |
| total | 394 | 19% | -12.7% | -0.5 | -1.5 | +0.3 | -3.9% |

Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us (adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20).
