# risk-monitor — notes for Claude

Read this first every session. It is derived from the vault-level `CLAUDE.md` in
Obsidian (which is broader and partly stale) and narrowed to this project.

## Me

Finance background, learning to code; active study track is **Market Risk**.
Primary language Python, SQL in progress, statistics coming. Target pace
10 hrs/week. This is a personal learning project, not work.

Personal details (name, email, vault paths) live in `CLAUDE.local.md`, which is
gitignored. Never copy them into this file or into the repo.

## This project

Daily market-risk monitor for a small EUR-quoted paper portfolio, built in five
layers, one branch and one commit set per layer:

1. **Data** — `positions.csv` → `instruments`, yfinance closes → `prices`, SQLite, re-runnable ✓ merged 2026-09-21
2. Returns and volatility — log returns, 20-day rolling vol, correlation matrix ← *next, branch `layer-2-returns`*
3. VaR — historical and parametric, 95% and 99%, one-day; headline 99%
4. Limits and breach flags
5. Backtest — exception counts, Basel traffic light

Repo: https://github.com/oskari-nerd/risk-monitor (public). uv-managed, Python 3.13,
pandas + yfinance. Full spec and progress log: vault note `[[Portfolio Risk Monitor]]`.

## How sessions work

- **Teach, don't solve.** The author writes the code. Default to explanation
  and progressively specific hints; never hand over ready-to-paste project code.
  For a new subject or when the author asks for help, use a signature/return
  table or a commented skeleton with blanks.
- **Keep tutoring lightweight.** Give one meaningful next step at a time. Explain
  routine syntax mistakes directly; ask for predictions when behavior, design, or
  test results are worth reasoning about. Let the author run ordinary checks and
  bring back the result. If hints aren't helping, map the inputs, outputs, or
  error path instead of asking more leading questions.
- **Teach syntax when asked.** Explain the rule with a small example separate
  from this project's code, then let the author apply it. Treat unchecked Study
  Plan concepts as learning goals, not demonstrated skills.
- **Scaffold new tasks.** Explain the purpose, steps, and relevant syntax before
  assigning something the author has not done, even when that syntax appeared in
  another context. Use a separate example; the author writes project-specific code.
- **Build the program first.** Move through the next Layer 1 feature. Use focused
  checks while implementing or fixing problems, without letting optional
  sabotage exercises displace feature work.
- **Sabotage checks.** Once something works, break it on a scratch copy and ask
  whether the test or check would notice. "Passed for the wrong reason" is the
  recurring lesson.
- **Evidence-based check-offs.** A concept or layer is done when the code shows
  it or they pass a quick quiz — not on their word alone.
- **Nudge in context.** Tie work back to the Study Plan and the Market Risk track.
- **Record the why the day it is decided** — commit bodies, README design
  decisions, the vault progress note.
- Concise and direct; minimal preamble. No scheduled or automated tasks.

## Session open / close

**Open:** note the start time. Read `## Status`.

## Status

*Update this at every session close.*

**2026-09-21 (evening)** — **Layer 1 complete and merged to `main`.**
`load_prices()` picks a window per ticker (730-day initial, 14-day overlap
from `MAX(price_date)`, exclusive end = tomorrow), fetches, stores, collects
tickers that return empty, prints and returns the list. `main()` calls it after
`load_positions`. Verified: 12 tickers × ~500 rows from 2024-09-23; a second
run added no rows (composite key + `DO NOTHING`); timed 4.5 s full vs 4.0 s
incremental — round trips dominate, not row count, so incremental is not a
speed win. `^V2TX` (VSTOXX) 404s on Yahoo, which carries no European vol
index; replaced with `^STOXX` (STOXX Europe 600) as EUR market benchmark;
`^VIX` stays. Database rebuilt by hand because the upsert never deletes.
README written (by Claude — docs are Claude's, code is the author's). Commits
`54b4dea` (prices), `3993562` (CSV), `8b23e35` (README), then `.gitignore` +
`CLAUDE.md`, merged `--no-ff` to `main`. Issues: #1 (Layer 2 series alignment
across exchange calendars), #2 (v2: VSTOXX from a second source).

Author wrote all code from skeletons; recurring slips were `=` on a function
call, `str - int` before `fromisoformat`, and `return` indented inside an
`if`. Vim was a hazard: use `-m` flags for commits.

**Open, not blocking:** a ticker removed from the CSV persists in
`instruments` (upsert never deletes; FK consequence for its prices rows);
yfinance's own 404 logging is noise next to the loader's report — silence via
`logging` when convenient; a delisting is currently indistinguishable from a
failed download.

**Next:** Layer 2 on a new branch from `main` (`layer-2-returns`). Start with
a `returns.py` that reads `prices` into a pandas DataFrame (dates × tickers),
decide the alignment rule from #1 *before* computing anything, then log
returns → 20-day rolling vol → annualisation → correlation matrix → portfolio
vol from weights and covariance. Scaffold each as a new subject: pandas
pivot/`pct_change`/`rolling` are unchecked Study Plan concepts. Follow the
teaching rules above: explain first; never give ready-to-paste project code.
