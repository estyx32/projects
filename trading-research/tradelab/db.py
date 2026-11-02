"""Database connection and schema setup."""

from __future__ import annotations

import sqlite3
from datetime import UTC, date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SCHEMA_PATHS = (
    Path(__file__).resolve().parent.parent / "schema.sql",
    Path(__file__).resolve().parent.parent / "schema_engine.sql",
)


MARKET_TZ = ZoneInfo("America/New_York")


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def market_today() -> date:
    """The current trading day. US markets follow New York time, not UTC."""
    return datetime.now(MARKET_TZ).date()


def market_day_start_utc(day: date) -> str:
    """UTC timestamp of midnight New York time on `day`, for comparing with stored UTC stamps."""
    start = datetime(day.year, day.month, day.day, tzinfo=MARKET_TZ)
    return start.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def connect(path: str | Path = "data/research.db") -> sqlite3.Connection:
    """Open the database with foreign keys on and the schema applied."""
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 5000")
    if str(path) != ":memory:":
        conn.execute("PRAGMA journal_mode = WAL")  # web reads while the worker writes
    conn.execute("PRAGMA foreign_keys = ON")
    for schema in SCHEMA_PATHS:
        conn.executescript(schema.read_text())
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
