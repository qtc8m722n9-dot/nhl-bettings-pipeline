# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 1 | 100.0% | 80.1% | +19.9 | – | +0.9 (1) | +21.8% (1) |
| Neither on b2b (control) | 10 | 50.0% | 54.0% | -4.0 | -33.5 to +25.1 | +0.6 (10) | -12.2% (10) |

Games with a fair moneyline since 2026-11-05: 11; dates 2026-11-05 – 2026-11-05.
