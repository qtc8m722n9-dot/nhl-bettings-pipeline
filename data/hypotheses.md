# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 17 | 47.1% | 58.2% | -11.2 | -35.4 to +12.7 | +0.3 (17) | -19.1% (17) |
| Neither on b2b (control) | 121 | 45.5% | 53.8% | -8.3 | -16.7 to +0.8 | -0.1 (121) | -20.1% (121) |

Games with a fair moneyline since 2026-11-05: 148; dates 2026-11-05 – 2026-11-25.
