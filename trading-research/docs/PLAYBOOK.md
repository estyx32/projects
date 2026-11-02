# Trading Research Playbook

Exported from the Claude doc "Trading Research Playbook" on 2026-11-01.

Fill in the risk rules first, score every idea on the scorecard, and log every trade, so research quality can be measured against results and benchmarked to SPY. Research tooling only, not financial advice.

## Risk rules

Write every limit below before the first trade. Claude flags breaches against these numbers and never overrides them; execution stays manual. The right column holds common reference points, not recommendations.

| Rule | Your limit | Common reference point |
| --- | --- | --- |
| Max loss per trade (% of account) | \_\_\_\_ | 0.5–1% |
| Max long position size (% of account) | \_\_\_\_ | 5–10% |
| Max short position size (% of account) | \_\_\_\_ | About half the long limit |
| Max total short exposure (% of account) | \_\_\_\_ | Set low while learning |
| Max gross exposure (longs + shorts) | \_\_\_\_ | Keep a cash buffer |
| Max net exposure / portfolio beta | \_\_\_\_ | Tie to the index regime |
| Max single-sector exposure | \_\_\_\_ | 25–30% |
| Short interest ceiling for new shorts (% of float) | \_\_\_\_ | Your squeeze threshold |
| Hold through earnings? | Yes / No per trade | Decide explicitly each time |
| Options: max premium at risk (all open puts) | \_\_\_\_ | Premium is the full loss |
| Options: expiry buffer past the catalyst | \_\_\_\_ | Weeks, not days |
| Drawdown circuit breaker | At \_\_\_\_% down, halve size or pause | Decide the trigger in advance |
| Invalidation level | Set at entry, never moved wider | Fixed |

In a risk-off index regime, longs need a higher bar. In a risk-on regime, shorts need one.

## Trade scorecard

Score every idea top-down before it becomes a trade. No variant view and no invalidation level means no trade. Copy this table once per ticker; for shorts and puts, fill the short-specific rows too.

| Layer | Question | Evidence (cite the source) | Score (-2 to +2) |
| --- | --- | --- | --- |
| Index regime | Risk-on, choppy or risk-off? Trend, breadth, VIX, credit spreads, liquidity |  |  |
| Sector | Top, middle or bottom third by relative strength vs. SPY? Revisions, macro sensitivity |  |  |
| Balance sheet | Net debt/EBITDA, interest coverage, maturity wall, cash runway, FCF vs. net income |  |  |
| Guidance | Raised, held or cut? Tone vs. last quarter, beat quality |  |  |
| Volume and technicals | Volume vs. 50-day average, accumulation or distribution, key levels, liquidity |  |  |
| Management | Guidance vs. delivery history, capital allocation, Form 4 insider activity, CFO turnover |  |  |
| Sentiment and crowding | Crowded or ignored? Short interest, social volume, put/call |  |  |
| Short-only: forensic case | Leverage, receivables or inventory vs. sales, non-GAAP reliance, incentives |  |  |
| Short-only: squeeze and borrow | Short interest, days to cover, borrow cost and availability |  |  |

Then answer five questions in writing:

1. **Direction and instrument:** long, short, put, or put spread?
2. **Variant view:** what does consensus believe, what do you believe, and why are you right?
3. **Catalyst and timing:** what event forces the market to see it, and by when?
4. **Invalidation:** the price or event that proves you wrong.
5. **Bear case:** Claude writes the strongest argument against the trade (for a short, the strongest argument against the short).

Every input also gets a source tier tag.

| Tier | Examples | Role |
| --- | --- | --- |
| 1. Primary | Filings and footnotes, proxy statements, Form 4s, court dockets | Can support a trade |
| 2. Secondary | Earnings calls, sell-side notes, trade press | Supports and cross-checks |
| 3. Idea generation | YouTube investors, social posts, news | Starts research, never triggers a trade |

## Journal schema

Log every trade, including passes and losers, in one table or database. Use synthetic or your own data only; never store account numbers or credentials. These fields feed the monthly review.

| Field | What to record |
| --- | --- |
| trade\_id, date\_opened, date\_closed | Unique id and dates |
| ticker, direction, instrument | Long, short, put or put spread; strike and expiry for options |
| idea\_source, source\_tier | Where the idea came from and its tier (1, 2 or 3) |
| scorecard\_snapshot | Link to the completed scorecard at entry |
| variant\_view, catalyst, invalidation | Your written answers at entry, never edited later |
| regime\_at\_entry | Risk-on, choppy or risk-off |
| entry\_price, size\_pct\_account, stop\_level | Fixed at entry |
| exit\_price, exit\_reason | Target hit, stop hit, thesis broken or time stop |
| pnl\_pct, pnl\_vs\_spy\_pct | Return and return relative to SPY over the same holding period |
| rule\_breaches | Any risk rule you broke, and why |
| post\_mortem | Right for the right reasons? Right by luck? Wrong with a good process? |

For the YouTube pipeline, add a second table for each investor call: speaker, video date, ticker, direction, price at the time of the video, stated timeframe, and graded outcome at 30, 90 and 180 days vs. SPY.

## Review cadence

The reviews decide which sources and layers earn trust. Claude drafts each review from the journal; you verify the numbers against raw data.

| When | Check | Action |
| --- | --- | --- |
| Weekly | Rule breaches, open positions vs. limits, upcoming earnings and catalysts | Fix breaches before opening anything new |
| Monthly | Source hit rate by tier and by investor, win rate and average win vs. loss by direction, return vs. SPY after costs and taxes | Cut sources that added nothing |
| Quarterly | Which scorecard layer actually predicted outcomes, hit rate of longs vs. shorts vs. puts, size of the process-vs-luck gap | Reweight layers, tighten or loosen rules |
| After any drawdown trigger | Whether the circuit breaker fired and was obeyed | Pause, review, then resume at reduced size |

The benchmark question comes first every quarter: after short-term taxes and costs, does this process beat simply holding SPY? If not, run it as a small sleeve beside an index core while the evidence builds.

Paper trade shorts and puts first, and confirm what your broker allows (margin approval, options level, borrow availability).
