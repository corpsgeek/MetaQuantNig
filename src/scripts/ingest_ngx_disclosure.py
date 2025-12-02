#!/usr/bin/env python
from __future__ import annotations


#!/usr/bin/env python
from __future__ import annotations

import sys
from pathlib import Path

# Make sure the 'src' directory is on sys.path so 'metaquant_ngx' can be imported
ROOT = Path(__file__).resolve().parents[1]  # this is .../MetaQuantNig/src
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse
from datetime import datetime, date

from metaquant_ngx.etl.ngx_disclosure_pipeline import run as run_pipeline


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{value}', expected YYYY-MM-DD"
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest NGX corporate disclosures into DuckDB"
    )
    parser.add_argument(
        "--since",
        type=parse_date,
        help="Only ingest filings on/after this date (YYYY-MM-DD). Optional.",
    )
    args = parser.parse_args()

    n = run_pipeline(since=args.since)
    print(f"Done. {n} filings processed.")


if __name__ == "__main__":
    main()
