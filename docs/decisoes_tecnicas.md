# Registro de Decisões Técnicas e Arquiteturais

---

## 1. Contexto Geral e Diagnóstico da Base Bruta
A base bruta do **AprovaEdu Analytics** é composta por 9 tabelas relacionais cobrindo o período de 2021 a 2025. Embora apresente 100% de integridade referencial entre as chaves primárias e estrangeiras (`aluno_id`), foram diagnosticadas três categorias principais de inconsistências que exigem tratamento prévio:
1. **Divergências de Padronização de Texto e Categorias** (caixa alta/baixa e variações ortográficas).
2. **Formatos Mistos de Datas** (`YYYY-MM-DD`, `MM-DD-YYYY` e `DD/MM/YYYY HH:MM`).
3. **Valores Ausentes (Nulos) e Registros Suspeitos**.

---

## 2. Decisões de Tratamento e Justificativas Técnicas

### 2.1. Normalização de Nomes de Matérias
- **Problema Encontrado**: A coluna de matéria apresenta mais de 28 variações de escrita para apenas 11 matérias reais (ex.: `"Mat."`, `"Matematica"`, `"MATEMÁTICA"`, `"Fisica"`, `"FÍSICA"`).
- **Tratamento Escolhido**: Mapeamento via dicionário de substituição explícito no pipeline de ETL.
- **Justificativa**: Sem a unificação das matérias, qualquer agrupamento por disciplina para avaliar o desempenho acadêmico ficaria fragmentado e geraria indicadores distorcidos.

### 2.2. Padronização de Texto em Colunas Categóricas
- **Problema Encontrado**: Inconsistências de caixa (maiúsculas/minúsculas) e acentuação em colunas como `cidade`, `escola_origem`, `universidade`, `status_presenca`, `modalidade_aula`, `status_realizacao`, `dispositivo`, `unidade_aplicacao`, `status_professor` e `bolsa_aprovacao`.
- **Tratamento Escolhido**: Aplicação de limpeza com `.str.strip().str.title()` para textos gerais e `.str.upper()` para siglas de universidades (`UECE`, `UFC`, `UFRN`, `IFCE`).
- **Justificativa**: Garante consistência em filtros e joins no banco de dados e no Dashboard Streamlit.

### 2.3. Padronização de Formato de Datas
- **Problema Encontrado**: Presença de datas em formato americano (`MM-DD-YYYY`) em `estudantes.data_cadastro` (33 linhas) e `aprovacoes_vestibular.data_resultado` (12 linhas), além do formato brasileiro (`DD/MM/YYYY HH:MM`) em `resultados_simulados.inicio_simulado` (880 linhas).
- **Tratamento Escolhido**: Conversão unificada para o padrão ISO 8601 (`YYYY-MM-DD` ou `YYYY-MM-DD HH:MM:SS`) usando `pd.to_datetime(..., format='mixed')`.
- **Justificativa**: O padrão ISO é nativamente suportado por bancos SQL (SQLite), Pandas e ferramentas de BI, evitando erros em ordenações e agrupamentos temporais.

### 2.4. Trata de Valores Ausentes (Nulos)
- **Problema Encontrado**: Presença de nulos em várias colunas (`bolsa_percentual` em matrículas, `atraso_min` e `justificativa` em presenças, `nota` e `acertos` em resultados de simulados).
- **Tratamento Escolhido**:
  - `bolsa_percentual`: Preenchimento com `0` (aluno sem bolsa).
  - `atraso_min`: Preenchimento com `0` em presenças confirmadas.
  - `justificativa` e `nota`/`acertos` de ausentes: Preservados como `null` ou preenchidos com rótulo explícito `"Não Informado"`.
- **Justificativa**: Impede distorções no cálculo de médias numéricas (evita tratar ausência em prova como nota zero ou atraso inexistente como valor nulo).

### 2.5. Registros Suspeitos de Aprovação
- **Problema Encontrado**: 15 registros em `aprovacoes_vestibular.csv` possuem o valor `"Cadastro duplicado?"` na coluna `chamada`.
- **Tratamento Escolhido**: Deduplicação lógica verificando a combinação (`aluno_id`, `universidade`, `curso_aprovado`, `ano_vestibular`). Se for duplicata real, descarta-se a linha excedente; caso contrário, altera-se a chamada para `"Não Informado"`.
- **Justificativa**: Mantém a precisão na contagem da taxa de aprovação sem desconsiderar aprovações legítimas.

---

## 3. Armazenamento e Modelagem Relacional (SQLite)
- **Decisão**: Utilização do **SQLite** (`data/processed/aprovaedu.db`).
- **Justificativa**: O SQLite é nativo da biblioteca padrão do Python (`sqlite3`), não exige instalação de servidores externos e permite consultas relacionais de alta performance diretamente no Dashboard Streamlit.

---

## 4. Arquitetura de Produção e Dashboard
- **Decisão**: Separação clara entre a lógica de ETL (`src/etl.py`), banco de dados (`src/database.py`), engenharia de atributos (`src/features.py`), modelagem (`src/model.py`) e visualização (`dashboard/app.py`).
- **Justificativa**: Promove modularidade, facilitando testes, manutenção e reprodutibilidade do projeto.
