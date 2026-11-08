# Pre-registered hypotheses

Specs live in `nhlpipe/hypotheses.py` and were written before any game they are judged on. Edge = actual home win rate minus the pick-time fair price, in points; CI = 95% bootstrap.

## H1: away team on a back-to-back (registered 2026-11-05)

Home side vs fair price when only the away team played yesterday. Interim look 2026-12-31; a verdict needs ~400 games.

| Group | Games | Home win | Fair | Edge, pts | 95% CI | Close move, pts (n) | Kalshi ROI (n) |
|---|--:|--:|--:|--:|--:|--:|--:|
| Only away on b2b (H1) | 4 | 75.0% | 68.1% | +6.9 | – | +0.5 (4) | +3.5% (4) |
| Neither on b2b (control) | 21 | 57.1% | 55.8% | +1.4 | -18.2 to +20.2 | +0.5 (21) | -5.0% (21) |

Games with a fair moneyline since 2026-11-05: 26; dates 2026-11-05 – 2026-11-07.
