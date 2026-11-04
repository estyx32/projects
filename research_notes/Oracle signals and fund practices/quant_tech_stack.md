# Quant Research Tech Stacks for Small Shops and Individual Researchers (as of 2026-11-02)

Method note: release dates and licenses below come from the PyPI JSON API (queried 2026-11-02), which is a primary source for release activity. The GitHub REST API, duckdb.org, quantconnect.com and vectorbt.pro could not be fetched directly from this session (network allow-list), so star counts are mostly missing and some QuantConnect/DuckDB facts come from search-result summaries of official pages. Those cases are flagged.

## Q1. For daily-bar, small-universe research, which stack choices are best supported and least likely to be abandoned?

### Takeaway
The data layer (DuckDB, Polars, pandas, Parquet) is very healthy, and all three libraries shipped new major or minor versions in Sep-Oct 2026. Among backtesting frameworks, LEAN, NautilusTrader, vectorbt (open-source), bt and zipline-reloaded are all actively released. backtrader has not released since April 2023 and should be treated as abandoned. Qlib releases slowly, its official dataset is disabled, and it is China-market oriented. For a daily, small-universe US equity book, plain DuckDB/Polars/pandas plus your own small engine is the best-supported and lowest-abandonment-risk choice. Frameworks add dependency risk without adding much at this scale.

### Cited Findings
**Data / dataframe layer**
- DuckDB: MIT license. 2.0.0 stable was released 2026-10-21, after 1.5.6 (2026-09-28), 1.5.5 (2026-07-22) and 1.5.4/1.4.5 (2026-06-17). Nightly 2.1.0 dev builds were published on 2026-11-01. Releases are very active. — [PyPI duckdb](https://pypi.org/project/duckdb/)
- Polars: MIT license. 2.0.0 was released 2026-10-06 and 2.1.0 on 2026-10-25, with the 1.44.x line in Aug-Sep 2026. — [PyPI polars](https://pypi.org/project/polars/)
- pandas: BSD-3-Clause license. 3.0.x patch releases ran May-Sep 2026 and 3.1.0 was released 2026-10-22. — [PyPI pandas](https://pypi.org/project/pandas/)
- Benchmarks (secondary sources, treat as indicative):
  - DuckDB Labs has maintained the H2O.ai db-benchmark since 2023. — [DuckDB blog, 2023-04-14](https://duckdb.org/2023/04/14/h2oai)
  - A 2026 vendor-run test on 10M rows: Polars 2.0 ran the 10 group-by queries in 2.86 s, DuckDB 1.5 in 3.91 s and pandas 3.0 in 16.39 s. pandas was slowest on every query. — [Uvik 2026](https://uvik.net/blog/polars-vs-pandas/)
  - Another 2026 blog cites roughly 0.45 s for Polars against 12.5 s for pandas on a 10M-row group-by. — [tech-insider 2026](https://tech-insider.org/polars-vs-pandas-2026/)
  - No ClickBench numbers were retrieved.
- ArcticDB (Man Group):
  - Releases are very active (6.28.0 to 6.28.2 in Oct 2026). — [PyPI arcticdb](https://pypi.org/project/arcticdb/)
  - It is under the Business Source License 1.1, and each version converts to Apache 2.0 after a set period. — [ArcticDB licensing docs](https://docs.arcticdb.io/dev/licensing/)
  - ArcticDB's sales page says business use, including research environments, needs a commercial license. — [arcticdb.io/sales](https://arcticdb.io/sales/)
  - Per-version conversion dates were not verified.
- TimescaleDB: no current release data was retrieved (GitHub API blocked). See Gaps.

**Backtesting / trading frameworks**
- QuantConnect LEAN CLI (`lean` package): Apache-2.0 license. Version 1.0.233 was released 2026-10-27, and releases are frequent. — [PyPI lean](https://pypi.org/project/lean/)
- NautilusTrader:
  - License is LGPL-3.0-or-later. The last stable release is 1.231.0 (2026-08-02). The 2.0.0 release candidates rc3 to rc8 ran Aug-Oct 2026, with rc8 on 2026-10-29. — [PyPI nautilus_trader](https://pypi.org/project/nautilus-trader/)
  - The 2.0 line drops the legacy Cython package for a Rust + PyO3 core and offers "a deterministic event-driven runtime for both research and live execution". Interactive Brokers is a listed integration. — [NautilusTrader v2.0.0rc3 release notes](https://github.com/nautechsystems/nautilus_trader/releases/tag/v2.0.0rc3)
  - Flag: 2.0 is still pre-release, and PyPI warns it may not be production-stable. — [PyPI 2.0.0rc8](https://pypi.org/project/nautilus-trader/2.0.0rc8/)
- zipline-reloaded:
  - 3.2.0 was released 2026-10-18 and 3.2.1 on 2026-10-25. Before that, the previous release was 3.1.1 in July 2025. — [PyPI zipline-reloaded](https://pypi.org/project/zipline-reloaded/)
  - 3.2.x supports Python 3.11 to 3.14. "Pandas 3 and Python 3.15 remain excluded." 3.2.0 fixed accounting for stock dividends, reverse splits and partial fills. — [zipline-reloaded releases](https://github.com/stefan-jansen/zipline-reloaded/releases)
  - The maintainers say Zipline is kept for compatibility and critical bug fixes, and they point new feature work to the ML4T libraries. — [zipline-reloaded releases](https://github.com/stefan-jansen/zipline-reloaded/releases)
  - The successor, `ml4t-backtest`, is MIT-licensed and at 0.2.0 (2026-10-22), so it is very young. — [PyPI ml4t-backtest](https://pypi.org/project/ml4t-backtest/)
- backtrader: license is GPLv3+. The last release was 1.9.78.123 on 2023-04-19, and before that 2020-07-03. There have been no releases for more than 3.5 years, so it is effectively unmaintained. — [PyPI backtrader](https://pypi.org/project/backtrader/)
- vectorbt (open-source):
  - Releases resumed in 2026: 1.0.0 (2026-04-22), 1.1.0 (2026-07-05) and 1.2.0 (2026-10-19). — [PyPI vectorbt](https://pypi.org/project/vectorbt/)
  - Historically the license is Apache 2.0 with Commons Clause, which restricts selling the software. — [PyPI vectorbt 0.24.2](https://pypi.org/project/vectorbt/0.24.2)
  - The current 1.x license was not re-verified.
- vectorbt PRO:
  - A paid, private-repo product. The FAQ describes a one-time payment, but says access to the private repo, Discord and new releases ends with the paid term. Commercial use requires contacting the vendor. — [vectorbt.pro FAQ](https://vectorbt.pro/faq)
  - Current price could not be retrieved (site not reachable from this session).
- bt (pmorissette): MIT license. Versions 1.3.0, 1.4.0 and 1.4.1 were released 2026-10-03 to 10-10. It is a portfolio/rebalancing-style vectorized backtester and is active. — [PyPI bt](https://pypi.org/project/bt/)
- backtesting.py: AGPL-3.0 license. Version 0.6.6 was released 2026-07-22. Releases are slow but alive. — [PyPI backtesting](https://pypi.org/project/backtesting/)
- Qlib (Microsoft):
  - PyPI `pyqlib` 0.9.7 (2025-08-15) is the latest release, with about one release a year. MIT license. — [PyPI pyqlib](https://pypi.org/project/pyqlib/)
  - The GitHub README says the official dataset is "temporarily disabled" because of a data security policy. Bundled data commands target China (`--region cn`), and the data comes from Yahoo Finance, which "might not be perfect". — [microsoft/qlib](https://github.com/microsoft/qlib)
  - About 49.9k stars. The README's feature list still shows v0.9.0 (Dec 2022) as the latest release, which conflicts with PyPI 0.9.7. — [microsoft/qlib](https://github.com/microsoft/qlib)
  - The sister project RD-Agent does LLM-driven factor mining. — [microsoft/qlib](https://github.com/microsoft/qlib)
- Lumibot, a newer entrant with live-broker focus: GPL-3.0 license, with several releases a day (4.6.42 on 2026-11-02). — [PyPI lumibot](https://pypi.org/project/lumibot/)
- Supporting libraries: exchange_calendars 4.13.2 (2026-03-10) and quantstats 0.0.86 (2026-09-27). — [PyPI exchange_calendars](https://pypi.org/project/exchange-calendars/); [PyPI quantstats](https://pypi.org/project/quantstats/)

### Inferences
- **Event-driven vs vectorized** (my classification from project design, not from a single source):
  - Event-driven: LEAN, NautilusTrader, zipline-reloaded, backtrader and Lumibot.
  - Vectorized: vectorbt and bt (portfolio-tree, closer to vectorized).
  - backtesting.py is a bar-iteration hybrid.
- **Live trading:** LEAN, NautilusTrader and Lumibot have live trading. zipline-reloaded, bt, vectorbt OSS and Qlib are research/backtest only.
- **Don't recommend:** backtrader (abandoned). Qlib for US daily equities is not a good fit (China-centric, dataset disabled, slow releases).
- **Use with care:**
  - zipline-reloaded: maintenance mode, and it pins pandas below 3, which will conflict with a pandas-3 stack.
  - NautilusTrader 2.0: pre-release.
  - vectorbt: its license has a Commons Clause.
- At tens to a few hundred names on daily bars, a dataset is roughly 300 tickers × 252 days × 20 years, about 1.5M rows. pandas handles this in memory without trouble. Polars and DuckDB matter for ergonomics and correctness (explicit lazy plans, SQL as-of joins) more than for speed.

### Gaps
- GitHub stars, open-issue counts and contributor counts for most projects (GitHub API blocked). TimescaleDB release status and license detail (Apache-2 core vs Timescale License for some features) were not verified this session.
- vectorbt 1.x current license text and vectorbt PRO current price.
- Independent, dated ClickBench comparison.

## Q2. Can DuckDB query a SQLite file directly, and is that a good pattern for research on top of an OLTP store?

### Takeaway
Yes. DuckDB's core `sqlite` extension can `ATTACH` a SQLite file and read its tables as if they were DuckDB tables. Locking is delegated to SQLite, so there are many concurrent readers and one writer. That works well for ad-hoc analysis over a WAL-mode SQLite system of record. The extension can also write, so research access should use `ATTACH ... (TYPE sqlite, READ_ONLY)` or a periodic Parquet export.

### Cited Findings
- `ATTACH 'file.db' AS name;` lets "the tables in the file … be read as if they were normal DuckDB tables". Data is read from SQLite at query time. — [duckdb/duckdb-sqlite README](https://github.com/duckdb/duckdb-sqlite)
- The extension also supports CREATE, INSERT, UPDATE, DELETE, ALTER, DROP and transactions that "directly modify the SQLite database", plus `COPY` to and from Parquet. — [duckdb/duckdb-sqlite README](https://github.com/duckdb/duckdb-sqlite)
- Concurrency is handled by SQLite, not DuckDB: mutexes within a process and file-system locks across processes. Many readers and one writer, and behaviour depends on SQLite settings such as WAL mode. — [DuckDB SQLite extension docs (current)](https://duckdb.org/docs/current/core_extensions/sqlite) (via search summary; page not directly fetchable)
- Newer docs list `BUSY_TIMEOUT` (default 5000 ms) and `JOURNAL_MODE` attach options. — [DuckDB 2.0 SQLite docs](https://duckdb.org/docs/2.0/core_extensions/sqlite) (via search summary)
- `sqlite_all_varchar` reads every column as VARCHAR. It avoids type-mismatch errors caused by SQLite's dynamic typing, and it must be set before ATTACH. — [DuckDB SQLite docs](https://duckdb.org/docs/current/core_extensions/sqlite) (via search summary)
- Local test, DuckDB 2.0.0: `ATTACH 'x.db' AS o (TYPE sqlite, READ_ONLY)` blocked an INSERT and saw rows held in the WAL. A SQLite trigger fired on an UPDATE sent through a writable attach. `ATTACH 'file:x.db?mode=ro'` was taken as a literal filename and created a new, empty database.

### Inferences
- **Good pattern at this scale:** the worker writes to SQLite (WAL), and research uses DuckDB `ATTACH` for ad-hoc joins and window functions. WAL readers don't block the writer.
- **Caveats:**
  - DuckDB writes are allowed on a writable attach, so the immutability triggers in SQLite are the real guard. Triggers fire on writes via DuckDB too, because SQLite itself executes them (confirmed in the local test).
  - Attaching with `READ_ONLY` is safer than relying on discipline. Do not use a `mode=ro` URI in `ATTACH`. Take any copy of the live file with SQLite's backup API, because in the local test a plain file copy missed a committed row still in the WAL.
  - Scans through the extension are row-store reads, so repeated heavy backtests re-read and re-convert data each time.
- **Recommended layering:** keep SQLite as the system of record. Run a nightly or on-demand `COPY (SELECT … ) TO 'snapshot_YYYYMMDD/*.parquet'` to create immutable, versioned research snapshots. Run backtests against Parquet with DuckDB or Polars. This gives reproducibility (a backtest is pinned to a snapshot hash) and isolates research from production writes.

### Gaps
- Official documentation of read-only attach semantics. The behaviour above was tested locally only.
- No measured benchmark of `sqlite_scan` throughput against Parquet for this data size was found.

## Q3. Which backtesting frameworks correctly handle point-in-time fundamentals, delistings and corporate actions, and how much do they cost?

### Takeaway
Correct point-in-time handling is mostly a data problem, not a framework problem. QuantConnect is the only option reviewed that bundles survivorship-aware US equity prices, a security master (splits, dividends, symbol changes) and Morningstar fundamentals including delisted companies. Even there, users report gaps for some delisted names. Every open-source framework (zipline-reloaded, Nautilus, vectorbt, bt) is only as point-in-time-correct as the data you feed it. That data typically has to be paid for from vendors such as Norgate or Sharadar.

### Cited Findings
- QuantConnect's Morningstar US Fundamentals covers about 8,000 US equities from January 1998 at daily frequency. It relies on the US Equity Security Master (splits, dividends, symbol changes), and the docs reference fundamentals for "all US Equities (including delisted companies)". — [QC US Fundamental Data docs](https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/morningstar/us-fundamental-data) (via search summary)
- QC staff confirmed that Morningstar no longer had data for a delisted name (CTEK) and were "waiting to hear back" on wider survivorship impact. A relisted name (PFGC) lacked fundamentals for its earlier listing period. — [QC forum 14219](https://www.quantconnect.com/forum/discussion/14219/fundamental-data-missing-for-delisted-stocks/) (user and staff forum; colour)
- QuantConnect pricing (official page via search summary):
  - Researcher is about $84/month ($888/year). Team is about $168/month with 2 to 10 users.
  - Live-node prices are listed separately and were not retrieved.
  - Third-party sites show older or lower prices, so they conflict.
  - — [QuantConnect pricing](https://www.quantconnect.com/pricing.md); [tier features](https://www.quantconnect.com/docs/v2/cloud-platform/organizations/tier-features)
- LEAN CLI live deployment with Schwab requires a paid-tier organization. — [QC LEAN CLI Schwab docs](https://www.quantconnect.com/docs/v2/lean-cli/live-trading/brokerages/charles-schwab) (via search summary)
- zipline-reloaded 3.2.0 fixed accounting for stock dividends, reverse splits and partial fills. This means corporate-action handling had bugs until October 2026. — [zipline-reloaded releases](https://github.com/stefan-jansen/zipline-reloaded/releases)
- Qlib's default data is Yahoo-sourced and "might not be perfect". Users are advised to prepare their own high-quality data. — [microsoft/qlib](https://github.com/microsoft/qlib)
- Practitioner guidance (blogs, colour only):
  - Look-ahead often hides in an innocent-looking fundamentals `merge()`. The fix is point-in-time data that keeps the first-published value and later revisions. — [dev.to tradevodata](https://dev.to/tradevodata/your-backtest-saw-the-future-lookahead-bias-in-fundamental-data-measured-across-313562-rows-4cba)
  - Building a universe from today's ticker list causes survivorship bias. The fix is to include delisted securities and historical index membership. — [dev.to survivorship vs lookahead](https://dev.to/tradevodata/survivorship-bias-vs-lookahead-bias-the-two-silent-backtest-killers-pmm)

### Inferences
- For the target architecture, store fundamentals bitemporally, with `period_end`, `filed_at`/`available_at` and `ingested_at`, in the append-only SQLite store. Always join with an as-of rule (`available_at <= decision_time`). DuckDB `ASOF JOIN` and Polars `join_asof` make this explicit.
- Store raw unadjusted prices plus a corporate-actions table, and derive adjusted series at query time. That is more robust than storing vendor-adjusted prices, which change retroactively.
- Paying for survivorship-free data matters more than choosing a framework.

### Gaps
- Current prices of Norgate, Sharadar (Nasdaq Data Link) and similar point-in-time US datasets were not retrieved this session.
- No authoritative audit of point-in-time correctness was found for any open-source framework.

## Q4. Is there a mature Python client for the Charles Schwab Trader API, and how well maintained is it?

### Takeaway
There are two unofficial, MIT-licensed options. schwab-py (alexgolec, successor to tda-api) is the more established design, but it has not had a release since June 2025 or a commit since August 2025, so it is stale as of Nov 2026. schwabdev (Tyler Bowers) is more actively released, with 4.0.0 in August 2026. QuantConnect/LEAN also has a first-party Schwab brokerage integration. Neither Python library supports paper trading, because Schwab's API does not.

### Cited Findings
- schwab-py: MIT license. Latest release is 1.5.1 (2025-06-30), after 1.5.0 (2025-03-09) and 1.4.0 (2024-09-14). — [PyPI schwab-py](https://pypi.org/project/schwab-py/)
- schwab-py repo: about 480 stars, 131 forks, 39 open issues and 17 open PRs. — [GitHub alexgolec/schwab-py](https://github.com/alexgolec/schwab-py)
- schwab-py features: auth with token refresh, quotes, fundamentals, price history, option chains, streaming quotes and book depth, orders and account info. No paper trading. Unofficial and not endorsed by Schwab. — [GitHub alexgolec/schwab-py](https://github.com/alexgolec/schwab-py)
- The last commits on schwab-py main are 2025-08-04 ("Update patreon info") and 2025-06-30 (v1.5.1). — [schwab-py commits](https://github.com/alexgolec/schwab-py/commits/main)
- schwabdev:
  - MIT license. 4.0.0 was released 2026-08-09, after 3.0.4 and 3.0.5 in May 2026. — [PyPI schwabdev](https://pypi.org/project/schwabdev/)
  - Features automatic token management and streaming with auto-restart. Needs both "Accounts and Trading Production" and "Market Data Production" on the Schwab app. Rate limit is 120 requests per minute. — [PyPI schwabdev](https://pypi.org/project/schwabdev/)
  - About 761 stars per an aggregator, which is unverified. — [gittrend](https://gittrend.io/repo/tylerebowers/Schwabdev)
- QuantConnect Schwab integration:
  - Supports equities, options, index options, and cash and margin accounts. No futures and no Schwab paper trading (QC's own paper brokerage is used instead).
  - Available in QC Cloud, local platform and LEAN CLI (paid tier). Source is in Lean.Brokerages.CharlesSchwab.
  - Users report authentication friction and a weekly token renewal step.
  - A 2026 LEAN update added Schwab StopLimit orders.
  - — [QC Schwab docs](https://quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/charles-schwab); [LEAN update](https://www.quantconnect.com/lean/19555/async-non-market-orders-schwab-stoplimit-cme-fops/); [forum 18001](https://www.quantconnect.com/forum/discussion/18001/integrate-brokerage-schwab-in-quantconnect/) (vendor-stated or forum)

### Inferences
- **Recommended setup:** put the Schwab client behind a thin internal adapter interface such as `BrokerClient.place_order` or `get_positions`, so you can swap schwab-py and schwabdev. Schwab refresh tokens expire after about 7 days (QC's "weekly token renewal" is consistent with this), so the worker needs a re-auth alert in the dashboard.
- **schwab-py staleness:** this is not yet abandonment, because the API surface is stable, but it is worth monitoring.
- **No paper trading:** a dry-run mode in your own engine, logging intended orders, is required.

### Gaps
- Whether schwab-py has unreleased activity or an announced status was not found. schwabdev's GitHub stars were not verified directly.

## Q5. Assessment of the proposed architecture: should it add a DuckDB/Parquet research store, when should it move to Postgres, and what are the common mistakes?

The proposed architecture:
- SQLite in WAL mode as the system of record, with immutability triggers and an audit log
- a separate worker process for data collection
- FastAPI with a server-rendered Jinja dashboard
- a deterministic pure-function engine for sizing, risk and exits, shared by backtest and live
- an LLM research process that can only write proposals
- single user on a personal machine, tens to a few hundred US stocks, daily data

### Takeaway
The architecture fits the scale. Its strongest features are the shared deterministic engine and the append-only, audited store, and they directly address the biggest practitioner failure modes. Add DuckDB as a read-only analytical layer now; it is cheap. Add Parquet snapshots once backtests or signal sweeps become frequent or need to be reproducible. Postgres is not justified by data volume at this scale. Move to it only on concurrency or topology triggers: multiple writers, multiple users or machines, a remote or always-on server, or a need for row-level permissions. Do not adopt a large framework such as LEAN, Nautilus or zipline unless you need its specific capability, for example LEAN's bundled point-in-time data or broker adapters.

### Cited Findings
- The volume sizing in Q1 (about 1.5M rows) is my inference. At that size, the pandas, Polars and DuckDB speed gaps in benchmarks (seconds on 10M+ rows) are immaterial. — [Uvik 2026 benchmark](https://uvik.net/blog/polars-vs-pandas/)
- DuckDB can attach the SQLite store directly and `COPY` to Parquet, which supports the "OLTP + columnar snapshot" pattern without a new server. — [duckdb-sqlite README](https://github.com/duckdb/duckdb-sqlite)
- SQLite allows one writer at a time across processes, with locking via file-system locks. This is the hard limit that would motivate Postgres. — [DuckDB SQLite docs](https://duckdb.org/docs/current/core_extensions/sqlite) (via search summary)
- NautilusTrader's own docs warn that live execution brings in "venue, transport, timing, persistence, external-activity, and reconciliation behavior" that a simulation may not reproduce. This applies equally to a home-grown shared engine. — [NautilusTrader 2.0.0rc3 notes](https://github.com/nautechsystems/nautilus_trader/releases/tag/v2.0.0rc3)
- zipline-reloaded pins pandas below 3, so adopting it would constrain the whole Python environment. — [zipline-reloaded releases](https://github.com/stefan-jansen/zipline-reloaded/releases)
- Common look-ahead mistakes (blogs, colour):
  - `shift(-1)`, and rolling or normalisation statistics computed on the full series before a train/test split. — [skills.sh backtest-review checklist](https://www.skills.sh/shakeebshaan/claude-code-quant-skills/backtest-review)
  - Same-bar execution, where a signal from today's close trades at today's close. — [Python in Plain English 2026](https://python.plainenglish.io/backtesting-in-python-why-most-backtests-lie-2026-d0600dd75f72)
  - Forgetting to lag positions with `shift(1)`, described as "the most common failure in retail backtests". — [dev.to backtesting guide](https://dev.to/kakembo_muhammed_53dbbc54/backtesting-trading-strategies-in-python-the-complete-guide-for-developers-fai)
  - Anecdotal magnitude: one blog reports a look-ahead bug turning a strategy of about 4.7% into about 164%. This is unverified.

### Inferences
**Recommendations for this architecture** (synthesis, not sourced as a single claim):
1. **DuckDB now.** Use it as a research query engine with `ATTACH` on the SQLite file, attached with `READ_ONLY`. It brings SQL window functions and `ASOF JOIN` for point-in-time joins at no operational cost.
2. **Parquet research store when needed.** Add it when any of these apply:
   - backtests run often or as parameter sweeps
   - you want each backtest or LLM proposal pinned to an immutable data snapshot (record the snapshot id or hash in the audit log)
   - you add wide feature or factor tables that don't belong in the OLTP schema
   - Layout: Hive-partitioned by table or date, written only by an export job, never edited.
3. **Postgres (TimescaleDB is optional and unnecessary for daily bars).** Move when any of these apply:
   - more than one machine or user, or the dashboard is served remotely
   - several concurrent writers (for example multiple collectors or the LLM process writing proposals at high frequency) and `SQLITE_BUSY` contention appears
   - you need role-based access, such as making the LLM process unable to write by database permission rather than by application code
   - you need managed backups or point-in-time recovery for a service that must be up
   - Data size alone is not a trigger for daily bars on a few hundred names.
4. **Keep the engine pure and shared.** Make the backtest loop "replay of the live path":
   - Feed decision-time snapshots in.
   - Make `decision_time` and `data_available_at` explicit arguments, so no function can read data stamped after `decision_time`.
   - Add a test that asserts no data with a timestamp after the decision time is accessible to the engine.
5. **LLM write-only-proposals boundary.** Enforce it at the storage layer: a separate SQLite file or table with triggers, or Postgres roles later. Keep LLM-generated research code in a separate package from the production engine.

**Common mistakes** (synthesised from practitioner sources above plus general consensus):
- Rewriting into a big framework too early. You inherit its data model, pandas pins and abandonment risk, as with backtrader and zipline's maintenance mode, without needing its features at daily frequency.
- pandas look-ahead: negative shifts, full-sample normalisation, same-bar fills, and fundamentals merged on period end instead of filing date.
- Survivorship bias from using today's ticker list.
- Using vendor back-adjusted prices that silently change history, which breaks reproducibility.
- Mixing research notebooks and production code: production imports from notebooks, or research code path-dependent on live state.
- Unpinned data snapshots, which make backtest results irreproducible.

### Gaps
- No conference talk (PyData or QuantCon) specifically endorsing "SQLite + DuckDB + Parquet for single-user quant" was retrieved. The recommendation is an inference from tool capabilities and scale.
- No authoritative source quantifies SQLite write-contention thresholds for this workload.
