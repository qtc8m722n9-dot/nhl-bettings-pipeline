# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 12 | 58.3% | 57.5% | +0.8 | -29.3 to +27.2 | +0.4 (12) | +2.6% (12) |
| Neither on b2b (control) | 62 | 40.3% | 53.5% | -13.2 | -24.4 to -1.6 | -0.0 (62) | -30.7% (62) |

Games with a fair moneyline since 2026-11-05: 81; dates 2026-11-05 – 2026-11-16.
