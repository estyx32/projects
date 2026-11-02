"""Pre-trade risk gate. Every check must pass; a missing input blocks the trade.

Modeled on the controls in the FIA automated-trading risk paper: max order size,
max position, price tolerance, daily loss limit, kill switch, stale-data checks,
and "no limit set means no trade".
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import date, timedelta

from ..db import market_day_start_utc, market_today
from .config import Config
from .regime import compute_regime, global_shocks
from .state import current_mode, kill_switch_on


@dataclass
class GateResult:
    blocked: list[str] = field(default_factory=list)
    passed: list[str] = field(default_factory=list)

    @property
    def approved(self) -> bool:
        return not self.blocked


def current_equity(conn: sqlite3.Connection, cfg: Config) -> float:
    row = conn.execute("SELECT equity FROM equity_snapshots ORDER BY ts DESC LIMIT 1").fetchone()
    return float(row["equity"]) if row else cfg.account_equity


def _drawdown_and_daily(conn: sqlite3.Connection, cfg: Config, today: date) -> tuple[float, float]:
    """Returns (drawdown from peak, loss since the day's first snapshot), both as fractions."""
    equity = current_equity(conn, cfg)
    peak = conn.execute("SELECT MAX(equity) FROM equity_snapshots").fetchone()[0] or equity
    day_start = conn.execute(
        "SELECT equity FROM equity_snapshots WHERE ts >= ? ORDER BY ts ASC LIMIT 1",
        (market_day_start_utc(today),),
    ).fetchone()
    start = float(day_start["equity"]) if day_start else equity
    return max(0.0, 1 - equity / max(peak, equity)), max(0.0, 1 - equity / start)


def evaluate(
    conn: sqlite3.Connection,
    cfg: Config,
    p: dict,
    *,
    qty: int,
    notional: float,
    pct_of_account: float,
    today: date | None = None,
    exclude_proposal_id: int | None = None,
) -> GateResult:
    today = today or market_today()
    res = GateResult()

    def check(ok: bool, passed_msg: str, blocked_msg: str) -> None:
        (res.passed if ok else res.blocked).append(passed_msg if ok else blocked_msg)

    ticker = p["ticker"].upper()
    direction = p["direction"]

    check(not kill_switch_on(conn), "kill switch off", "kill switch is ON")
    check(current_mode(conn) == "shadow", "mode is shadow", "only shadow mode is supported")
    check(p["instrument"] == "stock", "instrument supported",
          f"instrument {p['instrument']} not supported yet (stocks only)")
    check(ticker in cfg.allowlist, "ticker on allowlist", f"{ticker} is not on the allowlist")
    check(qty > 0, "size above zero",
          "size is zero: position limits or stop distance leave no whole shares")

    check(notional <= cfg.max_order_notional, "within max order notional",
          f"order notional {notional:,.0f} exceeds max {cfg.max_order_notional:,.0f}")
    pos_limit = cfg.max_long_position_pct if direction == "long" else cfg.max_short_position_pct
    check(pct_of_account <= pos_limit + 1e-9, "within position limit",
          f"position {pct_of_account:.2f}% exceeds {direction} limit {pos_limit:g}%")

    open_rows = conn.execute(
        "SELECT ticker, size_pct_account FROM trades WHERE date_closed IS NULL"
    ).fetchall()
    check(len(open_rows) < cfg.max_open_positions, "open positions below max",
          f"{len(open_rows)} open positions at the max of {cfg.max_open_positions:g}")
    gross = sum(r["size_pct_account"] for r in open_rows) + pct_of_account
    check(gross <= cfg.max_gross_exposure_pct, "within gross exposure",
          f"gross exposure would be {gross:.1f}%, max {cfg.max_gross_exposure_pct:g}%")

    pending = conn.execute(
        "SELECT id FROM proposals WHERE ticker = ? AND status = 'pending' AND id != ?",
        (ticker, exclude_proposal_id or -1),
    ).fetchall()
    held = any(r["ticker"] == ticker for r in open_rows)
    check(not held and not pending, "no existing position or pending proposal",
          f"{ticker} already has an open position or pending proposal")

    drawdown, daily_loss = _drawdown_and_daily(conn, cfg, today)
    check(drawdown * 100 < cfg.max_drawdown_pct, "drawdown within limit",
          f"drawdown {drawdown:.1%} reached the {cfg.max_drawdown_pct:g}% breaker")
    check(daily_loss * 100 < cfg.max_daily_loss_pct, "daily loss within limit",
          f"daily loss {daily_loss:.1%} reached the {cfg.max_daily_loss_pct:g}% limit")

    cutoff = (today - timedelta(days=int(cfg.max_price_age_days))).isoformat()
    last = conn.execute(
        "SELECT close, trade_date FROM prices WHERE ticker = ? ORDER BY trade_date DESC LIMIT 1",
        (ticker,),
    ).fetchone()
    if last is None or last["trade_date"] < cutoff:
        res.blocked.append(f"no fresh price for {ticker} (stale-data check)")
    else:
        dev = abs(p["entry_price"] / last["close"] - 1) * 100
        check(dev <= cfg.price_tolerance_pct, "entry within price tolerance",
              f"entry {p['entry_price']:.2f} is {dev:.1f}% from last close {last['close']:.2f}, "
              f"tolerance {cfg.price_tolerance_pct:g}%")

    if direction == "short":
        si = p.get("short_interest_pct")
        if si is None:
            res.blocked.append("short interest missing for a short")
        else:
            check(si <= cfg.max_short_interest_pct, "short interest below ceiling",
                  f"short interest {si:g}% above ceiling {cfg.max_short_interest_pct:g}%")

    dte = p.get("days_to_earnings")
    if dte is None:
        res.blocked.append("earnings date missing")
    else:
        check(dte > cfg.earnings_blackout_days, "outside earnings blackout",
              f"earnings in {dte} days, inside the {cfg.earnings_blackout_days:g}-day blackout")

    regime = compute_regime(conn, cfg, today)
    if not regime.complete:
        res.blocked.append("regime cannot be verified: " + "; ".join(regime.reasons))
    else:
        check(p["regime"] == regime.label, f"claimed regime matches engine ({regime.label})",
              f"claimed regime {p['regime']} but engine computed {regime.label}")
        if direction == "long" and regime.label == "risk_off" and cfg.block_longs_in_risk_off:
            res.blocked.append("new longs blocked in a risk-off regime")
        if direction == "short" and regime.label == "risk_on" and cfg.block_shorts_in_risk_on:
            res.blocked.append("new shorts blocked in a risk-on regime")

    shocks = global_shocks(conn, cfg, today)
    if direction == "long" and shocks:
        res.blocked.append("global shock, new longs paused: " + ", ".join(shocks))
    else:
        res.passed.append("no global shock against longs")

    return res
