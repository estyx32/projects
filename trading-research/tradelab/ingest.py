"""Ingestion helpers. Raw documents are stored exactly as received, with a hash.

fetch_youtube_transcript() uses the unofficial youtube-transcript-api package.
It has NOT been exercised against live YouTube from this environment; run it
once on your own machine before relying on it.
"""

from __future__ import annotations

import hashlib
import sqlite3

from .db import utc_now


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def store_raw_document(
    conn: sqlite3.Connection,
    *,
    source: str,
    source_tier: int,
    external_id: str,
    content: str,
    url: str | None = None,
    published_at: str | None = None,
) -> int:
    """Insert a raw document once. Re-fetching identical bytes returns the same id."""
    digest = sha256_text(content)
    conn.execute(
        """INSERT OR IGNORE INTO raw_documents
           (source, source_tier, external_id, url, published_at, retrieved_at,
            content, content_sha256)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (source, source_tier, external_id, url, published_at, utc_now(), content, digest),
    )
    row = conn.execute(
        "SELECT id FROM raw_documents WHERE source=? AND external_id=? AND content_sha256=?",
        (source, external_id, digest),
    ).fetchone()
    conn.commit()
    return int(row["id"])


def store_price(
    conn: sqlite3.Connection,
    *,
    ticker: str,
    trade_date: str,
    close: float,
    price_source: str,
    adj_close: float | None = None,
    volume: int | None = None,
) -> None:
    conn.execute(
        """INSERT OR REPLACE INTO prices
           (ticker, trade_date, close, adj_close, volume, price_source, retrieved_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (ticker.upper(), trade_date, close, adj_close, volume, price_source, utc_now()),
    )
    conn.commit()


def store_market_snapshot(
    conn: sqlite3.Connection,
    *,
    symbol: str,
    grp: str,
    as_of: str,
    value: float,
    source: str,
    change_pct: float | None = None,
) -> None:
    """Store one day's reading for a market (index, rate, FX, commodity, VIX...)."""
    conn.execute(
        """INSERT OR REPLACE INTO market_snapshots
           (symbol, grp, as_of, value, change_pct, source, retrieved_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (symbol.upper(), grp, as_of, value, change_pct, source, utc_now()),
    )
    conn.commit()


def store_news_item(
    conn: sqlite3.Connection,
    *,
    raw_document_id: int,
    published_at: str,
    region: str,
    headline: str,
    classified_by: str,
    tickers: str | None = None,
    topic: str | None = None,
    impact: str | None = None,
) -> int:
    """A news item always points at the raw document it came from."""
    cur = conn.execute(
        """INSERT INTO news_items (raw_document_id, published_at, region, headline, tickers, topic,
           impact, classified_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (raw_document_id, published_at, region, headline, tickers, topic, impact, classified_by),
    )
    conn.commit()
    return int(cur.lastrowid)


def fetch_youtube_transcript(video_id: str) -> str:
    """Return the transcript text for a video (youtube-transcript-api 1.x)."""
    from youtube_transcript_api import YouTubeTranscriptApi

    snippets = YouTubeTranscriptApi().fetch(video_id)
    return " ".join(s.text for s in snippets)
