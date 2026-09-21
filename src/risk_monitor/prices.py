import yfinance as yf
from datetime import date, timedelta

INITIAL_WINDOW_DAYS = 730  # two years: 250-day backtest window on top of a 250-day VaR lookback (Layer 5)
OVERLAP_DAYS = 14  # re-fetch days already saved, so a healthy ticker never returns empty; longer than any holiday gap

def fetch_history(ticker, start_date, end_date):
    history = yf.Ticker(ticker).history(
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=True,
    )
    return history

def store_history(conn, ticker, history):
    for timestamp, row in history.iterrows():
        price_date = timestamp.date().isoformat()
        close = row["Close"]

        conn.execute(
            """INSERT INTO prices (ticker, price_date, value)
            VALUES (?, ?, ?)
            ON CONFLICT (ticker, price_date) DO NOTHING""",
            (ticker, price_date, close)
        )
    conn.commit()

def load_prices(conn):
    missing = []
    for (ticker,) in conn.execute("SELECT ticker FROM instruments"):
        latest = conn.execute(
            "SELECT MAX(price_date) FROM prices WHERE ticker = ?",
            (ticker,),
        ).fetchone()[0]

        if latest is None:
            start_date = date.today() - timedelta(days=INITIAL_WINDOW_DAYS)
        else:
            start_date = date.fromisoformat(latest) - timedelta(days=OVERLAP_DAYS)

        end_date = date.today() + timedelta(days=1)
        history = fetch_history(ticker, start_date, end_date)
        if history.empty:
            missing.append(ticker)
            continue
        store_history(conn, ticker, history)
    if missing:
        print("No data returned for", missing)
    return missing