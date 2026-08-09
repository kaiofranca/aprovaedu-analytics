# AprovaEdu Analytics

Projeto de **engenharia de dados, análise exploratória, modelagem preditiva e dashboard BI** para o cursinho pré-vestibular **AprovaEdu**, cobrindo dados operacionais e pedagógicos de 2021 a 2025.

---

## Estrutura do Projeto

```text
aprovaedu-analytics/
├── README.md                   # Documentação principal do projeto
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Containerização da aplicação
├── .dockerignore               # Arquivos excluídos da imagem Docker
├── .gitignore                  # Arquivos ignorados pelo Git
├── main.py                     # Script principal (executa ETL + treinamento do modelo)
├── data/
│   ├── raw/                    # CSVs originais (9 tabelas brutas)
│   └── processed/              # CSVs tratados + Banco SQLite (aprovaedu.db)
├── src/
│   ├── etl.py                  # Pipeline de ETL (limpeza e padronização)
│   ├── database.py             # Conexão e persistência no SQLite
│   ├── features.py             # Engenharia de atributos (Feature Engineering)
│   └── model.py                # Treinamento e avaliação do modelo Random Forest
├── notebooks/
│   ├── exploracao.ipynb        # Análise Exploratória de Dados
│   ├── analises.ipynb          # Análises obrigatórias e extras
│   └── modelo_preditivo.ipynb  # Treinamento, avaliação e gráficos do modelo de ML
├── dashboard/
│   └── app.py                  # Dashboard BI interativo (Streamlit + Plotly)
├── models/
│   └── modelo.pkl              # Modelo treinado serializado (gerado pelo main.py)
├── reports/
│   ├── relatorio_final.md      # Relatório executivo e técnico consolidado
│   └── figures/                # Gráficos gerados pelos notebooks (.png)
└── docs/
    ├── decisoes_tecnicas.md    # Registro de decisões arquiteturais e técnicas
    └── uso_ia.md               # Transparência sobre o uso de IA no projeto
```

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Função no Projeto |
|---|---|---|
| **Python** | 3.10+ | Linguagem principal |
| **Pandas** | ≥ 2.0 | Manipulação e transformação de dados |
| **NumPy** | ≥ 1.24 | Operações numéricas |
| **SQLite 3** | Nativo | Banco de dados relacional embarcado |
| **Scikit-Learn** | ≥ 1.3 | Algoritmos de Machine Learning (Random Forest) |
| **Joblib** | ≥ 1.3 | Serialização de modelos treinados |
| **Streamlit** | ≥ 1.28 | Dashboard BI interativo |
| **Plotly** | ≥ 5.17 | Gráficos dinâmicos no dashboard |
| **Matplotlib** | ≥ 3.7 | Gráficos estáticos para o relatório |
| **Seaborn** | ≥ 0.12 | Visualizações estatísticas nos notebooks |
| **Docker** | — | Containerização da aplicação |

---

## Como Executar

### Opção 1: Execução Local

```bash
# 1. Clonar o repositório
git clone https://github.com/kaiofranca/aprovaedu-analytics.git
cd aprovaedu-analytics

# 2. Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar o pipeline completo (ETL + Modelo)
python3 main.py

# 5. Iniciar o Dashboard
streamlit run dashboard/app.py
```

Acesse o dashboard em **http://localhost:8501**.

### Opção 2: Execução via Docker

```bash
# 1. Construir a imagem (inclui ETL + treinamento do modelo)
docker build -t aprovaedu-analytics .

# 2. Rodar o container
docker run -p 8501:8501 aprovaedu-analytics
```

Acesse o dashboard em **http://localhost:8501**.

---

## Funcionalidades do Dashboard

O painel BI está organizado em **4 abas interativas**:

| Aba | Conteúdo |
|---|---|
| **Visão Geral** | KPIs principais (alunos, aprovados, taxa), distribuição por escola e canal |
| **Desempenho Acadêmico** | Evolução da aprovação por ano, notas por matéria, top cursos |
| **Frequência e Engajamento** | Presença vs aprovação, eficiência dos canais, impacto da escola |
| **Simulador Preditivo** | Simulador interativo com o modelo Random Forest (ativado por botão) |

---

## Documentação Complementar

- **[Relatório Final Executivo](reports/relatorio_final.md)**: Síntese completa das análises obrigatórias, extras e do modelo preditivo.
- **[Decisões Técnicas](docs/decisoes_tecnicas.md)**: Registro formal de todas as decisões arquiteturais e de modelagem.
- **[Transparência sobre o Uso de IA](docs/uso_ia.md)**: Declaração sobre como ferramentas de IA foram utilizadas no projeto.
