"""
Pipeline Principal — AprovaEdu Analytics

Executa o pipeline completo do sistema com um único comando:
  1. ETL: Lê os CSVs brutos, limpa e popula o banco SQLite
  2. Modelo: Gera features, treina o Random Forest e salva o modelo em disco
"""

import sys
from pathlib import Path

# Adicionar src/ ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from etl import run_pipeline
from features import create_features, prepare_model_data
from model import train_model, save_model


def main():
    print("=" * 60)
    print("AprovaEdu Analytics — Pipeline Principal")
    print("=" * 60)

    # Etapa 1: ETL
    print("\n Etapa 1/2: Executando pipeline de ETL...")
    run_pipeline()

    # Etapa 2: Modelo Preditivo
    print("\n Etapa 2/2: Treinando modelo preditivo...")
    df = create_features()
    X, y = prepare_model_data(df)
    model, X_test, y_test, _, _ = train_model(X, y)
    model_path = save_model(model)
    print(f"  Modelo salvo em: {model_path}")

    print("\n" + "=" * 60)
    print("   Pipeline finalizado com sucesso!")
    print("   Para iniciar o dashboard, execute:")
    print("   streamlit run dashboard/app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
