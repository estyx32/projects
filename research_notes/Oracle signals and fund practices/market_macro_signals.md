# Evidence for US equity return-predicting signals built from free market, positioning, options and macro data

Scope note: US equities and US macro data only. Not financial advice. Practitioner sources (AQR, Alpha Architect, CXO Advisory, Quantpedia, Research Affiliates) are marked **[PRACTITIONER]**. In this session WebFetch could not reach nber.org, finra.org or gwern.net (blocked network domains), so most figures come from search-result abstracts and secondary summaries. Several standard literature facts that could not be verified this session are listed under "Gaps" or labeled "background knowledge, unverified" in Inferences. Treat them as leads to check, not citations.

---

## Q0. Cross-cutting: how much do published anomalies decay, and where do they live?

### Takeaway
Published cross-sectional anomalies lose a large share of their returns after publication, and the loss is largest where in-sample returns were biggest and where arbitrage is cheap. Assume a significant haircut on any backtested premium from the original paper.

### Cited Findings
- McLean & Pontiff, "Does Academic Research Destroy Stock Return Predictability?", *Journal of Finance*, Feb 2016 (peer-reviewed). The study covers 97 published predictors and concludes that investors learn about mispricing from academic publications. — [SUFE abstract listing](https://academicnewsletter.sufe.edu.cn/info/359722); [working-paper PDF (Ivey)](https://ivey.uwo.ca/media/3775549/pontiff.pdf)
- Working-paper versions put the post-publication decay at about 32-35%. The widely quoted published figure ("26% lower out-of-sample, 58% lower post-publication") **could not be verified this session**, so check DOI 10.1111/jofi.12365 before quoting it. — [Hedge Fund Alpha summary](https://hedgefundalpha.com/?p=521337); [Counterpoint copy of paper](https://counterpointfunds.com/wp-content/uploads/2017/07/PredictabilityMcleanPontiff.pdf)

### Inferences
- Background knowledge, unverified this session: McLean & Pontiff also report that post-publication decay is larger for anomalies with larger in-sample returns and for those concentrated in liquid, low-idiosyncratic-risk stocks. That means anomalies that survive tend to be the ones that are expensive to trade.
- Background knowledge, unverified: Hou, Xue & Zhang, "Replicating Anomalies" (*RFS* 2020) found that most of 452 anomalies become insignificant once microcaps are controlled for (NYSE breakpoints, value weighting). Chen & Zimmermann's "Open Source Cross-Sectional Asset Pricing" (*Critical Finance Review* 2022) replicated most clear predictors. Both are the replication references to cite. Verify them first.

### Gaps
- Exact published McLean-Pontiff percentages were not confirmed (the fetch was blocked).
- No verified, signal-by-signal post-2016 out-of-sample decay numbers for most signals below.

---

## Q1. Price momentum family: 12-1 momentum, short-term reversal, industry momentum, 52-week high, time-series momentum and trend filters

### Takeaway
Cross-sectional 12-1 momentum is among the best-replicated anomalies, but it carries severe, partly forecastable crash risk (2009, 1932). Industry momentum and 52-week-high momentum are peer-reviewed variants. Time-series momentum is strong in diversified futures, but its statistical support has been seriously challenged (Huang et al. 2020). For single-market timing with "price vs 200-day average" filters, the evidence is mainly practitioner work and weak.

### Cited Findings
- **Momentum crashes.** Daniel & Moskowitz, "Momentum Crashes", *JFE* 122(2): 221-247, 2016 (peer-reviewed; NBER w20439). Momentum has "infrequent and persistent strings of negative returns" that are partly forecastable. The crashes happen in "panic" states, after market declines and when volatility is high, and they coincide with market rebounds. A dynamic, volatility-scaled momentum strategy is proposed. — [NBER w20439](https://www.nber.org/papers/w20439); [Chicago Booth Review](https://www.chicagobooth.edu/review/understanding-momentum-crashes)
- In the 1927-2013 US sample, during the worst episode the past-loser decile rose 163% while the past-winner decile gained only 8%. That episode was the 2009 rebound, according to background knowledge (March-May 2009, not verified here). — [NBER w20439 PDF](https://www.nber.org/system/files/working_papers/w20439/w20439.pdf) (via search snippet)
- Barroso & Santa-Clara, "Momentum Has Its Moments" (*JFE* 2015) reaches similar conclusions about volatility-managed momentum. — [search summary of NBER w20439 context](https://www.nber.org/papers/w20439)
- **Industry momentum.** Moskowitz & Grinblatt, "Do Industries Explain Momentum?", *Journal of Finance* 1999 (peer-reviewed). It uses 1963-1995 data and goes long the top 30% of industries and short the bottom 30%. — [IDEAS/RePEc related listing](https://ideas.repec.org/a/eee/pacfin/v32y2015icp111-130.html); [Alpha Architect summary](https://alphaarchitect.com/the-secret-to-momentum-is-the-52-week-high/) **[PRACTITIONER]**
- **52-week high.** George & Hwang, *Journal of Finance* 2004 (peer-reviewed). Nearness to the 52-week high "dominates and improves upon the forecasting power of past returns (both individual and industry returns)". A later study finds both industry and 52-week-high strategies profitable, but neither beats conventional momentum. — [Alpha Architect](https://alphaarchitect.com/the-secret-to-momentum-is-the-52-week-high/) **[PRACTITIONER]**; [IDEAS: 52-week high & sentiment](https://ideas.repec.org/a/eee/finana/v57y2018icp167-183.html); [IDEAS listing](https://ideas.repec.org/a/eee/intfin/v20y2010i4p423-435.html)
- **Time-series momentum.** Moskowitz, Ooi & Pedersen, *JFE* 2012 (peer-reviewed). The paper finds significant TSMOM in "each of the 58 liquid instruments" across equity index, currency, commodity and bond futures. TSMOM compares an asset's return with its own past, while cross-sectional momentum compares assets with each other. — [search summary](https://alphaarchitect.com/are-trend-following-and-time-series-momentum-research-results-robust/) **[PRACTITIONER summary]**
- A separate paper, Hurst, Ooi & Pedersen (AQR), reports a 136-year trend-following study with about 11% annualized excess return. It is a practitioner paper, not the MOP 2012 paper. — [search note](https://alphaarchitect.com/are-trend-following-and-time-series-momentum-research-results-robust/) **[PRACTITIONER]**
- **Challenge to TSMOM.** Huang, Li, Wang & Zhou, "Time-Series Momentum: Is It There?", *JFE* March 2020, 774-794 (peer-reviewed). The pooled-regression t-statistic "is not statistically reliable" because it falls below bootstrap critical values. The pooled slope is biased upward when assets have different mean returns without fixed effects, and volatility scaling makes this worse. Asset-by-asset tests show "little evidence of TSM, both in- and out-of-sample". — [WUSTL profile](https://profiles.wustl.edu/en/publications/time-series-momentum-is-it-there/); [SMU repository](https://ink.library.smu.edu.sg/lkcsb_research/6550); [CXO Advisory](https://www.cxoadvisory.com/momentum-investing/intrinsic-time-series-momentum-does-not-really-exist/) **[PRACTITIONER]**
- Rebuttal view: the pooled regression is flawed, but it is not the main evidence for TSMOM. Portfolio-level returns across many markets are. — [Philosophical Multicore blog](https://buttondown.com/mdickens/archive/contra-time-series-momentum-is-it-there/) (blog, not peer-reviewed)

### Inferences
- The case for TSMOM rests on diversification across about 58 futures markets. Evidence for a **single US equity index** trend rule (S&P 500 vs its 200-day moving average) is much thinner. It is mostly practitioner work, such as Faber's 2007 "A Quantitative Approach to Tactical Asset Allocation" (SSRN, practitioner; unverified this session). Its documented benefit is drawdown reduction rather than higher returns. The weaknesses are whipsaw in V-shaped recoveries (2020, 2022-23 style), few independent episodes (a handful of bear markets), and parameter mining over lookback windows.
- Short-term reversal (Jegadeesh 1990 *JF*; Lehmann 1990 *QJE*; background knowledge, unverified) is a 1-month signal with very high turnover. It is widely reported to be largely consumed by trading costs and concentrated in small, illiquid stocks. This needs verification before it is cited.
- Momentum pitfalls: (1) skip the most recent month to avoid contamination from short-term reversal (the "12-1" construction); (2) survivorship bias, since free price sources such as Yahoo usually omit delisted names, which inflates winner and loser returns; (3) delisting returns, since losers delist more often; (4) shorting losers runs into borrow costs and constraints in exactly the stocks that crash upward in rebounds.
- Volatility scaling (Daniel-Moskowitz, Barroso-Santa-Clara) is the main published crash mitigant. It uses only free daily price data.

### Gaps
- No verified post-publication or after-cost numbers for 12-1 momentum, short-term reversal or 52-week high in this session.
- No peer-reviewed source verified for the 200-day moving-average market-timing rule.
- The exact Daniel-Moskowitz 1932 crash figures were not retrieved.

---

## Q2. Low volatility / betting-against-beta

### Takeaway
The low-beta anomaly is peer-reviewed (Frazzini & Pedersen, *JFE* 2014). However, Novy-Marx & Velikov (*JFE* 2022) show that the published BAB construction is effectively equal-weighted and loaded on small, costly stocks. The value-weighted effect is smaller and largely spanned by profitability and investment factors. AQR-linked defenders dispute this.

### Cited Findings
- Novy-Marx & Velikov, "Betting Against Betting Against Beta", *JFE* 2022 (peer-reviewed). BAB's rank weighting is a "back door to equal weighting" that overweights the smallest stocks, which have limited capacity and are expensive to trade. BAB and equal-weighted BAB have a 0.996 monthly return correlation. — [Novy-Marx PDF](https://mysimon.rochester.edu/novy-marx/research/BABAB.pdf); [SUFE listing](https://academicnewsletter.sufe.edu.cn/info/354881)
- Value-weighted BAB still earned about 56 bp/month according to one summary. Cap-weighted BAB is similar to a portfolio of the profitability and investment factors. — [CXO Advisory](https://cxoadvisory.com/?p=31988) **[PRACTITIONER]**; [Alpha Architect](https://alphaarchitect.com/betting-against-beta-new-insights/) **[PRACTITIONER]**
- AQR-linked defense: over the 1920s to the present, value, rank and equal weighting perform similarly. Novy-Marx & Velikov look at only part of the sample, and their trading-cost estimates may be overstated. — [Alpha Architect, BAB construction](https://alphaarchitect.com/betting-against-beta-bab-construction/) **[PRACTITIONER]**

### Inferences
- Background knowledge, unverified: the original papers are Frazzini & Pedersen, "Betting Against Beta" (*JFE* 2014), and Ang, Hodrick, Xing & Zhang (*JF* 2006) on idiosyncratic volatility. Low-vol ETFs became very crowded around 2016 and lagged during rate shocks, so interest-rate (bond-proxy) exposure is a known risk.
- Pitfalls: beta estimation windows (Frazzini-Pedersen use separate correlation and volatility windows); BAB's leverage of the low-beta leg (a long-only investor cannot replicate it); the short leg in high-beta small caps carries borrow costs.

### Gaps
- The Frazzini-Pedersen effect sizes (Sharpe ratio, alpha) were not verified this session.
- No verified post-2014 out-of-sample US numbers.

---

## Q3. Short interest and days-to-cover (FINRA data, timing, daily short-sale volume)

### Takeaway
Stock-level short interest, especially scaled by turnover (days-to-cover), predicts low future returns. Aggregate short interest is a strong market-level predictor in the published sample, but its construction contains a look-ahead trap. FINRA data is free but semi-monthly with a lag of about 7 business days, and a 2026 FINRA proposal would change that schedule.

### Cited Findings
- **Days to cover.** Hong, Li, Ni, Scheinkman & Yan, "Days to Cover and Stock Returns", NBER WP w21166 (May 2015). It is a **working paper**; publication in a peer-reviewed journal was not confirmed. DTC is the short-interest ratio divided by average daily turnover, measured over 1988-2012. Equal-weighted long-low and short-high DTC deciles earn 1.19%/month gross, and value-weighted deciles earn 0.67%/month. DTC predicts returns better than the plain short ratio. — [NBER w21166](https://nber.org/papers/w21166); [CXO Advisory summary](https://www.cxoadvisory.com/short-selling/days-to-cover-short-interest-as-a-stock-return-predictor) **[PRACTITIONER]**
- Crash or implementation risk: DTC short positions are hard to cover and suffered large losses during the 2008 short-sale ban on financial stocks. — [CXO Advisory](https://www.cxoadvisory.com/short-selling/days-to-cover-short-interest-as-a-stock-return-predictor) **[PRACTITIONER]**
- **Aggregate short interest.** Rapach, Ringgenberg & Zhou, "Short Interest and Aggregate Stock Returns", *JFE* 2016 (peer-reviewed). The authors call it "arguably the strongest known predictor of aggregate stock returns". Annual R² is 12.89% in sample and 13.24% out of sample, with mean-variance utility gains above 300 bp per year. The sample runs 1973-2013, and a VAR decomposition attributes the predictability mainly to cash-flow news. — [SUFE listing](https://academicnewsletter.sufe.edu.cn/info/356349); [EconPapers](https://econpapers.repec.org/RePEc:cuf:wpaper:716); [WashU Olin release](https://source.washu.edu/2015/05/why-investors-should-listen-to-short-sellers-yes-short-sellers/) (author institution)
- The Short Interest Index (SII) is the equal-weighted average of short interest as a percentage of shares outstanding, **linearly detrended** and then standardized. The SII strategy does not outperform in 1990-1995 and underperforms in 2000-2007. — [CXO Advisory](https://cxoadvisory.com/short-selling/aggregate-short-interest-and-future-stock-market-returns) **[PRACTITIONER]**
- **FINRA timing (current rule).** Member firms report short positions by 6 p.m. ET on the 2nd business day after the reporting settlement date. FINRA makes the data available for publication on the **7th business day after the settlement date**. Settlement dates are mid-month (the 15th or the prior settlement day) and month-end, and FINRA publishes an annual calendar. — [FINRA Short Interest Reporting](https://www.finra.org/filing-reporting/short-interest); [FINRA Equity Short Interest data](https://finra.org/finra-data/browse-catalog/equity-short-interest)
- **Proposed change.** SR-FINRA-2026-012, filed 13 May 2026, proposes **weekly** reporting, a 1-business-day reporting turnaround, and dissemination **5 business days** after settlement instead of 7. SEC approval status was not confirmed. — [SR-FINRA-2026-012 PDF](https://www.finra.org/sites/default/files/2026-05/SR-FINRA-2026-012.pdf); [Federal Register public inspection](https://public-inspection.federalregister.gov/2026-09864.pdf)

### Inferences
- **Look-ahead in SII:** the published SII is detrended using the full sample. A real-time version must detrend with only past data (expanding-window regression), or the in-sample fit is overstated. Rapach et al. report out-of-sample R², but anyone building it from FINRA data should rebuild the detrending recursively.
- **Point-in-time timing:** a short-interest observation for settlement date T is not public until about T + 7 business days, which can mean 9-11 calendar days. A backtest keyed to settlement date has look-ahead.
- **Daily short-sale volume is not short interest** (background knowledge; FINRA documentation not fetched). FINRA's daily "Reg SHO" short-sale volume files count trades marked short on a given day. Much of that volume comes from market makers and liquidity providers shorting to fill customer buys, which is closed out the same day. The files measure flow, not outstanding positions, and they do not show covering. Short-volume ratios near 40-50% for many stocks are normal and should not be read as bearish positioning.
- DTC is cheap to compute from free data: FINRA short interest divided by average daily volume from free price feeds. The large equal-weighted vs value-weighted gap (1.19% vs 0.67%) suggests the effect is concentrated in smaller stocks. The short side is exactly where borrow is costly or unavailable.

### Gaps
- No verified post-2012 or post-2013 out-of-sample performance for DTC or SII.
- FINRA's documentation on the daily short-sale volume files could not be fetched (domain blocked).
- Whether SR-FINRA-2026-012 has been approved or put into effect as of Nov 2026 is unknown.

---

## Q4. Options-implied signals: put/call ratios, VIX term structure, IV skew, implied-realized spread; free vs paid

### Takeaway
The best peer-reviewed stock-level option signal (Xing, Zhang & Zhao 2010 smirk) needs per-stock implied volatilities. Those come from paid data (OptionMetrics or Cboe DataShop), not free sources. Free data covers aggregate Cboe put/call ratios (daily statistics page, with a free archive for 2006-2019) and index-level VIX family indices. Signals built on free data are mostly index-level, and their evidence is thinner.

### Cited Findings
- **IV smirk.** Xing, Zhang & Zhao, "What Does the Individual Option Volatility Smirk Tell Us About Future Equity Returns?", *JFQA* 45(3): 641-662, June 2010 (peer-reviewed). Stocks with the steepest smirks underperform those with the flattest smirks on a risk-adjusted basis. The sample covers 1996-2005 for all optionable stocks. Predictability persists for holding periods of up to about 6 months, with diminishing returns, and it is robust to size, B/M, idiosyncratic volatility and momentum. — [IDEAS/RePEc](https://ideas.repec.org/a/cup/jfinqa/v45y2010i03p641-662_00.html); [Cambridge Core](https://resolve.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/what-does-the-individual-option-volatility-smirk-tell-us-about-future-equity-returns/ECFD16BA9ACBDC8D577D1BD866FBEA72); [CXO Advisory](https://www.cxoadvisory.com/volatility-effects/smirking-because-they-know-something/) **[PRACTITIONER]**
- The roughly 10.9%/year spread is reported only secondhand (an arXiv paper citing the original for 1996-2005), so it is unverified. — [arXiv 2608.26115](https://arxiv.org/pdf/2608.26115)
- **Cboe put/call data.** Cboe's historical page has a free file of volume and put/call ratios from 01 Nov 2006 to 04 Oct 2019. Current figures are on the free Cboe Daily Market Statistics page, and custom history is sold through Cboe DataShop (paid). — [Cboe Historical Options Data](https://cboe.com/us/options/market_statistics/historical_data/); [Cboe Daily Market Statistics](https://www.cboe.com/us/options/market_statistics/daily/)
- A third-party claim says Cboe "retired" its free historical ratio files in 2019. That conflicts with the archive still listed on Cboe's page. — [The Trading Tools manual](https://www.thetrading.tools/manuals/put-call-ratio); [Cboe page](https://ww2.cboe.com/us/options/market_statistics/historical_data)
- Third-party aggregators republish the equity put/call series, for example Alphacast from 2006 to 2026. How it is compiled was not verified. — [Alphacast](https://www.alphacast.io/datasets/equity-put-call-ratio-38727)

### Inferences
- What is free: Cboe daily total, index and equity put/call ratios from the daily statistics page (scraping is needed for continuity); VIX, VIX9D, VIX3M and VIX6M index levels, also on FRED for VIXCLS (background knowledge); and realized volatility from free daily prices. What is paid: per-stock implied volatility surfaces, skew and open interest history (OptionMetrics/WRDS, Cboe DataShop, ORATS).
- **Put/call:** Background knowledge, unverified: Pan & Poteshman (*RFS* 2006) found that open-buy put/call ratios built from non-public, signed volume data predict stock returns. Public aggregate put/call ratios are mostly a contrarian sentiment gauge with weak, regime-dependent evidence. Do not cite Pan-Poteshman as support for the free aggregate ratio.
- **VIX term structure** (VIX/VIX3M above 1 means backwardation, or stress): no peer-reviewed evidence was retrieved this session on equity return prediction from VIX/VIX3M or VIX9D. Most claims are practitioner work, and many concern VIX futures and ETP returns rather than equities.
- **Implied-realized spread** (variance risk premium): background knowledge, unverified. Bollerslev, Tauchen & Zhou (*RFS* 2009) found that the index-level VIX² minus realized variance predicts quarterly market returns. It can be computed from free VIX and S&P data, but it works at the **index level** only. The stock-level version needs paid data.
- Pitfalls: Cboe changed its product mix and the definitions of its index and equity put/call ratios over time; VIX methodology changed in 2003 (VXO vs VIX); VIX3M was renamed from VXV; and put/call data is published after the close, so same-day trading on it is look-ahead.

### Gaps
- Effect sizes for VIX term-structure and put/call-ratio equity timing were not verified.
- No verified post-2005 out-of-sample evidence for the Xing-Zhang-Zhao smirk.

---

## Q5. Volume and attention: abnormal volume, high-volume return premium

### Takeaway
The high-volume return premium is a peer-reviewed, internationally replicated, short-horizon effect (days to about 50 days) attributed to investor visibility. It needs only free price and volume data, but it is a short-horizon, higher-turnover signal.

### Cited Findings
- Gervais, Kaniel & Mingelgrin, "The High-Volume Return Premium", *Journal of Finance* 56(3): 877-919, 2001 (peer-reviewed). Stocks with unusually high volume over a day or week earn positive excess returns afterward, and the effect is significant over 50-day horizons in NYSE data. It is attributed to Merton's (1987) investor-recognition effect. — [IDEAS/RePEc](https://ideas.repec.org/p/fth/pennfi/01-99.html); [Wharton WP PDF](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9901.pdf)
- Kaniel, Li & Starks find the premium persistent in almost all developed and emerging markets. — [search summary, SUFE listing](https://academicnewsletter.sufe.edu.cn/info/361520)

### Inferences
- Abnormal volume should be measured relative to a trailing window that excludes the event day. Volume data from free sources (consolidated vs primary exchange) can differ, so be consistent.
- After-cost performance is unverified. The short horizon implies high turnover, which likely matters most in small caps.

### Gaps
- No verified post-2001 US decay or after-cost numbers.

---

## Q6. Macro and cross-asset: credit spreads and the excess bond premium, yield curve, dollar, oil, copper/gold, macro surprises, pre-FOMC drift

### Takeaway
The best-documented macro signals are the excess bond premium, which is peer-reviewed, published free by the Fed monthly, and mainly predicts **economic activity and recession**, and the oil-predicts-stocks effect (Driesprong et al. 2008, peer-reviewed, about 1-month horizon). The pre-FOMC drift was large in 1994-2011 but has shifted, shrunk and possibly disappeared since. The copper/gold ratio is practitioner-only. All are index- or sector-level signals.

### Cited Findings
- **Excess bond premium.** Gilchrist & Zakrajšek, "Credit Spreads and Business Cycle Fluctuations", *American Economic Review* 102(4): 1692-1720, June 2012. It is peer-reviewed, and note it is in the *AER*, not a finance journal. The GZ credit spread splits into an expected-default component and a residual excess bond premium (EBP), and the predictive content of spreads comes mainly from the EBP. A rising EBP signals a fall in financial-sector risk-bearing capacity and a contraction in credit supply. — [NBER w17021](https://www.nber.org/papers/w17021); [CMU WP PDF](https://www.cmu.edu/tepper/faculty-and-research/assets/docs/GZ_25June2010.pdf)
- FEDS Notes (2016) use the EBP to predict NBER recessions. The EBP is significantly more informative than the expected-default component. Since Oct 2016 the Fed has published monthly updates of the EBP and the model-implied recession probability (CSV linked from the note; data from Jan 1973). The page was last updated 05 Mar 2026. — [FEDS Note Apr 2016](https://www.federalreserve.gov/econresdata/notes/feds-notes/2016/recession-risk-and-the-excess-bond-premium-20160408.html); [FEDS Note Oct 2016 update](https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html); [openICPSR replication files](https://openicpsr.org/openicpsr/project/112536/version/V1/view)
- **Oil.** Driesprong, Jacobsen & Maat, "Striking Oil: Another Puzzle?", *JFE* 2008 (peer-reviewed). Oil price changes predict stock returns in 12 of 18 developed markets and in the world index. Rising oil is followed by lower stock returns. The effect is not explained by time-varying risk; the authors attribute it to underreaction, and it strengthens with multi-day lags. A related paper finds the effect lasts about 1 month. — [Erasmus repository](https://repub.eur.nl/pub/1017); [SUFE listing](https://academicnewsletter.sufe.edu.cn/info/357332); [ECU WP](https://economics.ecu.edu/wp-content/pv-uploads/sites/165/2019/07/ECU0912.pdf)
- **Pre-FOMC drift.** Lucca & Moench (NY Fed SR512; published in *JF* 2015) found that about 80% of annual realized US excess equity returns since 1994 are accounted for by the drift before scheduled FOMC announcements. — [NY Fed SR512](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf)
- Decay: the authors' 2018 update finds positive post-2011 pre-FOMC returns only on press-conference days. — [Liberty Street Economics 2018](https://libertystreeteconomics.newyorkfed.org/2018/11/the-pre-fomc-announcement-drift-more-recent-evidence.html)
- A BIS paper finds the drift moved to the 2nd day before announcements and shrank to about 22 bp after 2011, with about one third explained by liquidity shocks. — [BIS WP 1079](https://www.bis.org/publ/work1079.pdf)
- Kurov, Wolfe & Gilbert, "The Disappearing Pre-FOMC Announcement Drift" (*Finance Research Letters*, per background knowledge): the drift disappeared for non-press-conference meetings and weakened substantially from 2016 even with press conferences. Versions differ on the break date (2015 vs 2016). — [Skidmore PDF](https://www.skidmore.edu/economics/documents/KurovWolfeGilbert-TheDisappearingPre-FOMC-Announce-Drift-200914.pdf); [SSRN author page](https://papers.ssrn.com/author=3571041)
- Counter-view: the drift concentrates in high-uncertainty periods, so the apparent post-2011 fade may be time variation. — [Quantpedia](https://vvv.quantpedia.com/es/wp-json/wp/v2/posts/4197) **[PRACTITIONER summary]**

### Inferences
- The EBP is first a **macro and recession** predictor. Using it for equity returns is a step removed. A rising EBP coincides with equity drawdowns rather than reliably preceding them at short horizons. The free FRED alternatives are BAA10Y (Moody's Baa minus 10-year Treasury) and BAMLH0A0HYM2 (ICE BofA HY OAS). Background knowledge: FRED's ICE BofA series have had history-length restrictions imposed by the licensor, so check current coverage.
- **EBP vintages:** the EBP is a model residual re-estimated each month, so history can be revised. Use archived vintages (or record your own) for honest backtests. The same applies to any macro series subject to revision (use ALFRED vintages for FRED data).
- **Yield-curve slope** (T10Y3M, T10Y2Y on FRED): background knowledge, unverified. The literature (Estrella & Mishkin 1998 and others) supports the slope as a **recession** predictor at 12-18 month horizons. Its record for equity-return timing is weak, with long, variable lags. Few independent recessions exist, so the sample is small.
- **Dollar:** no peer-reviewed source verified this session for US equity return prediction from the trade-weighted dollar (FRED DTWEXBGS).
- **Copper/gold ratio:** no peer-reviewed source found. Treat it as a **practitioner-only** claim, usually framed as a 10-year yield co-movement indicator rather than an equity-return predictor.
- **Macro surprise indices:** Citi Economic Surprise Index is proprietary (Bloomberg). A free alternative would need consensus forecasts, which are mostly paid. Free proxies include the Philadelphia Fed Survey of Professional Forecasters, Atlanta Fed GDPNow vs consensus, and ALFRED first releases. No peer-reviewed evidence on surprise-index equity timing was verified.
- Oil-to-energy-sector linkage: the Driesprong result concerns broad market returns. A sector-level oil-to-energy-stock lead-lag was not verified separately. Contemporaneous co-movement of oil and energy stocks is not a predictive signal.

### Gaps
- No verified evidence on EBP or credit spreads predicting equity returns specifically (as opposed to activity).
- No peer-reviewed support found for copper/gold or the dollar as US equity predictors.
- Post-2008 out-of-sample performance of the oil effect was not verified.

---

## Q7. Seasonality and calendar effects: turn of the month, earnings-announcement premium, pre-holiday

### Takeaway
The earnings-announcement premium is peer-reviewed-adjacent and widely cited (Frazzini & Lamont, NBER), with international follow-ups. The evidence for turn-of-the-month and pre-holiday effects was not verified this session. They are index-level effects with old origins and risk from multiple testing.

### Cited Findings
- Frazzini & Lamont, "The Earnings Announcement Premium and Trading Volume", NBER WP w13090 (2007). It is a **working paper**, and journal publication was not confirmed. Monthly strategies earn 7-18% annual excess returns around earnings announcements, and the premium is linked to trading volume. Buying stocks expected to announce in the coming month and shorting the rest earns more than 60 bp/month. — [NBER w13090](https://www.nber.org/papers/w13090); [NBER Digest](https://www.nber.org/digest/mar08/stocks-rise-around-earnings-announcements)
- Replication caveat: no earnings-announcement premium was found on the Oslo Stock Exchange for 1999-2007 (non-US thesis). — [NHH thesis](https://openaccess.nhh.no/nhh-xmlui/handle/11250/168103)
- Global version: practitioner summary. — [Alpha Architect](https://alphaarchitect.com/introducing-the-global-earnings-announcement-premium/) **[PRACTITIONER]**

### Inferences
- Implementation needs **expected** announcement dates known in advance. Frazzini-Lamont predict them from the prior year's dates. Using actual dates, as found in free calendars after the fact, is look-ahead.
- Turn of the month (Ariel 1987 *JFE*; Lakonishok & Smidt 1988 *RFS*; McConnell & Xu 2008 *Financial Analysts Journal*) and pre-holiday (Ariel 1990 *JF*) are background knowledge, unverified this session. They are index-level, small per-event effects. Sullivan, Timmermann & White (1999) on data-snooping in calendar effects is the key caution reference (unverified).

### Gaps
- No verified effect sizes or post-publication evidence for turn-of-the-month or pre-holiday effects.
- The 7.3% earnings-announcement-premium figure in the brief was not verified (the search found a 7-18% range).

---

## Q8. Sector rotation by business cycle or regime

### Takeaway
Textbook business-cycle sector rotation adds little. Even with perfect knowledge of NBER cycle phases it beat the market by only about 2.3%/year (1948-2007), and realistic timing errors and costs eliminate statistical significance.

### Cited Findings
- Stangl, Jacobsen & Visaltanachoti, "Sector Rotation over Business Cycles" (working paper). It uses 1948-2007 monthly industry returns across 10 NBER cycles. Perfect cycle foresight yields about 2.3%/year outperformance, and realistic timing errors and frictions eliminate significance. — [CXO Advisory](https://www.cxoadvisory.com/economic-indicators/perfect-sector-rotation) **[PRACTITIONER summary]**; [Scribd copy](https://es.scribd.com/document/54155014/Sector-Rotation-Over-Business-Cycles)
- Molchanov & Stangl, "The Myth of Business Cycle Sector Rotation", *International Journal of Finance and Economics* 2023 (peer-reviewed). Conventional rotation yields modest outperformance that "quickly diminishes" after transaction costs and cycle-timing errors. — [Massey repository](https://mro.massey.ac.nz/handle/10179/69590); [AUT PDF](https://acfr.aut.ac.nz/__data/assets/pdf_file/0005/294287/The-Myth-of-Sector-Rotation-non-blind.pdf)

### Inferences
- NBER dates are announced months to more than a year after the fact, so any backtest using them is pure look-ahead. Real-time regime classification needs vintage macro data (ALFRED).
- The rotation-style evidence that is better supported is industry momentum (Q1), not macro-phase rotation.

### Gaps
- No verified peer-reviewed evidence for regime-switching (for example, Markov-model) sector rotation that survives costs out of sample.
