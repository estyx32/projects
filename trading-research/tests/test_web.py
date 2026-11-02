"""Web tests: rendering from real rows, escaping, and the local-only request guards."""

from __future__ import annotations

import re

import pytest
from conftest import BASE_CONFIG, idea, seed_world
from fastapi.testclient import TestClient

from tradelab.db import connect, utc_now
from tradelab.engine import engine as eng
from tradelab.engine.config import parse_config
from tradelab.ingest import store_news_item, store_raw_document
from tradelab.web import views
from tradelab.web.app import create_app
from tradelab.web.format import DASH, age, local_time, money, pct_frac


@pytest.fixture()
def env(tmp_path):
    db = tmp_path / "t.db"
    conn = connect(db)
    seed_world(conn)
    cfg_path = tmp_path / "risk.toml"
    lines = []
    for k, v in BASE_CONFIG.items():
        if isinstance(v, bool):
            lines.append(f"{k} = {'true' if v else 'false'}")
        elif isinstance(v, list):
            import json
            lines.append(f"{k} = {json.dumps(v)}")
        else:
            lines.append(f"{k} = {v}")
    cfg_path.write_text("\n".join(lines))
    client = TestClient(create_app(str(db), str(cfg_path)))
    return conn, client, parse_config(dict(BASE_CONFIG))


def token(client) -> str:
    html = client.get("/").text
    return re.search(r'name="csrf-token" content="([^"]+)"', html).group(1)


# ---------------------------------------------------------- request guards
def test_index_renders_every_section(env):
    _, client, _ = env
    res = client.get("/")
    assert res.status_code == 200
    for needle in ("Risk limits", "Global markets", "Data quality", "Proposals waiting", "RISK ON"):
        assert needle in res.text
    assert "default-src 'none'" in res.headers["content-security-policy"]
    assert res.headers["cache-control"] == "no-store"


def test_unknown_host_is_refused(env):
    _, client, _ = env
    assert client.get("/", headers={"host": "evil.example"}).status_code == 400


def test_posts_need_csrf_token_and_same_origin(env):
    _, client, _ = env
    body = {"on": True}
    assert client.post("/api/kill", json=body).status_code == 403
    assert client.post("/api/kill", json=body, headers={"x-csrf-token": "wrong"}).status_code == 403
    good = {"x-csrf-token": token(client)}
    assert client.post("/api/kill", json=body,
                       headers={**good, "origin": "https://evil.example"}).status_code == 403
    assert client.post("/api/kill", json=body,
                       headers={**good, "origin": "http://localhost:8000"}).status_code == 200


def test_kill_switch_endpoint_validates_body_and_persists(env):
    conn, client, _ = env
    h = {"x-csrf-token": token(client)}
    assert client.post("/api/kill", json={"on": "yes"}, headers=h).status_code == 422
    assert client.post("/api/kill", json={"on": True}, headers=h).status_code == 200
    assert conn.execute("SELECT value FROM system_state WHERE key='kill_switch'").fetchone()[0] == "on"
    assert "Resume trading" in client.get("/fragment/status").text


def test_approve_reject_endpoints(env):
    conn, client, cfg = env
    h = {"x-csrf-token": token(client)}
    a = eng.submit_proposal(conn, cfg, idea(conn, "AAPL"))
    b = eng.submit_proposal(conn, cfg, idea(conn, "MSFT"))
    assert client.post(f"/api/proposals/{a}/approve", headers=h).json()["status"] == "approved"
    assert client.post(f"/api/proposals/{b}/reject", headers=h).json()["status"] == "rejected"
    assert client.post(f"/api/proposals/{a}/approve", headers=h).status_code == 409  # already decided
    assert client.post(f"/api/proposals/{a}/explode", headers=h).status_code == 404
    assert conn.execute("SELECT COUNT(*) FROM orders WHERE status != 'shadow'").fetchone()[0] == 0


def test_unknown_fragment_and_missing_config(tmp_path):
    conn = connect(tmp_path / "x.db")
    conn.close()
    client = TestClient(create_app(str(tmp_path / "x.db"), str(tmp_path / "missing.toml")))
    page = client.get("/")
    assert page.status_code == 200 and "Engine config not loaded" in page.text
    assert client.get("/fragment/status").status_code == 503


# ---------------------------------------------------------------- escaping
def test_untrusted_text_is_escaped_and_bad_links_not_rendered(env):
    conn, client, cfg = env
    payload = "<script>alert(1)</script>"
    eng.submit_proposal(conn, cfg, idea(conn, "AAPL", variant_view=payload, idea_source="<img src=x>"))
    doc = store_raw_document(conn, source="news", source_tier=3, external_id="n1", content="x",
                             url="javascript:alert(1)", published_at=utc_now())
    store_news_item(conn, raw_document_id=doc, published_at=utc_now(), region="us",
                    headline="<b>bold</b> headline", classified_by="t")
    html = client.get("/").text
    assert payload not in html and "&lt;script&gt;" in html
    assert "<img src=x>" not in html
    assert "<b>bold</b>" not in html
    assert "javascript:" not in html


def test_safe_url_only_allows_http():
    assert views.safe_url("https://example.com/a") == "https://example.com/a"
    assert views.safe_url("javascript:alert(1)") is None
    assert views.safe_url("data:text/html,x") is None
    assert views.safe_url(None) is None


# ------------------------------------------------------- data to display
def test_status_shows_regime_heartbeat_and_staleness(env):
    conn, _, cfg = env
    s = views.build_status(conn, cfg)
    assert s["regime"].label == "risk_on" and s["heartbeat_class"] == "ok" and not s["kill"]
    conn.execute("UPDATE system_state SET value='2020-01-01T00:00:00Z' WHERE key='heartbeat'")
    conn.commit()
    assert views.build_status(conn, cfg)["heartbeat_class"] == "bad"


def test_risk_meters_reflect_open_positions(env):
    conn, _, cfg = env
    conn.execute(
        """INSERT INTO trades (ticker, direction, instrument, date_opened, source_tier, idea_source,
           regime_at_entry, variant_view, catalyst, invalidation, entry_price, size_pct_account, stop_level)
           VALUES ('AAPL','long','stock','2026-01-02',1,'s','risk_on','v','c','i',100,40,90)""")
    conn.commit()
    gross = next(m for m in views.build_risk(conn, cfg)["meters"] if m["label"] == "Gross exposure")
    assert gross["used"] == 40 and gross["limit"] == 50 and gross["level"] == "warn"


def test_position_return_and_r_multiple_use_latest_price(env):
    conn, _, cfg = env
    last = conn.execute("SELECT close FROM prices WHERE ticker='AAPL' ORDER BY trade_date DESC LIMIT 1").fetchone()[0]
    entry = round(last / 1.10, 2)
    conn.execute(
        """INSERT INTO trades (ticker, direction, instrument, date_opened, source_tier, idea_source,
           regime_at_entry, variant_view, catalyst, invalidation, entry_price, size_pct_account, stop_level)
           VALUES ('AAPL','long','stock','2026-01-02',1,'s','risk_on','v','c','i',?,5,?)""",
        (entry, entry * 0.95))
    conn.commit()
    p = views.build_positions(conn, cfg)["positions"][0]
    assert abs(p["ret"] - 0.10) < 0.01 and p["r_multiple"] > 1.5 and not p["stale"]


def test_missing_values_render_as_dash_never_zero():
    assert money(None) == DASH and pct_frac(None) == DASH and local_time(None) == DASH and age(None) == DASH
    assert money(1234.5) == "$1,234.50"
    assert local_time("2026-11-02T04:26:00Z") == "Nov 1, 11:26 PM ET"
