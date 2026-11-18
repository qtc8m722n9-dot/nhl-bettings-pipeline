# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 12 | 58.3% | 57.5% | +0.8 | -29.3 to +27.2 | +0.4 (12) | +2.6% (12) |
| Neither on b2b (control) | 73 | 42.5% | 53.6% | -11.1 | -22.1 to -0.1 | -0.2 (73) | -26.3% (73) |

Games with a fair moneyline since 2026-11-05: 92; dates 2026-11-05 – 2026-11-17.
