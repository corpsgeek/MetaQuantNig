from __future__ import annotations

from datetime import date
import pandas as pd

from ..connection import get_connection


class FilingsRepository:
    """
    Stores corporate filings metadata (NGX disclosures).

    Schema:
        company_name       TEXT
        symbol             TEXT
        disclosure_title   TEXT
        disclosure_type    TEXT
        disclosure_date    DATE
        source_url         TEXT   -- NGX web page / link
        pdf_url            TEXT   -- direct PDF link if available
        local_pdf_path     TEXT   -- where we saved the PDF locally
    """

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path
        with get_connection(self.db_path) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS corporate_filings (
                    company_name TEXT,
                    symbol TEXT,
                    disclosure_title TEXT,
                    disclosure_type TEXT,
                    disclosure_date DATE,
                    source_url TEXT,
                    pdf_url TEXT,
                    local_pdf_path TEXT
                )
                """
            )

    def upsert(self, df: pd.DataFrame) -> None:
        """Insert only filings whose source_url is not already in the table."""
        if df is None or df.empty:
            return

        cols = {c.lower(): c for c in df.columns}
        required = [
            "company_name",
            "symbol",
            "disclosure_title",
            "disclosure_type",
            "disclosure_date",
            "source_url",
            "pdf_url",
            "local_pdf_path",
        ]
        missing = [c for c in required if c not in cols]
        if missing:
            raise ValueError(f"Missing required columns in filings DataFrame: {missing}")

        df_norm = df.rename(columns={cols[c]: c for c in required})[required]

        with get_connection(self.db_path) as con:
            con.register("filings_df", df_norm)
            con.execute(
                """
                INSERT INTO corporate_filings
                SELECT *
                FROM filings_df
                WHERE source_url NOT IN (
                    SELECT DISTINCT source_url FROM corporate_filings
                )
                """
            )

    def fetch_latest(self, limit: int = 50) -> pd.DataFrame:
        with get_connection(self.db_path) as con:
            return con.execute(
                """
                SELECT *
                FROM corporate_filings
                ORDER BY disclosure_date DESC
                LIMIT ?
                """,
                [limit],
            ).df()

    def fetch_since(self, since: date) -> pd.DataFrame:
        with get_connection(self.db_path) as con:
            return con.execute(
                """
                SELECT *
                FROM corporate_filings
                WHERE disclosure_date >= ?
                ORDER BY disclosure_date
                """,
                [since],
            ).df()
