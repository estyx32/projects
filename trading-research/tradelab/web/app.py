"""Command center web app (FastAPI, server-rendered).

No login yet, by request. Instead it is local-only by construction: bind it to
127.0.0.1, it rejects unexpected Host headers (DNS rebinding) and cross-site
POSTs, and every state-changing call needs a per-process CSRF token.
Add real authentication before exposing it beyond your own machine.
"""

from __future__ import annotations

import os
import secrets
from contextlib import contextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..db import connect
from ..engine import engine as eng
from ..engine.config import ConfigError, load_config
from ..engine.state import log_event, set_kill_switch
from .format import FILTERS
from .views import SECTIONS

HERE = Path(__file__).resolve().parent
ALLOWED_HOSTS = {"127.0.0.1", "localhost", "[::1]", "testserver"}
LOCAL_USER = "local-operator"


def _hostname(hostport: str) -> str:
    """'localhost:8000' -> 'localhost'; '[::1]:8000' -> '[::1]'."""
    if hostport.startswith("["):
        return hostport.split("]")[0] + "]"
    return hostport.rsplit(":", 1)[0] if ":" in hostport else hostport


def create_app(db_path: str, config_path: str) -> FastAPI:
    app = FastAPI(title="Trading command center", docs_url=None, redoc_url=None, openapi_url=None)
    templates = Jinja2Templates(directory=str(HERE / "templates"))
    templates.env.autoescape = True  # never render untrusted text unescaped
    templates.env.filters.update(FILTERS)
    app.mount("/static", StaticFiles(directory=str(HERE / "static")), name="static")

    csrf_token = secrets.token_urlsafe(32)

    try:
        cfg = load_config(config_path)
        config_error = None
    except (ConfigError, FileNotFoundError, ValueError) as exc:
        cfg, config_error = None, str(exc)

    @contextmanager
    def db():
        conn = connect(db_path)
        try:
            yield conn
        finally:
            conn.close()

    @app.middleware("http")
    async def guard(request: Request, call_next):
        if _hostname(request.headers.get("host", "")) not in ALLOWED_HOSTS:
            return JSONResponse({"error": "host not allowed"}, status_code=400)
        if request.method == "POST":
            origin = request.headers.get("origin")
            if origin is not None and _hostname(origin.split("://", 1)[-1]) not in ALLOWED_HOSTS:
                return JSONResponse({"error": "cross-site request refused"}, status_code=403)
            if not secrets.compare_digest(request.headers.get("x-csrf-token", ""), csrf_token):
                return JSONResponse({"error": "missing or bad CSRF token"}, status_code=403)
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
            "connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response

    def render(request: Request, name: str, ctx: dict) -> HTMLResponse:
        return templates.TemplateResponse(request, name, ctx)

    def section_data(name: str) -> dict:
        if cfg is None:
            return {}
        with db() as conn:
            return SECTIONS[name](conn, cfg)

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        if cfg is None:
            return render(request, "config_error.html", {"error": config_error, "csrf": csrf_token})
        ctx = {name: section_data(name) for name in SECTIONS}
        ctx.update(csrf=csrf_token)
        return render(request, "index.html", ctx)

    @app.get("/fragment/{name}", response_class=HTMLResponse)
    def fragment(request: Request, name: str):
        if name not in SECTIONS:
            raise HTTPException(404)
        if cfg is None:
            raise HTTPException(503, "config not loaded")
        return render(request, f"partials/{name}.html", {name: section_data(name), "csrf": csrf_token})

    @app.post("/api/kill")
    async def kill(request: Request):
        body = await request.json()
        if not isinstance(body, dict) or not isinstance(body.get("on"), bool):
            raise HTTPException(422, "body must be {\"on\": true|false}")
        with db() as conn:
            set_kill_switch(conn, body["on"], LOCAL_USER)
        return {"kill": body["on"]}

    @app.post("/api/proposals/{proposal_id}/{action}")
    def decide(proposal_id: int, action: str):
        if cfg is None:
            raise HTTPException(503, "config not loaded")
        if action not in ("approve", "reject"):
            raise HTTPException(404)
        with db() as conn:
            try:
                if action == "approve":
                    ok = eng.approve(conn, cfg, proposal_id, LOCAL_USER)
                    return {"ok": ok, "status": "approved" if ok else "blocked"}
                eng.reject(conn, proposal_id, LOCAL_USER)
                return {"ok": True, "status": "rejected"}
            except eng.ProposalError as exc:
                raise HTTPException(409, str(exc)) from exc

    @app.get("/healthz")
    def healthz():
        return {"ok": True}

    _ = log_event  # re-exported for operators who extend the app
    return app


def app_from_env() -> FastAPI:
    return create_app(
        os.environ.get("TRADELAB_DB", "data/research.db"),
        os.environ.get("TRADELAB_CONFIG", "config/risk.toml"),
    )
