# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 7 | 85.7% | 60.6% | +25.1 | -5.0 to +46.6 | +0.2 (7) | +42.3% (7) |
| Neither on b2b (control) | 23 | 56.5% | 55.2% | +1.4 | -17.7 to +20.2 | +0.4 (23) | -4.6% (23) |

Games with a fair moneyline since 2026-11-05: 32; dates 2026-11-05 – 2026-11-08.
