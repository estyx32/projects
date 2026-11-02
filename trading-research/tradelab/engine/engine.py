"""Engine entry points: submit a proposal, approve or reject it, shadow orders."""

from __future__ import annotations

import json
import sqlite3
from datetime import date

from ..db import utc_now
from .config import Config
from .risk_gate import GateResult, current_equity, evaluate
from .sizing import position_size, stop_from_atr
from .state import log_event

REQUIRED_FIELDS = (
    "ticker", "direction", "instrument", "entry_price", "variant_view", "catalyst",
    "invalidation", "source_tier", "idea_source", "regime",
)


class ProposalError(Exception):
    pass


def _gate_json(res: GateResult) -> str:
    return json.dumps({"blocked": res.blocked, "passed": res.passed})


def submit_proposal(
    conn: sqlite3.Connection, cfg: Config, data: dict, *, proposed_by: str = "claude",
    today: date | None = None,
) -> int:
    """Validate, size and gate a trade idea. Returns the proposal id.

    The idea is stored either as 'pending' (waiting for you) or 'blocked' (with reasons).
    Nothing is ever sent to a broker from here.
    """
    missing = [f for f in REQUIRED_FIELDS if data.get(f) in (None, "")]
    if missing:
        raise ProposalError(f"missing fields: {', '.join(missing)}")

    p = dict(data)
    p["ticker"] = str(p["ticker"]).upper()
    entry = float(p["entry_price"])
    if p.get("stop_price") is None:
        if p.get("atr") is None:
            raise ProposalError("provide stop_price or atr")
        stop = stop_from_atr(p["direction"], entry, float(p["atr"]), cfg.atr_stop_multiple)
    else:
        stop = float(p["stop_price"])

    pos_limit = cfg.max_long_position_pct if p["direction"] == "long" else cfg.max_short_position_pct
    try:
        size = position_size(
            equity=current_equity(conn, cfg), risk_pct=cfg.risk_per_trade_pct,
            direction=p["direction"], entry=entry, stop=stop,
            max_position_pct=pos_limit, max_order_notional=cfg.max_order_notional,
        )
    except ValueError as exc:
        raise ProposalError(str(exc)) from exc

    res = evaluate(conn, cfg, p, qty=size.qty, notional=size.notional,
                   pct_of_account=size.pct_of_account, today=today)
    status = "pending" if res.approved else "blocked"
    cur = conn.execute(
        """INSERT INTO proposals (created_at, proposed_by, ticker, direction, instrument, entry_price,
           stop_price, atr, scorecard_score, variant_view, catalyst, invalidation, source_tier,
           idea_source, regime, short_interest_pct, days_to_earnings, status, qty, risk_dollars,
           size_pct_account, gate_reasons)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (utc_now(), proposed_by, p["ticker"], p["direction"], p["instrument"], entry, stop,
         p.get("atr"), p.get("scorecard_score"), p["variant_view"], p["catalyst"], p["invalidation"],
         int(p["source_tier"]), p["idea_source"], p["regime"], p.get("short_interest_pct"),
         p.get("days_to_earnings"), status, size.qty, size.risk_dollars, size.pct_of_account,
         _gate_json(res)),
    )
    conn.commit()
    pid = int(cur.lastrowid)
    actor = "claude" if proposed_by.startswith("claude") else "user"
    log_event(conn, actor, "proposal",
              f"proposed {p['direction']} {p['ticker']} qty {size.qty} at {entry:.2f}, stop {stop:.2f}", pid)
    if res.approved:
        log_event(conn, "risk_gate", "passed", f"{p['ticker']}: all checks passed, awaiting your approval", pid)
    else:
        log_event(conn, "risk_gate", "blocked", f"{p['ticker']}: " + "; ".join(res.blocked), pid)
    return pid


def _row_to_p(row: sqlite3.Row) -> dict:
    return dict(row)


def approve(conn: sqlite3.Connection, cfg: Config, proposal_id: int, user: str,
            today: date | None = None) -> bool:
    """Re-run the gate on today's data, then record shadow orders. Returns True if approved."""
    row = conn.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,)).fetchone()
    if row is None or row["status"] != "pending":
        raise ProposalError("proposal is not pending")

    p = _row_to_p(row)
    res = evaluate(conn, cfg, p, qty=p["qty"], notional=p["qty"] * p["entry_price"],
                   pct_of_account=p["size_pct_account"], today=today, exclude_proposal_id=proposal_id)
    if not res.approved:
        conn.execute(
            "UPDATE proposals SET status='blocked', gate_reasons=?, decided_at=?, decided_by=? WHERE id=?",
            (_gate_json(res), utc_now(), "risk_gate", proposal_id),
        )
        conn.commit()
        log_event(conn, "risk_gate", "blocked",
                  f"{p['ticker']}: blocked at approval time: " + "; ".join(res.blocked), proposal_id)
        return False

    conn.execute(
        "UPDATE proposals SET status='approved', gate_reasons=?, decided_at=?, decided_by=? WHERE id=?",
        (_gate_json(res), utc_now(), user, proposal_id),
    )
    _record_shadow_orders(conn, cfg, p, proposal_id)
    conn.commit()
    log_event(conn, "user", "approved", f"{user} approved {p['ticker']} (shadow orders recorded, none sent)",
              proposal_id)
    return True


def reject(conn: sqlite3.Connection, proposal_id: int, user: str) -> None:
    row = conn.execute("SELECT ticker, status FROM proposals WHERE id = ?", (proposal_id,)).fetchone()
    if row is None or row["status"] != "pending":
        raise ProposalError("proposal is not pending")
    conn.execute(
        "UPDATE proposals SET status='rejected', decided_at=?, decided_by=? WHERE id=?",
        (utc_now(), user, proposal_id),
    )
    conn.commit()
    log_event(conn, "user", "rejected", f"{user} rejected {row['ticker']}", proposal_id)


def _record_shadow_orders(conn: sqlite3.Connection, cfg: Config, p: dict, proposal_id: int) -> None:
    long = p["direction"] == "long"
    entry, stop, qty = p["entry_price"], p["stop_price"], p["qty"]
    risk = abs(entry - stop)
    now = utc_now()

    def add(kind: str, side: str, q: int, price: float) -> None:
        conn.execute(
            """INSERT INTO orders (proposal_id, created_at, ticker, side, kind, qty, price, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'shadow')""",
            (proposal_id, now, p["ticker"], side, kind, q, round(price, 4)),
        )

    add("entry_limit", "buy" if long else "sell_short", qty, entry)
    add("protective_stop", "sell" if long else "buy_to_cover", qty, stop)
    left = qty
    for r_mult, fraction in sorted(cfg.targets):
        q = min(left, max(1, int(qty * fraction)))
        if q <= 0:
            break
        add("target", "sell" if long else "buy_to_cover", q,
            entry + r_mult * risk if long else entry - r_mult * risk)
        left -= q
