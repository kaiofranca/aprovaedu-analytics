# AprovaEdu Analytics 📊

Projeto de engenharia de dados, análise exploratória, modelagem preditiva e dashboard para o **AprovaEdu**.

---

## 📁 Estrutura do Projeto

```text
aprovaedu-analytics/
├── README.md                   # Documentação do projeto
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Containerização da aplicação
├── data/
│   ├── raw/                    # CSVs originais (intocados)
│   └── processed/              # Base tratada (CSV/Parquet + Banco SQLite .db)
├── src/
│   ├── etl.py                  # Ingestão e limpeza de dados
│   ├── features.py             # Engenharia de atributos (Feature Engineering)
│   ├── database.py             # Schema e manipulação SQLite
│   └── model.py                 # Treino e avaliação de modelos de ML
├── notebooks/
│   ├── 01_exploracao.ipynb     # Análise Exploratória de Dados (EDA)
│   ├── 02_tratamento.ipynb     # Experimentos de limpeza e transformação
│   ├── 03_analises_obrigatorias.ipynb  # Resposta às análises obrigatórias do negócio
│   └── 04_modelo_preditivo.ipynb # Experimentos de Machine Learning
├── dashboard/
│   └── app.py                  # Aplicação em Streamlit
├── reports/
│   └── relatorio_final.md       # Relatório final executivo e técnico
└── docs/
    └── decisoes_tecnicas.md    # Registro de decisões arquiteturais e técnicas
```

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.10+
- **Manipulação de Dados**: Pandas, NumPy
- **Banco de Dados**: SQLite
- **Machine Learning**: Scikit-Learn
- **Visualização & Dashboard**: Streamlit, Plotly, Matplotlib, Seaborn
- **Containerização**: Docker

---

## 🚀 Como Executar

### 1. Execução Local

```bash
# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate   # No Windows

# Instalar dependências
pip install -r requirements.txt

# Executar Ingestão / ETL
python src/etl.py

# Executar Treinamento do Modelo
python src/model.py

# Iniciar Dashboard Streamlit
streamlit run dashboard/app.py
```

### 2. Execução via Docker

```bash
# Construir a imagem Docker
docker build -t aprovaedu-analytics .

# Executar o container (disponibiliza o Dashboard na porta 8501)
docker run -p 8501:8501 aprovaedu-analytics
```
