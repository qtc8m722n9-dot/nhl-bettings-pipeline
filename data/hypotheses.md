# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 14 | 50.0% | 58.2% | -8.2 | -35.6 to +18.6 | +0.4 (14) | -12.1% (14) |
| Neither on b2b (control) | 99 | 44.4% | 53.3% | -8.8 | -18.4 to +0.6 | -0.1 (99) | -21.2% (99) |

Games with a fair moneyline since 2026-11-05: 121; dates 2026-11-05 – 2026-11-21.
