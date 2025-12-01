from __future__ import annotations

import pandas as pd
from ..connection import get_connection


class PriceRepository:
    """
    Daily OHLCV table in DuckDB.

    Expected DataFrame columns (case-insensitive, will be normalized):
    - date
    - open, high, low, close
    - volume
    - symbol  (e.g. 'MTNN')
    """

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path
        with get_connection(self.db_path) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS eod_prices (
                    date DATE,
                    open DOUBLE,
                    high DOUBLE,
                    low DOUBLE,
                    close DOUBLE,
                    volume BIGINT,
                    symbol TEXT
                )
                """
            )

    def upsert(self, df: pd.DataFrame) -> None:
        """Insert a batch of rows into eod_prices."""
        if df is None or df.empty:
            return

        # normalize columns
        cols = {c.lower(): c for c in df.columns}
        required = ["date", "open", "high", "low", "close", "volume", "symbol"]
        missing = [c for c in required if c not in cols]
        if missing:
            raise ValueError(f"Missing required columns in EOD DataFrame: {missing}")

        df_norm = df.rename(columns={cols[c]: c for c in required})[required]

        with get_connection(self.db_path) as con:
            con.register("eod_df", df_norm)
            con.execute("INSERT INTO eod_prices SELECT * FROM eod_df")

    def fetch(self, symbols, start=None, end=None) -> pd.DataFrame:
        """Fetch OHLCV for a list of symbols and optional date range."""
        if isinstance(symbols, str):
            symbols = [symbols]

        placeholders = ",".join(["?"] * len(symbols))
        query = f"""
            SELECT * FROM eod_prices
            WHERE symbol IN ({placeholders})
        """
        params = list(symbols)

        if start is not None:
            query += " AND date >= ?"
            params.append(start)
        if end is not None:
            query += " AND date <= ?"
            params.append(end)

        with get_connection(self.db_path) as con:
            return con.execute(query, params).df()
