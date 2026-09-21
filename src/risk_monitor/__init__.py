from .db import connect
from .positions import load_positions
from .prices import load_prices

def main() -> None:
    conn = connect() 
    load_positions(conn)
    load_prices(conn)
    conn.close()

