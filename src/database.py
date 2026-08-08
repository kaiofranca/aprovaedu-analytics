from pathlib import Path
import sqlite3
import pandas as pd

PROCESSED_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
DB_PATH = PROCESSED_DATA_DIR / "aprovaedu.db"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def save_to_sqlite(df: pd.DataFrame, table_name: str) -> None:
    with get_connection() as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)


def query_sqlite(query: str, params: tuple = ()) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)


def list_tables() -> list[str]:
    with get_connection() as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return [row[0] for row in cursor.fetchall()]


def table_info(table_name: str) -> pd.DataFrame:
    return query_sqlite(f"PRAGMA table_info({table_name})")


def count_rows(table_name: str) -> int:
    result = query_sqlite(f"SELECT COUNT(*) as total FROM {table_name}")
    return int(result["total"].iloc[0])


if __name__ == "__main__":
    print("=== Verificação do Banco de Dados ===")
    tables = list_tables()
    if not tables:
        print("Banco vazio. Execute 'python src/etl.py' para popular.")
    else:
        for t in tables:
            print(f"  {t}: {count_rows(t)} linhas")
