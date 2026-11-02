"""Display formatting. Missing values always show as an em dash, never as 0."""

from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

DASH = "—"
LOCAL_TZ = ZoneInfo("America/New_York")


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        if len(value) == 10:  # YYYY-MM-DD
            return datetime.fromisoformat(value).replace(tzinfo=UTC)
        return datetime.fromisoformat(value)  # 3.11+ accepts a trailing Z
    except ValueError:
        return None


def money(x: float | None) -> str:
    return DASH if x is None else f"${x:,.2f}"


def num(x: float | None, digits: int = 2) -> str:
    return DASH if x is None else f"{x:,.{digits}f}"


def pct_frac(x: float | None, digits: int = 1, signed: bool = False) -> str:
    """For fractions: 0.05 -> 5.0%."""
    if x is None:
        return DASH
    return f"{x:+.{digits}%}" if signed else f"{x:.{digits}%}"


def pct_pts(x: float | None, digits: int = 2) -> str:
    """For values already in percent: 5.0 -> 5.00%."""
    return DASH if x is None else f"{x:.{digits}f}%"


def local_time(value: str | None) -> str:
    dt = parse_ts(value)
    if dt is None:
        return DASH
    if value and len(value) == 10:
        return dt.strftime("%b %-d")
    local = dt.astimezone(LOCAL_TZ)
    return local.strftime("%b %-d, %-I:%M %p ET")


def age(value: str | None, now: datetime | None = None) -> str:
    dt = parse_ts(value)
    if dt is None:
        return DASH
    now = now or datetime.now(UTC)
    secs = max(0, int((now - dt).total_seconds()))
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def change_class(x: float | None) -> str:
    if x is None:
        return "flat"
    return "up" if x > 0 else "down" if x < 0 else "flat"


FILTERS = {
    "money": money,
    "num": num,
    "pct_frac": pct_frac,
    "pct_pts": pct_pts,
    "local_time": local_time,
    "age": age,
    "change_class": change_class,
}
