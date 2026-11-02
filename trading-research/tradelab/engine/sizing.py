"""Position sizing: fixed-fractional risk against a stop distance, then capped."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class SizeResult:
    qty: int
    risk_dollars: float
    notional: float
    pct_of_account: float
    capped_by: str | None  # None, 'position_limit' or 'order_notional'


def stop_from_atr(direction: str, entry: float, atr: float, multiple: float) -> float:
    """Place a stop `multiple` x ATR from entry, on the losing side."""
    if direction == "long":
        return entry - multiple * atr
    if direction == "short":
        return entry + multiple * atr
    raise ValueError(f"bad direction: {direction}")


def position_size(
    *,
    equity: float,
    risk_pct: float,
    direction: str,
    entry: float,
    stop: float,
    max_position_pct: float,
    max_order_notional: float,
) -> SizeResult:
    """Shares such that hitting the stop loses about risk_pct of equity, never more.

    Rounds down. Returns qty 0 if even one share would exceed the risk budget.
    """
    if min(equity, risk_pct, entry, stop) <= 0:
        raise ValueError("equity, risk_pct, entry and stop must be positive")
    if direction == "long" and stop >= entry:
        raise ValueError("long stop must be below entry")
    if direction == "short" and stop <= entry:
        raise ValueError("short stop must be above entry")

    risk_budget = equity * risk_pct / 100
    per_share_risk = abs(entry - stop)
    qty = math.floor(risk_budget / per_share_risk)
    capped_by = None

    max_by_position = math.floor(equity * max_position_pct / 100 / entry)
    if qty > max_by_position:
        qty, capped_by = max_by_position, "position_limit"

    max_by_notional = math.floor(max_order_notional / entry)
    if qty > max_by_notional:
        qty, capped_by = max_by_notional, "order_notional"

    qty = max(qty, 0)
    return SizeResult(
        qty=qty,
        risk_dollars=round(qty * per_share_risk, 2),
        notional=round(qty * entry, 2),
        pct_of_account=round(qty * entry / equity * 100, 4),
        capped_by=capped_by,
    )
