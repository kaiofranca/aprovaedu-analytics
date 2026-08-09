"""
Dashboard Streamlit - AprovaEdu Analytics
"""

import sys
from pathlib import Path

# Adicionar src/ ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import joblib
import numpy as np

# --- Configuração da Página ---
st.set_page_config(
    page_title="AprovaEdu Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Conexão com o Banco ---
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "aprovaedu.db"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "modelo.pkl"


@st.cache_data
def query(sql):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(sql, conn)


# --- Cabeçalho ---
st.markdown(
    "<h1 style='text-align: center;'>AprovaEdu Analytics</h1>"
    "<p style='text-align: center; color: gray;'>Painel de inteligência de negócios de cursinho pré-vestibular</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- Abas ---
aba1, aba2, aba3, aba4 = st.tabs([
    "Visão Geral",
    "Desempenho Acadêmico",
    "Frequência e Engajamento",
    "Simulador Preditivo",
])


# ABA 1 — VISÃO GERAL (KPIs)
with aba1:
    total_alunos = query("SELECT COUNT(DISTINCT aluno_id) as n FROM estudantes").iloc[0, 0]
    total_aprovados = query("SELECT COUNT(DISTINCT aluno_id) as n FROM aprovacoes_vestibular").iloc[0, 0]
    taxa_global = round(total_aprovados / total_alunos * 100, 1)
    total_materias = query("SELECT COUNT(DISTINCT materia) as n FROM simulados").iloc[0, 0]
    total_professores = query("SELECT COUNT(DISTINCT professor_id) as n FROM professores").iloc[0, 0]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total de alunos", f"{total_alunos}")
    c2.metric("Aprovados", f"{total_aprovados}")
    c3.metric("Taxa de aprovação", f"{taxa_global}%")
    c4.metric("Disciplinas", f"{total_materias}")
    c5.metric("Professores", f"{total_professores}")

    st.markdown("---")

    col_esq, col_dir = st.columns(2)

    with col_esq:
        df_escola = query("""
            SELECT escola_origem, COUNT(DISTINCT aluno_id) as total
            FROM estudantes
            WHERE escola_origem != 'Não Informado'
            GROUP BY escola_origem
            ORDER BY total DESC
        """)
        fig_escola = px.bar(
            df_escola, x="escola_origem", y="total",
            color="escola_origem",
            title="Distribuição de alunos por escola de origem",
            labels={"escola_origem": "Escola de origem", "total": "Quantidade de alunos"},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_escola.update_layout(showlegend=False)
        st.plotly_chart(fig_escola, use_container_width=True)

    with col_dir:
        df_canal = query("""
            SELECT canal_captacao, COUNT(DISTINCT aluno_id) as total
            FROM estudantes
            WHERE canal_captacao != 'Não Informado'
            GROUP BY canal_captacao
            ORDER BY total DESC
        """)
        fig_canal = px.bar(
            df_canal, x="canal_captacao", y="total",
            color="canal_captacao",
            title="Distribuição de alunos por canal de captação",
            labels={"canal_captacao": "Canal de captação", "total": "Quantidade de alunos"},
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_canal.update_layout(showlegend=False)
        st.plotly_chart(fig_canal, use_container_width=True)


# ABA 2 — DESEMPENHO ACADÊMICO
with aba2:
    # Evolução da taxa de aprovação por ano
    df_mat_ano = query("SELECT ano, COUNT(DISTINCT aluno_id) as matriculados FROM matriculas GROUP BY ano")
    df_apr_ano = query("SELECT ano_vestibular as ano, COUNT(DISTINCT aluno_id) as aprovados FROM aprovacoes_vestibular GROUP BY ano_vestibular")
    df_evolucao = df_mat_ano.merge(df_apr_ano, on="ano", how="left").fillna(0)
    df_evolucao["taxa"] = (df_evolucao["aprovados"] / df_evolucao["matriculados"] * 100).round(1)

    fig_evolucao = go.Figure()
    fig_evolucao.add_trace(go.Bar(
        x=df_evolucao["ano"], y=df_evolucao["aprovados"],
        name="Aprovados", marker_color="#4C72B0", opacity=0.7,
    ))
    fig_evolucao.add_trace(go.Scatter(
        x=df_evolucao["ano"], y=df_evolucao["taxa"],
        name="Taxa de aprovação (%)", yaxis="y2",
        mode="lines+markers+text", text=[f"{v}%" for v in df_evolucao["taxa"]],
        textposition="top center", line=dict(color="#C44E52", width=3),
    ))
    fig_evolucao.update_layout(
        title="Evolução da taxa de aprovação por ano (2021–2025)",
        yaxis=dict(title="Aprovados (absoluto)"),
        yaxis2=dict(title="Taxa (%)", overlaying="y", side="right", range=[20, 45]),
        legend=dict(orientation="h", y=-0.15),
    )
    st.plotly_chart(fig_evolucao, use_container_width=True)

    st.markdown("---")

    col_mat, col_cursos = st.columns(2)

    with col_mat:
        df_mat = query("""
            SELECT s.materia, ROUND(AVG(r.nota), 2) as media_nota
            FROM resultados_simulados r
            JOIN simulados s ON r.simulado_id = s.simulado_id
            WHERE r.status_realizacao = 'Finalizado' AND s.materia != 'Redação'
            GROUP BY s.materia
            ORDER BY media_nota ASC
        """)
        fig_mat = px.bar(
            df_mat, x="media_nota", y="materia", orientation="h",
            title="Nota média nos simulados por matéria (escala 0–100)",
            labels={"media_nota": "Nota média", "materia": "Matéria"},
            color_discrete_sequence=["#4C72B0"],
            text="media_nota",
        )
        fig_mat.update_layout(xaxis_range=[55, 65])
        fig_mat.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig_mat, use_container_width=True)

    with col_cursos:
        df_cursos = query("""
            SELECT curso_aprovado, COUNT(*) as total
            FROM aprovacoes_vestibular
            GROUP BY curso_aprovado
            ORDER BY total DESC
            LIMIT 10
        """)
        df_cursos = df_cursos.sort_values("total", ascending=True)
        fig_cursos = px.bar(
            df_cursos, x="total", y="curso_aprovado", orientation="h",
            title="Top 10 cursos universitários com mais aprovados",
            labels={"total": "Aprovações", "curso_aprovado": "Curso"},
            color_discrete_sequence=["#55A868"],
            text="total",
        )
        fig_cursos.update_traces(textposition="outside")
        st.plotly_chart(fig_cursos, use_container_width=True)

# ABA 3 — FREQUÊNCIA E ENGAJAMENTO
with aba3:
    # Box plot: presença por status de aprovação
    df_pres = query("""
        SELECT aluno_id,
               ROUND(SUM(CASE WHEN status_presenca IN ('Presente', 'Atrasado') THEN 1.0 ELSE 0.0 END)
               / COUNT(*) * 100, 2) as pct_presenca
        FROM presencas_aulas
        GROUP BY aluno_id
    """)
    df_aprov_ids = query("SELECT DISTINCT aluno_id, 1 as aprovado FROM aprovacoes_vestibular")
    df_pres = df_pres.merge(df_aprov_ids, on="aluno_id", how="left")
    df_pres["aprovado"] = df_pres["aprovado"].fillna(0).astype(int)
    df_pres["Status"] = df_pres["aprovado"].map({1: "Aprovado", 0: "Não aprovado"})

    fig_box = px.box(
        df_pres, x="Status", y="pct_presenca", color="Status",
        title="Distribuição da taxa de presença por status de aprovação",
        labels={"pct_presenca": "Taxa de presença (%)", "Status": ""},
        color_discrete_map={"Aprovado": "#55A868", "Não aprovado": "#C44E52"},
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    col_canal, col_escola = st.columns(2)

    with col_canal:
        df_canal_apr = query("""
            SELECT e.canal_captacao,
                   COUNT(DISTINCT e.aluno_id) as total,
                   COUNT(DISTINCT a.aluno_id) as aprovados
            FROM estudantes e
            LEFT JOIN aprovacoes_vestibular a ON e.aluno_id = a.aluno_id
            WHERE e.canal_captacao != 'Não Informado'
            GROUP BY e.canal_captacao
        """)
        df_canal_apr["taxa"] = (df_canal_apr["aprovados"] / df_canal_apr["total"] * 100).round(2)
        df_canal_apr = df_canal_apr.sort_values("taxa", ascending=True)

        fig_canal_apr = px.bar(
            df_canal_apr, x="taxa", y="canal_captacao", orientation="h",
            title="Taxa de aprovação por canal de captação (%)",
            labels={"taxa": "Taxa de aprovação (%)", "canal_captacao": "Canal"},
            color_discrete_sequence=["#55A868"],
            text="taxa",
        )
        fig_canal_apr.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig_canal_apr.update_layout(xaxis_range=[20, 50])
        st.plotly_chart(fig_canal_apr, use_container_width=True)

    with col_escola:
        df_escola_apr = query("""
            SELECT e.escola_origem,
                   COUNT(DISTINCT e.aluno_id) as total,
                   COUNT(DISTINCT a.aluno_id) as aprovados
            FROM estudantes e
            LEFT JOIN aprovacoes_vestibular a ON e.aluno_id = a.aluno_id
            WHERE e.escola_origem != 'Não Informado'
            GROUP BY e.escola_origem
        """)
        df_escola_apr["taxa"] = (df_escola_apr["aprovados"] / df_escola_apr["total"] * 100).round(2)

        fig_escola_apr = px.bar(
            df_escola_apr, x="escola_origem", y="taxa",
            title="Taxa de aprovação por escola de origem (%)",
            labels={"taxa": "Taxa de aprovação (%)", "escola_origem": "Escola de origem"},
            color_discrete_sequence=["#4C72B0"],
            text="taxa",
        )
        fig_escola_apr.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig_escola_apr.update_layout(yaxis_range=[20, 50])
        st.plotly_chart(fig_escola_apr, use_container_width=True)


# ABA 4 — SIMULADOR PREDITIVO
with aba4:
    st.markdown(
        "### Simulador de aprovação no vestibular\n"
        "Este simulador utiliza o modelo **Random Forest** treinado com dados reais "
        "de **812 alunos** para estimar a probabilidade de aprovação com base "
        "nos indicadores acadêmicos e comportamentais do aluno."
    )

    if st.button("Ativar simulador preditivo", type="primary", use_container_width=True):
        st.session_state["simulador_ativo"] = True

    if st.session_state.get("simulador_ativo", False):
        st.markdown("---")
        st.markdown("#### Preencha os indicadores do aluno:")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            presenca = st.slider("Presença em aulas (%)", 0.0, 100.0, 84.0, 0.5)
            nota_sim = st.slider("Nota média nos simulados", 0.0, 100.0, 62.0, 0.5)
            nota_diag = st.slider("Nota diagnóstico (entrada)", 0.0, 100.0, 57.0, 0.5)

        with col_b:
            sim_finalizados = st.slider("Simulados finalizados", 0, 70, 20)
            total_mat = st.slider("Total de matrículas", 0, 35, 10)
            mat_concluidas = st.slider("Matrículas concluídas", 0, 25, 7)

        with col_c:
            bolsa = st.slider("Percentual de bolsa (%)", 0.0, 100.0, 15.0, 0.5)
            escola = st.selectbox("Escola de origem", ["Federal", "Privada", "Pública", "Não Informado"])
            canal = st.selectbox("Canal de captação", ["Feira Escolar", "Google", "Indicação", "Instagram", "Não Informado", "Whatsapp"])

        # Montar DataFrame com one-hot encoding idêntico ao treinamento
        input_data = {
            "pct_presenca": presenca,
            "media_nota_simulados": nota_sim,
            "simulados_finalizados": sim_finalizados,
            "total_matriculas": total_mat,
            "matriculas_concluidas": mat_concluidas,
            "media_bolsa": bolsa,
            "nota_diagnostico": nota_diag,
            "escola_origem_Não Informado": escola == "Não Informado",
            "escola_origem_Privada": escola == "Privada",
            "escola_origem_Pública": escola == "Pública",
            "canal_captacao_Google": canal == "Google",
            "canal_captacao_Indicação": canal == "Indicação",
            "canal_captacao_Instagram": canal == "Instagram",
            "canal_captacao_Não Informado": canal == "Não Informado",
            "canal_captacao_Whatsapp": canal == "Whatsapp",
        }

        X_input = pd.DataFrame([input_data])

        if st.button("Calcular previsão", use_container_width=True):
            try:
                model = joblib.load(MODEL_PATH)
                prob = model.predict_proba(X_input)[0][1]
                pred = model.predict(X_input)[0]

                st.markdown("---")
                st.markdown("### Resultado da previsão")

                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.metric(
                        "Probabilidade de aprovação",
                        f"{prob:.1%}",
                    )
                with col_res2:
                    if pred == 1:
                        st.success("Previsão: **APROVADO**")
                    else:
                        st.warning("Previsão: **NÃO APROVADO**")

                st.progress(prob)

            except FileNotFoundError:
                st.error("Modelo não encontrado. Execute `python main.py` antes de usar o simulador.")
