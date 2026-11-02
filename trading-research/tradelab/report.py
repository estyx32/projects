"""Monthly report: validation first, then closed-trade and source statistics."""

from __future__ import annotations

import csv
import sqlite3
from datetime import date
from pathlib import Path

from .validate import has_errors, run_all


class ReportBlocked(Exception):
    """Raised when data-quality errors make a report untrustworthy."""


def _pct(x: float | None) -> str:
    return "n/a" if x is None else f"{x:.1%}"


def build_report(conn: sqlite3.Connection, month: str, today: date | None = None) -> str:
    """month is 'YYYY-MM'. Returns markdown. Raises ReportBlocked on validation errors."""
    findings = run_all(conn, today)
    if has_errors(findings):
        details = "; ".join(f.detail for f in findings if f.severity == "error")
        raise ReportBlocked(details)

    rows = conn.execute(
        "SELECT * FROM v_closed_trades WHERE substr(date_closed, 1, 7) = ?", (month,)
    ).fetchall()

    lines = [f"# Trading report {month}", ""]
    lines.append("## Data quality")
    warnings = [f for f in findings if f.severity == "warning"]
    lines += [f"- warning ({f.check}): {f.detail}" for f in warnings] or ["- no findings"]
    lines.append("")

    lines.append("## Closed trades")
    if not rows:
        lines.append("No closed trades this month.")
    else:
        lines.append("| Direction | Trades | Win rate | Avg return | Avg vs SPY |")
        lines.append("| --- | --- | --- | --- | --- |")
        for direction in ("long", "short"):
            sub = [r for r in rows if r["direction"] == direction]
            if not sub:
                continue
            wins = sum(1 for r in sub if r["trade_return"] > 0)
            avg = sum(r["trade_return"] for r in sub) / len(sub)
            spy = [r["trade_return"] - r["spy_return"] for r in sub if r["spy_return"] is not None]
            avg_rel = sum(spy) / len(spy) if spy else None
            lines.append(f"| {direction} | {len(sub)} | {_pct(wins / len(sub))} | {_pct(avg)} | {_pct(avg_rel)} |")
    lines.append("")

    lines.append("## Source hit rate (calls that beat SPY)")
    hits = conn.execute("SELECT * FROM v_source_hit_rate ORDER BY speaker, horizon_days").fetchall()
    if hits:
        lines.append("| Speaker | Horizon (days) | Graded calls | Beat SPY |")
        lines.append("| --- | --- | --- | --- |")
        for h in hits:
            lines.append(f"| {h['speaker']} | {h['horizon_days']} | {h['graded_calls']} | {_pct(h['beat_spy_rate'])} |")
    else:
        lines.append("No graded calls yet.")
    lines.append("")
    lines.append("Small samples mislead: treat any rate under about 30 graded calls as noise.")
    return "\n".join(lines) + "\n"


def export_csv(conn: sqlite3.Connection, table_or_view: str, path: str | Path) -> None:
    allowed = {"trades", "calls", "call_outcomes", "prices", "v_closed_trades", "v_source_hit_rate", "audit_log"}
    if table_or_view not in allowed:
        raise ValueError(f"cannot export {table_or_view}")
    cur = conn.execute(f"SELECT * FROM {table_or_view}")
    with open(path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([c[0] for c in cur.description])
        writer.writerows(cur.fetchall())
