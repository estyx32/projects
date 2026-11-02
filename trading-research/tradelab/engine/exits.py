"""Exit rules as a pure function: stop, scale-out targets, trailing stop, time stop.

Stops only ever tighten. There is no averaging down and no widening.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Position:
    direction: str            # 'long' or 'short'
    entry: float
    initial_stop: float
    stop: float               # current stop (starts equal to initial_stop)
    qty_initial: int
    qty_remaining: int
    days_held: int
    atr: float
    extreme: float            # best price since entry (highest for long, lowest for short)
    targets_taken: set[float] = field(default_factory=set)  # R multiples already sold


@dataclass(frozen=True)
class ExitAction:
    kind: str                 # 'close_all' or 'scale_out'
    qty: int
    reason: str


@dataclass(frozen=True)
class ExitDecision:
    actions: tuple[ExitAction, ...]
    new_stop: float
    new_extreme: float


def r_multiple(pos: Position, price: float) -> float:
    risk = abs(pos.entry - pos.initial_stop)
    move = price - pos.entry if pos.direction == "long" else pos.entry - price
    return move / risk


def evaluate_exit(
    pos: Position,
    price: float,
    *,
    targets: tuple[tuple[float, float], ...],
    trail_atr_multiple: float,
    time_stop_days: int,
) -> ExitDecision:
    """Decide what to do at `price`. Does not mutate `pos`."""
    long = pos.direction == "long"
    extreme = max(pos.extreme, price) if long else min(pos.extreme, price)

    # 1. Stop hit: close everything. Checked first so nothing overrides it.
    stop_hit = price <= pos.stop if long else price >= pos.stop
    if stop_hit:
        return ExitDecision(
            (ExitAction("close_all", pos.qty_remaining, "stop hit"),), pos.stop, extreme
        )

    # 2. Time stop.
    if pos.days_held >= time_stop_days:
        return ExitDecision(
            (ExitAction("close_all", pos.qty_remaining, "time stop"),), pos.stop, extreme
        )

    # 3. Scale-out targets, each taken once.
    actions: list[ExitAction] = []
    remaining = pos.qty_remaining
    taken = set(pos.targets_taken)
    r_now = r_multiple(pos, price)
    for r_target, fraction in sorted(targets):
        if r_target in taken or r_now < r_target or remaining <= 0:
            continue
        qty = min(remaining, max(1, int(pos.qty_initial * fraction)))
        actions.append(ExitAction("scale_out", qty, f"target {r_target:g}R"))
        remaining -= qty
        taken.add(r_target)

    # 4. Tighten the stop: breakeven after the first target, then trail by ATR.
    new_stop = pos.stop
    if taken:
        new_stop = max(new_stop, pos.entry) if long else min(new_stop, pos.entry)
        trail = extreme - trail_atr_multiple * pos.atr if long else extreme + trail_atr_multiple * pos.atr
        new_stop = max(new_stop, trail) if long else min(new_stop, trail)
        # never move a stop past the current price
        new_stop = min(new_stop, price) if long else max(new_stop, price)

    return ExitDecision(tuple(actions), new_stop, extreme)
