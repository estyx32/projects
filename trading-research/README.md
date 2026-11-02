# tradelab

Auditable data layer for a personal trading research workflow. Research tooling only, not financial advice.

## What it guarantees

| Control | How it is enforced |
| --- | --- |
| Raw data is never edited | `raw_documents` blocks UPDATE and DELETE; each row stores a SHA-256 of its content |
| Every derived row has a source | `calls` reference `raw_documents`; foreign keys are on |
| Entry-time trade facts cannot be rewritten | Trigger locks variant view, invalidation, entry price, size and stop after insert |
| Closed trades are final | A trade can be closed once; only review fields (`rule_breaches`, `post_mortem`) stay editable |
| Trades are never deleted | Trigger blocks DELETE |
| Every trade change is logged | Append-only `audit_log` written by triggers |
| Bad inputs are rejected | CHECK constraints: positive prices, valid directions, stop on the losing side of entry, close needs exit price and reason |
| Reports are trustworthy | `build_report` runs validation first and refuses to report on errors (tampered hashes, orphan rows, stale prices on open positions) |
| Backups are verifiable | Online backup plus a SHA-256 manifest |

## Use

```python
from tradelab.db import connect
from tradelab.ingest import store_raw_document
from tradelab.report import build_report

conn = connect("data/research.db")
store_raw_document(conn, source="youtube", source_tier=3, external_id="VIDEO_ID", content="...")
print(build_report(conn, "2026-11"))
```

Run the checks: `pip install pytest && pytest -q`

## Rules for keeping it clean

1. Use only synthetic data in tests. Never commit your real journal, account numbers or credentials; add `data/` and `backups/` to `.gitignore`.
2. Fetch, then validate, then extract. Claude's extracted calls are stored with `extracted_by` and `human_verified = 0` until you check them against the source.
3. Record the price at the time of the video, not when you watched it.
4. Fix mistakes by adding a correcting record and a `post_mortem` note, never by editing history.
5. Run `tradelab.backup.backup()` daily and `verify()` monthly.

## Command center and engine

See `CLAUDE.md` for the architecture, hard rules, commands and the full list of what is and is not built, and `docs/STACK.md` for the stack decision.

## Not yet built or verified (data layer)

- `fetch_youtube_transcript` has not been run against live YouTube; test it on your own machine first.
- No price-feed, EDGAR, FRED or sentiment collectors yet.
- No scheduler. Run ingestion from cron or a systemd timer once collectors exist.
- The Claude extraction step (transcript to structured call) is not written.
