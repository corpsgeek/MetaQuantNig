from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from ..core import settings
from ..data.providers.ngx_disclosure_playwright_provider import (
    NgxDisclosurePlaywrightProvider as NgxDisclosureProvider,
)

from ..data.repositories import FilingsRepository


def run(since: date | None = None) -> int:
    """
    Fetch NGX corporate disclosures, optionally filter by date,
    download PDFs, and store metadata in DuckDB.

    Returns the number of filings ingested (after filtering and dedup).
    """
    provider = NgxDisclosureProvider()
    repo = FilingsRepository()

    df = provider.fetch_page()
    if df.empty:
        print("No disclosures found on page.")
        return 0

    # Filter by date if requested
    if since is not None:
        df = df[
            df["disclosure_date"].notna()
            & (df["disclosure_date"] >= since)
        ]

    if df.empty:
        print(f"No disclosures on or after {since}.")
        return 0

    # Ensure all expected columns exist
    required_cols = [
        "company_name",
        "symbol",
        "disclosure_title",
        "disclosure_type",
        "disclosure_date",
        "source_url",
        "pdf_url",
        "local_pdf_path",
    ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    # Download PDFs
    dest_dir = Path(settings.NGX_DISCLOSURES_DATA_DIR)
    local_paths: list[str | None] = []

    for _, row in df.iterrows():
        pdf_url = row.get("pdf_url")
        if pdf_url:
            local = provider.download_pdf(pdf_url, dest_dir)
            local_paths.append(str(local) if local is not None else None)
        else:
            local_paths.append(None)

    df["local_pdf_path"] = local_paths

    # Upsert into DB
    repo.upsert(df)
    print(f"Ingested/updated {len(df)} corporate filings.")
    return len(df)
