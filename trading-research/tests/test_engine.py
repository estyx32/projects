"""Engine tests: sizing, exits, config, regime, risk gate, proposal flow."""

from __future__ import annotations

import sqlite3
from datetime import UTC

import pytest
from conftest import BASE_CONFIG, idea, last_close, make_cfg, seed_world

from tradelab.db import market_day_start_utc, market_today
from tradelab.engine import engine as eng
from tradelab.engine.config import ConfigError, parse_config
from tradelab.engine.exits import Position, evaluate_exit
from tradelab.engine.regime import compute_regime, global_shocks
from tradelab.engine.sizing import position_size, stop_from_atr
from tradelab.engine.state import set_kill_switch
from tradelab.ingest import store_market_snapshot


# ---------------------------------------------------------------- sizing
def test_size_risks_fixed_fraction_and_rounds_down():
    r = position_size(equity=100_000, risk_pct=1, direction="long", entry=50, stop=48,
                      max_position_pct=100, max_order_notional=1e9)
    assert r.qty == 500 and r.risk_dollars == 1000.0 and r.capped_by is None


def test_size_is_capped_by_position_limit_and_notional():
    r = position_size(equity=100_000, risk_pct=1, direction="long", entry=50, stop=49.9,
                      max_position_pct=5, max_order_notional=1e9)
    assert r.qty == 100 and r.capped_by == "position_limit"
    r = position_size(equity=100_000, risk_pct=1, direction="long", entry=50, stop=49.9,
                      max_position_pct=100, max_order_notional=2_000)
    assert r.qty == 40 and r.capped_by == "order_notional"


def test_short_sizing_and_bad_stops_rejected():
    r = position_size(equity=10_000, risk_pct=1, direction="short", entry=100, stop=105,
                      max_position_pct=100, max_order_notional=1e9)
    assert r.qty == 20
    with pytest.raises(ValueError):
        position_size(equity=10_000, risk_pct=1, direction="long", entry=100, stop=101,
                      max_position_pct=100, max_order_notional=1e9)
    with pytest.raises(ValueError):
        position_size(equity=10_000, risk_pct=1, direction="short", entry=100, stop=99,
                      max_position_pct=100, max_order_notional=1e9)


def test_stop_from_atr_sides():
    assert stop_from_atr("long", 100, 2, 2) == 96
    assert stop_from_atr("short", 100, 2, 2) == 104


# ----------------------------------------------------------------- exits
def pos(**over):
    base = {"direction": "long", "entry": 100.0, "initial_stop": 95.0, "stop": 95.0, "qty_initial": 90,
            "qty_remaining": 90, "days_held": 3, "atr": 2.0, "extreme": 100.0}
    base.update(over)
    return Position(**base)


KW = {"targets": ((1.0, 0.33), (2.0, 0.33)), "trail_atr_multiple": 2.0, "time_stop_days": 60}


def test_stop_hit_closes_everything_even_if_a_target_was_also_reached():
    d = evaluate_exit(pos(), 94.0, **KW)
    assert [a.kind for a in d.actions] == ["close_all"] and d.actions[0].qty == 90


def test_scale_out_then_breakeven_and_trail():
    d = evaluate_exit(pos(), 105.0, **KW)  # +1R
    assert [a.reason for a in d.actions] == ["target 1R"] and d.actions[0].qty == 29
    assert d.new_stop >= 100.0  # breakeven at least
    d2 = evaluate_exit(pos(extreme=110.0, targets_taken={1.0}, qty_remaining=61), 108.0, **KW)
    assert d2.new_stop == 106.0  # trail: 110 - 2*2 ATR


def test_each_target_taken_once_and_stops_never_loosen():
    p = pos(targets_taken={1.0}, qty_remaining=61, stop=102.0, extreme=106.0)
    d = evaluate_exit(p, 105.5, **KW)
    assert d.actions == () and d.new_stop >= 102.0
    d = evaluate_exit(pos(stop=98.0), 99.0, **KW)  # no target yet: stop unchanged
    assert d.new_stop == 98.0


def test_time_stop_and_short_mirror():
    assert evaluate_exit(pos(days_held=60), 101.0, **KW).actions[0].reason == "time stop"
    s = pos(direction="short", initial_stop=105.0, stop=105.0)
    assert evaluate_exit(s, 106.0, **KW).actions[0].reason == "stop hit"
    d = evaluate_exit(s, 95.0, **KW)  # +1R for a short
    assert d.actions[0].reason == "target 1R" and d.new_stop <= 100.0


# ---------------------------------------------------------------- config
def test_config_refuses_unreviewed_missing_and_out_of_range():
    with pytest.raises(ConfigError):
        parse_config({**BASE_CONFIG, "config_reviewed": False})
    missing = {k: v for k, v in BASE_CONFIG.items() if k != "max_daily_loss_pct"}
    with pytest.raises(ConfigError, match="max_daily_loss_pct"):
        parse_config(missing)
    with pytest.raises(ConfigError):
        parse_config({**BASE_CONFIG, "risk_per_trade_pct": 50})
    with pytest.raises(ConfigError):
        parse_config({**BASE_CONFIG, "risk_per_trade_pct": True})
    with pytest.raises(ConfigError):
        parse_config({**BASE_CONFIG, "targets": [[1, 0.7], [2, 0.7]]})
    with pytest.raises(ConfigError):
        parse_config({**BASE_CONFIG, "vix_risk_on_level": 30})
    with pytest.raises(ConfigError):
        parse_config({**BASE_CONFIG, "allowlist": []})


# ---------------------------------------------------------------- regime
def test_regime_is_computed_and_fails_closed(conn, cfg):
    assert compute_regime(conn, cfg).label == "unknown"  # no data at all
    seed_world(conn, trend=0.0006, vix=15)
    assert compute_regime(conn, cfg).label == "risk_on"
    store_market_snapshot(conn, symbol="VIX", grp="volatility", as_of=_today(), value=30,
                          source="synthetic")
    assert compute_regime(conn, cfg).label == "choppy"  # trend up, vol high: one vote each way


def test_regime_risk_off_in_downtrend_with_high_vix(conn, cfg):
    seed_world(conn, trend=-0.0008, vix=30)
    assert compute_regime(conn, cfg).label == "risk_off"


def test_global_shock_detection(conn, cfg):
    store_market_snapshot(conn, symbol="NIKKEI", grp="global_index", as_of=_today(),
                          value=1, change_pct=-0.045, source="synthetic")
    store_market_snapshot(conn, symbol="DAX", grp="global_index", as_of=_today(),
                          value=1, change_pct=-0.01, source="synthetic")
    shocks = global_shocks(conn, cfg)
    assert len(shocks) == 1 and "NIKKEI" in shocks[0]


def _today():
    return market_today().isoformat()


# -------------------------------------------------------------- risk gate
def submit(conn, cfg, **over):
    pid = eng.submit_proposal(conn, cfg, idea(conn, **over.pop("idea", {})), **over)
    return pid, conn.execute("SELECT * FROM proposals WHERE id=?", (pid,)).fetchone()


def reasons(row):
    import json
    return " | ".join(json.loads(row["gate_reasons"])["blocked"])


def test_clean_long_passes_in_risk_on(world, cfg):
    _, row = submit(world, cfg)
    assert row["status"] == "pending" and row["qty"] > 0


def test_gate_fails_closed_without_regime_data(conn, cfg):
    from tradelab.ingest import store_price
    # a fresh price for the ticker, but no SPY history and no VIX: regime cannot be computed
    store_price(conn, ticker="AAPL", trade_date=market_today().isoformat(), close=200.0, price_source="s")
    base = {"ticker": "AAPL", "direction": "long", "instrument": "stock", "entry_price": 200.0,
            "atr": 0.5, "catalyst": "c", "regime": "risk_on", "source_tier": 1, "idea_source": "s",
            "days_to_earnings": 20, "variant_view": "v", "invalidation": "i"}
    pid = eng.submit_proposal(conn, cfg, base)
    row = conn.execute("SELECT * FROM proposals WHERE id=?", (pid,)).fetchone()
    assert row["status"] == "blocked" and "regime cannot be verified" in reasons(row)


@pytest.mark.parametrize("over, expect", [
    ({"ticker": "XOM2"}, "not on the allowlist"),
    ({"days_to_earnings": 1}, "blackout"),
    ({"days_to_earnings": None}, "earnings date missing"),
])
def test_gate_blocks(world, cfg, over, expect):
    data = idea(world)
    if over.get("ticker") == "XOM2":
        # a ticker with a fresh price but not on the allowlist
        from tradelab.ingest import store_price
        store_price(world, ticker="XOM2", trade_date=market_today().isoformat(), close=50.0, price_source="s")
        data.update(ticker="XOM2", entry_price=50.0)
    else:
        data.update(over)
    pid = eng.submit_proposal(world, cfg, data)
    row = world.execute("SELECT * FROM proposals WHERE id=?", (pid,)).fetchone()
    assert row["status"] == "blocked" and expect in reasons(row)


def test_gate_blocks_off_price_stale_and_claimed_regime(world, cfg):
    _, row = submit(world, cfg, idea={"entry_price": last_close(world, "AAPL") * 1.2})
    assert "from last close" in reasons(row)
    _, row = submit(world, cfg, idea={"ticker": "MSFT", "regime": "risk_off"})
    assert "claimed regime" in reasons(row)
    from datetime import timedelta
    pid = eng.submit_proposal(world, cfg, idea(world, "XOM"), today=market_today() + timedelta(days=30))
    stale = world.execute("SELECT * FROM proposals WHERE id=?", (pid,)).fetchone()
    assert stale["status"] == "blocked" and "stale" in reasons(stale)


def test_shorts_need_a_non_risk_on_regime_and_short_interest(world, cfg):
    _, row = submit(world, cfg, idea={"ticker": "XOM", "direction": "short"})  # regime is risk_on
    assert "shorts blocked in a risk-on" in reasons(row)
    _, row = submit(world, cfg, idea={"ticker": "MSFT", "direction": "short", "short_interest_pct": None})
    assert "short interest missing" in reasons(row)


def test_longs_blocked_in_risk_off_and_on_global_shock(conn, cfg):
    seed_world(conn, trend=-0.0008, vix=30)
    pid = eng.submit_proposal(conn, cfg, idea(conn, regime="risk_off"))
    assert "longs blocked in a risk-off" in reasons(conn.execute("SELECT * FROM proposals WHERE id=?", (pid,)).fetchone())


def test_global_shock_pauses_longs(world, cfg):
    store_market_snapshot(world, symbol="NIKKEI", grp="global_index", as_of=_today(), value=1,
                          change_pct=-0.05, source="synthetic")
    _, row = submit(world, cfg)
    assert "global shock" in reasons(row)


def test_zero_size_is_blocked_and_only_stocks_supported(world, cfg):
    _, row = submit(world, make_cfg(max_long_position_pct=0.1))
    assert "size is zero" in reasons(row)
    _, row = submit(world, cfg, idea={"instrument": "put"})
    assert "not supported yet" in reasons(row)


def test_missing_fields_raise(world, cfg):
    bad = idea(world)
    bad["variant_view"] = ""
    with pytest.raises(eng.ProposalError, match="variant_view"):
        eng.submit_proposal(world, cfg, bad)


# ----------------------------------------------------------- proposal flow
def test_approve_records_shadow_orders_only(world, cfg):
    pid, _ = submit(world, cfg)
    assert eng.approve(world, cfg, pid, "tester") is True
    rows = world.execute("SELECT kind, status FROM orders WHERE proposal_id=?", (pid,)).fetchall()
    assert {r["kind"] for r in rows} >= {"entry_limit", "protective_stop"}
    assert {r["status"] for r in rows} == {"shadow"}  # nothing is ever sent
    with pytest.raises(sqlite3.IntegrityError):  # a decided proposal is final
        world.execute("UPDATE proposals SET qty = 999 WHERE id=?", (pid,))
    with pytest.raises(eng.ProposalError):
        eng.approve(world, cfg, pid, "tester")


def test_kill_switch_blocks_new_proposals_and_approval_regates(world, cfg):
    pid, _ = submit(world, cfg)
    set_kill_switch(world, True, "tester")
    assert eng.approve(world, cfg, pid, "tester") is False
    row = world.execute("SELECT status FROM proposals WHERE id=?", (pid,)).fetchone()
    assert row["status"] == "blocked"
    assert world.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0
    _, row2 = submit(world, cfg, idea={"ticker": "MSFT"})
    assert "kill switch is ON" in reasons(row2)


def test_reject_and_event_trail(world, cfg):
    pid, _ = submit(world, cfg)
    eng.reject(world, pid, "tester")
    assert world.execute("SELECT status FROM proposals WHERE id=?", (pid,)).fetchone()[0] == "rejected"
    kinds = [r["kind"] for r in world.execute("SELECT kind FROM events ORDER BY id")]
    assert kinds[:3] == ["proposal", "passed", "rejected"]
    with pytest.raises(sqlite3.IntegrityError):
        world.execute("DELETE FROM events")


def test_daily_loss_and_drawdown_breakers(world, cfg):
    from datetime import datetime, timedelta
    today = market_today()
    start = datetime.strptime(market_day_start_utc(today), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    stamp = lambda hours: (start + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    world.execute("INSERT INTO equity_snapshots VALUES (?, ?)", (stamp(1), 10_000))
    world.execute("INSERT INTO equity_snapshots VALUES (?, ?)", (stamp(5), 9_700))
    world.commit()
    _, row = submit(world, cfg)
    assert "daily loss" in reasons(row)


def test_trading_day_follows_new_york_not_utc():
    from datetime import date
    # 11 PM ET on Nov 1 is already Nov 2 in UTC; the trading day must still be Nov 1
    assert market_day_start_utc(date(2026, 11, 1)) == "2026-11-01T04:00:00Z"  # EDT until Nov 1 02:00
    assert market_day_start_utc(date(2026, 11, 2)) == "2026-11-02T05:00:00Z"  # EST after the change
