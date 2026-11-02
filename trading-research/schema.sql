-- Trading research data layer (SQLite).
-- Principles: raw data is immutable, every derived row points at its source,
-- entry-time trade fields cannot be edited after the fact, and every change
-- to a trade is written to an append-only audit log.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------- raw layer
CREATE TABLE IF NOT EXISTS raw_documents (
    id            INTEGER PRIMARY KEY,
    source        TEXT NOT NULL,                       -- e.g. 'youtube', 'edgar', 'reddit'
    source_tier   INTEGER NOT NULL CHECK (source_tier IN (1, 2, 3)),
    external_id   TEXT NOT NULL,                       -- video id, accession number, post id
    url           TEXT,
    published_at  TEXT,                                -- ISO 8601 UTC, when the source published it
    retrieved_at  TEXT NOT NULL,                       -- ISO 8601 UTC, when we fetched it
    content       TEXT NOT NULL,
    content_sha256 TEXT NOT NULL CHECK (length(content_sha256) = 64),
    UNIQUE (source, external_id, content_sha256)       -- same doc, same bytes: stored once
);

CREATE TRIGGER IF NOT EXISTS raw_documents_no_update
BEFORE UPDATE ON raw_documents
BEGIN SELECT RAISE(ABORT, 'raw_documents is immutable'); END;

CREATE TRIGGER IF NOT EXISTS raw_documents_no_delete
BEFORE DELETE ON raw_documents
BEGIN SELECT RAISE(ABORT, 'raw_documents is immutable'); END;

-- --------------------------------------------------------------- prices
CREATE TABLE IF NOT EXISTS prices (
    ticker        TEXT NOT NULL,
    trade_date    TEXT NOT NULL,                       -- YYYY-MM-DD
    close         REAL NOT NULL CHECK (close > 0),
    adj_close     REAL CHECK (adj_close IS NULL OR adj_close > 0),
    volume        INTEGER CHECK (volume IS NULL OR volume >= 0),
    price_source  TEXT NOT NULL,
    retrieved_at  TEXT NOT NULL,
    PRIMARY KEY (ticker, trade_date, price_source)
);

-- ----------------------------------------------------- investor calls (YouTube etc.)
CREATE TABLE IF NOT EXISTS calls (
    id               INTEGER PRIMARY KEY,
    raw_document_id  INTEGER NOT NULL REFERENCES raw_documents(id),
    speaker          TEXT NOT NULL,
    ticker           TEXT NOT NULL,
    direction        TEXT NOT NULL CHECK (direction IN ('long', 'short', 'neutral')),
    called_at        TEXT NOT NULL,                    -- YYYY-MM-DD the video was published
    price_at_call    REAL CHECK (price_at_call IS NULL OR price_at_call > 0),
    timeframe_days   INTEGER CHECK (timeframe_days IS NULL OR timeframe_days > 0),
    thesis           TEXT NOT NULL,
    invalidation     TEXT,
    extracted_by     TEXT NOT NULL,                    -- model id + prompt version
    human_verified   INTEGER NOT NULL DEFAULT 0 CHECK (human_verified IN (0, 1)),
    created_at       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS call_outcomes (
    call_id        INTEGER NOT NULL REFERENCES calls(id),
    horizon_days   INTEGER NOT NULL CHECK (horizon_days IN (30, 90, 180)),
    ticker_return  REAL NOT NULL,                      -- fractional, e.g. 0.05 = +5%
    spy_return     REAL NOT NULL,
    graded_at      TEXT NOT NULL,
    PRIMARY KEY (call_id, horizon_days)
);

-- ------------------------------------------------------------- trade journal
CREATE TABLE IF NOT EXISTS trades (
    id                INTEGER PRIMARY KEY,
    ticker            TEXT NOT NULL,
    direction         TEXT NOT NULL CHECK (direction IN ('long', 'short')),
    instrument        TEXT NOT NULL CHECK (instrument IN ('stock', 'put', 'put_spread', 'call', 'call_spread')),
    date_opened       TEXT NOT NULL,
    date_closed       TEXT,
    source_tier       INTEGER NOT NULL CHECK (source_tier IN (1, 2, 3)),
    idea_source       TEXT NOT NULL,
    regime_at_entry   TEXT NOT NULL CHECK (regime_at_entry IN ('risk_on', 'choppy', 'risk_off')),
    -- fixed at entry (protected by trigger below)
    variant_view      TEXT NOT NULL CHECK (length(variant_view) > 0),
    catalyst          TEXT NOT NULL,
    invalidation      TEXT NOT NULL CHECK (length(invalidation) > 0),
    entry_price       REAL NOT NULL CHECK (entry_price > 0),
    size_pct_account  REAL NOT NULL CHECK (size_pct_account > 0 AND size_pct_account <= 100),
    stop_level        REAL NOT NULL CHECK (stop_level > 0),
    -- filled at close
    exit_price        REAL CHECK (exit_price IS NULL OR exit_price > 0),
    exit_reason       TEXT CHECK (exit_reason IS NULL OR exit_reason IN ('target', 'stop', 'thesis_broken', 'time_stop', 'other')),
    spy_return        REAL,                            -- SPY return over the same holding period
    rule_breaches     TEXT,
    post_mortem       TEXT,
    CHECK (date_closed IS NULL OR date_closed >= date_opened),
    CHECK ((date_closed IS NULL) = (exit_price IS NULL)),
    CHECK (date_closed IS NULL OR exit_reason IS NOT NULL),
    -- a stop must sit on the losing side of entry
    CHECK ((direction = 'long'  AND stop_level < entry_price) OR
           (direction = 'short' AND stop_level > entry_price))
);

-- Entry-time facts cannot change after the trade is logged.
CREATE TRIGGER IF NOT EXISTS trades_entry_fields_locked
BEFORE UPDATE OF ticker, direction, instrument, date_opened, source_tier, idea_source,
                 regime_at_entry, variant_view, catalyst, invalidation,
                 entry_price, size_pct_account, stop_level
ON trades
BEGIN SELECT RAISE(ABORT, 'entry-time trade fields are locked'); END;

-- A closed trade is final except for the review fields.
CREATE TRIGGER IF NOT EXISTS trades_closed_locked
BEFORE UPDATE OF date_closed, exit_price, exit_reason, spy_return
ON trades
WHEN OLD.date_closed IS NOT NULL
BEGIN SELECT RAISE(ABORT, 'closed trades cannot be re-closed'); END;

CREATE TRIGGER IF NOT EXISTS trades_no_delete
BEFORE DELETE ON trades
BEGIN SELECT RAISE(ABORT, 'trades cannot be deleted; void them with a post_mortem'); END;

-- ------------------------------------------------------------------ audit log
CREATE TABLE IF NOT EXISTS audit_log (
    id          INTEGER PRIMARY KEY,
    table_name  TEXT NOT NULL,
    row_id      INTEGER NOT NULL,
    action      TEXT NOT NULL,
    changed_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    detail      TEXT
);

CREATE TRIGGER IF NOT EXISTS audit_trades_insert
AFTER INSERT ON trades
BEGIN
    INSERT INTO audit_log (table_name, row_id, action, detail)
    VALUES ('trades', NEW.id, 'insert', NEW.ticker || ' ' || NEW.direction || ' ' || NEW.instrument);
END;

CREATE TRIGGER IF NOT EXISTS audit_trades_update
AFTER UPDATE ON trades
BEGIN
    INSERT INTO audit_log (table_name, row_id, action, detail)
    VALUES ('trades', NEW.id, 'update',
            'closed=' || COALESCE(NEW.date_closed, 'open') ||
            ' exit=' || COALESCE(NEW.exit_price, 'none'));
END;

CREATE TRIGGER IF NOT EXISTS audit_log_no_update
BEFORE UPDATE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;

CREATE TRIGGER IF NOT EXISTS audit_log_no_delete
BEFORE DELETE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;

-- --------------------------------------------------------------- report views
CREATE VIEW IF NOT EXISTS v_closed_trades AS
SELECT
    id, ticker, direction, instrument, source_tier, idea_source, regime_at_entry,
    date_opened, date_closed, entry_price, exit_price, size_pct_account,
    CASE direction
        WHEN 'long'  THEN (exit_price - entry_price) / entry_price
        WHEN 'short' THEN (entry_price - exit_price) / entry_price
    END AS trade_return,
    spy_return
FROM trades
WHERE date_closed IS NOT NULL;

CREATE VIEW IF NOT EXISTS v_source_hit_rate AS
SELECT
    c.speaker,
    o.horizon_days,
    COUNT(*) AS graded_calls,
    ROUND(AVG(CASE
        WHEN c.direction = 'long'  AND o.ticker_return > o.spy_return THEN 1.0
        WHEN c.direction = 'short' AND o.ticker_return < o.spy_return THEN 1.0
        ELSE 0.0 END), 3) AS beat_spy_rate
FROM calls c
JOIN call_outcomes o ON o.call_id = c.id
WHERE c.direction IN ('long', 'short')
GROUP BY c.speaker, o.horizon_days;
