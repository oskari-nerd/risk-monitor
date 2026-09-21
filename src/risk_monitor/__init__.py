from .db import connect
from .positions import load_positions

def main() -> None:
    conn = connect() 
    load_positions(conn)
    conn.close()

