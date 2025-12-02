from __future__ import annotations

from datetime import datetime, date
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from ...core.config import settings


class NgxDisclosurePlaywrightProvider:
    """
    Uses Playwright (real browser) to load the NGX corporate disclosures page
    so we can see JS-rendered tables.
    """

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or settings.NGX_CORP_DISCLOSURES_URL

    def fetch_page(self) -> pd.DataFrame:
        """Load page via Chromium, parse disclosures table into a DataFrame."""
        html = self._fetch_html_via_browser()
        soup = BeautifulSoup(html, "lxml")

        tables = soup.find_all("table")
        if not tables:
            print("Debug: no <table> tags found in rendered HTML.")
            return pd.DataFrame()

        # Find the table whose headers look like "Company | Disclosures | Date Submitted"
        disclosures_table = None
        for t in tables:
            header_row = t.find("tr")
            if not header_row:
                continue

            header_cells = [
                th.get_text(strip=True).lower()
                for th in header_row.find_all(["th", "td"])
            ]
            if not header_cells:
                continue

            has_company = any("company" in h or "issuer" in h for h in header_cells)
            has_disclosures = any("disclosure" in h or "headline" in h or "subject" in h for h in header_cells)
            has_date = any("date" in h for h in header_cells)

            if has_company and (has_disclosures or has_date):
                disclosures_table = t
                break

        if disclosures_table is None:
            print("Debug: could not find disclosures table based on headers.")
            return pd.DataFrame()

        rows = disclosures_table.find_all("tr")
        if len(rows) <= 1:
            print("Debug: disclosures table has no data rows.")
            return pd.DataFrame()

        header_cells = [
            th.get_text(strip=True).lower()
            for th in rows[0].find_all(["th", "td"])
        ]

        def find_idx(candidates: list[str]) -> Optional[int]:
            for cand in candidates:
                for idx, name in enumerate(header_cells):
                    if cand in name:
                        return idx
            return None

        issuer_idx = find_idx(["issuer", "company", "security"])
        title_idx = find_idx(["disclosure", "title", "headline", "subject", "description"])
        date_idx = find_idx(["date", "submitted", "released"])
        type_idx = find_idx(["category", "type", "segment", "classification"])

        data = []
        for row in rows[1:]:
            cells = row.find_all("td")
            if not cells:
                continue

            def safe_get(idx: Optional[int]) -> str:
                if idx is None or idx >= len(cells):
                    return ""
                return cells[idx].get_text(strip=True)

            company_name = safe_get(issuer_idx)
            title = safe_get(title_idx)
            disclosure_type = safe_get(type_idx) or None
            date_text = safe_get(date_idx)
            disclosure_date = self._parse_date(date_text)

            link = row.find("a", href=True)
            source_url = urljoin(self.base_url, link["href"]) if link else None

            pdf_url = None
            if source_url and source_url.lower().endswith(".pdf"):
                pdf_url = source_url

            data.append(
                {
                    "company_name": company_name or None,
                    "symbol": None,  # we'll map later
                    "disclosure_title": title or None,
                    "disclosure_type": disclosure_type,
                    "disclosure_date": disclosure_date,
                    "source_url": source_url,
                    "pdf_url": pdf_url,
                    "local_pdf_path": None,
                }
            )

        df = pd.DataFrame(data)
        df = df[df["disclosure_title"].notna()]  # keep only real rows
        print(f"Debug: parsed {len(df)} disclosure rows from rendered HTML.")
        return df.reset_index(drop=True)

    def _fetch_html_via_browser(self) -> str:
        """Use Playwright Chromium to render the page and return HTML."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.base_url, wait_until="networkidle")
            html = page.content()
            browser.close()
        return html

    @staticmethod
    def _parse_date(text: str) -> Optional[date]:
        if not text:
            return None
        text = text.strip()
        formats = [
            "%d-%b-%Y",
            "%d %b %Y",
            "%b %d, %Y",
            "%Y-%m-%d",
            "%d/%m/%Y",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue
        return None
