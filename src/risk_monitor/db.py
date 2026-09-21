import sqlite3
from pathlib import Path
SCHEMA_PATH = Path(__file__).parent.parent.parent/ "schema.sql"

def connect(path="prices.db"):
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA FOREIGN_KEYS = ON")
    conn.executescript(SCHEMA_PATH.read_text())
    return conn