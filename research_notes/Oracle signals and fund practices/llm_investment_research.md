# LLMs in Equity Investment Research (2023-2026): Where They Add Measurable Value, and How They Fail

Research note. Not financial advice. Collection limits: arxiv.org, ar5iv and faculty.chicagobooth.edu could not be fetched from this session (network allow-list), so paper details below come from search-result abstracts and snippets, not full texts. Figures that could not be checked against a primary full text are flagged. Peer-review status is given as "working paper" unless a journal or conference acceptance was found.

## Which LLM uses show out-of-sample, after-cost evidence, and which are only in-sample or marketing?

### Takeaway
The strongest evidence is for **news-headline sentiment → next-day returns** (Lopez-Lira & Tang). Its signal is reported as out-of-sample relative to the training cutoff, but it falls sharply after realistic costs, sits in small stocks and negative news, and has decayed as LLM adoption spread. It is still a working paper. The flagship evidence for **financial-statement analysis/forecasting** (Kim, Muhn & Nikolaev) and **"Bloated Disclosures"** reportedly has been withdrawn after replication problems. **Agentic trading systems** largely fail once tested after the model's training cutoff ("profit mirage"; StockBench). Earnings-call LLM signals are mostly preprints, student projects or vendor research.

### Cited Findings

**News headline sentiment (Lopez-Lira & Tang, "Can ChatGPT Forecast Stock Price Movements?")**
- First posted April 2023; latest arXiv version is v6, dated 28 Oct 2025. The search found no journal publication (no journal name or DOI), so it remains a **working paper** (arXiv/SSRN). Lopez-Lira also wrote a Wiley book (2024) based on it. — [arXiv v6](https://arxiv.org/abs/2304.07619v6); [Awesome LLM Papers listing](https://awesomepapers.io/large-language-models/publications/lopezlira2023can); [e-bookshelf book excerpt](https://content.e-bookshelf.de/media/reading/L-24459016-a587883cfc.pdf)
- Claim: ChatGPT sentiment scores significantly predict out-of-sample daily stock returns and subsume traditional sentiment methods. Predictability is stronger in smaller stocks and after negative news. — [arXiv v6 abstract](https://arxiv.org/abs/2304.07619v6)
- **After-cost (2023 version):** the long-short strategy's cumulative return was over 500% before costs. It falls to about 350% at 10 bp per trade and about 50% at 25 bp per trade. — [arXiv 2304.07619 (via search snippet)](https://arxiv.org/pdf/2304.07619v6); [Wharton Jacobs Levy slides](https://jacobslevycenter.wharton.upenn.edu/wp-content/uploads/2024/09/Lopez-Lira.pdf)
- **Decay (Oct 2025 version):** "Strategy returns decline as LLM adoption rises, consistent with improved price efficiency." The authors also say exploiting the pattern is feasible only for participants with very low trading costs, such as market makers. — [arXiv v6](https://arxiv.org/html/2304.07619v6)
- **Independent replication:** a University of Vienna thesis using GPT-3.5-Turbo found "only a small part of positive returns seem to persist after transaction costs." This is a thesis, not peer-reviewed. — [Univie Phaidra](https://services.phaidra.univie.ac.at/api/object/o:2082913/download)
- **Related working paper (ChatGPT and DeepSeek, 2025):** reports net-of-cost certainty-equivalent-return gains of 3.55%, and attributes part of the predictability to ChatGPT labelling more than half of WSJ news as neutral. — [arXiv 2502.10008](https://arxiv.org/pdf/2502.10008)
- Press coverage at the time presented the result as "ChatGPT beats the market", without cost caveats. This is an example of marketing-style amplification. — [ai-cio](https://ai-cio.com/news/ai-application-chatgpt-beats-stock-market-study-says); [PlanAdviser](https://www.planadviser.com/print-page?cid=88677)

**Financial statement analysis (Kim, Muhn & Nikolaev, "Financial Statement Analysis with Large Language Models", Chicago Booth, May 2024)**
- Method: GPT-4 (GPT-4-Turbo era) received standardized, **anonymized** balance sheets and income statements with chain-of-thought prompts. Reported results: it beat the median analyst at forecasting the direction of annual earnings, performed on par with a purpose-trained ANN, and "trading strategies based on GPT's prediction yield a higher Sharpe ratio and alphas than strategies based on machine-learning-based models." The authors argued the results do not stem from memorization. — [Chicago Booth Fama-Miller page](https://www.chicagobooth.edu/research/fama-miller/finance-research/funding/a-demand-system-approach-for-fixed-income/financial-statement-analysis-with-large-language-models); [CLS Blue Sky Blog](https://clsbluesky.law.columbia.edu/2024/09/16/will-large-language-models-propel-financial-statement-analysis-into-a-new-era/?amp=1)
- **Status:** a search summary of the arXiv listing (2407.17866) says the paper is **withdrawn by Valeri Nikolaev**, with the latest version dated Feb 2025. **Not verified directly**, because arXiv was unreachable. — [arXiv 2407.17866v3](https://arxiv.org/abs/2407.17866v3)
- Commentary notes that earnings-direction accuracy does not directly translate into market-beating returns. — [Market Monetarist](https://marketmonetarist.com/2024/05/28/)

**"Bloated Disclosures: Can ChatGPT Help Investors Process Information?" (Kim, Muhn & Nikolaev)**
- Nikolaev's Booth faculty page (per search snippet) says a co-author's replication attempt "did not support the reported findings." Nikolaev reviewed and confirmed the inconsistencies, and the working paper "has been withdrawn from circulation." A separate paper by the same authors, "From Transcripts to Insights: Uncovering Corporate Risks Using Generative AI", is not withdrawn. — [Nikolaev ongoing research page](https://faculty.chicagobooth.edu/valeri-nikolaev/ongoing-research-projects)

**Earnings calls**
- ECC Analyzer (GPT-4-Turbo) extracts fine-grained earnings-call signals for **volatility** prediction and beats prior methods. *Directly prompting* the LLM for volatility performed poorly. Preprint. — [arXiv 2404.18470](https://arxiv.org/pdf/2404.18470)
- "Same Company, Same Signal" (preprint) finds that company identity drives much of what models learn from transcripts. This is a leakage/shortcut concern. — [arXiv 2412.18029](https://arxiv.org/pdf/2412.18029)
- S&P Global Market Intelligence (industry research reported in Fortune, Sept 2025) says LLM long-short strategies built on transcripts roughly doubled benchmark returns. **Vendor research**: not peer-reviewed, and no after-cost or post-cutoff details were given. — [Fortune](https://fortune.com/2025/09/23/how-ai-changing-earnings-call-analysis-stock-picks)
- A Sharpe of 2.26 for an LLM earnings-call signal circulates on Substack, but its paper and venue could not be verified. — [Substack note](https://substack.com/@quantitativo/note/c-253874660)
- Sarkar & Vafa found **look-ahead bias** in predicting risk factors from earnings calls with Llama-2 (see next section). — [NBER conference PDF](https://conference.nber.org/conf_papers/f205530/f205530.pdf)

**Agentic research / trading systems**
- "Profit Mirage" (preprint, Oct 2025) splits test periods around each underlying model's training cutoff. "All LLM-based agents show a significant drop in the generalization setting": back-tested returns "evaporate once the model's knowledge window ends." — [arXiv 2510.07920](https://arxiv.org/html/2510.07920v1)
- StockBench (preprint, Oct 2025) is a contamination-free multi-month benchmark on DJIA stocks, March to July 2025. Agents see only data available at each decision time. Most LLM agents fail to beat buy-and-hold, and "excelling at static financial knowledge tasks does not necessarily translate into successful trading strategies." — [arXiv 2510.02209](https://arxiv.org/pdf/2510.02209); [Multi-agent evaluation survey, arXiv 2603.27539](https://arxiv.org/pdf/2603.27539)

### Inferences
- The table below summarises evidence quality per use case.

| Use case | Representative study / model | Data and period | Out-of-sample vs cutoff? | After-cost? | Decay | Peer-reviewed? |
|---|---|---|---|---|---|---|
| Headline sentiment | Lopez-Lira & Tang; ChatGPT (GPT-3.5/4) | US news headlines, daily returns | Claimed yes | Yes, large haircut | Yes (adoption) | No (working paper) |
| Financial-statement forecasting | Kim/Muhn/Nikolaev; GPT-4 | Compustat-style statements, anonymized | Argued, mostly pre-cutoff | Sharpe/alpha reported | n/a | No; reportedly withdrawn |
| Disclosure summarisation | "Bloated Disclosures"; GPT-3.5 | 10-K/MD&A, earnings calls | n/a | n/a | n/a | Withdrawn |
| Earnings-call signals | ECC Analyzer, S&P Global | Transcripts | Mostly unclear | Rarely | Unknown | Preprints / vendor |
| Agentic trading | Profit Mirage, StockBench | Post-cutoff 2025 windows | Yes | Partially | Fails post-cutoff | Preprints |

- Exact sample sizes, dates and model versions for several rows could not be confirmed from full text (see Gaps).
- Practically, no LLM return signal in this set has peer-reviewed, post-cutoff, after-cost evidence. The best case (headline sentiment) is real but has been arbitraged down and is cost-sensitive.

### Gaps
- Lopez-Lira & Tang specifics (sample period, headline count, GPT versions, daily long-short return or Sharpe) could not be read from the full text because arXiv was blocked. From memory, and **unverified here**: the original sample ran from about Oct 2021 to Dec 2022, after GPT-3.5's stated ~Sept 2021 cutoff.
- No 2023-2026 peer-reviewed journal acceptance (JF, JFE, RFS, Management Science, JAR) was confirmed for any LLM return-prediction paper in this search. Glasserman & Lin is listed in *Journal of Financial Data Science* per secondary sources.
- No practitioner reports from Man Group, Two Sigma, Bridgewater AIA, JPMorgan or Goldman were retrieved. Their claims could not be assessed.
- The reason for withdrawing the Kim/Muhn/Nikolaev financial statement analysis paper was not retrieved.

## How large is the look-ahead bias problem when backtesting LLM signals, and what mitigations exist?

### Takeaway
Look-ahead and memorization are severe for **pre-cutoff** tests of frontier models. GPT-4o recalls pre-cutoff macro and market numbers almost perfectly. Prompt instructions to ignore future data do not work, and masking names often does not either. For headline-sentiment signals specifically, two studies (Glasserman & Lin; ChronoBERT) found the bias to be modest. The robust mitigations are time-stamped (chronologically consistent) models and genuinely post-cutoff evaluation over adequate samples. Anonymization helps partially.

### Cited Findings
- **Glasserman & Lin (Sept 2023; listed in *J. Financial Data Science*):** they separate *look-ahead bias* from a *distraction effect*, in which the model's general knowledge about a firm distorts sentiment. In-sample, **anonymized headlines outperformed** the originals, so distraction outweighed look-ahead. Out-of-sample, look-ahead was not a concern but distraction remained. They propose anonymization for both backtesting and live use. — [arXiv 2309.17322](https://arxiv.org/html/2309.17322v1); [IDEAS/RePEc](https://ideas.repec.org/p/arx/papers/2309.17322.html)
- **Sarkar & Vafa, "Lookahead Bias in Pretrained Language Models" (Harvard; ICML 2025 workshop):** they build one-sided tests that use events assumed unpredictable; if a model predicts one, leakage is confirmed. They find look-ahead bias when predicting risk factors from earnings calls (Llama-2) and election winners from biographies. Prompting fixes are limited. Their remedy is models trained only on text produced before the analysis period, i.e. time-indexed LMs. — [NBER conference PDF](https://conference.nber.org/conf_papers/f205530/f205530.pdf); [ICML 2025](https://icml.cc/virtual/2025/48685); [CXO Advisory summary](https://www.cxoadvisory.com/investing-expertise/lookahead-bias-in-large-language-model-training-data)
- **Lopez-Lira, Tang & Zhu, "The Memorization Problem" (Apr 2025, SSRN revised Apr 2026; working paper, AFA program):** GPT-4o recalls S&P 500 levels, unemployment and GDP figures from before its Oct 2023 cutoff. Directional accuracy exceeds 96%, and recall is near-perfect for rates. There is **no recall after the cutoff**. Instructions to ignore post-cutoff data failed, and masking entity names failed because the model reconstructs entities and dates from context. Small post-cutoff "robustness" samples cannot separate skill from memorization. They suggest converting text to anonymized "economic logic." — [SSRN 5217505](https://papers.ssrn.com/abstract=5217505); [arXiv 2504.14765](https://arxiv.org/html/2504.14765v2); [Quantpedia summary](https://quantpedia.com/the-memorization-problem-can-we-trust-llms-forecasts/)
- **He, Lv, Manela & Wu, "Chronologically Consistent LLMs" (ChronoBERT/ChronoGPT, Feb 2025, v3 Jul 2025; AEA 2026 program):** a pair of models per year from 1999, trained only on text available at that date. On next-day return prediction from news, ChronoBERT's real-time outputs reach Sharpe ratios comparable to state-of-the-art models, "indicating that lookahead bias is modest." AEA listing: portfolio performance matches a much larger Llama 3.1. — [arXiv 2502.21206](https://arxiv.org/html/2502.21206v2); [AEA 2026](https://www.aeaweb.org/conference/2026/program/paper/BrRDGQHe)
- **DATEDGPT (2026 preprint):** a family of 1.3B models with strict annual cutoffs, 2013-2024. **Look-Ahead-Bench (Jan 2026 preprint):** a standardized benchmark of point-in-time LLMs that reports significant look-ahead bias in standard LLMs. — [DATEDGPT, arXiv 2603.11838](https://arxiv.org/pdf/2603.11838); [Look-Ahead-Bench, arXiv 2601.13770](https://arxiv.org/pdf/2601.13770)
- Agent-level evidence: the "Profit Mirage" collapse after cutoff (above). — [arXiv 2510.07920](https://arxiv.org/html/2510.07920v1)
- "Anonymization and Information Loss" (Nov 2025 preprint) studies the cost of anonymizing: stripping identifiers also removes useful information. — [arXiv 2511.15364](https://arxiv.org/pdf/2511.15364)

### Inferences
- The size of the bias is **task-dependent**:
  - It is small for short-horizon headline sentiment, where the label is the model's reading of tone (ChronoBERT; Glasserman-Lin).
  - It is large for anything that asks the model to *forecast* numeric outcomes it may have seen (macro levels, earnings, agent P&L).
- Mitigation hierarchy:
  1. Point-in-time / chronologically consistent models.
  2. Evaluation strictly after the deployed model's cutoff, with large enough samples and pre-registered signal definitions.
  3. Anonymization: it reduces distraction but does not reliably stop memorization, and it loses information.
  4. Prompt instructions alone: ineffective.
- Every model upgrade resets the clean out-of-sample window to that model's own cutoff. Back-history evaluated with a new model is contaminated by construction.

### Gaps
- No study found that quantifies the look-ahead inflation of Sharpe ratios for 10-K-based signals specifically.
- Vendor "point-in-time" claims for commercial LLMs could not be verified.

## Which tasks (extraction, summarisation, change detection, sentiment, forecasting) are most reliable?

### Takeaway
Reliability ranks roughly as follows:
1. **Sentiment/classification of short text.** Robust across studies and least prone to look-ahead.
2. **Extraction / QA over provided documents**, when the full relevant context is given and outputs are checked. With poor retrieval it fails often.
3. **Summarisation.** The flagship evidence was withdrawn.
4. **Direct numeric forecasting and autonomous trading.** Weakest; most exposed to memorization.

### Cited Findings
- **FinanceBench (Islam et al., Patronus AI, Nov 2023; preprint):** 10,231 open-book questions on SEC filings. Human review covered 2,400 answers from 16 configurations on 150 cases.
  - GPT-4-Turbo with a shared-vector-store retrieval system answered incorrectly or refused **81%** of questions (19% correct, 68% refused).
  - With a per-document store it reached about 50% correct and 39% refused.
  - With long context it reached 79% correct (Claude-2: 76%). An oracle page gave 85%. Closed-book accuracy was about 9-11%.
  - GPT-4-Turbo tended to refuse when uncertain, whereas Llama-2 hallucinated more.
  - A third-party aggregator reports a 17-21% hallucination rate for the long-context setups; that figure is not from the paper.
  — [Patronus AI announcement](https://patronus.ai/announcements/patronus-ai-launches-financebench-the-industrys-first-benchmark-for-llm-performance-on-financial-questions); [arXiv 2311.11944](https://web3.arxiv.org/abs/2311.11944?context=cs); [Beancount research log](https://beancount.io/bean-labs/research-logs/2026/05/12/financebench-open-book-financial-qa-benchmark); [benchmarklist](https://benchmarklist.com/benchmarks/financebench/)
- Sentiment: headline sentiment predicts returns out-of-sample (Lopez-Lira & Tang), and point-in-time small models match larger ones (ChronoBERT). This suggests the task does not need frontier-model world knowledge. — [arXiv 2304.07619](https://arxiv.org/abs/2304.07619v6); [arXiv 2502.21206](https://arxiv.org/html/2502.21206v2)
- Earnings calls: LLM *extraction* of fine-grained features, followed by a downstream model, beat direct LLM prompting for volatility. — [arXiv 2404.18470](https://arxiv.org/pdf/2404.18470)
- Agents: static financial-knowledge skill does not translate into trading skill. — [StockBench](https://arxiv.org/pdf/2510.02209)
- Summarisation: "Bloated Disclosures" was withdrawn after a failed replication. — [Nikolaev page](https://faculty.chicagobooth.edu/valeri-nikolaev/ongoing-research-projects)

### Inferences
- The most reliable architecture uses the LLM as a **feature extractor or classifier**, with a separate, conventionally validated statistical model on top. Using the LLM as an end-to-end forecaster or trader is less reliable. ECC Analyzer and ChronoBERT both point this way.
- Change detection between filings (e.g. new risk factors) is plausibly reliable, because it is an extraction/diff task. No 2023-2026 study with return evidence was retrieved for it.

### Gaps
- No peer-reviewed numbers were found for structured extraction accuracy from XBRL or 10-Q tables.
- No change-detection return study was retrieved, although "Lazy Prices"-style LLM follow-ups may exist.

## What verification practices do practitioners use, and what failure modes are documented?

### Takeaway
Documented failure modes include:
- hallucinated or unsupported numbers (FinanceBench);
- look-ahead/memorization (above);
- distraction by firm identity (Glasserman-Lin; "Same Company, Same Signal");
- withdrawn or unreplicable results (Bloated Disclosures);
- indirect prompt injection via ingested documents;
- correlated behaviour or herding when many firms use the same models.

Verification practice centres on grounding outputs in cited source spans, schema-constrained outputs, deterministic numeric checks and isolating the agent from execution. Evidence on prompt-wording sensitivity and overconfidence was not retrieved in this pass.

### Cited Findings
- **Prompt injection:**
  - "Poisoning Agentic Alpha" (2026 preprint): indirect injection via a social-media analyst agent achieved 29.8% success for SELL-targeted and 24.0% for BUY-targeted attacks in a multi-agent trading system. Its arXiv ID (2608.24069) is unusual and unverified. — [arXiv 2608.24069](https://arxiv.org/pdf/2608.24069)
  - ICLR 2026: vulnerabilities across all roles (Analyst, Researcher, Trader, Risk Manager) on six large tech stocks. — [ICLR 2026](https://iclr.cc/virtual/2026/10016542)
  - A fintech survey ranks indirect injection through RAG-ingested reports as the highest-priority risk. — [arXiv 2605.30650](https://arxiv.org/pdf/2605.30650)
  - A red-teaming competition (464 participants, 272k attempts, 13 models) compromised every model in at least one scenario. — [arXiv 2603.15714 via Emergent Mind](https://www.emergentmind.com/papers/2603.15714)
  - In the wild, Forcepoint (Apr 2026) found hidden payloads targeting financial fraud, including a fully specified PayPal transaction aimed at agents. — [Help Net Security](https://helpnetsecurity.com/2026/04/24/indirect-prompt-injection-in-the-wild)
  - Design pattern: a paper-trading agent is built so that a successful injection cannot reach the broker. — [lablab.ai](https://lablab.ai/ai-hackathons/alpaca-ai-trading-agents-hackathon/cleanroom)
- **Herding/crowding:**
  - Bank of England (2025): if many firms use similar AI models and data, they are more likely to take similar positions and amplify shocks under stress. — [PYMNTS on BoE](https://www.pymnts.com/news/artificial-intelligence/2025/bank-england-warns-higher-market-volatility-from-ai-driven-trading/)
  - The IMF reportedly ranked herding and concentration as top GenAI capital-market risks. This was reported secondhand.
  - Federal Reserve Board (Nov 2025): LLM agents were rational 61-97% of the time vs 46-51% for humans in lab experiments, but they can be induced to herd. — [FRBSF / Fed Board](https://www.frbsf.org/research-and-insights/publications/board-of-governors/2025/11/financial-stability-implications-generative-ai-taming-the-animal-spirits/); [Investment Executive](https://www.investmentexecutive.com/news/research-and-markets/ai-traders-more-rational-less-herd-like/)
  - Gensler & Bailey (2020) argued that model standardization and interconnection raise herding risk. — [MIT Sloan](https://mitsloan.mit.edu/node/45966)
  - Lopez-Lira & Tang's finding that strategy returns decline as adoption rises is direct evidence of crowding in one signal. — [arXiv v6](https://arxiv.org/html/2304.07619v6)
- **Citations / structured outputs:**
  - Anthropic's Citations feature returns `cited_text` with `document_index` and start/end character offsets, letting each claim be checked against the exact source span. — [claudemaster guide](https://claudemaster.net/learn/how-to-add-citations-to-claude-api-responses); [Citeformer ADR-013](https://citeformer.readthedocs.io/en/latest/decisions/013-citation-rich-attribution.html)
  - Anthropic's documentation confirms that Citations **cannot be combined** with structured outputs in a single request (it returns a 400). It suggests asking for one cited `field: value` line per fact and parsing the lines in code. — [Anthropic Citations docs](https://platform.claude.com/docs/en/build-with-claude/citations)

### Inferences
Practical design implications for a system where an LLM reads filings and proposes trades, while code verifies the numbers:
1. **Separate reading from deciding.** The LLM extracts typed facts (value, unit, period, filing accession, page/span) into a strict schema. Code computes ratios and deltas and generates signals. The LLM never emits a final number that code has not recomputed.
2. **Ground every number.** Require a verbatim source span for each extracted figure, then check it deterministically:
   - the string appears in the filing;
   - the parsed value matches;
   - it reconciles to XBRL where available.

   Citations and JSON schema cannot be combined in one call, so use two passes (cite, then structure), parse cited `field: value` lines, or have code match spans itself.
3. **Treat filings as untrusted input.** The model that reads documents gets no tool access to orders. Trades go through a code-enforced risk layer, with position limits and human approval above thresholds.
4. **Backtest only with point-in-time inputs and post-cutoff windows** for the exact model version. Freeze model versions per backtest. Consider chronologically consistent models for history. Anonymize to reduce distraction, but do not rely on it against memorization. Revalidate on each model upgrade.
5. **Prefer the LLM as a feature generator** feeding a simple, conventionally validated model, with realistic costs. Expect small-cap/negative-news concentration and alpha decay as adoption spreads.
6. **Robustness checks:**
   - test prompt-paraphrase stability and run-to-run variance (temperature, versions);
   - log prompts and outputs for audit;
   - monitor correlation of signals with widely available LLM-sentiment factors to detect crowding.
7. **Prefer abstention over guessing.** FinanceBench shows a refusal is safer than a hallucination, so route refusals or low-confidence extractions to human review.

### Gaps
- No primary study on **prompt-wording sensitivity** of financial LLM signals was retrieved in this pass. It is a known issue but uncited here.
- No primary study on **LLM overconfidence or calibration** in financial forecasting was retrieved.
- No practitioner write-ups (Man Group, Two Sigma, Bridgewater AIA, JPMorgan, Goldman) on verification workflows were retrieved. Claims about industry practice in the Inferences above are design reasoning, not documented practice.
- OpenAI's official structured-output and citation documentation was not fetched directly.
