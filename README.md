# risk-monitor

A daily market-risk monitor for a small, EUR-quoted paper portfolio. One
command pulls the latest closing prices, stores them in SQLite, and — as the
layers below are built — recomputes volatility and VaR, checks the result
against limits, and reports any breach.

Built in five layers, each on its own branch with its own commits:

| Layer | What | Status |
|---|---|---|
| 1 | Data — positions and daily closes into SQLite, re-runnable | done |
| 2 | Returns and volatility — log returns, 20-day rolling vol, correlation | next |
| 3 | VaR — historical and parametric, 95% and 99%, one-day | |
| 4 | Limits — a limits table, daily check, breach flags | |
| 5 | Backtest — exception counts, Basel traffic light | |

Personal learning project. Nothing is bought; the portfolio is invented.

## Run

Requires Python 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run risk-monitor
```

The first run fetches two years of history for every ticker in
`positions.csv` (about 5 s). Later runs fetch only what is new. The database
is `prices.db` in the working directory; it is gitignored and can be deleted
and rebuilt at any time.

If a ticker returns no data, the run finishes the others and prints
`No data returned for [...]` at the end.

## Layer 1 — data

`positions.csv` defines the portfolio: 11 positions on Helsinki, Amsterdam
and Xetra, plus two `reference` rows (`^VIX`, `^STOXX`) that are tracked but
not held. `load_positions` reads it into `instruments`; `load_prices` pulls
daily closes from yfinance into `prices`. `schema.sql` is applied on every
connection with `IF NOT EXISTS`, so there is no separate setup step.

### Decisions

- **`prices` is keyed on `(ticker, price_date)` with `ON CONFLICT DO NOTHING`.**
  The composite key *is* the re-runnability rule: a repeated fetch cannot
  create a second row for the same day. First value wins, so a later provider
  revision cannot silently change a number already reported.
- **`instruments` follows the CSV.** Rows are upserted by ticker, so editing a
  name or share count and re-running updates the table. Open: an upsert never
  deletes, so a ticker removed from the CSV stays in `instruments` until the
  database is rebuilt.
- **`shares` is `NULL` for reference rows**, not `1`. A `1` would be a false
  fact that Layer 2 would compute P&L on.
- **Two-year initial window (730 calendar days).** Layer 5 needs a 250-day
  backtest window on top of a 250-day VaR lookback.
- **14-day overlap on later runs.** Each fetch starts 14 days before the
  latest saved date, so a healthy ticker always returns rows and an empty
  result can only mean the provider failed. The overlap is longer than any
  holiday gap; the duplicates it produces are dropped by the primary key.
- **An empty fetch does not stop the run.** The ticker is collected, the
  others still load, and the list is printed and returned at the end.
- **Incremental fetch is not a speed win.** Measured 4.5 s for the full
  two-year load of 12 tickers against 4.0 s for the incremental run: the
  time is 13 HTTP round trips, not row count. The incremental branch saves
  transfer and inserts, not seconds.
- **`value REAL`, not integer cents.** These are measurements consumed as
  ratios, not amounts that must reconcile.
- **Foreign keys on.** `prices.ticker` references `instruments`; the
  connection enables `PRAGMA foreign_keys` every time, because SQLite
  defaults it off per connection.

### Missing days

Row counts differ by exchange over the same window — Helsinki 498, Xetra
503–505, Amsterdam 509 — because each has its own holiday calendar. A date
missing for one ticker and present for another is normal. Three cases to keep
apart:

| Case | Looks like | Handled |
|---|---|---|
| Exchange holiday | one ticker has no row, others do | Layer 2 aligns series — [#1](https://github.com/oskari-nerd/risk-monitor/issues/1) |
| Failed download | whole ticker empty | reported at end of run |
| Delisting | series stops and never resumes | not yet — reported as failed download until a rule exists |

### Data source

yfinance (Yahoo Finance), adjusted closes, daily. Yahoo does not carry
VSTOXX or any other European volatility index, so `^VIX` is the only
implied-vol reference in v1 — a US number next to a EUR portfolio.
`^STOXX` (STOXX Europe 600) is the market benchmark. VSTOXX from a second
source is a v2 item — [#2](https://github.com/oskari-nerd/risk-monitor/issues/2).

## Not in v1

Options or greeks, intraday data, Monte Carlo VaR, a web front end, a second
currency, FX. Each is a v2 that should be refused until Layer 5 works.
