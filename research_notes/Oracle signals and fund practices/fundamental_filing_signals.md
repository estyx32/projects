# Fundamental and Filing-Based US Equity Signals Built from Free Data (EDGAR, XBRL, Form 4, 13F/13D, 8-K, earnings reactions)

Notes for the report writer. Not financial advice.

**How to read the sourcing in this file.**
- Links marked **[verified this session]** were checked through web search results during this research.
- Items marked **[prior knowledge, not re-verified]** are standard, widely cited literature facts that I could not re-check in this session. The session's network blocked direct fetches of sec.gov and anderson-review.ucla.edu, and I had a limited budget of tool calls. Treat their exact numbers as approximate and check them against the original paper before you publish. Wherever a number was uncertain, I left it out or moved it to Gaps.
- Labels used: **PR** = peer-reviewed journal; **WP** = working paper; **PRACT** = practitioner or vendor source.

---

## 1. Cross-cutting evidence: replication, post-publication decay, trading costs

### Takeaway
Most published anomalies replicate in-sample with CAPM alphas (JKP 2023). However, their returns fall by roughly half to 60% after publication (McLean & Pontiff 2016). About two-thirds lose significance once microcaps are down-weighted (Hou, Xue & Zhang 2020). Only low-turnover signals reliably survive trading costs (Novy-Marx & Velikov 2016). For a retail trader in large and mid caps, a reasonable starting assumption is that a published filing signal keeps a small fraction of its paper alpha.

### Cited Findings
- **McLean & Pontiff (2016), JF 71(1) [PR]:** studies 97 predictors. Returns are about 26% lower out-of-sample and about 58% lower after publication. The authors attribute the gap of roughly 32 percentage points (58% − 26%) to publication-informed trading. Trading volume and short interest in the predictor stocks rise after publication. — [CFA Digest summary](https://rpc.cfainstitute.org/research/cfa-digest/2016/06/does-academic-research-destroy-stock-return-predictability-digest-summary); [paper PDF](https://Www.Gwern.net/doc/economics/2016-mclean.pdf) [verified this session]
- **Hou, Xue & Zhang (2020), "Replicating Anomalies," RFS 33(5) [PR]:**
  - The tests use NYSE breakpoints and value weights to limit the influence of microcaps.
  - 65% of 452 anomalies fail |t| ≥ 1.96, including 96% of the trading-frictions category.
  - With a multiple-testing hurdle of t = 2.78, 82% fail.
  - Microcaps are about 3% of market cap but about 60% of the stocks.
  - Even the anomalies that replicate have "much smaller" magnitudes than originally reported.
  - Sources: [Alpha Architect summary (PRACT)](https://alphaarchitect.com/replicating-anomalies/); [NBER WP w23394](https://www.nber.org/papers/w23394.pdf); [RePEc record](https://ideas.repec.org/a/oup/rfinst/v33y2020i5p2019-2133..html) [verified this session]
- **Jensen, Kelly & Pedersen (2023), "Is There a Replication Crisis in Finance?", JF 78(5) [PR]:**
  - Uses a Bayesian framework that accounts for multiple testing and publication bias.
  - Covers 153 factors in 93 countries; the factors cluster into 13 themes.
  - Most factors replicate, and they hold out-of-sample internationally.
  - Alpha Architect (PRACT) reports a replication rate of about 82.4% in the published version and 85% in the working paper. Check which specification the published abstract uses before quoting a number.
  - Data and code are at jkpfactors.com.
  - Sources: [NBER w28432](https://www.nber.org/papers/w28432); [CBS publisher version](https://research-api.cbs.dk/ws/portalfiles/portal/95651880/theis_ingerslev_jensen_et_al_is_there_a_replication_crisis_in_finance_publishersversion.pdf); [Alpha Architect (PRACT)](https://alphaarchitect.com/factors-are-global-respectable-and-repeatable/) [verified this session]
  - Note: JKP's "replication" means the in-sample CAPM alpha is significant. It does **not** mean the factor survives costs or kept its strength after publication. The JKP and HXZ results are therefore not contradictory. They answer different questions: HXZ applies value weights, NYSE breakpoints and factor-model alphas, while JKP uses CAPM alphas with Bayesian shrinkage.
- **Novy-Marx & Velikov (2016), "A Taxonomy of Anomalies and Their Trading Costs," RFS 29(1) [PR]:**
  - Most anomalies with one-sided monthly turnover below 50% keep significant net spreads, at least when the strategy is designed to reduce costs.
  - Few anomalies with higher turnover do.
  - A buy/hold spread (hysteresis band) is the most effective way to reduce costs.
  - Sources: [author PDF](https://mysimon.rochester.edu/novy-marx/research/ToAatTC.pdf); [NBER w20721](https://nber.org/papers/w20721); [Alpha Architect (PRACT)](https://alphaarchitect.com/trading-costs-destroy-factor-investing/) [verified this session]
- **Chen & Zimmermann, "Open Source Cross-Sectional Asset Pricing," Critical Finance Review (2022) [PR]:**
  - Open-source code and portfolio returns for about 200+ firm-level predictors, at openassetpricing.com.
  - Most of the signals in this file are included: accruals, gross profitability, asset growth, net share issuance, F-score, SUE, EAR, insider-related signals, and others.
  - Useful as a reference implementation for checking your own build.
  - [prior knowledge, not re-verified] — https://www.openassetpricing.com
- **Chen & Velikov (2023), "Zeroing in on the Expected Returns of Anomalies," JFQA [PR]:** combines trading costs with post-publication decay. They conclude that the average anomaly's expected net return to a sophisticated trader is only a few basis points per month. [prior knowledge, not re-verified; exact bps not confirmed]
- **Stambaugh, Yu & Yuan (2012), JFE [PR]:** anomaly profits come disproportionately from the **short leg**, especially after periods of high investor sentiment. This is consistent with limits to arbitrage from short-sale constraints. [prior knowledge, not re-verified]

### Inferences
- A conservative haircut for planning: take the original paper's value-weighted, NYSE-breakpoint alpha (not the equal-weighted headline), cut it by about 50-60% for post-publication decay, then subtract costs. Many signals end near zero, and slow-moving annual accounting signals have the best chance of keeping something.
- A long-only retail implementation loses the short leg, which is often where most of the anomaly return sits. Long-leg-only results should be tested separately.

### Gaps
- I could not verify the exact Chen & Velikov net-return figure or the Chen & Zimmermann signal count this session.

---

## 2. Data infrastructure and point-in-time pitfalls (applies to every card)

### Takeaway
Free EDGAR data is enough to build all of these signals. The main risk is look-ahead bias: always key a data point to the date it was **filed** (and, ideally, the acceptance timestamp), never to the fiscal period end. Also, XBRL "frames" return the latest value reported, which may be a restated number.

### Cited Findings (all [prior knowledge, not re-verified]; sec.gov fetch was blocked in this session)
**Main sources, mostly sec.gov:**
- **SEC EDGAR APIs** (data.sec.gov):
  - `submissions/CIK##########.json`: filing history with form type, filingDate, acceptanceDateTime and accession number.
  - `api/xbrl/companyfacts/CIK##########.json`: every XBRL fact. Each fact carries `val`, `fy`, `fp`, `form`, `filed`, `accn`, `start`/`end` and, sometimes, `frame`.
  - `companyconcept`: one tag for one company.
  - `frames/{taxonomy}/{tag}/{unit}/{period}`: a cross-section of one tag for one calendar period.
  - Nightly bulk ZIPs of submissions and companyfacts are available.
  - A declared User-Agent is required, and the fair-access limit is about 10 requests per second.
  - Reference: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- **Look-ahead from restatements in frames and companyfacts:**
  - The `frame` field is assigned to the fact that best represents a calendar period, which is often the value from the **latest** filing, including a later 10-K's comparative column.
  - For point-in-time work, reconstruct "as first reported" by keeping, for each (tag, period), the fact from the earliest `filed` date. Then make the signal available only from that filing's acceptance time.
- **XBRL coverage:**
  - Phased in from 2009 (large accelerated filers) to 2011 (all filers).
  - Before 2009 there is no structured free data. The fallbacks are the SEC Financial Statement Data Sets (also XBRL-based, from 2009) or parsing HTML/text filings.
  - So a free-data backtest generally starts in 2009-2011. That is **after** publication for accruals, the F-score, net issuance and asset growth, but before publication of gross profitability (2013) and quality minus junk (2019). It is useful as out-of-sample evidence for the older signals, and the sample is short (about 15 years).
- **Tag inconsistency:** companies use different and custom tags for the same item (for example `Revenues`, `RevenueFromContractWithCustomerExcludingAssessedTax`, `SalesRevenueNet`). Build fallback chains, and check sign conventions.
- **Fiscal quarter Q4:** Q4 values are usually not reported directly. You get them as the 10-K annual value minus Q1-Q3, and the 10-K comes out later than a 10-Q.
- **Insider Transactions Data Sets (SEC):** quarterly structured extracts of Forms 3/4/5. Raw Form 4 XML is in EDGAR. Since Sarbanes-Oxley (Aug 2002), Form 4 has been due within 2 business days of the trade.
- **Form 13F Data Sets (SEC):**
  - Due 45 days after quarter end; filers are managers with ≥$100M in 13(f) securities.
  - Covers long positions only (no shorts). Managers can request confidential treatment, which delays disclosure.
- **Schedule 13D:** historically due within 10 days of crossing 5%. SEC amendments adopted in Oct 2023 shortened this to 5 business days, effective early 2024.
- **8-K:** the item taxonomy was overhauled in Aug 2004, with most items due within 4 business days. Item 2.02 (results) is the free source of **earnings announcement dates**. Use acceptanceDateTime to tell pre-market from after-close releases. EDGAR full-text search covers 2001+.
- **Survivorship:** EDGAR keeps filings of delisted firms, which is good. But free *price* data (for example Yahoo) is usually survivor-biased and lacks delisting returns. This is a major free-data weakness for every long-short backtest here, particularly for short legs, distress and accrual signals.

**One verified data point:**
- A 13D filing reveals an activist's stake, but the fund begins accumulating shares 1-10 days *before* the filing. Part of the price move is therefore not capturable from the public filing. — [Brav, Jiang, Partnoy & Thomas WP](https://corpgov.law.harvard.edu/wp-content/uploads/2008/03/hedge_fund_activism-final.pdf) [verified this session]

### Inferences
- Use the timestamp on every signal. Any XBRL value used before its own `filed` date is look-ahead.
- Before trusting a free-price-data backtest of short legs, collect delisting events from EDGAR (Form 25, 15) and price final returns conservatively.

### Gaps
- I could not fetch the SEC API documentation page (network blocked), so the rate limit, bulk-file details and `frame` semantics above are from prior knowledge. Confirm them on sec.gov.

---

## 3. PEAD, SUE from reported EPS, and EAR as a free surprise proxy

### Takeaway
PEAD is the classic anomaly (Ball & Brown 1968; Bernard & Thomas 1989/1990). Strong evidence says it has **disappeared for large caps since about 2006** and is now concentrated in microcaps and illiquid stocks (Martineau 2022). Papers accepted in 2025 claim it is alive, but the disagreement appears to depend on whether microcaps are included. For a retail trader in large and mid caps, expect little or nothing after costs.

### Cited Findings
- **Martineau (2022), "Rest in Peace Post-Earnings Announcement Drift," Critical Finance Review 11(3-4):613-646 [PR]:** prices now fully reflect earnings surprises on the announcement day. PEAD has been "non-existent since 2006 for large stocks" and disappeared only recently for microcaps. — [CFR PDF](https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf); [RePEc](https://ideas.repec.org/a/now/jnlcfr/104.00000122.html) [verified this session]
- **Counter-evidence from 2025:**
  - Per a UCLA Anderson Review brief (PRACT/academic summary), two papers accepted for publication in 2025 say PEAD is "alive and well." One is by Dickerson et al., which reportedly did not separate out microcaps.
  - **Subrahmanyam's WP "Keeping it Simple: How Can Post-Earnings Return Drift Exist and Not Exist Simultaneously?"** (SSRN 5930255) attributes the disagreement to research design. As reported in the brief: t = 2.18 with all stocks, t = 1.43 excluding microcaps.
  - Sources: [UCLA Anderson Review](https://anderson-review.ucla.edu/is-post-earnings-announcement-drift-a-thing-again/) (via search snippet only; direct fetch blocked) [verified this session at snippet level]
- **Foundational papers [prior knowledge, not re-verified]:**
  - Ball & Brown (1968), JAR [PR].
  - Bernard & Thomas (1989), JAR supplement, and (1990), JAE [PR]. SUE from a seasonal random walk on quarterly EPS. Drift continues for about 60 trading days and clusters around the next few earnings announcements.
- **SUE construction:**
  - Unexpected earnings = EPS_q − EPS_{q−4} (seasonal random walk, optionally with drift), scaled by the standard deviation of past surprises (for example over the last 8 quarters).
  - EAR = 3-day abnormal return centred on the announcement.
  - A common combined strategy goes long stocks in the top quantiles of both SUE and EAR and short the bottom of both, entering on day +2.
  - — [QuantConnect/Quantpedia backtest page (PRACT)](https://www.quantconnect.com/terminal/quantpediaBacktestResult/embedded_backtest_e142cda1b0856b80971baadbe0650b3a.html) [verified this session]
- **EAR as a free proxy for surprise [prior knowledge, not re-verified]:**
  - Chan, Jegadeesh & Lakonishok (1996), JF [PR]: SUE, EAR and analyst revisions each predict returns over the next 6-12 months.
  - Brandt, Kishore, Santa-Clara & Venkatachalam, "Earnings Announcements Are Full of Surprises" (WP, about 2008): EAR-based drift is at least as strong as SUE drift and is weakly correlated with it.
  - Chen & Zimmermann's library includes both "AnnouncementReturn" and "EarningsSurprise".
  - My search did not surface the Brandt et al. paper itself, so its numbers are unverified.
- **Liquidity and costs [prior knowledge, not re-verified]:**
  - Chordia, Goyal, Sadka, Sadka & Shivakumar (2009), FAJ [PR]: PEAD is concentrated in illiquid stocks, and transaction costs absorb most of the paper profit (roughly 70-100%).
  - Livnat & Mendenhall (2006), JAR [PR]: analyst-based SUE gives a larger drift than time-series SUE. So a free time-series SUE is a weaker signal than the consensus-based version.
- **Free data needed:**
  - Quarterly diluted EPS (us-gaap:EarningsPerShareDiluted) from companyfacts, as first reported and keyed by `filed`. The 10-Q/10-K date lags the earnings release.
  - Announcement date and time from the 8-K Item 2.02 acceptanceDateTime.
  - Daily prices.
  - A market or size/B-M benchmark for the abnormal return (Ken French's data library is free).

### Inferences
- **Pitfall: release date vs filing date.** The 8-K 2.02 press release usually comes days to weeks before the 10-Q. SUE built from XBRL is only available at the 10-Q filing date, so an XBRL-only SUE enters *late* and misses the early drift. EAR has no such lag, which is a practical reason to prefer EAR with free data.
- **Pitfall: GAAP vs street EPS.** XBRL EPS is GAAP. Market surprise is usually judged against non-GAAP "street" EPS, so GAAP-based SUE is a noisy proxy (special items, one-offs).
- **Pitfall: release timing.** Use acceptance time to classify after-close releases. Day 0 is then the next trading day.

### Gaps
- No verified effect sizes for EAR drift after 2010 in large caps. I also could not identify the published venues of the 2025 "PEAD alive" papers beyond Dickerson et al.

---

## 4. Analyst revisions (consensus not free) and free proxies

### Takeaway
Analyst forecast revisions and revision momentum are well documented as predictive (Stickel 1991; Chan, Jegadeesh & Lakonishok 1996). But I/B/E-S-type consensus is not free. Free proxies are indirect: the earnings-announcement return (EAR), the price reaction to 8-K guidance (Items 2.02 and 7.01), and time-series SUE. None replicate a revision signal.

### Cited Findings
- Chan, Jegadeesh & Lakonishok (1996), JF [PR]: analyst revisions, SUE and EAR each add predictive power. [prior knowledge, not re-verified]
- Livnat & Mendenhall (2006), JAR [PR]: the analyst-based surprise produces a larger drift than time-series SUE, so the free proxy understates the signal. [prior knowledge, not re-verified]
- The EAR/SUE combination used as a revision-free strategy is described by [QuantConnect/Quantpedia (PRACT)](https://www.quantconnect.com/terminal/quantpediaBacktestResult/embedded_backtest_e142cda1b0856b80971baadbe0650b3a.html) [verified this session]

### Inferences
- Candidate free proxies:
  1. EAR at earnings (Section 3).
  2. Abnormal returns on 8-K Item 7.01/8.01 guidance updates, with direction taken from the return sign.
  3. Change in tone between consecutive Item 2.02 press releases (Exhibit 99.1).
  4. Price momentum (overlaps with revision momentum).
- Analyst-revision signals are among the more crowded quant factors in practice. Expect substantial decay after publication.

### Gaps
- I found no peer-reviewed study validating a specific free substitute for consensus revisions.

---

## 5. Insider trading from Form 4

### Takeaway
Insider **purchases** (not sales) predict returns. Cohen, Malloy & Pomorski (2012) show that the predictive power comes from **opportunistic** insiders, whose trades show no calendar pattern: 72 bp/month value-weighted on buys alone and 82 bp/month buys minus sells, while routine buys minus sells earn -20 bp. The signal is strongest in small, less-covered stocks.

### Cited Findings
- **Cohen, Malloy & Pomorski (2012), "Decoding Inside Information," JF 67(3):1009-1043 [PR]; NBER WP 16454 (2010):**
  - Only insiders with at least one trade in each of the prior 3 years are classified. Routine insiders traded in the same calendar month for at least 3 consecutive years; the rest of that universe is opportunistic. First-time buyers fall outside the tested sample.
  - Table IV, five-factor alphas, 1989-2007 (read from the NBER PDF): opportunistic buys minus sells earn 82 bp/month value-weighted (t=2.15) and 180 bp/month equal-weighted (t=6.07). Opportunistic buys alone earn 72 bp and 158 bp. Routine buys minus sells earn -20 bp value-weighted and 43 bp equal-weighted (t=1.73).
  - Opportunistic trades predict future firm news and events.
  - Sources: [NBER](https://www.nber.org/papers/w16454); [AQR (PRACT summary)](https://www.aqr.com/Insights/Research/Journal-Article/Decoding-Inside-Information); [HBS Working Knowledge](https://hbswk.hbs.edu/item/decoding-inside-information) [verified this session]
  - The large gap between the equal-weighted and value-weighted figures signals that much of the effect is in small stocks.
- **Earlier evidence [prior knowledge, not re-verified]:**
  - Seyhun (1986), JFE; Lakonishok & Lee (2001), RFS [PR]: purchases are informative, sales largely are not, and the effect concentrates in small firms.
  - Jeng, Metrick & Zeckhauser (2003), REStat [PR]: purchases earn about 50 bp/month abnormal; sales do not.
- **CEO/CFO and cluster buying:** the practitioner rule that CEO or CFO open-market purchases and clusters of several insiders buying within a short window carry more signal is widely cited. I did **not** verify a specific peer-reviewed cluster-buying effect size this session.
- **Free data needed:**
  - Form 4 XML from EDGAR, or the SEC Insider Transactions Data Sets.
  - Transaction code **P** (open-market purchase) and **S** (sale). Exclude A, M, F, G and others (awards, option exercises, tax withholding, gifts).
  - Reporter role (officer title, director, 10% owner), shares, price, and the filing timestamp.
  - The Rule 10b5-1 checkbox, which has been on Form 4 since 2023 and marks pre-planned trades.

### Inferences
- **Pitfall: trade date vs filing date.** Pre-SOX (before Aug 2002), filings could lag trades by weeks. Backtests must use the filing date, especially when the sample includes the 1990s literature period.
- The opportunistic/routine classification needs 3+ years of an insider's trade history. That history is fully available free from EDGAR.
- In large and mid caps, CEO purchases are rare and the per-trade alpha is smaller. The strategy is sparse and event-driven, so it has low turnover, which helps after costs.

### Gaps
- I did not find a post-publication decay study specifically for the Cohen, Malloy & Pomorski opportunistic signal. I also found no verified cluster-buying effect size.

---

## 6. 13D activism and 13F institutional holdings changes

### Takeaway
13D filings by hedge-fund activists bring about a +7% abnormal return in a window around the filing, with no reversal over the following year (Brav et al. 2008). Much of that move happens before or on the filing day, so a follower captures only part of it. 13F holdings arrive up to 45 days after quarter end, which makes copying holdings stale. The evidence for copying 13Fs is weaker and mostly comes from working papers or practitioners.

### Cited Findings
- **Brav, Jiang, Partnoy & Thomas (2008), "Hedge Fund Activism, Corporate Governance, and Firm Performance," JF [PR]:**
  - Abnormal return of about 7% around the activism announcement (7-8% over a (−20, +20) day window), with no reversal in the next year.
  - Activists start buying 1-10 days before the 13D filing.
  - A companion FAJ (2008) paper reports high returns *to the activist funds*.
  - Sources: [Harvard Law WP PDF](https://corpgov.law.harvard.edu/wp-content/uploads/2008/03/hedge_fund_activism-final.pdf); [Duke PDF](https://law.duke.edu/sites/default/files/centers/gfmc/session_3/2_brav_et_al-hedge_fund_activism-2008.pdf); [FAJ RePEc](https://ideas.repec.org/a/taf/ufajxx/v64y2008i6p45-61.html) [verified this session]
- **13F:**
  - Mechanics: 45-day lag, long-only, $100M threshold, confidential treatment possible. [prior knowledge, not re-verified]
  - Agarwal, Jiang, Tang & Yang (2013), JF [PR]: positions hedge funds keep confidential (filed late) earn abnormal returns. This implies the publicly visible 13F positions carry less of the alpha. [prior knowledge, not re-verified]

### Inferences
- **Pitfall: windows that start before the filing.** A (−20, +20) window includes returns before the filing. A follower who trades at the filing timestamp (or the next open) sees a much smaller effect. Measure from the acceptanceDateTime.
- **13D deadline change.** The SEC's shortening of the 13D deadline to 5 business days (effective 2024) changes how much accumulation happens before filing.
- **13F lag.** By the time a 13F is filed, up to 135 days may have passed since the trade, for a position bought at the start of a quarter.

### Gaps
- No verified peer-reviewed effect size for following 13F changes ("best ideas," crowded-holdings signals) after accounting for the filing lag. I did not verify post-2008 decay of the 13D event return.

---

## 7. Accounting anomalies: accruals, gross profitability, quality/QMJ, Piotroski F-score, asset growth, net share issuance

### Takeaway
These slow-moving annual signals are the best fit for free XBRL data and for low-turnover retail trading. The evidence by signal:
- **Profitability and quality:** robust and still present in large caps, though partly priced in.
- **Investment and asset growth:** robust and absorbed into the Fama-French 5-factor model.
- **Net share issuance:** robust.
- **Accruals:** decayed substantially after about 2000.
- **F-score:** concentrated in small, low-coverage value stocks.

### Cited Findings
- **Sloan (1996), "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?", The Accounting Review [PR]:** low-accrual firms outperform high-accrual firms. [prior knowledge, not re-verified]
  - Green, Hand & Soliman (2011), *Management Science* [PR], "Going, Going, Gone? The Apparent Demise of the Accruals Anomaly": the accruals hedge return largely disappeared in the 2000s. This is consistent with arbitrage capital entering after publication. [prior knowledge, not re-verified]
- **Novy-Marx (2013), "The Other Side of Value: The Gross Profitability Premium," JFE [PR]:** gross profits / total assets predicts returns about as strongly as book-to-market. It works in large stocks, and its low turnover makes it cost-robust (consistent with the Novy-Marx & Velikov 2016 low-turnover result above). [prior knowledge, not re-verified]
- **Asness, Frazzini & Pedersen, "Quality Minus Junk," Review of Accounting Studies (2019) [PR; AQR authors]:** quality combines profitability, growth, safety and payout. QMJ earns positive risk-adjusted returns in the US and 24 countries. AQR's own factor data is PRACT. [prior knowledge, not re-verified]
- **Piotroski (2000), JAR supplement [PR]:** a 9-point F-score applied to high book-to-market stocks. The high-minus-low score return is large, but it is concentrated in small, low-analyst-following, low-share-turnover firms. [prior knowledge, not re-verified; exact magnitude not cited]
- **Cooper, Gulen & Schill (2008), "Asset Growth and the Cross-Section of Stock Returns," JF [PR]:** firms with low total-asset growth beat firms with high growth. The effect is much larger equal-weighted than value-weighted. It is closely related to the Fama-French (2015) CMA investment factor. [prior knowledge, not re-verified]
- **Pontiff & Woodgate (2008), JF; Daniel & Titman (2006), JF [PR]:** net share issuance (positive) predicts low returns, and repurchases (negative issuance) predict higher returns. This is among the more robust anomalies and is included in many multi-factor models (for example Stambaugh-Yuan "mispricing" factors). [prior knowledge, not re-verified]
- **Replication context:** HXZ (2020) report that trading-frictions anomalies fail most often (96%). Profitability and investment signals are in the categories that replicate better. — [Alpha Architect summary of HXZ (PRACT)](https://alphaarchitect.com/replicating-anomalies/) [verified this session; category-level detail beyond the frictions figure is prior knowledge]
- **Free data (XBRL companyfacts):**
  - Accruals: NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets. Use the cash-flow-statement definition, (NI − CFO) / average assets, which is cleaner than Sloan's balance-sheet version.
  - Gross profitability: Revenues, CostOfRevenue (or GrossProfit), Assets.
  - F-score: ROA, CFO, change in ROA, accruals, change in leverage (LongTermDebt), change in current ratio, shares issued, change in gross margin, change in asset turnover.
  - Asset growth: Assets_t / Assets_{t−1} − 1.
  - Net share issuance: change in split-adjusted shares outstanding (dei:EntityCommonStockSharesOutstanding or WeightedAverageNumberOfDilutedSharesOutstanding), with care around splits.
  - QMJ inputs also need price and volatility data.

### Inferences
- **Point-in-time rule.** Classic papers assume a 4-6 month lag from fiscal year-end; with EDGAR you can use the actual `filed` date instead. Do not form portfolios at period end.
- **Restatements.** Use first-reported values; frames and later comparatives contain restated numbers.
- **Financials and utilities.** Usually excluded, because gross profit and accruals are poorly defined for them.
- **Fit for retail.** These are annual rebalancing signals with low turnover, which makes them the most retail-viable in this file. The expected premium is still modest after decay.

### Gaps
- I did not re-verify exact original effect sizes (for example Sloan's hedge return, Piotroski's annual spread, Novy-Marx's monthly spread). They are left out rather than quoted from memory.

---

## 8. Textual change signals: Lazy Prices, risk factors, tone, readability

### Takeaway
Cohen, Malloy & Nguyen (2020) find that firms that **change** their 10-K/10-Q language (low year-over-year similarity) later underperform, and "non-changers" outperform. The long-short alpha is up to 188 bp/month. The signal is buildable entirely from free EDGAR text, but implementing it is laborious, and I found no independent post-publication replication.

### Cited Findings
- **Cohen, Malloy & Nguyen (2020), "Lazy Prices," JF 75(3):1371-1415 [PR]; NBER WP w25084:**
  - Sample: 1995-2014 filings.
  - Going long non-changers and short changers earns up to 188 bp/month alpha (over 22% per year annualized in the WP).
  - Language changes predict future earnings, profitability, news announcements and bankruptcies.
  - The returns arrive slowly, which the authors attribute to investor inattention.
  - The changes that matter most are in risk factors and in the management discussion of litigation and executives.
  - Sources: [NBER](https://www.nber.org/papers/w25084); [Harvard DASH](https://dash.harvard.edu/entities/publication/576a041c-19c4-47d8-b28d-2a5ef079f54f); [Harvard Magazine](https://www.harvardmagazine.com/index%2Ephp/2019/04/stock-market-efficiency-investors) [verified this session]
- **Tone [prior knowledge, not re-verified]:** Loughran & McDonald (2011), JF [PR], built finance-specific sentiment word lists (negative, uncertainty, litigious). The lists are freely downloadable. The 10-K negative-word proportion relates to filing-period returns. Evidence for long-horizon return prediction is weaker.
- **Readability [prior knowledge, not re-verified]:** Li (2008), JAE [PR]: firms with lower earnings file less readable annual reports (Fog index), and readability relates to earnings persistence. Loughran & McDonald later criticised the Fog index for financial text and proposed file size as a simpler proxy.
- **Free data needed:**
  - Full 10-K/10-Q text from EDGAR Archives, ideally the same section in consecutive filings (Item 1A Risk Factors, Item 7 MD&A).
  - Similarity measures: cosine on term frequency, Jaccard, minimum edit distance.
  - The signal date is the filing acceptance date.

### Inferences
- **Pitfall: parsing.** Section extraction from HTML 10-Ks is error-prone; boilerplate, exhibits and table changes add noise.
- **Pitfall: alignment.** Compare like with like: the 10-K with the prior 10-K, and Q2 10-Q with the prior-year Q2.
- **Pitfall: timing.** Filing dates cluster by fiscal year-end, so cross-sectional portfolios form unevenly. The paper's alpha builds over months, which suggests low turnover.
- **Crowding risk.** This signal is now widely known (the paper is highly cited, and vendors sell "lazy prices" text datasets), so expect decay after 2020.

### Gaps
- No verified independent replication or post-2014 out-of-sample estimate of the Lazy Prices alpha. I did not check whether it is in the Chen & Zimmermann library.

---

## 9. 8-K event types

### Takeaway
8-K item codes, standardized since Aug 2004, give free, timestamped event flags. **Item 4.02 (non-reliance/restatement)** has a documented negative announcement reaction of about −1% next day and about −2% over 20 days (vendor analysis). Evidence on longer-run drift is mixed. For **Item 5.02 departures**, I found no clean peer-reviewed return study this session; volume reactions differ by role. **Item 2.02** is mainly useful as the source of earnings dates and timestamps for EAR/PEAD.

### Cited Findings
- **Item 4.02 announcement effect:** sec-api.io's analysis (PRACT/vendor, not peer-reviewed) of 8,000+ Item 4.02 filings, 2004-2023, finds an average CAR of about −1.1% at day +1, widening to about −2% over 20 days. — [sec-api.io](https://sec-api.io/resources/stock-price-reactions-to-item-4-02-disclosures-in-sec-form-8-k-filings) [verified this session]
- **Long-run returns after restatements:**
  - Audit Analytics (PRACT): 5,111 non-reliance restatements, 2005-2016. No significant abnormal returns in the first 30 days after restated financials are filed. The long-term returns are later positive, with a negative window in between per the Cooley summary.
  - Note: Audit Analytics measures from the *restated-financials filing*, not the 4.02 announcement. The two studies measure different events.
  - Sources: [Audit Analytics](https://blog.auditanalytics.com/long-term-capital-market-consequences-of-financial-restatements/); [Cooley PubCo](https://cooleypubco.com/2019/02/15/audit-analytics-consequences-of-restatements/) [verified this session]
- **Item 5.02 departures:**
  - An arXiv WP (2026, not peer-reviewed) on fine-grained 8-K event extraction finds abnormal trading volume of about 1.32× normal for CEO departures vs about 1.06× for routine officer appointments. The coarse 5.02 label therefore mixes events with very different information content. — [arXiv 2607.08346](https://arxiv.org/pdf/2607.08346) [verified this session]
  - Audit Analytics (PRACT): over half of CEO/CFO departure 8-Ks give no reason. Departures close to restatements or investigations are more serious signals. — [Audit Analytics](https://blog.auditanalytics.com/ceo-and-cfo-departures-2016-2018/?amp=1) [verified this session]
- **Lerman & Livnat (2010), "The New Form 8-K Disclosures," Review of Accounting Studies [PR]:** after the 2004 reform, many new 8-K items bring abnormal volume and return volatility, so they carry information. [prior knowledge, not re-verified]

### Inferences
- **Free data:** EDGAR submissions JSON and the 8-K header list item numbers. Pair them with acceptanceDateTime and daily prices.
- **Pitfalls:**
  - Many 8-Ks are filed after hours, so day 0 is the next session.
  - Items are often bundled; for example 2.02 with 5.02, or 4.02 together with a 2.02 earnings delay.
  - Item 1.01 (material agreement) is very heterogeneous. Without text classification of the agreement type, expect noise.
- **Tradeability.** Most 8-K reactions happen at the announcement. Post-filing drift strong enough to cover retail costs in large caps is not documented in what I found.

### Gaps
- No verified peer-reviewed abnormal-return estimates for Items 5.02 or 1.01, or for post-event drift in large caps.

---

## 10. Dividend initiations/omissions and buyback announcements

### Takeaway
Michaely, Thaler & Womack (1995) document drift after dividend initiations (positive) and omissions (negative). The drift is larger than PEAD and was profitable in 22 of 25 years. Later work questions how robust it is (Boehme & Sorescu 2002). For buybacks, the classic finding is long-run outperformance after open-market repurchase announcements (Ikenberry, Lakonishok & Vermaelen 1995). Later evidence suggests that anomaly weakened after about 2003, and long-horizon event-study inference is fragile.

### Cited Findings
- **Michaely, Thaler & Womack (1995), "Price Reactions to Dividend Initiations and Omissions: Overreaction or Drift?", JF 50(2):573-608 [PR]:** post-event drift exists, is distinct from and larger than the post-earnings drift, and a trading rule using both samples earns positive returns in 22 of 25 years. — [NBER w4778](https://www.nber.org/papers/w4778) [verified this session]
- **Boehme & Sorescu (2002), JF [PR]:** the long-run drift after dividend initiations and resumptions is sensitive to methodology and may be a "product of chance." [prior knowledge, not re-verified]
- **Ikenberry, Lakonishok & Vermaelen (1995), "Market Underreaction to Open Market Share Repurchases," JFE [PR]:** commonly cited as about 12.1% 4-year abnormal return after buyback announcements, concentrated in high book-to-market firms. **The 12.1% figure was NOT verified this session; my search did not surface the paper.** [prior knowledge, not re-verified]
- **Peyer & Vermaelen (2009), RFS [PR]:** the buyback underreaction persists. **Fu & Huang (2016), Management Science [PR]:** long-run abnormal returns after repurchases weaken or disappear in the post-2003 sample. [prior knowledge, not re-verified]
- **Free data needed:**
  - **Dividends:** a dividend history derived from XBRL (CommonStockDividendsPerShareDeclared) or from free price/dividend data. Initiation = first dividend after no dividend for N years. 8-K Items 8.01/7.01 or Exhibit 99 press releases give the announcement date.
  - **Buybacks:**
    - Authorization announcements usually come in an 8-K (often Item 8.01) or the earnings release.
    - Actual repurchases are disclosed quarterly in 10-Q/10-K (Part II Item 2 issuer repurchase table).
    - The SEC's 2023 share-repurchase disclosure modernization rule was later vacated by the Fifth Circuit (prior knowledge, not re-verified).
    - The net share issuance signal (Section 7) captures *executed* buybacks from XBRL share counts.

### Inferences
- **Pitfall: long horizons.** Long-horizon (3-4 year) event studies are highly sensitive to benchmark choice and cross-correlation, and survivorship in free price data inflates results.
- **Pitfall: announcements vs execution.** Buyback authorizations often go uncompleted. Executed repurchases (via net issuance) are the cleaner, better-replicated signal.
- **Fit for retail.** Events are rare per stock and the holding periods are long. Costs are low, but the evidence of decay means expectations should be modest.

### Gaps
- I could not verify the Ikenberry et al. 12.1% figure or any post-2010 dividend-initiation drift estimate.

---

## Summary table (for the report writer)

| Signal | Key PR evidence | Headline effect (as reported) | Holding period | Decay / crowding | Large/mid-cap after cost (retail) | Free data |
|---|---|---|---|---|---|---|
| PEAD / SUE / EAR | Bernard & Thomas 1989/90; Martineau 2022 CFR | Historically sizeable; ~0 in large caps since ~2006 | ~60 trading days | Strong decay; 2025 dispute hinges on microcaps | Likely ~nil | XBRL EPS, 8-K 2.02 time, prices |
| Analyst revisions | Chan, Jegadeesh & Lakonishok 1996 | n/v | 6-12 months | Crowded | Not buildable free; proxies weak | (EAR proxy) |
| Insider (opportunistic) | Cohen, Malloy & Pomorski 2012 JF | Buys only 72 bp/mo VW, 158 bp/mo EW; long-short 82 and 180 | ~1 month+ | Unverified | Small; effect is small-cap heavy | Form 4 XML |
| 13D activism | Brav et al. 2008 JF | ~7% (−20, +20) window | Event; no 1-yr reversal | Partly pre-filing | Partial capture only | 13D filings |
| 13F changes | Agarwal et al. 2013 (confidential holdings) | n/v | Quarterly | 45-day lag | Weak/unclear | 13F data sets |
| Accruals | Sloan 1996 TAR | n/v | ~1 yr | Largely gone after 2000s (Green et al. 2011) | Weak | XBRL NI, CFO, assets |
| Gross profitability / QMJ | Novy-Marx 2013; Asness, Frazzini & Pedersen 2019 | n/v | ~1 yr | Partly priced | Best candidates, modest | XBRL |
| F-score | Piotroski 2000 | n/v | ~1 yr | Small-cap concentrated | Weak in large caps | XBRL |
| Asset growth | Cooper, Gulen & Schill 2008 | n/v (much weaker VW) | ~1 yr | In FF5 CMA | Modest | XBRL assets |
| Net issuance / buybacks | Pontiff & Woodgate 2008; Daniel & Titman 2006 | n/v | ~1 yr | Robust in replications | Modest | XBRL shares |
| Lazy Prices | Cohen, Malloy & Nguyen 2020 JF | up to 188 bp/mo | months | Unknown after 2020; vendor-crowded | Unknown | 10-K/10-Q text |
| 8-K 4.02 | sec-api (vendor) | −1.1% day+1; −2% 20d | Event | n/a | Hard to trade (short) | 8-K items |
| Dividend init/omit | Michaely, Thaler & Womack 1995 JF | drift > PEAD; 22/25 yrs | ~1 yr | Disputed (Boehme & Sorescu 2002) | Uncertain | XBRL dividends, 8-K |

n/v = not verified this session (prior-knowledge figures deliberately left out).
