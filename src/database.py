"""
Módulo de Banco de Dados (SQLite).
"""

from pathlib import Path
import sqlite3
import pandas as pd

PROCESSED_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
DB_PATH = PROCESSED_DATA_DIR / "aprovaedu.db"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Retorna conexão com o banco SQLite."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def save_to_sqlite(df: pd.DataFrame, table_name: str) -> None:
    """Salva um DataFrame pandas no banco SQLite."""
    with get_connection() as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)


def query_sqlite(query: str) -> pd.DataFrame:
    """Executa consulta SQL no SQLite e retorna DataFrame."""
    with get_connection() as conn:
        return pd.read_sql_query(query, conn)
