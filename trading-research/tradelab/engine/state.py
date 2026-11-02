"""System state (kill switch, mode, heartbeat) and the append-only activity feed."""

from __future__ import annotations

import sqlite3

from ..db import utc_now

SUPPORTED_MODES = ("shadow",)  # no broker adapter exists yet, so nothing can be sent


def get_state(conn: sqlite3.Connection, key: str, default: str | None = None) -> str | None:
    row = conn.execute("SELECT value FROM system_state WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def set_state(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        """INSERT INTO system_state (key, value, updated_at) VALUES (?, ?, ?)
           ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at""",
        (key, value, utc_now()),
    )
    conn.commit()


def log_event(
    conn: sqlite3.Connection,
    actor: str,
    kind: str,
    message: str,
    proposal_id: int | None = None,
) -> None:
    conn.execute(
        "INSERT INTO events (ts, actor, kind, message, proposal_id) VALUES (?, ?, ?, ?, ?)",
        (utc_now(), actor, kind, message, proposal_id),
    )
    conn.commit()


def kill_switch_on(conn: sqlite3.Connection) -> bool:
    return get_state(conn, "kill_switch", "off") == "on"


def set_kill_switch(conn: sqlite3.Connection, on: bool, user: str) -> None:
    set_state(conn, "kill_switch", "on" if on else "off")
    log_event(conn, "user", "kill_switch", f"{user} turned the kill switch {'ON' if on else 'off'}")


def heartbeat(conn: sqlite3.Connection) -> None:
    set_state(conn, "heartbeat", utc_now())


def current_mode(conn: sqlite3.Connection) -> str:
    return get_state(conn, "mode", "shadow") or "shadow"
