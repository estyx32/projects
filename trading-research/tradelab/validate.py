"""Data-quality checks. Run before every report; a failing check blocks the report."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta

from .db import market_today
from .ingest import sha256_text

MAX_DAILY_MOVE = 0.40      # flag a >40% one-day close-to-close move as suspect
MAX_PRICE_AGE_DAYS = 5     # flag tickers whose latest price is older than this


@dataclass
class Finding:
    check: str
    severity: str  # 'error' blocks reporting, 'warning' does not
    detail: str


def check_raw_hashes(conn: sqlite3.Connection) -> list[Finding]:
    out = []
    for r in conn.execute("SELECT id, content, content_sha256 FROM raw_documents"):
        if sha256_text(r["content"]) != r["content_sha256"]:
            out.append(Finding("raw_hash", "error", f"raw_documents id={r['id']} hash mismatch"))
    return out


def check_orphans(conn: sqlite3.Connection) -> list[Finding]:
    out = []
    fk = conn.execute("PRAGMA foreign_key_check").fetchall()
    for r in fk:
        out.append(Finding("foreign_key", "error", f"{r[0]} row {r[1]} -> missing {r[2]}"))
    return out


def check_duplicate_calls(conn: sqlite3.Connection) -> list[Finding]:
    rows = conn.execute(
        """SELECT speaker, ticker, direction, called_at, COUNT(*) n FROM calls
           GROUP BY speaker, ticker, direction, called_at HAVING n > 1"""
    )
    return [
        Finding("duplicate_call", "warning",
                f"{r['speaker']} {r['ticker']} {r['direction']} {r['called_at']} x{r['n']}")
        for r in rows
    ]


def check_unverified_calls(conn: sqlite3.Connection) -> list[Finding]:
    n = conn.execute("SELECT COUNT(*) FROM calls WHERE human_verified = 0").fetchone()[0]
    return [Finding("unverified_calls", "warning", f"{n} calls not yet human-verified")] if n else []


def check_price_jumps(conn: sqlite3.Connection) -> list[Finding]:
    out = []
    rows = conn.execute(
        "SELECT ticker, trade_date, close, price_source FROM prices ORDER BY ticker, price_source, trade_date"
    ).fetchall()
    prev = None
    for r in rows:
        key = (r["ticker"], r["price_source"])
        if prev and prev[0] == key:
            move = abs(r["close"] / prev[1] - 1)
            if move > MAX_DAILY_MOVE:
                out.append(Finding("price_jump", "warning",
                                   f"{r['ticker']} {r['trade_date']} moved {move:.0%}; check for splits or bad data"))
        prev = (key, r["close"])
    return out


def check_stale_prices(conn: sqlite3.Connection, today: date | None = None) -> list[Finding]:
    today = today or market_today()
    cutoff = (today - timedelta(days=MAX_PRICE_AGE_DAYS)).isoformat()
    out = []
    for r in conn.execute(
        """SELECT DISTINCT t.ticker FROM trades t WHERE t.date_closed IS NULL"""
    ):
        latest = conn.execute(
            "SELECT MAX(trade_date) FROM prices WHERE ticker = ?", (r["ticker"],)
        ).fetchone()[0]
        if latest is None or latest < cutoff:
            out.append(Finding("stale_price", "error",
                               f"open position {r['ticker']} latest price {latest or 'none'}"))
    return out


def check_call_price_coverage(conn: sqlite3.Connection) -> list[Finding]:
    n = conn.execute(
        "SELECT COUNT(*) FROM calls WHERE price_at_call IS NULL AND direction != 'neutral'"
    ).fetchone()[0]
    return [Finding("call_price_missing", "warning", f"{n} calls have no price at call time")] if n else []


def run_all(conn: sqlite3.Connection, today: date | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for fn in (check_raw_hashes, check_orphans, check_duplicate_calls, check_unverified_calls,
               check_price_jumps, check_call_price_coverage):
        findings += fn(conn)
    findings += check_stale_prices(conn, today)
    return findings


def has_errors(findings: list[Finding]) -> bool:
    return any(f.severity == "error" for f in findings)
