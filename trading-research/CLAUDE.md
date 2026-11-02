# Trading research and command center (tradelab)

Personal, single-user trading research system. Claude researches and proposes; deterministic code
sizes, gates and records. **Today it runs in shadow mode only: no broker adapter exists and nothing
can be sent.** Research tooling, not financial advice.

Start here in a new session: read `docs/SESSION_HANDOFF.md` (what the user asked for, decisions, research, open questions), `docs/PLAYBOOK.md` (the user's risk rules, scorecard, journal, review cadence) and `docs/STACK.md`.

## Hard rules (violating one is a bug even when tests pass)

1. Claude never decides or places orders. It writes proposals via `engine.submit_proposal()`; the
   engine sizes them, the risk gate checks them, the user approves.
2. The web process never holds broker credentials and never talks to a broker.
3. The gate fails closed: a missing or stale input (price, regime, earnings date, short interest)
   blocks the trade. Never turn a missing value into a pass or a zero.
4. Limits live only in `config/risk.toml`. The engine refuses to run unless `config_reviewed = true`.
   Do not invent default limits. `config/risk.example.toml` numbers are placeholders, not advice.
5. Raw data is immutable (trigger-enforced). Entry-time trade fields, decided proposals, events and
   the audit log cannot be edited or deleted. Fix mistakes with a new record, never an UPDATE.
6. "Today" means the New York trading day: use `tradelab.db.market_today()` and
   `market_day_start_utc()`. Never `date.today()` or the UTC date (the daily-loss limit would reset at 7-8 PM ET).
7. Untrusted text (transcripts, news, Claude output) is autoescaped in templates; links go through
   `views.safe_url`. Never `|safe`. Never put untrusted text in an inline script or style (CSP forbids it).
8. Tests use synthetic data only. Never commit real account data, journal, keys or tokens. `data/` and `backups/` are git-ignored.
9. The UI has no login yet (by request). It is local-only by construction: bind 127.0.0.1, Host and Origin checks, CSRF token.
   **Add real authentication before it is reachable from anywhere else.**

## Layout

- `schema.sql` raw layer, prices, calls, trades, audit log, report views. `schema_engine.sql` proposals, orders, events, system state, equity, market snapshots, news.
- `tradelab/ingest.py` store raw docs (hashed), prices, market snapshots, news. `validate.py` data-quality checks. `report.py`, `backup.py`.
- `tradelab/engine/` `config.py` `sizing.py` `exits.py` (pure functions) `regime.py` `risk_gate.py` `state.py` (kill switch, events) `engine.py` (submit, approve, reject, shadow orders).
- `tradelab/web/` FastAPI app, `views.py` (rows to display dicts, no HTML), `format.py`, Jinja `templates/partials/` (one per panel, polled by `static/app.js`).
- `scripts/seed_demo.py` synthetic demo data. `scripts/run_ui.sh` local server. `tests/` 55 tests.

## Commands

```
pip install -e ".[web,dev]"        # or: pip install fastapi uvicorn jinja2 httpx pytest ruff
pytest -q                          # all tests (~3s)
ruff check tradelab tests scripts
python3 scripts/seed_demo.py       # synthetic data -> data/demo.db, config/demo.toml (demo only)
TRADELAB_DB=data/demo.db TRADELAB_CONFIG=config/demo.toml scripts/run_ui.sh   # http://127.0.0.1:8000
```

## Status (what is and is not verified)

Verified by tests and a real-browser click-through on synthetic data: sizing, exits, config validation,
regime from stored data, the risk gate, approve/reject/kill switch, shadow orders, event feed, escaping,
CSRF/Host/Origin guards, the New York trading-day boundary.

Not built:
- Worker process (collectors, equity snapshots, heartbeat, exit monitor). The heartbeat in the demo is seeded.
- Collectors: prices, VIX and global indices, FRED, EDGAR, news, short interest, earnings dates. Nothing real flows in yet.
- Claude research agent that reads transcripts/filings and calls `submit_proposal` (use structured output, validate against the proposal fields).
- Broker adapter (Schwab) and any non-shadow mode. `SUPPORTED_MODES = ("shadow",)` and the gate blocks other modes.
- Fills: approving records shadow orders but no `trades` row, so "Open positions" stays empty until fills exist. Needs a fill handler that inserts the trade and a loop that calls `evaluate_exit`.
- Options (puts, spreads) are rejected by the gate. Sector and correlation exposure limits from the playbook are not implemented yet.
- Backtest harness (replay through the same pure functions; log every variant tested; report deflated Sharpe) and walk-forward validation.
- Authentication, Postgres port (the immutability triggers are SQLite syntax), push alerts.
- `fetch_youtube_transcript` has never run against live YouTube.

Known design wrinkles: the demo `market_snapshots` SPY value differs from the SPY price history (two sources for one quantity;
derive snapshots from `prices` in the real collectors). Regime uses only SPY vs 200-day average and VIX; global markets feed the
shock check and the dashboard but do not vote yet.

## Broker notes (from a third-party library's docs, verify on Schwab's developer portal)

App approval is manual. Refresh tokens expire after 7 days, so unattended runs need a weekly browser re-login. Stops and targets must rest
at the broker as bracket/stop orders so they fire if this system is down. Stop and bracket support, short selling and a paper/sandbox
mode were unclear. Rate limits apply (HTTP 429, honor Retry-After).

## Rollout plan

Shadow (now) -> approval mode (user taps approve, orders sent) -> automate exits and risk limits first -> auto-entries only later at a small
size cap, if the journal justifies it. Manual `workflow` for the user: playbook doc, journal, and quarterly review against SPY.
