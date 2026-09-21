import csv
from pathlib import Path

POSITIONS_PATH = Path(__file__).parent.parent.parent / "positions.csv"

UPSERT = """ INSERT INTO INSTRUMENTS(ticker, name, shares, sector, role)
VALUES(?, ?, ?, ?, ?)
ON CONFLICT (ticker) DO UPDATE SET
    name = excluded.name,
    shares = excluded.shares,
    sector = excluded.sector,
    role = excluded.role
"""

def load_positions(conn):
    with POSITIONS_PATH.open(newline="", encoding="utf-8")as file:
        for row in csv.DictReader(file):
            shares_text = row["shares"]
            if shares_text:
                shares = int(shares_text)
            else:
                shares = None 
            values = (
                row["ticker"],
                row["name"],
                shares, 
                row["sector"],
                row["role"],
            )
            conn.execute(UPSERT, values)

    conn.commit()