"""Integrity tests. All data here is synthetic."""

import sqlite3
from datetime import date

import pytest

from tradelab import backup as bk
from tradelab import validate
from tradelab.db import connect
from tradelab.ingest import store_price, store_raw_document
from tradelab.report import ReportBlocked, build_report, export_csv


@pytest.fixture()
def conn():
    c = connect(":memory:")
    yield c
    c.close()


def add_trade(conn, **over):
    row = {
        "ticker": "AAA",
        "direction": "long",
        "instrument": "stock",
        "date_opened": "2026-01-05",
        "source_tier": 1,
        "idea_source": "10-K footnote",
        "regime_at_entry": "risk_on",
        "variant_view": "Consensus misses margin recovery",
        "catalyst": "Q1 earnings",
        "invalidation": "Close below 90",
        "entry_price": 100.0,
        "size_pct_account": 5.0,
        "stop_level": 90.0,
    }
    row.update(over)
    cols = ", ".join(row)
    marks = ", ".join("?" for _ in row)
    cur = conn.execute(f"INSERT INTO trades ({cols}) VALUES ({marks})", tuple(row.values()))
    conn.commit()
    return cur.lastrowid


def close_trade(conn, trade_id, exit_price, closed="2026-02-05", spy=0.01):
    conn.execute(
        "UPDATE trades SET date_closed=?, exit_price=?, exit_reason='target', spy_return=? WHERE id=?",
        (closed, exit_price, spy, trade_id),
    )
    conn.commit()


# ------------------------------------------------------------------ raw layer
def test_raw_document_stored_once_and_immutable(conn):
    a = store_raw_document(conn, source="youtube", source_tier=3, external_id="vid1", content="hello")
    b = store_raw_document(conn, source="youtube", source_tier=3, external_id="vid1", content="hello")
    assert a == b
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE raw_documents SET content='tampered' WHERE id=?", (a,))
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("DELETE FROM raw_documents WHERE id=?", (a,))


def test_changed_source_content_is_a_new_version(conn):
    a = store_raw_document(conn, source="edgar", source_tier=1, external_id="acc1", content="v1")
    b = store_raw_document(conn, source="edgar", source_tier=1, external_id="acc1", content="v2")
    assert a != b


def test_hash_check_catches_tampering(conn):
    doc = store_raw_document(conn, source="youtube", source_tier=3, external_id="vid2", content="original")
    conn.execute("DROP TRIGGER raw_documents_no_update")  # simulate someone editing the file directly
    conn.execute("UPDATE raw_documents SET content='edited' WHERE id=?", (doc,))
    findings = validate.check_raw_hashes(conn)
    assert any(f.severity == "error" for f in findings)


# --------------------------------------------------------------------- trades
def test_stop_must_be_on_losing_side(conn):
    with pytest.raises(sqlite3.IntegrityError):
        add_trade(conn, direction="long", stop_level=110.0)
    with pytest.raises(sqlite3.IntegrityError):
        add_trade(conn, direction="short", stop_level=90.0)
    add_trade(conn, direction="short", stop_level=110.0)  # valid


def test_entry_fields_locked_after_insert(conn):
    t = add_trade(conn)
    for col, val in [("variant_view", "rewritten later"), ("stop_level", 50.0), ("entry_price", 101.0)]:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(f"UPDATE trades SET {col}=? WHERE id=?", (val, t))


def test_close_once_and_review_fields_stay_editable(conn):
    t = add_trade(conn)
    close_trade(conn, t, 110.0)
    with pytest.raises(sqlite3.IntegrityError):
        close_trade(conn, t, 120.0)
    conn.execute("UPDATE trades SET post_mortem='right for the right reasons' WHERE id=?", (t,))


def test_trades_cannot_be_deleted(conn):
    t = add_trade(conn)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("DELETE FROM trades WHERE id=?", (t,))


def test_close_requires_exit_price_and_reason_together(conn):
    t = add_trade(conn)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE trades SET date_closed='2026-02-01' WHERE id=?", (t,))


def test_audit_log_records_changes_and_is_append_only(conn):
    t = add_trade(conn)
    close_trade(conn, t, 110.0)
    actions = [r["action"] for r in conn.execute("SELECT action FROM audit_log ORDER BY id")]
    assert actions == ["insert", "update"]
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("DELETE FROM audit_log")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE audit_log SET detail='x'")


# --------------------------------------------------------------- validation
def test_price_jump_flagged(conn):
    store_price(conn, ticker="AAA", trade_date="2026-03-02", close=100.0, price_source="synthetic")
    store_price(conn, ticker="AAA", trade_date="2026-03-03", close=40.0, price_source="synthetic")
    assert any(f.check == "price_jump" for f in validate.check_price_jumps(conn))


def test_stale_price_on_open_position_blocks_report(conn):
    add_trade(conn)
    store_price(conn, ticker="AAA", trade_date="2026-01-06", close=101.0, price_source="synthetic")
    findings = validate.check_stale_prices(conn, today=date(2026, 3, 1))
    assert validate.has_errors(findings)
    with pytest.raises(ReportBlocked):
        build_report(conn, "2026-02", today=date(2026, 3, 1))


def test_duplicate_calls_warned(conn):
    doc = store_raw_document(conn, source="youtube", source_tier=3, external_id="v3", content="x")
    for _ in range(2):
        conn.execute(
            """INSERT INTO calls (raw_document_id, speaker, ticker, direction, called_at, thesis,
               extracted_by, created_at) VALUES (?, 'Speaker A', 'AAA', 'long', '2026-01-02',
               'thesis', 'model-x/prompt-1', '2026-01-02T00:00:00Z')""",
            (doc,),
        )
    assert any(f.check == "duplicate_call" for f in validate.check_duplicate_calls(conn))


def test_orphan_rows_rejected_by_foreign_keys(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            """INSERT INTO calls (raw_document_id, speaker, ticker, direction, called_at, thesis,
               extracted_by, created_at) VALUES (999, 'S', 'AAA', 'long', '2026-01-02', 't', 'm', 'now')"""
        )


# ------------------------------------------------------------------- reports
def test_report_and_csv_export(conn, tmp_path):
    t1 = add_trade(conn, ticker="AAA")
    t2 = add_trade(conn, ticker="BBB", direction="short", entry_price=50.0, stop_level=55.0)
    close_trade(conn, t1, 110.0, spy=0.02)   # long +10%
    close_trade(conn, t2, 45.0, spy=0.02)    # short +10%

    doc = store_raw_document(conn, source="youtube", source_tier=3, external_id="v4", content="x")
    conn.execute(
        """INSERT INTO calls (raw_document_id, speaker, ticker, direction, called_at, thesis,
           extracted_by, created_at, price_at_call, human_verified)
           VALUES (?, 'Speaker A', 'AAA', 'long', '2026-01-02', 't', 'm', 'now', 100.0, 1)""",
        (doc,),
    )
    conn.execute("INSERT INTO call_outcomes VALUES (1, 30, 0.08, 0.02, '2026-02-01')")
    conn.commit()

    md = build_report(conn, "2026-02", today=date(2026, 2, 10))
    assert "| long | 1 | 100.0% | 10.0% | 8.0% |" in md
    assert "| short | 1 | 100.0% | 10.0% | 8.0% |" in md
    assert "Speaker A" in md

    out = tmp_path / "trades.csv"
    export_csv(conn, "v_closed_trades", out)
    assert out.read_text().splitlines()[0].startswith("id,ticker")
    with pytest.raises(ValueError):
        export_csv(conn, "sqlite_master", tmp_path / "x.csv")


# -------------------------------------------------------------------- backup
def test_backup_and_verify(tmp_path):
    db = tmp_path / "r.db"
    c = connect(db)
    store_raw_document(c, source="youtube", source_tier=3, external_id="v5", content="x")
    c.close()
    dest = bk.backup(db, tmp_path / "backups")
    assert bk.verify(dest, tmp_path / "backups" / "MANIFEST.txt")
    dest.write_bytes(dest.read_bytes() + b"corrupt")
    assert not bk.verify(dest, tmp_path / "backups" / "MANIFEST.txt")
