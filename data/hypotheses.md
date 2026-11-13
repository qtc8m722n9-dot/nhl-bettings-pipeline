# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 11 | 63.6% | 55.9% | +7.8 | -20.2 to +33.9 | +0.5 (11) | +11.9% (11) |
| Neither on b2b (control) | 44 | 50.0% | 53.1% | -3.1 | -16.9 to +10.3 | +0.1 (44) | -13.5% (44) |

Games with a fair moneyline since 2026-11-05: 58; dates 2026-11-05 – 2026-11-12.
