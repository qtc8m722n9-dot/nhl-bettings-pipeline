# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 8 | 75.0% | 58.5% | +16.5 | -13.1 to +41.7 | +0.0 (8) | +24.6% (8) |
| Neither on b2b (control) | 32 | 53.1% | 53.4% | -0.2 | -16.2 to +15.3 | +0.1 (32) | -7.1% (32) |

Games with a fair moneyline since 2026-11-05: 42; dates 2026-11-05 – 2026-11-10.
