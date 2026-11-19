# H22 Six-leg tickets: leg quality vs ticket count (registered 2026-11-19, Evan approved; live from the 2026-11-20 lock)

Evan's idea: many 6-leg tickets of ~60% legs, so that most nights one ticket hits and pays back the day.
Two paper methods (`nhlpipe/tickets.py`), 1 unit per ticket:
- T1_tickets_fair: as many 6-leg tickets as possible from legs with Pinnacle fair 55-65% priced AT OR BETTER than
  fair (best edge first). Typically 0-3 tickets a night.
- T2_tickets_all20: 20 six-leg tickets from ALL priced 55-65% legs, any price, random order.
Both: no leg reused, one leg per game per ticket (so nights with fewer than 6 games produce no tickets), the same
bet at several venues counted once at the cheapest price, PrizePicks excluded; price = product of leg prices.
Expectation before any result (from the 2026-11-17 and 11-19 replays): T1 tickets priced ~+10-18% above fair,
T2 ~-20%. Primary: ROI per ticket, T1 vs T2, and the share of nights where ticket returns >= stakes.
Look at 30 qualifying nights; verdict at 60.
