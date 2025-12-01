from __future__ import annotations

from pathlib import Path
from datetime import date
import pandas as pd


class NgxEodProvider:
    """
    Load NGX daily price list files (CSV/XLSX) from disk and normalize them.

    This is intentionally simple to start with; you can later extend it to:
    - Download from NGX directly
    - Parse PDFs instead of CSV/XLSX
    """

    def load_file(self, path: str | Path, trading_date: date | None = None) -> pd.DataFrame:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)

        if path.suffix.lower() in {".xlsx", ".xls"}:
            raw = pd.read_excel(path, engine="openpyxl")
        else:
            raw = pd.read_csv(path)

        df = self._normalize_columns(raw, trading_date)
        return df

    def _normalize_columns(self, raw: pd.DataFrame, trading_date) -> pd.DataFrame:
        cols_lower = {c.lower(): c for c in raw.columns}

        # Try to guess columns – adjust this once you see the actual NGX file headers
        symbol_col = cols_lower.get("symbol") or cols_lower.get("ticker")
        open_col = cols_lower.get("open")
        high_col = cols_lower.get("high")
        low_col = cols_lower.get("low")
        close_col = (
            cols_lower.get("close")
            or cols_lower.get("price")
            or cols_lower.get("last")
        )
        volume_col = cols_lower.get("volume") or cols_lower.get("vol")

        missing = [
            name
            for name, col in [
                ("symbol", symbol_col),
                ("open", open_col),
                ("high", high_col),
                ("low", low_col),
                ("close", close_col),
                ("volume", volume_col),
            ]
            if col is None
        ]
        if missing:
            raise ValueError(f"Could not infer NGX columns for: {missing}")

        df = raw[[symbol_col, open_col, high_col, low_col, close_col, volume_col]].copy()
        df.columns = ["symbol", "open", "high", "low", "close", "volume"]

        # Attach date
        if trading_date is not None:
            df["date"] = trading_date
        else:
            # If the file itself has a date column, use it; otherwise error.
            date_col = cols_lower.get("date")
            if date_col:
                df["date"] = pd.to_datetime(raw[date_col]).dt.date
            else:
                raise ValueError("No trading_date provided and no 'Date' column in file")

        # Basic cleaning
        df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
        df["volume"] = df["volume"].fillna(0).astype("int64")

        return df[["date", "open", "high", "low", "close", "volume", "symbol"]]
