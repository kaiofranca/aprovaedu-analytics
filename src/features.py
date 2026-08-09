"""
Módulo de Engenharia de Atributos (Feature Engineering).
"""

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "aprovaedu.db"


def create_features() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)

    # 1. Presença em aulas (% de aulas com status Presente ou Atrasado)
    df_presenca = pd.read_sql_query("""
        SELECT aluno_id,
               ROUND(
                   SUM(CASE WHEN status_presenca IN ('Presente', 'Atrasado') THEN 1.0 ELSE 0.0 END)
                   / COUNT(*) * 100, 2
               ) as pct_presenca
        FROM presencas_aulas
        GROUP BY aluno_id
    """, conn)

    # 2. Desempenho em simulados (apenas finalizados)
    df_simulados = pd.read_sql_query("""
        SELECT aluno_id,
               AVG(CASE WHEN status_realizacao = 'Finalizado' THEN nota ELSE NULL END) as media_nota_simulados,
               SUM(CASE WHEN status_realizacao = 'Finalizado' THEN 1 ELSE 0 END) as simulados_finalizados
        FROM resultados_simulados
        GROUP BY aluno_id
    """, conn)

    # 3. Matrículas (persistência, bolsa e nota diagnóstico)
    df_matriculas = pd.read_sql_query("""
        SELECT aluno_id,
               COUNT(*) as total_matriculas,
               SUM(CASE WHEN status_matricula = 'Concluída' THEN 1 ELSE 0 END) as matriculas_concluidas,
               AVG(bolsa_percentual) as media_bolsa,
               AVG(nota_diagnostico) as nota_diagnostico
        FROM matriculas
        GROUP BY aluno_id
    """, conn)

    # 4. Dados cadastrais do estudante (categóricos)
    df_estudantes = pd.read_sql_query("""
        SELECT aluno_id, escola_origem, canal_captacao
        FROM estudantes
    """, conn)

    # 5. Target: aprovado ou não no vestibular
    df_aprovados = pd.read_sql_query("""
        SELECT DISTINCT aluno_id, 1 as aprovado
        FROM aprovacoes_vestibular
    """, conn)

    conn.close()

    # Juntar tudo pela chave aluno_id
    df = df_estudantes.copy()
    df = df.merge(df_presenca, on="aluno_id", how="left")
    df = df.merge(df_simulados, on="aluno_id", how="left")
    df = df.merge(df_matriculas, on="aluno_id", how="left")
    df = df.merge(df_aprovados, on="aluno_id", how="left")

    # Preencher aprovado = 0 para quem não tem registro
    df["aprovado"] = df["aprovado"].fillna(0).astype(int)

    # Preencher nulls numéricos com 0
    numeric_cols = [
        "pct_presenca", "media_nota_simulados", "simulados_finalizados",
        "total_matriculas", "matriculas_concluidas", "media_bolsa", "nota_diagnostico"
    ]
    df[numeric_cols] = df[numeric_cols].fillna(0)

    return df


def prepare_model_data(df: pd.DataFrame):
    # Separar target
    y = df["aprovado"]

    # Selecionar features
    feature_cols = [
        "pct_presenca", "media_nota_simulados", "simulados_finalizados",
        "total_matriculas", "matriculas_concluidas", "media_bolsa",
        "nota_diagnostico", "escola_origem", "canal_captacao"
    ]
    X = df[feature_cols].copy()

    # One-hot encoding para categóricas
    X = pd.get_dummies(X, columns=["escola_origem", "canal_captacao"], drop_first=True)

    return X, y
