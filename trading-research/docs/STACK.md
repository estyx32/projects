# Stack and backend decision

Decision: **Python, one SQLite database (Postgres later), a separate worker process, and a small FastAPI
server that renders the UI.** Claude runs as a separate research process that can only write proposals.

## Shape

```
collectors (prices, FRED, EDGAR, news) --> database <-- worker (heartbeat, equity, exit monitor)
Claude research agent --> submit_proposal --> sizing --> risk gate --> proposals
you (browser) --> FastAPI UI --> approve / reject / kill switch --> engine
(later) engine --> broker adapter --> Schwab        [only the worker/adapter holds credentials]
```

The database is the single source of truth. The UI only reads it and sends three kinds of commands:
approve, reject, kill switch.

## Choices and why

| Layer | Choice | Why | Revisit when |
| --- | --- | --- | --- |
| Language | Python 3.11+ | Data and finance libraries, broker clients, the Anthropic SDK; the engine is small pure functions that are easy to test | Never needed for this scale |
| Database | SQLite in WAL mode | One user, local, zero ops, constraints and triggers enforce integrity | Remote hosting, several writers, or retention needs: move to PostgreSQL (port the triggers) |
| Web | FastAPI + Jinja server-rendered panels + ~100 lines of vanilla JS polling | Read-heavy dashboard, all data comes from the database, tiny XSS surface, strict CSP with no inline script | You need rich interactive charts or live streaming: add Server-Sent Events, then a chart library served from `/static` |
| Why not a React SPA | Extra build chain, a second place to get formatting and auth wrong | Fewer moving parts for the same result | A multi-user product |
| Worker | Separate long-running process (APScheduler or a systemd timer) | Keeps collection, exits and broker calls out of the web process, so a UI bug can't send an order | Needs more than one machine |
| Claude's role | Separate process using the Anthropic SDK with structured output, no broker credentials | Transcripts and news are untrusted text; a model that cannot place orders cannot be steered into placing them | Never relax |
| Backtest | Replay history through the same pure sizing, gate and exit functions | One code path for backtest, shadow and live, so results mean something | When adding multi-asset portfolios |
| Alerts | Push notification on kill switch, blocked order, stalled heartbeat, reconciliation mismatch | Knight Capital had warnings nobody read; they must reach your phone | Always |
| Deploy | Your own machine or one small VM, bound to localhost; reach it remotely only through a private network (e.g. Tailscale) after auth exists | No public attack surface | Multi-user |
| Secrets | Environment variables or the OS keychain; never in the repo or the database | Broker tokens expire weekly anyway | Moving to a cloud secret store |

## What would change this

If this becomes multi-user or hosted: PostgreSQL, real authentication and per-user authorization, row-level audit,
a managed secret store, and a front end framework only if the product needs it.
