# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 11 | 63.6% | 55.9% | +7.8 | -20.2 to +33.9 | +0.5 (11) | +11.9% (11) |
| Neither on b2b (control) | 60 | 40.0% | 53.2% | -13.2 | -24.7 to -1.5 | +0.0 (60) | -31.5% (60) |

Games with a fair moneyline since 2026-11-05: 74; dates 2026-11-05 – 2026-11-14.
