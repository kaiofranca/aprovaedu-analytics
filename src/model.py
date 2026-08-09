"""
Módulo de Treinamento e Avaliação do Modelo Preditivo.
"""

from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"


def train_model(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=random_state,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    return model, X_test, y_test, X_train, y_train


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(y_test, y_pred, target_names=["Não Aprovado", "Aprovado"]),
    }

    return metrics


def get_feature_importance(model, feature_names: list) -> pd.DataFrame:
    importance = model.feature_importances_
    df_imp = pd.DataFrame({
        "feature": feature_names,
        "importance": importance
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    return df_imp


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
