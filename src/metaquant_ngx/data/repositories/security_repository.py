from __future__ import annotations

import pandas as pd
from ..connection import get_connection


class SecurityRepository:
    """Securities master table: basic metadata for each ticker."""

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path
        with get_connection(self.db_path) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS securities (
                    ticker TEXT PRIMARY KEY,
                    company TEXT,
                    sector TEXT,
                    industry TEXT
                )
                """
            )

    def upsert(self, df: pd.DataFrame) -> None:
        if df is None or df.empty:
            return

        cols = {c.lower(): c for c in df.columns}
        required = ["ticker", "company", "sector", "industry"]
        missing = [c for c in required if c not in cols]
        if missing:
            raise ValueError(
                f"Missing required columns in securities DataFrame: {missing}"
            )

        df_norm = df.rename(columns={cols[c]: c for c in required})[required]

        with get_connection(self.db_path) as con:
            con.register("sec_df", df_norm)
            con.execute(
                """
                INSERT OR REPLACE INTO securities (ticker, company, sector, industry)
                SELECT ticker, company, sector, industry FROM sec_df
                """
            )

    def list_tickers(self) -> list[str]:
        with get_connection(self.db_path) as con:
            rows = con.execute(
                "SELECT ticker FROM securities ORDER BY ticker"
            ).fetchall()
        return [r[0] for r in rows]
