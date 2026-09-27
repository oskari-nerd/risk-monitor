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
2. Returns and volatility — log returns, 20-day rolling vol, correlation matrix ← *in progress, branch `layer-2-returns`*
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

**2026-09-27** — **Layer 2 in progress on `layer-2-returns` (pushed).**
`returns.py`: `load_price_table(conn)` reads `prices`, pivots to dates ×
tickers, `dropna()`; `log_returns(prices)` = `np.log(prices / prices.shift(1))`
then `dropna()`. Verified 515 → 479 aligned dates, returns 478 × 13, 0 NaN.
**#1 decided:** keep only dates where every ticker has a close, before returns
(forward-fill biases correlation down; proxying plants correlation = 1).
Cost 36 dates, driven by Helsinki holidays (17 blanks each), not `^VIX` (13).
README has a Layer 2 decisions section (Claude's). Commits `9cdd836`,
`f89562f`. #1 closes on merge to `main`.

**Resolved:** VALMT.HE +0.110 on 2024-09-25 (22.92 → 25.60) is real — a
large order announcement that day (author's information, not checked against a
second source); `^STOXX` was −0.0011, so it is stock-specific. Keep it: the
kind of day historical VaR must include and parametric VaR underweights —
use it when comparing the two in Layer 3.

13 tickers: 11 positions (7 Helsinki, 3 Xetra, 1 Amsterdam) + `^VIX`,
`^STOXX`. The old "12 tickers" figure was wrong.

Author wrote both functions from skeletons with blanks. Slips: thought the
query was `db.ticker`, thought `dropna` was SQL, first commit bodies had a
vague "because". **No `Co-Authored-By` trailers, ever** (author's rule).

**Open, not blocking:** `EUNL.DE` 12 blanks vs 10 for SAP/MBG on the same
exchange; SAP.DE exactly 0.0 on 2024-09-24 (real or stale?); a ticker removed from the CSV persists in
`instruments`; yfinance 404 logging noise; delisting indistinguishable from a
failed download.

**Next:** 20-day rolling vol — `rolling(20).std()` is new syntax, scaffold it
on a separate example first. Then annualise (√252) → correlation matrix →
portfolio vol from weights (shares × latest close) and covariance. Follow the
teaching rules above: explain first; never give ready-to-paste project code.
