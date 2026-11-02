"""Market regime and global-shock checks, computed from stored data (never asserted).

Regime votes come from two verifiable signals: SPY vs its 200-day average and the
VIX level. Other markets (global indices, rates, FX, commodities) feed the global
shock check and the dashboard; they do not vote on regime yet.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta

from ..db import market_today
from .config import Config

TREND_DAYS = 200


@dataclass(frozen=True)
class Regime:
    label: str                 # 'risk_on', 'choppy', 'risk_off' or 'unknown'
    reasons: tuple[str, ...]
    complete: bool


def _today(today: date | None) -> date:
    return today or market_today()


def _latest_snapshot(conn: sqlite3.Connection, symbol: str, cutoff: str):
    return conn.execute(
        "SELECT value, change_pct, as_of FROM market_snapshots WHERE symbol = ? AND as_of >= ? "
        "ORDER BY as_of DESC LIMIT 1",
        (symbol, cutoff),
    ).fetchone()


def compute_regime(conn: sqlite3.Connection, cfg: Config, today: date | None = None) -> Regime:
    today = _today(today)
    cutoff = (today - timedelta(days=int(cfg.max_price_age_days))).isoformat()
    votes: list[int] = []
    reasons: list[str] = []

    rows = conn.execute(
        "SELECT trade_date, MAX(close) AS close FROM prices WHERE ticker = 'SPY' "
        "GROUP BY trade_date ORDER BY trade_date DESC LIMIT ?",
        (TREND_DAYS,),
    ).fetchall()
    if len(rows) < TREND_DAYS or rows[0]["trade_date"] < cutoff:
        reasons.append("SPY trend unavailable: need 200 recent daily closes")
        trend = None
    else:
        sma = sum(r["close"] for r in rows) / len(rows)
        last = rows[0]["close"]
        trend = 1 if last > sma else -1
        reasons.append(f"SPY {last:.2f} {'above' if trend == 1 else 'below'} 200-day average {sma:.2f}")
        votes.append(trend)

    vix = _latest_snapshot(conn, "VIX", cutoff)
    if vix is None:
        reasons.append("VIX unavailable or stale")
        vix_vote = None
    else:
        level = vix["value"]
        if level <= cfg.vix_risk_on_level:
            vix_vote = 1
        elif level >= cfg.vix_risk_off_level:
            vix_vote = -1
        else:
            vix_vote = 0
        reasons.append(f"VIX {level:.1f} (risk-on at or below {cfg.vix_risk_on_level:g}, risk-off at or above {cfg.vix_risk_off_level:g})")
        votes.append(vix_vote)

    if trend is None or vix_vote is None:
        return Regime("unknown", tuple(reasons), False)

    total = sum(votes)
    label = "risk_on" if total >= 1 else "risk_off" if total <= -1 else "choppy"
    return Regime(label, tuple(reasons), True)


def global_shocks(conn: sqlite3.Connection, cfg: Config, today: date | None = None) -> list[str]:
    """Watched US and global indices that fell by at least global_shock_pct on their latest day."""
    today = _today(today)
    cutoff = (today - timedelta(days=int(cfg.max_price_age_days))).isoformat()
    rows = conn.execute(
        """SELECT m.symbol, m.change_pct, m.as_of FROM market_snapshots m
           JOIN (SELECT symbol, MAX(as_of) AS as_of FROM market_snapshots
                 WHERE grp IN ('us_index', 'global_index') AND as_of >= ? GROUP BY symbol) latest
             ON latest.symbol = m.symbol AND latest.as_of = m.as_of
           WHERE m.grp IN ('us_index', 'global_index') AND m.change_pct IS NOT NULL""",
        (cutoff,),
    ).fetchall()
    limit = -cfg.global_shock_pct / 100
    return [f"{r['symbol']} {r['change_pct']:.1%} on {r['as_of']}" for r in rows if r["change_pct"] <= limit]
