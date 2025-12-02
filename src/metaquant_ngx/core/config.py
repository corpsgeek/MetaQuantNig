from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global settings for MetaQuant NGX."""

    # Path to your DuckDB file
    DUCKDB_PATH: str = "metaquant_ngx.duckdb"

    # Where raw NGX EOD files are stored (CSV/XLSX/PDF)
    NGX_EOD_DATA_DIR: str = "data/raw/ngx_eod"

    # NGX corporate disclosures page
    NGX_CORP_DISCLOSURES_URL: str = (
        "https://ngxgroup.com/exchange/data/corporate-disclosures/"
    )

    # Where to store downloaded disclosure PDFs
    NGX_DISCLOSURES_DATA_DIR: str = "data/raw/ngx_disclosures"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
