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
- **Commits:** Claude writes the message as a ready `git commit -m … -m …`
  command; the author runs it. Claude never runs `git commit` itself.
- Concise and direct; minimal preamble. No scheduled or automated tasks.

## Session open / close

**Open:** note the start time. Read `## Status`.

## Status

*Update this at every session close.*

**2026-10-11** — **Layer 2: vol, annualising and correlation done;
portfolio vol explained, not started.** Commits `f00bdd1` (`rolling_vol`),
`32ba096` (`annualise_vol` = `daily_vol * np.sqrt(periods)`, default 252),
`b0ac51f` (`correlation_matrix` = `returns.corr()`), **not pushed**. README
bullets for annualising and correlation are uncommitted, with this file.
Verified: rolling vol matches a NumPy recomputation of every window; annual ÷
daily = √252 in every cell; correlation matches `np.corrcoef`, 78 pairs.
**Prediction confirmed:** Nokia–ASML 0.34 > Nokia–Kesko 0.04. Average pairwise
correlation among the 11 positions 0.17; `^VIX` −0.37 to −0.02 against every
position (understated: VIX closes in New York hours after Europe). Correlating
prices instead would give Nokia–ASML 0.89.

`n − 1` re-quiz passed (window 5 → 4 NaN days). The author declined quizzes
and sabotage this session ("I just want to build") after 11 days away: keep
to explanations and prediction-before-check; sabotage stays optional.
Concepts held; Python mechanics were rusty. Slips: parameter named
`rolling_vol` (shadowing again); unsure how a result gets into a function
(call-site binding: `annualise_vol(vol)` puts `vol` into `daily_vol`);
`annualise_vol * np.rolling_vol(periods)`; `returns.pd.dataframe()` →
`returns.dataframe()` → `returns.corr.dataframe()`, because Claude's table said
"returns: DataFrame" and the author read it as a conversion step. Say "already gives
a DataFrame" next time. Claude committed `f00bdd1` itself, against the
agreement; the author kept it, and the rule is now under *How sessions work*.

**2026-09-27** — `load_price_table` (515 → 479 aligned dates) and
`log_returns` (478 × 13, 0 NaN) done, commits `9cdd836`, `f89562f`, pushed.
**#1 decided:** keep only dates where every ticker has a close, before returns
(forward-fill biases correlation down; proxying plants correlation = 1).
Cost 36 dates, driven by Helsinki holidays. #1 closes on merge to `main`.

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
`instruments` (now matters: a sold position would keep its weight); yfinance 404 logging noise; delisting indistinguishable from a
failed download.

**Data length:** prices end 2026-09-21; 478 returns, but Layer 5 needs 500
(250 lookback + 250 backtest). Re-run the Layer 1 load before Layer 5.

**Next:** push. Then portfolio vol in three functions, explained 2026-10-11:
`load_shares(conn)` in `positions.py` (`SELECT ticker, shares FROM instruments
WHERE role = 'position'`, `pd.read_sql(..., index_col="ticker")["shares"]`,
taught on a `books` example) → `position_weights(shares, prices)` (shares ×
`prices.iloc[-1]` for the positions, ÷ total) → `portfolio_vol(returns,
weights)` (`.cov()` on the positions, `w @ cov @ w`, √). `@` aligns on ticker
labels and raises "matrices are not aligned" if the sets differ. Then test the
other prediction: ASML 28–35% of risk (row of the grid ÷ total). Explain
first; never give ready-to-paste project code.
