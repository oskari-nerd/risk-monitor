import pandas as pd

def load_price_table(conn):
    query = "SELECT ticker, price_date, value FROM prices"
    long = pd.read_sql(query, conn)
    wide = long.pivot(index="price_date", columns="ticker", values="value")
    return wide.dropna()

