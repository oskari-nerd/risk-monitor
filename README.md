# risk-monitor

Daily market risk monitor for a small EUR-denominated equity portfolio. Pulls
closing prices, computes volatility and Value at Risk, checks the result against
position limits, and flags breaches. A learning project, built in layers.

## Sample output

```
TODO: paste the actual daily report once Layer 4 runs
```

## What it does

- [ ] Layer 1 — daily prices into SQLite, re-runnable
- [ ] Layer 2 — log returns, rolling volatility, correlations
- [ ] Layer 3 — historical and parametric VaR, 95% and 99%, one-day
- [ ] Layer 4 — limits and breach flags
- [ ] Layer 5 — exception backtest

## Running it

```
uv sync
TODO: the command, once there is one
```

Writes `prices.db` in the project root. The database is gitignored — it is
rebuildable from scratch by re-running the fetch.

## Data and caveats

- Prices from Yahoo Finance via `yfinance`, adjusted close.
- EUR-denominated listings only. No FX conversion anywhere, by design.
- Share counts are maintained by hand. Splits are flagged for review, not
  applied automatically.
- Historical VaR applies today's portfolio to past market moves, so position
  history is not stored.

## Design decisions

- Positions stored as share counts rather than euro amounts — TODO: your reason
- Prices stored as TODO: type — TODO: why, and why the integer-cents rule from
  an earlier project does not carry over
- One price per instrument per day, enforced by a constraint rather than by
  application code — TODO: ignore or overwrite on conflict, and why

## Limitations

- End-of-day only. Nothing intraday.
- Equities only — no options, so no greeks and no non-linear risk.
- Single currency.
- VaR says how bad a bad day is, not how bad the worst day gets. Expected
  Shortfall is the fix and is not implemented.

## Next

Layer 2 onwards, in order.
