Here’s a README you can drop straight into `README.md` and tweak as you evolve the project:

---

# MetaQuant NGX

MetaQuant NGX is a research-grade data platform for **Nigerian equities**.

It’s designed to:

* Ingest raw NGX market data (daily price lists, later intraday / order book, corporate disclosures).
* Store it in a **local DuckDB database**.
* Expose clean, queryable tables for **quant research and ML**.

Right now, the codebase has a **working daily EOD (end-of-day) ingestion pipeline**.
The rest (corporate actions, intraday, ML, etc.) will plug into the same structure.

---

## 1. Tech stack

* **Language**: Python (3.10+)
* **Package management**: `pip` + `venv`
* **Database**: [DuckDB](https://duckdb.org/) (local file: `metaquant_ngx.duckdb`)
* **Config**: `pydantic-settings` (Pydantic v2)
* **Data tools**: `pandas`, `numpy`
* **Scraping & parsing (for later)**: `requests`, `beautifulsoup4`, `lxml`, `openpyxl`, `playwright` (already in requirements, even if not fully used yet)

---

## 2. Project layout

Current tree (simplified to the important bits):

```text
metaquant_ngx/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ metaquant_ngx.duckdb        # created automatically after first run
├─ data/
│   └─ raw/
│       └─ ngx_eod/            # raw NGX daily price files (CSV/XLSX)
└─ src/
    ├─ scripts/
    │   └─ ingest_ngx_eod.py   # CLI script to ingest daily NGX EOD file
    └─ metaquant_ngx/
        ├─ __init__.py
        ├─ core/
        │   ├─ __init__.py
        │   └─ config.py       # global settings (paths, etc.)
        └─ data/
            ├─ __init__.py
            ├─ connection/
            │   ├─ __init__.py
            │   └─ duckdb_connection.py
            ├─ repositories/
            │   ├─ __init__.py
            │   ├─ price_repository.py
            │   └─ security_repository.py
            └─ providers/
                ├─ __init__.py
                └─ ngx_eod_provider.py
```

Future planned directories (not fully implemented yet, but reserved):

* `src/metaquant_ngx/etl/` – pipelines that glue providers + repositories.
* `src/metaquant_ngx/features/` – factor & feature engineering.
* `src/metaquant_ngx/ml/` – ML datasets & models.
* `src/metaquant_ngx/backtest/` – backtesting engines.
* `src/metaquant_ngx/ui/` – dashboards & visual tools.

---

## 3. Layered architecture (how it all fits)

The codebase is layered so each part has a clear responsibility:

1. **core** – global configuration & shared utilities
2. **data/connection** – how to connect to DuckDB
3. **data/repositories** – how to read/write from/to database tables
4. **data/providers** – how to turn external/raw files into normalized DataFrames
5. **scripts** – CLI entrypoints that orchestrate a small pipeline:
   `provider → repository → database`

For EOD prices, the flow is:

```text
CSV/XLSX file (NGX daily price list)
    ↓
NgxEodProvider (normalize columns, add trading_date)
    ↓
PriceRepository (create eod_prices table if needed & insert rows)
    ↓
DuckDB file (metaquant_ngx.duckdb)
```

---

## 4. Core module

### 4.1 `core/config.py`

This defines a `Settings` class which loads configuration from environment variables (via `.env`) using `pydantic-settings`.

```python
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
```

Usage:

```python
from metaquant_ngx.core import settings

print(settings.DUCKDB_PATH)
```

You get a single source of truth for paths and global options.

### 4.2 `.env.example`

Template for your actual `.env`:

```env
# copy this to .env and tweak as needed
DUCKDB_PATH=metaquant_ngx.duckdb
NGX_EOD_DATA_DIR=data/raw/ngx_eod
```

---

## 5. Database connection layer

### 5.1 `data/connection/duckdb_connection.py`

Central helper to open/close DuckDB connections safely.

```python
from contextlib import contextmanager
import duckdb
from ...core.config import settings


@contextmanager
def get_connection(db_path: str | None = None):
    """
    Context manager that yields a DuckDB connection and closes it afterwards.
    """
    path = db_path or settings.DUCKDB_PATH
    con = duckdb.connect(path)
    try:
        yield con
    finally:
        con.close()
```

Usage:

```python
from metaquant_ngx.data.connection import get_connection

with get_connection() as con:
    df = con.execute("SELECT 1").df()
```

Everything else (repositories) builds on top of this.

---

## 6. Repositories (DB access layer)

Repositories are responsible for:

* Creating tables if they don’t exist.
* Inserting/upserting bulk data from pandas.
* Querying the database and returning pandas DataFrames.

### 6.1 `PriceRepository` – daily OHLCV data

File: `src/metaquant_ngx/data/repositories/price_repository.py`

Tables:

* **`eod_prices`** – one row per security per trading day.

Schema (DuckDB):

```sql
CREATE TABLE IF NOT EXISTS eod_prices (
    date DATE,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    volume BIGINT,
    symbol TEXT
);
```

Key methods:

```python
class PriceRepository:
    def __init__(self, db_path: str | None = None) -> None:
        # ensures eod_prices table exists
        ...

    def upsert(self, df: pd.DataFrame) -> None:
        """
        Insert a batch of daily OHLCV rows.
        
        Expects columns (case-insensitive):
        - date
        - open, high, low, close
        - volume
        - symbol
        """

    def fetch(self, symbols, start=None, end=None) -> pd.DataFrame:
        """
        Fetch OHLCV data for a list of symbols and optional date range.
        """
```

The `upsert` method normalizes column names to lowercase, checks for required columns, and then inserts via DuckDB’s in-memory table registration.

Example usage:

```python
from metaquant_ngx.data.repositories import PriceRepository

repo = PriceRepository()
df = repo.fetch(symbols=["MTNN", "ZENITHBANK"])
print(df.head())
```

### 6.2 `SecurityRepository` – securities master

File: `src/metaquant_ngx/data/repositories/security_repository.py`

Tables:

* **`securities`** – basic metadata for each ticker.

Schema:

```sql
CREATE TABLE IF NOT EXISTS securities (
    ticker TEXT PRIMARY KEY,
    company TEXT,
    sector TEXT,
    industry TEXT
);
```

Key methods:

```python
class SecurityRepository:
    def upsert(self, df: pd.DataFrame) -> None:
        """
        Insert or replace securities metadata.

        Required columns:
        - ticker
        - company
        - sector
        - industry
        """

    def list_tickers(self) -> list[str]:
        """Return all ticker symbols in the securities table."""
```

The repo is ready for when you start building a full NGX universe with sector/industry mappings.

---

## 7. Providers (external/raw data → normalized DataFrames)

Providers know **how to read / parse external data sources**. They do **not** talk to the DB directly.

### 7.1 `NgxEodProvider` – daily price list loader

File: `src/metaquant_ngx/data/providers/ngx_eod_provider.py`

Responsibility:

* Read NGX daily price list files (CSV/XLSX) from disk.
* Infer which columns correspond to symbol/open/high/low/close/volume.
* Attach a trading date (either from argument or from a `Date` column).
* Return a clean DataFrame ready to be stored in `eod_prices`.

Key API:

```python
class NgxEodProvider:
    def load_file(self, path: str | Path, trading_date: date | None = None) -> pd.DataFrame:
        """
        Load a single EOD file and normalize it to:

        columns: ["date", "open", "high", "low", "close", "volume", "symbol"]
        """

    def _normalize_columns(self, raw: pd.DataFrame, trading_date) -> pd.DataFrame:
        """
        Internal: map file-specific headers to standardized column names.
        """
```

It tries to guess the correct headers using lowercase matches:

* `symbol` or `ticker` → `symbol`
* `open` → `open`
* `high` → `high`
* `low` → `low`
* `close` or `price` or `last` → `close`
* `volume` or `vol` → `volume`
* `date` (optional unless you pass `trading_date` explicitly)

It then:

* Cleans symbol formatting: `.str.strip().str.upper()`
* Ensures `volume` is integer
* Ensures there is a `date` column (from argument or from the file)

You can adapt this to match the *exact* format of NGX’s exported files once you lock in how you’re downloading them.

---

## 8. Scripts (CLI entrypoints)

Scripts are what you actually run from the terminal.

### 8.1 `scripts/ingest_ngx_eod.py`

File: `src/scripts/ingest_ngx_eod.py`

Responsibility:

* Accept a file path (CSV/XLSX) and optional trading date.
* Use `NgxEodProvider` to read & normalize the file.
* Use `PriceRepository` to insert the data into DuckDB.
* Print a simple summary.

Core logic (simplified):

```python
from metaquant_ngx.data.providers import NgxEodProvider
from metaquant_ngx.data.repositories import PriceRepository
from datetime import datetime, date


def run_ingestion(file_path: str, trading_date: str | None = None) -> None:
    provider = NgxEodProvider()
    repo = PriceRepository()

    if trading_date:
        dt = datetime.strptime(trading_date, "%Y-%m-%d").date()
    else:
        dt = date.today()

    df = provider.load_file(file_path, trading_date=dt)
    repo.upsert(df)

    print(f"Ingested {len(df)} rows into DuckDB for {dt}")
```

You run it like:

```bash
# from project root
export PYTHONPATH=src
source .venv/bin/activate

python src/scripts/ingest_ngx_eod.py data/raw/ngx_eod/test.csv
# or with explicit date
python src/scripts/ingest_ngx_eod.py data/raw/ngx_eod/test.csv --date 2025-12-01
```

After a successful run you’ll see:

```text
Ingested N rows into DuckDB for YYYY-MM-DD
```

And a file `metaquant_ngx.duckdb` will appear in the project root (if it wasn’t already there).

---

## 9. Setup & first run (step-by-step)

### 9.1 Create and activate virtual environment

```bash
cd metaquant_ngx

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
```

### 9.2 Install dependencies

```bash
pip install -r requirements.txt
```

If using Pydantic v2 (which you are), make sure `pydantic-settings` is installed (it should be in `requirements.txt`).

### 9.3 Create `.env`

Copy `.env.example` → `.env` and adjust if needed:

```bash
cp .env.example .env
```

Default values should be fine to start.

### 9.4 Prepare a test EOD file

Create `data/raw/ngx_eod/test.csv` with content like:

```csv
Symbol,Open,High,Low,Close,Volume,Date
MTNN,190.0,195.0,188.0,192.5,1234567,2025-12-01
ZENITHBANK,35.0,36.0,34.8,35.5,987654,2025-12-01
```

### 9.5 Run the ingestion script

From project root:

```bash
export PYTHONPATH=src
python src/scripts/ingest_ngx_eod.py data/raw/ngx_eod/test.csv
```

You should see:

```text
Ingested 2 rows into DuckDB for 2025-12-01
```

### 9.6 Inspect data in DuckDB

Python shell:

```python
import duckdb
con = duckdb.connect("metaquant_ngx.duckdb")
print(con.execute("SELECT * FROM eod_prices").df())
```

Or using your repository:

```python
from metaquant_ngx.data.repositories import PriceRepository

repo = PriceRepository()
df = repo.fetch(symbols=["MTNN", "ZENITHBANK"])
print(df)
```

---

## 10. Extending the codebase

This structure is intentionally modular so you can grow it into a full “MetaQuant for NGX”.

Next steps you can build on top of what’s already here:

1. **Corporate disclosures & corporate actions**

   * Add `NgxDisclosureProvider` under `data/providers/`.
   * Add `FilingsRepository` / `CorporateActionRepository` under `data/repositories/`.
   * Add `scripts/ingest_ngx_disclosures.py` to pull NGX corporate-disclosures and store metadata & PDF paths.

2. **Intraday / order book from InfoWARE / IDIA**

   * Add `IdiaProvider` under `data/providers/` to scrape or connect to the web client.
   * Add `IntradayRepository` / `OrderbookRepository` to store trades & quotes.

3. **ETL pipelines**

   * Create `src/metaquant_ngx/etl/` and move orchestration logic there.
   * Make scripts call ETL functions (like `run_eod_pipeline(date)`).

4. **Features & ML**

   * Create `src/metaquant_ngx/features/` for factors (momentum, volatility, liquidity, etc.).
   * Create `src/metaquant_ngx/ml/` for training and evaluating models on NGX data.

5. **Backtesting**

   * Build daily cross-sectional and intraday backtesting engines under `src/metaquant_ngx/backtest/`.

Each new dataset should follow the same pattern you’ve just used:

> **provider** (raw data → normalized DataFrame)
> → **repository** (DataFrame → DB table)
> → **script/ETL** ( orchestrates provider + repo )

That keeps the codebase tidy and makes it easy to plug ML and research on top.

---

You can paste this into `README.md` as-is and then evolve it as you add corporate disclosures, intraday, and ML pieces.
