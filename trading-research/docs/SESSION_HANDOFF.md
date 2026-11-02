# Session handoff (claude.ai session, Nov 1, 2026)

Read `CLAUDE.md` first (rules, layout, commands, what is built). This file carries the conversation history
that is not in the code: what the user asked for, what was decided, what was researched, and what is still open.

## The goal

The user wants Claude to help them become a better trader, run as a recurring routine, and eventually trade through
their Schwab API with more discipline than they have. It started as "pull YouTube transcripts from investors I
follow" and grew into a full top-down research, risk and execution system with a command-center UI.

## What the user decided (their words, condensed)

- Markets: US equities. Longs and shorts. Puts and put spreads are wanted too (the engine does not support options yet).
- Process: top-down, **index, then sector, then stock**, across **macro, technical and fundamental**. At the stock layer:
  balance sheet, guidance, trading volume, management competency. Add investor sentiment from the "loud places" and
  **global news and other key markets** (global indices, rates, FX, commodities) to complete the picture.
- Wants to play the downside as well as the upside, with sizing, entry timing, risk control, profit-taking and loss-cutting rules.
- "Monetize research": the edge is differentiated, timely research, sized and risk-controlled. They want information
  channels that are measured, not trusted.
- Wants Claude to trade via the Schwab API and always take profits. Claude's position (not rejected by the user): Claude
  proposes, deterministic code sizes and gates, the user approves, and exits and risk limits are automated first. See rollout.
- Data must be accurate, well kept, reportable and neat.
- Wants a **command center UI** to see what Claude and the system are doing. **No login for now; add later.** Focus on
  serving the backend and rendering database data correctly. Asked for the proper stack (see `docs/STACK.md`).
- Moving the work to Claude Code now.
- Wants it to run on a routine. They are now on a paid Claude plan, so a scheduled task in Claude is possible, or
  cron/systemd on their own machine once the worker exists.

## Positions Claude took (revisit freely)

1. LLMs read and propose; they never place orders. Transcripts, filings and news are untrusted text.
2. Crowd sentiment is a crowding indicator, not a trigger. YouTube is idea generation (source tier 3) and must be
   re-verified in primary sources (tier 1) before a trade. Score every investor call at 30/90/180 days vs SPY.
3. Most retail active traders underperform indexes and shorts amplify that. Benchmark against SPY after short-term
   taxes and costs; if the process does not beat it, run it as a small sleeve next to an index core.
4. Shorts are not inverted longs: uncapped loss, squeeze and borrow risk, need a catalyst and a forensic case, size smaller.
5. Fixed "always sell at target" tends to cut winners. Default design: scale out at R multiples, then trail by ATR, plus a
   time stop. Backtest the alternatives before trusting any of it.
6. Keep stops and targets resting at the broker, because the Schwab refresh token expires after 7 days (reported by a
   third-party library's docs, verify).
7. Rollout: shadow (now), approval mode, automate exits and limits first, auto-entries only later at a small cap if the journal justifies it.
8. Public-figure lenses (Griffin, Eisman, Visser, State Street) were applied from their well-known styles, not quotes, and not their current positions.

## Research gathered (sources actually opened)

- Knight Capital 2012: [SEC press release](https://www.sec.gov/news/press-release/2013-222). 4M+ orders to fill 212, over $460M lost
  in 45 minutes, 97 unread warning emails, no check of orders out vs in, no hard capital cap, weak deployment controls.
- [FIA automated-trading risk controls](https://fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf):
  max order size (reject if no limit), max position counting working orders, price tolerance, kill switch, halt after repeated fills,
  stale-data checks, daily loss limits with alerts. No numbers given. The risk gate mirrors these.
- Turtle rules via a [secondary write-up](https://www.mql5.com/en/articles/23448): 1% equity per unit, 2xATR stop, add only to winners, channel exits, no profit target.
- [Deflated Sharpe Ratio](https://papers.ssrn.com/abstract=2460551): corrects for selection bias from many trials and non-normal returns.
- [NautilusTrader architecture](https://docs.nautilustrader.io/concepts/architecture.html): shared code across backtest, sandbox and live.
  [QuantConnect framework](https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/overview): alpha, portfolio construction, risk, execution as separate parts.
- Schwab specifics came from a [third-party library page](https://lumibot.lumiwealth.com/brokers.schwab.html), not Schwab.

## Unverified or not retrieved (do not treat as fact)

- `youtube-transcript-api` was never run against live YouTube. Cloud IPs are often blocked; run it from a home machine.
- Kelly criterion and R-multiple sources could not be fetched; the "Kelly as a ceiling, not a target" stance is general knowledge.
- Schwab: approval timing, 7-day token expiry, bracket/OCO support, short selling, sandbox, multi-leg options. Check Schwab's developer portal.
- QuantConnect risk-model details and the Market Access Rule text were not retrievable here.

## Other artifacts

- Playbook (risk rules, scorecard, journal schema, review cadence): `docs/PLAYBOOK.md`, also a live Claude doc titled
  "Trading Research Playbook". Its risk-limit cells are intentionally blank: the user must choose their own numbers.
- A demo screenshot of the command center was sent in the chat (synthetic data).

## Open questions for the user

1. Which investors and YouTube channels to follow, and which sentiment sources are acceptable (official APIs preferred over scraping; X/Twitter API is paid).
2. Their actual risk limits (fill `config/risk.toml`; the engine will not run until `config_reviewed = true`).
3. Account type and Schwab permissions: margin approval, options level, borrow availability for shorts.
4. Price and fundamentals data provider (not chosen; unofficial free feeds can break).
5. Which brief channel (email or Telegram) and which alerts must reach their phone.
6. Whether to schedule the routine in Claude or run it locally with cron/systemd.

## Suggested first prompt for Claude Code

> Read CLAUDE.md, docs/SESSION_HANDOFF.md, docs/PLAYBOOK.md and docs/STACK.md. Run the tests. Then build the worker process
> and the first real collectors (daily prices, VIX and global indices written to market_snapshots derived from one source,
> and SEC EDGAR filings into raw_documents), with an equity snapshot job and a heartbeat. Keep everything in shadow mode,
> keep the hard rules in CLAUDE.md, add tests, and tell me plainly what you verified and what you could not.
