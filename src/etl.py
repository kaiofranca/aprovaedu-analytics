"""
Módulo de ETL (Ingestão e Limpeza de Dados).
"""

from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def load_raw_data():
    """Carrega as bases brutas da pasta data/raw/."""
    pass


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica as regras de limpeza e tratamento nos dados brutos."""
    pass


def save_processed_data(df: pd.DataFrame, filename: str) -> None:
    """Salva a base tratada na pasta data/processed/."""
    pass


if __name__ == "__main__":
    pass
