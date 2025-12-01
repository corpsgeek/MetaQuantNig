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
