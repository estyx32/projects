"""Turn database rows into display-ready dicts. No HTML here, so it is easy to test."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, date, datetime, timedelta

from .. import validate
from ..db import market_today
from ..engine.config import Config
from ..engine.regime import compute_regime, global_shocks
from ..engine.risk_gate import _drawdown_and_daily, current_equity
from ..engine.state import current_mode, get_state, kill_switch_on
from .format import parse_ts

HEARTBEAT_OK_SECONDS = 180
GROUP_ORDER = ["us_index", "global_index", "volatility", "rates", "fx", "commodity", "crypto", "sector"]
GROUP_LABELS = {
    "us_index": "US indices", "global_index": "Global indices", "volatility": "Volatility",
    "rates": "Rates", "fx": "Currencies", "commodity": "Commodities", "crypto": "Crypto",
    "sector": "Sectors",
}


def _today(today: date | None) -> date:
    return today or market_today()


def safe_url(url: str | None) -> str | None:
    """Only http(s) links are ever rendered as links."""
    if url and url.lower().startswith(("http://", "https://")):
        return url
    return None


def build_status(conn: sqlite3.Connection, cfg: Config, today: date | None = None) -> dict:
    today = _today(today)
    drawdown, daily_loss = _drawdown_and_daily(conn, cfg, today)
    regime = compute_regime(conn, cfg, today)
    hb = get_state(conn, "heartbeat")
    hb_dt = parse_ts(hb)
    if hb_dt is None:
        hb_state, hb_text = "bad", "not running (no heartbeat recorded yet)"
    else:
        secs = int((datetime.now(UTC) - hb_dt).total_seconds())
        hb_state = "ok" if secs <= HEARTBEAT_OK_SECONDS else "bad"
        hb_text = "running" if hb_state == "ok" else "stalled"
    regime_class = {"risk_on": "ok", "choppy": "warn", "risk_off": "bad"}.get(regime.label, "bad")
    return {
        "mode": current_mode(conn),
        "kill": kill_switch_on(conn),
        "equity": current_equity(conn, cfg),
        "drawdown": drawdown,
        "daily_loss": daily_loss,
        "regime": regime,
        "regime_class": regime_class,
        "shocks": global_shocks(conn, cfg, today),
        "heartbeat": hb,
        "heartbeat_class": hb_state,
        "heartbeat_text": hb_text,
        "prices_at": conn.execute("SELECT MAX(retrieved_at) FROM prices").fetchone()[0],
        "snapshots_at": conn.execute("SELECT MAX(retrieved_at) FROM market_snapshots").fetchone()[0],
    }


def _proposal(row: sqlite3.Row) -> dict:
    d = dict(row)
    try:
        gate = json.loads(d.get("gate_reasons") or "{}")
    except json.JSONDecodeError:
        gate = {}
    d["blocked_reasons"] = gate.get("blocked", [])
    d["passed_checks"] = gate.get("passed", [])
    return d


def build_queue(conn: sqlite3.Connection, cfg: Config, today: date | None = None) -> dict:
    pending = [_proposal(r) for r in conn.execute(
        "SELECT * FROM proposals WHERE status = 'pending' ORDER BY id DESC")]
    recent = [_proposal(r) for r in conn.execute(
        "SELECT * FROM proposals WHERE status != 'pending' ORDER BY id DESC LIMIT 10")]
    return {"pending": pending, "recent": recent}


def _level(share: float) -> str:
    return "ok" if share < 60 else "warn" if share < 90 else "hot"


def build_risk(conn: sqlite3.Connection, cfg: Config, today: date | None = None) -> dict:
    today = _today(today)
    drawdown, daily_loss = _drawdown_and_daily(conn, cfg, today)
    open_rows = conn.execute(
        "SELECT size_pct_account FROM trades WHERE date_closed IS NULL").fetchall()
    gross = sum(r["size_pct_account"] for r in open_rows)
    raw = [
        ("Gross exposure", gross, cfg.max_gross_exposure_pct, "%"),
        ("Open positions", float(len(open_rows)), cfg.max_open_positions, ""),
        ("Daily loss", daily_loss * 100, cfg.max_daily_loss_pct, "%"),
        ("Drawdown from peak", drawdown * 100, cfg.max_drawdown_pct, "%"),
    ]
    items = []
    for label, used, limit, unit in raw:
        share = min(100.0, used / limit * 100) if limit else 100.0
        digits = 0 if not unit else 1
        items.append({"label": label, "used": used, "limit": limit, "unit": unit, "digits": digits,
                      "share": round(share, 1), "level": _level(share)})
    return {"meters": items}


def build_positions(conn: sqlite3.Connection, cfg: Config, today: date | None = None) -> dict:
    today = _today(today)
    cutoff = (today - timedelta(days=int(cfg.max_price_age_days))).isoformat()
    rows = conn.execute(
        """SELECT t.*,
             (SELECT close FROM prices p WHERE p.ticker = t.ticker ORDER BY trade_date DESC LIMIT 1) AS last_close,
             (SELECT trade_date FROM prices p WHERE p.ticker = t.ticker ORDER BY trade_date DESC LIMIT 1) AS last_date
           FROM trades t WHERE t.date_closed IS NULL ORDER BY t.date_opened DESC"""
    ).fetchall()
    positions = []
    for r in rows:
        d = dict(r)
        last = d["last_close"]
        if last is None:
            d.update(ret=None, r_multiple=None, stale=True)
        else:
            move = last - d["entry_price"] if d["direction"] == "long" else d["entry_price"] - last
            d["ret"] = move / d["entry_price"]
            d["r_multiple"] = move / abs(d["entry_price"] - d["stop_level"])
            d["stale"] = d["last_date"] < cutoff
        positions.append(d)
    orders = [dict(r) for r in conn.execute(
        "SELECT * FROM orders ORDER BY id DESC LIMIT 15")]
    return {"positions": positions, "orders": orders}


def build_activity(conn: sqlite3.Connection, cfg: Config, today: date | None = None) -> dict:
    return {"events": [dict(r) for r in conn.execute(
        "SELECT * FROM events ORDER BY id DESC LIMIT 40")]}


def build_market(conn: sqlite3.Connection, cfg: Config, today: date | None = None) -> dict:
    today = _today(today)
    cutoff = (today - timedelta(days=int(cfg.max_price_age_days))).isoformat()
    rows = conn.execute(
        """SELECT m.* FROM market_snapshots m
           JOIN (SELECT symbol, MAX(as_of) AS a FROM market_snapshots GROUP BY symbol) l
             ON l.symbol = m.symbol AND l.a = m.as_of
           ORDER BY m.symbol"""
    ).fetchall()
    groups: dict[str, list[dict]] = {}
    for r in rows:
        d = dict(r)
        d["stale"] = d["as_of"] < cutoff
        groups.setdefault(d["grp"], []).append(d)
    ordered = [(GROUP_LABELS[g], groups[g]) for g in GROUP_ORDER if g in groups]
    news = []
    for r in conn.execute(
        """SELECT n.*, r.url, r.source FROM news_items n
           JOIN raw_documents r ON r.id = n.raw_document_id
           ORDER BY n.published_at DESC LIMIT 15"""
    ):
        d = dict(r)
        d["link"] = safe_url(d.get("url"))
        news.append(d)
    return {"groups": ordered, "news": news}


def build_quality(conn: sqlite3.Connection, cfg: Config, today: date | None = None) -> dict:
    findings = validate.run_all(conn, today)
    return {"findings": [
        {"check": f.check, "severity": f.severity, "detail": f.detail} for f in findings]}


SECTIONS = {
    "status": build_status,
    "queue": build_queue,
    "risk": build_risk,
    "positions": build_positions,
    "market": build_market,
    "activity": build_activity,
    "quality": build_quality,
}
