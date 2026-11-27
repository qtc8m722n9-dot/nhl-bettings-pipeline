# Kalshi resting-order paper test (H20)

Updated 2026-11-27 17:22 UTC. Bid = Pinnacle fair at the lock minus 1 cent; filled only if the market traded or was offered strictly through the bid before the start. ROI on 1 unit per bet.

| Market | Market sides | Fill rate | Fills: ROI at maker cost | Fills: avg CLV vs close, pts | Fills: fair drift lock->close, pts | Not filled: fair drift, pts | All sides bought at the ask (taker): ROI |
|---|--:|--:|--:|--:|--:|--:|--:|
| All | 7,872 | 21% | -6.6% | +0.3 | -0.7 | +0.2 | -5.7% |
| ml | 728 | 16% | -20.0% | -0.9 | -1.9 | +0.4 | -4.8% |
| p1_total | 364 | 38% | -11.2% | +0.5 | -0.5 | +0.3 | -5.4% |
| player_points | 6,022 | 21% | -5.0% | +0.5 | -0.6 | +0.1 | -6.0% |
| spread | 394 | 18% | -2.0% | -0.1 | -1.0 | +0.2 | -3.5% |
| total | 364 | 19% | -8.2% | -0.5 | -1.5 | +0.3 | -4.0% |

Reading it: a negative 'fills: fair drift' means our bids mostly fill when the price is about to move against us (adverse selection). The test works if fills' CLV stays positive after that. Verdict at 300 fills (H20).
