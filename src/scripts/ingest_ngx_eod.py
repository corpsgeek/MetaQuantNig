#!/usr/bin/env python
from __future__ import annotations

import sys
from pathlib import Path

# ensure src/ is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from metaquant_ngx.data.providers import NgxEodProvider
from metaquant_ngx.data.repositories import PriceRepository

import argparse
from datetime import datetime, date
from pathlib import Path

from metaquant_ngx.core import config
from metaquant_ngx.data.providers import NgxEodProvider
from metaquant_ngx.data.repositories import PriceRepository


def run_ingestion(file_path: str, trading_date: str | None = None) -> None:
    provider = NgxEodProvider()
    repo = PriceRepository()

    if trading_date:
        dt = datetime.strptime(trading_date, "%Y-%m-%d").date()
    else:
        # default: derive date from filename or use today
        dt = date.today()

    df = provider.load_file(file_path, trading_date=dt)
    repo.upsert(df)

    print(f"Ingested {len(df)} rows into DuckDB for {dt}")


def main():
    parser = argparse.ArgumentParser(description="Ingest NGX daily price list into DuckDB")
    parser.add_argument("file", help="Path to NGX EOD file (CSV/XLSX)")
    parser.add_argument(
        "--date",
        help="Trading date in YYYY-MM-DD (optional if the file has a Date column)",
    )
    args = parser.parse_args()

    run_ingestion(args.file, args.date)


if __name__ == "__main__":
    main()
