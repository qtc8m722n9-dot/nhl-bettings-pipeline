# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 13 | 53.8% | 57.0% | -3.2 | -30.5 to +23.9 | +0.3 (13) | -5.3% (13) |
| Neither on b2b (control) | 75 | 42.7% | 53.7% | -11.0 | -21.7 to -0.3 | -0.2 (75) | -25.8% (75) |

Games with a fair moneyline since 2026-11-05: 95; dates 2026-11-05 – 2026-11-18.
