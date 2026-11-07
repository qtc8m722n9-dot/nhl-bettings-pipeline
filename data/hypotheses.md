# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 3 | 66.7% | 66.2% | +0.4 | – | +0.7 (3) | -6.2% (3) |
| Neither on b2b (control) | 11 | 54.5% | 55.6% | -1.1 | -29.4 to +25.5 | +0.7 (11) | -7.6% (11) |

Games with a fair moneyline since 2026-11-05: 14; dates 2026-11-05 – 2026-11-06.
