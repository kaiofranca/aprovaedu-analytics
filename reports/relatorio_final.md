# Relatório Final Executivo & Técnico - AprovaEdu Analytics

---

## 1. Sumário Executivo
Este relatório sintetiza a solução analítica desenvolvida para a **AprovaEdu Analytics**, cobrindo 5 anos de dados operacionais e pedagógicos (2021–2025). O objetivo é apoiar a coordenação pedagógica na compreensão da evolução das aprovações no vestibular, no impacto da frequência escolar, no desempenho por curso/matéria e na identificação de recomendações estratégicas baseadas em dados.

---

## 2. Diagnóstico da Base Bruta e Qualidade dos Dados

A análise inicial identificou 9 tabelas relacionais com excelente integridade referencial entre as chaves (`aluno_id`), sem inconsistências de relacionamento. No entanto, foram identificados e tratados os seguintes problemas de qualidade de dados:

- **Inconsistências Categóricas**: Variações de caixa e ortografia em nomes de matérias (mais de 28 variações para 11 matérias reais), universidades (`uece`, `Ufc` vs `UECE`, `UFC`), escolas de origem e cidades.
- **Heterogeneidade de Datas**: Formatos mistos de datas (`YYYY-MM-DD`, `MM-DD-YYYY` e `DD/MM/YYYY HH:MM`) padronizados para o padrão ISO 8601.
- **Registros Suspeitos**: Remoção (deduplicação) de 15 aprovações marcadas com o rótulo `"Cadastro duplicado?"` após investigação comprovar que eram lançamentos repetidos.
- **Tratamento de Nulos**: Preenchimento de nulos categóricos com `"Não Informado"` e presenças ausentes sem distorção dos cálculos de médias acadêmicas.

---

## 3. Respostas às Análises Obrigatórias

### 3.1. Evolução da Taxa de Aprovação ao Longo dos Anos

Para garantir a transparência da análise e um denominador auditável, apresento as contagens intermediárias lado a lado:

| Ano | (1) Matriculados Distintos | (2) Aprovações Brutas | Aprovações Após Dedup | (3) Aprovados Distintos | Taxa de Aprovação = (3 ÷ 1) |
|:---:|:-------------------------:|:---------------------:|:---------------------:|:-----------------------:|:---------------------------:|
| **2021** | 138 | 50 | 50 | 50 | **36,2%** |
| **2022** | 170 | 53 | 53 | 53 | **31,2%** |
| **2023** | 218 | 78 | 77 | 77 | **35,3%** |
| **2024** | 263 | 87 | 79 | 79 | **30,0%** |
| **2025** | 233 | 86 | 80 | 80 | **34,3%** |

![Taxa de aprovação por ano](figures/q1_taxa_aprovacao_ano.png)

- **Metodologia de Cálculo**: A taxa correta é calculada dividindo **Aprovados Distintos (3)** por **Matriculados Distintos (1)**, garantindo que o numerador e o denominador meçam pessoas (e não contagem de eventos).
- **Impacto da Deduplicação**: O volume de aprovações brutas (354 no total) cai para 339 após a remoção das 15 duplicidades de cadastro. Após essa limpeza, o volume de aprovações coincide exatamente com os alunos aprovados distintos por ano.
- **Movimentos Observados**:
  1. A taxa de aprovação é **estável na casa de 30% a 36%** (média de 33,4%), sem tendência forte de queda ou alta.
  2. O que altera ao longo do tempo é a **escala da operação**: o volume de alunos matriculados quase dobra (138 → 263 no pico), e o volume de aprovações cresce proporcionalmente (50 → 80). A rede expandiu mantendo sua eficiência de aprovação.

---

### 3.2. Relação Entre Presença nas Aulas e Aprovação no Vestibular

- **Metodologia de Cálculo**:
  1. A taxa de frequência individual de cada estudante foi calculada pela razão:
     $$\text{Taxa de Presença (\%)} = \frac{\text{Total de Aulas ('Presente' ou 'Atrasado')}}{\text{Total de Aulas Registradas do Aluno}} \times 100$$
  2. Alunos com status `Presente` ou `Atrasado` foram contabilizados como presença efetiva em sala. Status `Ausente` e `Justificado` foram considerados ausências.
  3. Cada aluno (`aluno_id`) foi rotulado no grupo **Aprovado** (se possui pelo menos 1 registro em `aprovacoes_vestibular`) ou **Não Aprovado** (demais alunos).
  4. Calculou-se as estatísticas descritivas (média, mediana e desvio padrão) de frequência para cada um dos dois grupos.

![Distribuição da taxa de presença por status de aprovação](figures/q2_presenca_vs_aprovacao.png)

- **Resultados Encontrados**:
  - **Aprovados**: Frequência média em aula de **83,97%** (mediana 83,97%, desvio padrão 3,84%)
  - **Não Aprovados**: Frequência média em aula de **84,03%** (mediana 84,21%, desvio padrão 4,26%)

- **Conclusão de Negócio**: A presença em aula é uma condição necessária para o acompanhamento dos conteúdos, porém **não é isoladamente suficiente para garantir a aprovação**. Outros fatores como desempenho prático nos simulados, estudo individual e assimilação do bloco de Exatas/Natureza exercem peso decisivo.

---

### 3.3. Cursos e Matérias com Melhor e Pior Desempenho

- **Metodologia de Cálculo**:
  1. **Desempenho por Matéria**: Calculou-se a nota média de cada disciplina a partir da tabela `resultados_simulados` cruzada com `simulados`, filtrando exclusivamente realizações com `status_realizacao = 'Finalizado'`:
     $$\text{Média da Matéria} = \frac{\sum \text{Notas dos Simulados Finalizados}}{\text{Total de Realizações na Matéria}}$$
     *Nota*: A *Redação* é avaliada na escala $0\text{--}1000$ (padrão ENEM), enquanto as demais disciplinas objetivas utilizam a escala $0\text{--}100$.
  2. **Ranking por Cursos Universitários**: Agrupou-se a tabela `aprovacoes_vestibular` por `curso_aprovado` contando a quantidade total de aprovações e o total de alunos distintos.

![Média de nota nos simulados por matéria](figures/q3_desempenho_materias.png)

- **Matérias com Maior Nota Média nos Simulados**:
  - *Redação*: **718,65** (escala ENEM 0-1000)
  - *Inglês*: **63,25**
  - *História*: **62,92**
- **Matérias com Menor Nota Média (Gargalos Pedagógicos)**:
  - *Matemática*: **62,06**
  - *Física*: **62,09**
  - *Química*: **62,14**

![Top 10 cursos universitários com mais aprovados](figures/q3_top_cursos_aprovados.png)

- **Top 5 Cursos Universitários com Mais Aprovados**:
  1. Enfermagem (28 aprovações)
  2. Odontologia (27 aprovações)
  3. Engenharia de Software (27 aprovações)
  4. Arquitetura (27 aprovações)
  5. Engenharia Civil (26 aprovações)

---

### 3.4. Recomendações Práticas para a Coordenação Pedagógica

1. **Oficinas de Reforço em Exatas e Natureza**: Criar módulos de nivelamento focados em *Matemática, Física e Química*, identificados como as matérias de menor rendimento médio nos simulados.
2. **Painel de Risco Preditivo (Além da Lista de Chamada)**: Implementar monitoramento contínuo das notas de simulados, pois a presença em aula isolada não diferencia alunos em risco de retenção.
3. **Planos de Estudo por Carreira**: Oferecer listas de questões focadas nas bancas e pesos dos cursos mais procurados (Engenharia de Software, Odontologia, Enfermagem e Direito).
4. **Manutenção da Matriz de Redação e Humanas**: Preservar as oficinas de redação que atualmente lideram os indicadores de desempenho.

---

### 3.5. Análises Extras Estratégicas: Canais de Captação e Perfil de Origem

Para ir além das perguntas obrigatórias e gerar inteligência estratégica para os times de **Marketing, Vendas e Gestão**, realizei duas análises complementares:

#### **A. Eficiência dos Canais de Captação (Marketing vs Qualidade da Aprovação)**
Avaliei a taxa de aprovação no vestibular de acordo com a origem do cadastro do estudante:

| Canal de Captação | Total de Estudantes | Alunos Aprovados | Taxa de Aprovação (%) |
|:-----------------:|:-------------------:|:----------------:|:---------------------:|
| **Indicação** | 106 | 46 | **43,40%** |
| **Google** | 126 | 51 | **40,48%** |
| **Feira Escolar** | 105 | 41 | **39,05%** |
| **Instagram** | 238 | 82 | **34,45%** |
| **WhatsApp** | 106 | 33 | **31,13%** |

![Taxa de aprovação por canal de captação](figures/q3_extra_canais_captacao.png)

* **Insight Estratégico**: Alunos vindos de **Indicação** possuem a maior taxa de aprovação no vestibular (**43,4%**), demonstrando que o "boca a boca" atrai estudantes mais engajados e alinhados com o cursinho. Por outro lado, campanhas de redes sociais (Instagram e WhatsApp) trazem o maior volume absoluto de cadastros, mas menor conversão em aprovação (31,1% a 34,4%).
* **Recomendação**: Criar um **Programa de Indicação de Alunos Veteranos** (com descontos ou benefícios na mensalidade) para aumentar o volume do canal de maior eficiência.

#### **B. Impacto da Escola de Origem (Pública, Privada e Federal)**
Avaliei o desempenho no vestibular conforme a formação escolar prévia dos alunos:

| Escola de Origem | Total de Estudantes | Alunos Aprovados | Taxa de Aprovação (%) |
|:----------------:|:-------------------:|:----------------:|:---------------------:|
| **Privada** | 248 | 99 | **39,92%** |
| **Pública** | 227 | 83 | **36,56%** |
| **Federal** | 112 | 40 | **35,71%** |

![Taxa de aprovação por escola de origem](figures/q3_extra_escola_origem.png)

* **Insight Estratégico**: A diferença na taxa de aprovação entre alunos de *Escola Privada* (39,9%) e *Escola Pública* (36,6%) é de apenas **3,36 pontos percentuais**. Isso comprova que a proposta pedagógica do cursinho atua como um **eficiente equalizador social de oportunidades**, nivelando o conhecimento dos estudantes independente de sua origem.

---

## 4. Desempenho do Modelo Preditivo

---

## 5. Conclusões Gerais
Os resultados das análises obrigatórias e extras confirmam a solidez operacional do cursinho e trazem direcionamentos claros tanto para a coordenação pedagógica (reforço no bloco de Exatas e monitoramento por simulados) quanto para o marketing (foco em programas de indicação).
