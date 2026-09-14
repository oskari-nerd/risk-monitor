CREATE TABLE instruments (
    ticker TEXT PRIMARY KEY,
    name   TEXT    NOT NULL,
    shares INTEGER,
    sector TEXT,
    role TEXT   NOT NULL CHECK(role in('position', 'reference'))
);

CREATE TABLE prices(
    ticker TEXT NOT NULL REFERENCES instruments(ticker),
    price_date TEXT NOT NULL,
    value REAL NOT NULL,
    fetched_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (ticker, price_date)
);