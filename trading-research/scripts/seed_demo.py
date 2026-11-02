"""Create a SYNTHETIC demo database and config so the command center can be viewed.

Every number here is invented. Do not use data/demo.db or config/demo.toml for real decisions.
"""

from __future__ import annotations

import math
import sys
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tradelab.db import connect, market_today, utc_now
from tradelab.engine.config import load_config
from tradelab.engine.engine import submit_proposal
from tradelab.engine.state import heartbeat, log_event, set_state
from tradelab.ingest import (
    store_market_snapshot,
    store_news_item,
    store_price,
    store_raw_document,
)

DEMO_CONFIG = (ROOT / "config" / "risk.example.toml").read_text().replace(
    "config_reviewed = false", "config_reviewed = true  # DEMO ONLY"
)


def main(db_path: str = "data/demo.db", cfg_path: str = "config/demo.toml") -> None:
    Path(cfg_path).parent.mkdir(parents=True, exist_ok=True)
    Path(cfg_path).write_text(DEMO_CONFIG)
    for suffix in ("", "-wal", "-shm"):  # stale WAL files must never be replayed into a fresh db
        Path(db_path + suffix).unlink(missing_ok=True)
    cfg = load_config(cfg_path)
    conn = connect(db_path)
    today = market_today()

    # ~330 calendar days gives ~235 weekdays, enough for the engine's 200-day trend check
    bases = {"SPY": 480.0, "AAPL": 180.0, "MSFT": 400.0, "XOM": 105.0}
    for ticker, base in bases.items():
        for i in range(330):
            d = today - timedelta(days=329 - i)
            if d.weekday() >= 5:
                continue
            close = base * (1 + 0.0006 * i) * (1 + 0.02 * math.sin(i / 9))
            store_price(conn, ticker=ticker, trade_date=d.isoformat(), close=round(close, 2),
                        price_source="synthetic", volume=1_000_000)

    snaps = [
        ("SPY", "us_index", 531.2, 0.004), ("QQQ", "us_index", 462.9, 0.006),
        ("NIKKEI", "global_index", 38120.0, -0.011), ("DAX", "global_index", 18330.0, 0.002),
        ("FTSE", "global_index", 8120.0, -0.003), ("VIX", "volatility", 15.4, -0.03),
        ("US10Y", "rates", 4.31, 0.0), ("DXY", "fx", 104.2, 0.001),
        ("WTI", "commodity", 78.4, 0.012), ("GOLD", "commodity", 2410.0, 0.003),
        ("XLK", "sector", 214.5, 0.007), ("XLE", "sector", 93.1, 0.011),
    ]
    for sym, grp, val, chg in snaps:
        store_market_snapshot(conn, symbol=sym, grp=grp, as_of=today.isoformat(), value=val,
                              change_pct=chg, source="synthetic")

    doc = store_raw_document(conn, source="synthetic-news", source_tier=3, external_id="n1",
                             content="Synthetic headline body", url="https://example.com/demo",
                             published_at=utc_now())
    store_news_item(conn, raw_document_id=doc, published_at=utc_now(), region="asia",
                    headline="Demo: Asian equities slip as yields tick up", classified_by="demo",
                    topic="macro_data", impact="medium")

    set_state(conn, "mode", "shadow")
    heartbeat(conn)
    log_event(conn, "system", "start", "demo database seeded with synthetic data")

    base_idea = {
        "instrument": "stock", "catalyst": "Next product cycle", "regime": "risk_on", "source_tier": 1,
        "idea_source": "10-K footnote on margins", "days_to_earnings": 20,
        "variant_view": "Consensus models flat margins; filings show a cost step-down.",
        "invalidation": "Daily close below the stop.",
    }
    last = {t: conn.execute("SELECT close FROM prices WHERE ticker=? ORDER BY trade_date DESC LIMIT 1",
                            (t,)).fetchone()["close"] for t in ("AAPL", "XOM", "MSFT")}
    submit_proposal(conn, cfg, {**base_idea, "ticker": "AAPL", "direction": "long",
                                "entry_price": last["AAPL"], "atr": 3.2})
    submit_proposal(conn, cfg, {**base_idea, "ticker": "XOM", "direction": "short",
                                "entry_price": last["XOM"], "atr": 1.9, "short_interest_pct": 4.0})
    submit_proposal(conn, cfg, {**base_idea, "ticker": "MSFT", "direction": "long",
                                "entry_price": last["MSFT"] * 1.2, "atr": 6.0})  # blocked: off-price
    print(f"seeded {db_path} and {cfg_path} (synthetic)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
