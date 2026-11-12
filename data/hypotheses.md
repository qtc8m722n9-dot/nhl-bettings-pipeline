# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 9 | 66.7% | 58.3% | +8.3 | -22.2 to +35.1 | +0.1 (9) | +10.7% (9) |
| Neither on b2b (control) | 37 | 51.4% | 52.9% | -1.6 | -16.1 to +13.1 | +0.1 (37) | -10.8% (37) |

Games with a fair moneyline since 2026-11-05: 48; dates 2026-11-05 – 2026-11-11.
