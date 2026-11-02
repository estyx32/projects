-- Engine and command-center tables. Applied after schema.sql.

CREATE TABLE IF NOT EXISTS system_state (
    key         TEXT PRIMARY KEY,          -- 'kill_switch' ('on'/'off'), 'mode', 'heartbeat'
    value       TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS equity_snapshots (
    ts      TEXT NOT NULL,                 -- ISO 8601 UTC
    equity  REAL NOT NULL CHECK (equity > 0),
    PRIMARY KEY (ts)
);

-- Global picture: other key markets. One row per symbol per day per source.
CREATE TABLE IF NOT EXISTS market_snapshots (
    symbol        TEXT NOT NULL,                -- e.g. 'VIX', 'NIKKEI', 'DAX', 'US10Y', 'DXY', 'WTI', 'GOLD'
    grp           TEXT NOT NULL CHECK (grp IN
                  ('us_index', 'global_index', 'sector', 'rates', 'fx', 'commodity', 'volatility', 'crypto')),
    as_of         TEXT NOT NULL,                -- YYYY-MM-DD
    value         REAL NOT NULL,
    change_pct    REAL,                         -- 1-day change as a fraction: -0.02 = -2%
    source        TEXT NOT NULL,
    retrieved_at  TEXT NOT NULL,
    PRIMARY KEY (symbol, as_of, source)
);

-- Global news, always tied to the raw document it came from.
CREATE TABLE IF NOT EXISTS news_items (
    id               INTEGER PRIMARY KEY,
    raw_document_id  INTEGER NOT NULL REFERENCES raw_documents(id),
    published_at     TEXT NOT NULL,
    region           TEXT NOT NULL CHECK (region IN ('us', 'europe', 'asia', 'global')),
    headline         TEXT NOT NULL,
    tickers          TEXT,
    topic            TEXT CHECK (topic IS NULL OR topic IN
                     ('central_bank', 'geopolitics', 'earnings', 'macro_data', 'other')),
    impact           TEXT CHECK (impact IS NULL OR impact IN ('high', 'medium', 'low')),
    classified_by    TEXT NOT NULL,             -- model id + prompt version, or 'human'
    human_verified   INTEGER NOT NULL DEFAULT 0 CHECK (human_verified IN (0, 1))
);

-- Trade ideas from Claude (or you). The engine sizes and gates each one.
CREATE TABLE IF NOT EXISTS proposals (
    id                INTEGER PRIMARY KEY,
    created_at        TEXT NOT NULL,
    proposed_by       TEXT NOT NULL,
    ticker            TEXT NOT NULL,
    direction         TEXT NOT NULL CHECK (direction IN ('long', 'short')),
    instrument        TEXT NOT NULL CHECK (instrument IN ('stock', 'put', 'put_spread', 'call', 'call_spread')),
    entry_price       REAL NOT NULL CHECK (entry_price > 0),
    stop_price        REAL NOT NULL CHECK (stop_price > 0),
    atr               REAL CHECK (atr IS NULL OR atr > 0),
    scorecard_score   REAL,
    variant_view      TEXT NOT NULL CHECK (length(variant_view) > 0),
    catalyst          TEXT NOT NULL,
    invalidation      TEXT NOT NULL CHECK (length(invalidation) > 0),
    source_tier       INTEGER NOT NULL CHECK (source_tier IN (1, 2, 3)),
    idea_source       TEXT NOT NULL,
    regime            TEXT NOT NULL CHECK (regime IN ('risk_on', 'choppy', 'risk_off')),
    short_interest_pct REAL,
    days_to_earnings  INTEGER,
    status            TEXT NOT NULL DEFAULT 'pending'
                      CHECK (status IN ('pending', 'approved', 'rejected', 'blocked')),
    qty               INTEGER CHECK (qty IS NULL OR qty >= 0),
    risk_dollars      REAL,
    size_pct_account  REAL,
    gate_reasons      TEXT,                 -- JSON list; why it was blocked or what passed
    decided_at        TEXT,
    decided_by        TEXT,
    CHECK ((direction = 'long'  AND stop_price < entry_price) OR
           (direction = 'short' AND stop_price > entry_price))
);

-- A decided proposal is final.
CREATE TRIGGER IF NOT EXISTS proposals_decided_locked
BEFORE UPDATE ON proposals
WHEN OLD.status != 'pending'
BEGIN SELECT RAISE(ABORT, 'decided proposals are final'); END;

CREATE TRIGGER IF NOT EXISTS proposals_no_delete
BEFORE DELETE ON proposals
BEGIN SELECT RAISE(ABORT, 'proposals cannot be deleted'); END;

-- Orders the engine created. 'shadow' means recorded but never sent to a broker.
CREATE TABLE IF NOT EXISTS orders (
    id           INTEGER PRIMARY KEY,
    proposal_id  INTEGER NOT NULL REFERENCES proposals(id),
    created_at   TEXT NOT NULL,
    ticker       TEXT NOT NULL,
    side         TEXT NOT NULL CHECK (side IN ('buy', 'sell', 'sell_short', 'buy_to_cover')),
    kind         TEXT NOT NULL CHECK (kind IN ('entry_limit', 'protective_stop', 'target')),
    qty          INTEGER NOT NULL CHECK (qty > 0),
    price        REAL NOT NULL CHECK (price > 0),
    status       TEXT NOT NULL CHECK (status IN ('shadow', 'sent', 'filled', 'cancelled'))
);

-- Activity feed: everything Claude, the engine, the risk gate and you do. Append-only.
CREATE TABLE IF NOT EXISTS events (
    id           INTEGER PRIMARY KEY,
    ts           TEXT NOT NULL,
    actor        TEXT NOT NULL CHECK (actor IN ('claude', 'engine', 'risk_gate', 'user', 'system')),
    kind         TEXT NOT NULL,
    message      TEXT NOT NULL,
    proposal_id  INTEGER REFERENCES proposals(id)
);

CREATE TRIGGER IF NOT EXISTS events_no_update
BEFORE UPDATE ON events
BEGIN SELECT RAISE(ABORT, 'events is append-only'); END;

CREATE TRIGGER IF NOT EXISTS events_no_delete
BEFORE DELETE ON events
BEGIN SELECT RAISE(ABORT, 'events is append-only'); END;
