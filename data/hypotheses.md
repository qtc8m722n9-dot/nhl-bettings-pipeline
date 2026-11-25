# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 17 | 47.1% | 58.2% | -11.2 | -35.4 to +12.7 | +0.3 (17) | -19.1% (17) |
| Neither on b2b (control) | 107 | 44.9% | 53.4% | -8.6 | -17.5 to +1.1 | -0.2 (107) | -20.9% (107) |

Games with a fair moneyline since 2026-11-05: 134; dates 2026-11-05 – 2026-11-24.
