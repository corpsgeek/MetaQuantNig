from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global settings for MetaQuant NGX."""

    # Path to your DuckDB file
    DUCKDB_PATH: str = "metaquant_ngx.duckdb"

    # Where raw NGX EOD files are stored (CSV/XLSX/PDF)
    NGX_EOD_DATA_DIR: str = "data/raw/ngx_eod"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
