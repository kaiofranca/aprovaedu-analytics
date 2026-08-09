# Registro de Decisões Técnicas e Arquiteturais

---

## 1. Contexto Geral e Diagnóstico da Base Bruta
A base bruta do **AprovaEdu Analytics** é composta por 9 tabelas relacionais cobrindo o período de 2021 a 2025. Embora apresente 100% de integridade referencial entre as chaves primárias e estrangeiras (`aluno_id`), foram diagnosticadas três categorias principais de inconsistências que exigem tratamento prévio:
1. **Divergências de Padronização de Texto e Categorias** (caixa alta/baixa e variações ortográficas).
2. **Formatos Mistos de Datas** (`YYYY-MM-DD`, `MM-DD-YYYY` e `DD/MM/YYYY HH:MM`).
3. **Valores Ausentes (Nulos) e Registros Suspeitos**.

---

## 2. Stack Tecnológico Escolhido

| Tecnologia | Função no Projeto | Justificativa Técnica |
|---|---|---|
| **Python 3.12** | Linguagem Principal | Linguagem padrão de mercado para engenharia de dados, analytics e machine learning. |
| **SQLite 3** | Banco de Dados Relacional | Embarcado, sem necessidade de servidores externos, nativo do Python (`sqlite3`) e com excelente performance para relatórios e dashboards. |
| **Pandas & NumPy** | Leitura e Transformação de Dados | Alta eficiência na limpeza de strings, conversão de datas mistas e agregações estatísticas. |
| **Scikit-Learn** | Algoritmos de Machine Learning | Padrão da indústria para classificação, divisão estratificada de dados e métricas de avaliação. |
| **Joblib** | Persistência do Modelo | Serialização de modelos treinados em arquivos `.pkl` compactos para rápido carregamento em produção. |
| **Matplotlib & Seaborn** | Visualizações Estáticas | Geração de figuras em alta resolução ($200$ DPI) para o relatório final (`reports/figures/`). |
| **Plotly & Streamlit** | Dashboard BI Interativo | Construção de interface web responsiva e interativa diretamente em Python para a Sprint 4. |

---

## 3. Decisões de Tratamento e Justificativas Técnicas

### 3.1. Normalização de Nomes de Matérias
- **Problema Encontrado**: A coluna de matéria apresenta mais de 28 variações de escrita para apenas 11 matérias reais (ex.: `"Mat."`, `"Matematica"`, `"MATEMÁTICA"`, `"Fisica"`, `"FÍSICA"`).
- **Tratamento Escolhido**: Mapeamento via dicionário de substituição explícito no pipeline de ETL.
- **Justificativa**: Sem a unificação das matérias, qualquer agrupamento por disciplina para avaliar o desempenho acadêmico ficaria fragmentado e geraria indicadores distorcidos.

### 3.2. Padronização de Texto em Colunas Categóricas
- **Problema Encontrado**: Inconsistências de caixa (maiúsculas/minúsculas) e acentuação em colunas como `cidade`, `escola_origem`, `universidade`, `status_presenca`, `modalidade_aula`, `status_realizacao`, `dispositivo`, `unidade_aplicacao`, `status_professor` e `bolsa_aprovacao`.
- **Tratamento Escolhido**: Aplicação de limpeza com `.str.strip().str.title()` para textos gerais e `.str.upper()` para siglas de universidades (`UECE`, `UFC`, `UFRN`, `IFCE`).
- **Justificativa**: Garante consistência em filtros e joins no banco de dados e no Dashboard Streamlit.

### 3.3. Padronização de Formato de Datas
- **Problema Encontrado**: Presença de datas em formato americano (`MM-DD-YYYY`) em `estudantes.data_cadastro` (33 linhas) e `aprovacoes_vestibular.data_resultado` (12 linhas), além do formato brasileiro (`DD/MM/YYYY HH:MM`) em `resultados_simulados.inicio_simulado` (880 linhas).
- **Tratamento Escolhido**: Conversão unificada para o padrão ISO 8601 (`YYYY-MM-DD` ou `YYYY-MM-DD HH:MM:SS`) usando `pd.to_datetime(..., format='mixed')`.
- **Justificativa**: O padrão ISO é nativamente suportado por bancos SQL (SQLite), Pandas e ferramentas de BI, evitando erros em ordenações e agrupamentos temporais.

### 3.4. Trata de Valores Ausentes (Nulos)
- **Problema Encontrado**: Presença de nulos em várias colunas (`bolsa_percentual` em matrículas, `atraso_min` e `justificativa` em presenças, `nota` e `acertos` em resultados de simulados).
- **Tratamento Escolhido**:
  - `bolsa_percentual`: Preenchimento com `0` (aluno sem bolsa).
  - `atraso_min`: Preenchimento com `0` em presenças confirmadas.
  - `justificativa` e `nota`/`acertos` de ausentes: Preservados como `null` ou preenchidos com rótulo explícito `"Não Informado"`.
- **Justificativa**: Impede distorções no cálculo de médias numéricas (evita tratar ausência em prova como nota zero ou atraso inexistente como valor nulo).

### 3.5. Deduplicação de Registros Suspeitos de Aprovação
- **Problema Encontrado**: 15 registros em `aprovacoes_vestibular.csv` possuem o valor `"Cadastro duplicado?"` na coluna `chamada`.
- **Tratamento Escolhido**: Remoção (drop) dessas 15 linhas no pipeline de ETL.
- **Justificativa**: A investigação comprovou que cada um desses 15 alunos já possuía outra linha idêntica de aprovação no banco, porém com a chamada oficial (ex.: `"Lista de espera"`, `"1ª chamada"`). Manter essas 15 linhas geraria contagem dupla e inflaria erroneamente a taxa de aprovação do cursinho.

---

## 4. Arquitetura de Produção e Dashboard
- **Decisão**: Separação clara entre a lógica de ETL (`src/etl.py`), banco de dados (`src/database.py`), engenharia de atributos (`src/features.py`), modelagem (`src/model.py`) e visualização (`dashboard/app.py`).
- **Justificativa**: Promove modularidade, facilitando testes, manutenção e reprodutibilidade do projeto.

---

## 5. Decisões de Modelagem Preditiva

### 5.1. Tipo de Problema e Variável Alvo (Target)
- **Decisão**: Modelo de **Classificação Binária** prevendo a variável `aprovado` ($1 = \text{Aprovado}$, $0 = \text{Não Aprovado}$).
- **Justificativa**: O objetivo estratégico do cursinho é identificar alunos com maior risco de não aprovação durante o ciclo letivo para intervenção pedagógica preventiva.

### 5.2. Escolha do Algoritmo (Random Forest Classifier)
- **Decisão**: Escolha do algoritmo **Random Forest** com 100 árvores de decisão (`n_estimators=100`, `max_depth=10`, `class_weight="balanced"`).
- **Justificativa**:
  1. **Ensemble Robusto**: A combinação de 100 árvores reduz o risco de *overfitting* em comparação com uma árvore de decisão única.
  2. **Ranking de Importância de Features**: Fornece nativamente o peso relativo de cada variável, permitindo que a gestão identifique quais fatores mais impactam o resultado final.
  3. **Independência de Escala**: Não exige normalização ou padronização de variáveis numéricas (como MinMaxScaler ou StandardScaler).
  4. **Adequação ao Tamanho da Base**: Adequado para a base de 812 alunos, onde algoritmos mais complexos (como XGBoost ou redes neurais) correriam alto risco de *overfitting*.

### 5.3. Engenharia de Atributos (9 Features Agregadas)
- **Decisão**: Construção de 9 variáveis agregadas por aluno em `src/features.py`, cobrindo 5 dimensões comportamentais e acadêmicas:
  - *Frequência e Engajamento*: `pct_presenca` (% de aulas presentes/atrasadas).
  - *Rendimento Acadêmico*: `media_nota_simulados` e `nota_diagnostico`.
  - *Comprometimento*: `simulados_finalizados`.
  - *Retenção e Persistência*: `total_matriculas`, `matriculas_concluidas` e `media_bolsa`.
  - *Background e Captação*: `escola_origem` e `canal_captacao`.
- **Encoding Categórico**: Aplicação de *One-Hot Encoding* (`pd.get_dummies(..., drop_first=True)`) para variáveis qualitativas, evitando atribuir ordem ordinal arbitrária entre categorias.

### 5.4. Divisão de Dados e Balanceamento
- **Decisão**: Divisão em 80% treino (649 amostras) e 20% teste (163 amostras), com **amostragem estratificada** (`stratify=y`) e semente fixa (`random_state=42`).
- **Justificativa**: A amostragem estratificada mantém a proporção exata da classe positiva (~37,7% de aprovados) em ambos os conjuntos. O parâmetro `class_weight="balanced"` ajusta os pesos das árvores para compensar o desequilíbrio moderado entre as classes.

### 5.5. Persistência e Integração com Produção
- **Decisão**: Exportação do modelo treinado para `models/modelo.pkl` via `joblib`.
- **Justificativa**: Permite o carregamento instantâneo do modelo no simulador preditivo em tempo real do Dashboard Streamlit na Sprint 4, sem necessidade de re-treinamento a cada interação do usuário.
