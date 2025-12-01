from dataclasses import dataclass

@dataclass(frozen=True)
class Security:
    ticker: str
    company: str
    sector: str | None = None
    industry: str | None = None
    isin: str | None = None
    listing_date: str | None = None
