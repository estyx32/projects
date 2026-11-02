"""Shared fixtures. All data is synthetic."""

from __future__ import annotations

import math
from datetime import date, timedelta

import pytest

from tradelab.db import connect, market_today
from tradelab.engine.config import parse_config
from tradelab.engine.state import heartbeat, set_state
from tradelab.ingest import store_market_snapshot, store_price

BASE_CONFIG = {
    "config_reviewed": True,
    "account_equity": 10000,
    "risk_per_trade_pct": 0.5,
    "max_long_position_pct": 5,
    "max_short_position_pct": 2.5,
    "max_gross_exposure_pct": 50,
    "max_order_notional": 1000,
    "max_open_positions": 6,
    "max_daily_loss_pct": 2,
    "max_drawdown_pct": 8,
    "price_tolerance_pct": 3,
    "max_price_age_days": 4,
    "max_short_interest_pct": 15,
    "earnings_blackout_days": 3,
    "atr_stop_multiple": 2,
    "trail_atr_multiple": 2,
    "time_stop_days": 60,
    "targets": [[1.0, 0.33], [2.0, 0.33]],
    "vix_risk_on_level": 18,
    "vix_risk_off_level": 25,
    "global_shock_pct": 3,
    "allowlist": ["AAPL", "MSFT", "XOM"],
}


@pytest.fixture()
def cfg():
    return parse_config(dict(BASE_CONFIG))


def make_cfg(**over):
    return parse_config({**BASE_CONFIG, **over})


def seed_world(conn, *, trend: float = 0.0006, vix: float = 15.0, today: date | None = None):
    """Daily closes for SPY and the allowlist, a VIX reading, a heartbeat."""
    today = today or market_today()
    for ticker, base in {"SPY": 480.0, "AAPL": 200.0, "MSFT": 400.0, "XOM": 105.0}.items():
        for i in range(330):
            d = today - timedelta(days=329 - i)
            if d.weekday() >= 5:
                continue
            close = base * (1 + trend * i) * (1 + 0.01 * math.sin(i / 9))
            store_price(conn, ticker=ticker, trade_date=d.isoformat(), close=round(close, 2),
                        price_source="synthetic")
    store_market_snapshot(conn, symbol="VIX", grp="volatility", as_of=today.isoformat(),
                          value=vix, change_pct=0.0, source="synthetic")
    set_state(conn, "mode", "shadow")
    heartbeat(conn)
    return today


def last_close(conn, ticker):
    return conn.execute("SELECT close FROM prices WHERE ticker=? ORDER BY trade_date DESC LIMIT 1",
                        (ticker,)).fetchone()["close"]


def idea(conn, ticker="AAPL", direction="long", **over):
    p = {
        "ticker": ticker, "direction": direction, "instrument": "stock",
        "entry_price": last_close(conn, ticker), "atr": 0.5, "catalyst": "Product cycle",
        "regime": "risk_on", "source_tier": 1, "idea_source": "10-K footnote",
        "days_to_earnings": 20, "variant_view": "Consensus misses the cost step-down.",
        "invalidation": "Close below stop.",
    }
    if direction == "short":
        p["short_interest_pct"] = 4.0
        p["regime"] = "risk_off"
    p.update(over)
    return p


@pytest.fixture()
def conn():
    c = connect(":memory:")
    yield c
    c.close()


@pytest.fixture()
def world(conn):
    seed_world(conn)
    return conn
