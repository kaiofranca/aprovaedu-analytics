"""
Módulo de Treinamento e Avaliação do Modelo Preditivo.
"""

from pathlib import Path
import joblib
import pandas as pd

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"


def train_model(X: pd.DataFrame, y: pd.Series):
    """Treina o modelo de machine learning."""
    pass


def save_model(model, filename: str = "modelo.pkl") -> Path:
    """Salva o modelo treinado em disco."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_DIR / filename
    joblib.dump(model, model_path)
    return model_path


def load_model(filename: str = "modelo.pkl"):
    """Carrega o modelo salvo em disco."""
    model_path = MODELS_DIR / filename
    return joblib.load(model_path)
