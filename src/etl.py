from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


MAPA_MATERIAS = {
    "Mat.": "Matemática",
    "Matematica": "Matemática",
    "MATEMÁTICA": "Matemática",
    "Fisica": "Física",
    "FÍSICA": "Física",
    "Quimica": "Química",
    "QUÍMICA": "Química",
    "BIOLOGIA": "Biologia",
    "Historia": "História",
    "FILOSOFIA": "Filosofia",
    "SOCIOLOGIA": "Sociologia",
    "GEOGRAFIA": "Geografia",
    "Ingles": "Inglês",
    "Portugues": "Português",
    "PORTUGUÊS": "Português",
    "Redacao": "Redação",
    "REDAÇÃO": "Redação",
}

MAPA_ESCOLA = {
    "Publica": "Pública",
    "privada": "Privada",
    "Não informado": "Não Informado",
}

MAPA_MODALIDADE_VAGA = {
    "ampla concorrencia": "Ampla Concorrência",
    "Ampla concorrência": "Ampla Concorrência",
}


# Funções de padronização reutilizáveis

def padronizar_texto_title(series: pd.Series) -> pd.Series:
    return series.str.strip().str.title()


def padronizar_materia(series: pd.Series) -> pd.Series:
    s = series.str.strip()
    return s.replace(MAPA_MATERIAS)


def padronizar_data_mista(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, format="mixed", dayfirst=False)


def padronizar_datetime_mista(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, format="mixed", dayfirst=True)



# Funções de limpeza por tabela

def limpar_estudantes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cidade"] = padronizar_texto_title(df["cidade"])
    df["cidade"] = df["cidade"].replace({"Maracanau": "Maracanaú"})
    df["escola_origem"] = df["escola_origem"].str.strip().replace(MAPA_ESCOLA)
    df["canal_captacao"] = padronizar_texto_title(df["canal_captacao"])
    df["data_nascimento"] = padronizar_data_mista(df["data_nascimento"])
    df["data_cadastro"] = padronizar_data_mista(df["data_cadastro"])
    return df


def limpar_aprovacoes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Universidades
    df["universidade"] = df["universidade"].str.strip().str.upper()

    # Modalidade de vaga
    df["modalidade_vaga"] = df["modalidade_vaga"].str.strip().replace(MAPA_MODALIDADE_VAGA)
    df["modalidade_vaga"] = df["modalidade_vaga"].fillna("Não Informado")

    # Bolsa
    df["bolsa_aprovacao"] = padronizar_texto_title(df["bolsa_aprovacao"])
    df["bolsa_aprovacao"] = df["bolsa_aprovacao"].fillna("Não Informado")

    # Campus
    df["campus"] = padronizar_texto_title(df["campus"])
    df["campus"] = df["campus"].fillna("Não Informado")

    # Chamada
    df = df[df["chamada"] != "Cadastro duplicado?"].copy()
    df["chamada"] = df["chamada"].str.strip()

    # Data
    df["data_resultado"] = padronizar_data_mista(df["data_resultado"])

    return df


def limpar_matriculas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["materia_declarada"] = padronizar_materia(df["materia_declarada"])
    df["status_matricula"] = padronizar_texto_title(df["status_matricula"])
    df["status_matricula"] = df["status_matricula"].replace({"Concluida": "Concluída"})
    df["origem_captacao"] = padronizar_texto_title(df["origem_captacao"])
    df["bolsa_percentual"] = df["bolsa_percentual"].fillna(0)
    df["data_matricula"] = padronizar_data_mista(df["data_matricula"])
    return df


def limpar_ofertas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["materia"] = padronizar_materia(df["materia"])
    df["professor_nome_informado"] = padronizar_texto_title(df["professor_nome_informado"])
    df["modalidade"] = padronizar_texto_title(df["modalidade"])
    df["data_inicio"] = padronizar_data_mista(df["data_inicio"])
    df["data_fim"] = padronizar_data_mista(df["data_fim"])
    return df


def limpar_aulas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["materia"] = padronizar_materia(df["materia"])
    df["modalidade_aula"] = padronizar_texto_title(df["modalidade_aula"])
    df["tema_aula"] = df["tema_aula"].str.strip()
    df["data_aula"] = padronizar_data_mista(df["data_aula"])
    return df


def limpar_presencas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["status_presenca"] = padronizar_texto_title(df["status_presenca"])
    df["status_presenca"] = df["status_presenca"].fillna("Ausente")

    # Preencher atraso com 0 para quem estava presente
    mask_presente = df["status_presenca"].isin(["Presente", "Atrasado"])
    df.loc[mask_presente, "atraso_min"] = df.loc[mask_presente, "atraso_min"].fillna(0)

    return df


def limpar_simulados(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["materia"] = padronizar_materia(df["materia"])
    df["professor_nome_informado"] = padronizar_texto_title(df["professor_nome_informado"])
    df["dificuldade"] = padronizar_texto_title(df["dificuldade"])
    df["tipo_simulado"] = padronizar_texto_title(df["tipo_simulado"])
    df["data_simulado"] = padronizar_data_mista(df["data_simulado"])
    return df


def limpar_resultados_simulados(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["status_realizacao"] = padronizar_texto_title(df["status_realizacao"])
    df["status_realizacao"] = df["status_realizacao"].fillna("Não Informado")
    df["dispositivo"] = padronizar_texto_title(df["dispositivo"])
    df["unidade_aplicacao"] = padronizar_texto_title(df["unidade_aplicacao"])
    df["inicio_simulado"] = padronizar_datetime_mista(df["inicio_simulado"])
    return df


def _limpar_lista_materias(val):
    if pd.isna(val):
        return val
    partes = [p.strip() for p in str(val).split(";")]
    partes_limpas = [MAPA_MATERIAS.get(p, MAPA_MATERIAS.get(p.title(), p.title())) for p in partes]
    return "; ".join(partes_limpas)


def limpar_professores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["materia_principal"] = padronizar_materia(df["materia_principal"])
    df["materias_ensina"] = df["materias_ensina"].apply(_limpar_lista_materias)
    df["nome_professor"] = padronizar_texto_title(df["nome_professor"])
    df["email_professor"] = df["email_professor"].fillna("Não Informado")
    df["status_professor"] = padronizar_texto_title(df["status_professor"])
    df["observacoes"] = df["observacoes"].fillna("Sem Observações")
    df["data_contratacao"] = padronizar_data_mista(df["data_contratacao"])
    return df


# Funções de ingestão e orquestração

TABELAS = {
    "estudantes": ("estudantes.csv", limpar_estudantes),
    "matriculas": ("matriculas.csv", limpar_matriculas),
    "ofertas_curso": ("ofertas_curso.csv", limpar_ofertas),
    "aulas": ("aulas.csv", limpar_aulas),
    "presencas_aulas": ("presencas_aulas.csv", limpar_presencas),
    "simulados": ("simulados.csv", limpar_simulados),
    "resultados_simulados": ("resultados_simulados.csv", limpar_resultados_simulados),
    "professores": ("professores.csv", limpar_professores),
    "aprovacoes_vestibular": ("aprovacoes_vestibular.csv", limpar_aprovacoes),
}


def load_raw_data(file_name: str) -> pd.DataFrame:
    path = RAW_DATA_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return pd.read_csv(path, encoding="utf-8-sig")


def save_processed_data(df: pd.DataFrame, filename: str) -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / f"{filename}.csv"
    df.to_csv(output_path, index=False)
    print(f"  → CSV salvo: {output_path}")


def run_pipeline():
    from database import save_to_sqlite

    print("=" * 60)
    print("Pipeline de ETL — AprovaEdu Analytics")
    print("=" * 60)

    for table_name, (csv_file, clean_func) in TABELAS.items():
        print(f"\n[ETL] Processando: {table_name}")
        df_raw = load_raw_data(csv_file)
        print(f"  Carregado: {df_raw.shape[0]} linhas x {df_raw.shape[1]} colunas")

        df_clean = clean_func(df_raw)
        print(f"  Limpo: {df_clean.shape[0]} linhas x {df_clean.shape[1]} colunas")

        save_processed_data(df_clean, table_name)
        save_to_sqlite(df_clean, table_name)
        print(f"  → SQLite: tabela '{table_name}' gravada com sucesso")

    print("\n" + "=" * 60)
    print("Pipeline de ETL finalizado com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
