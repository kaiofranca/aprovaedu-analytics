# Relatório Final Executivo & Técnico - AprovaEdu Analytics

---

## 1. Sumário Executivo
Este relatório sintetiza a solução analítica desenvolvida para a **AprovaEdu Analytics**, cobrindo 5 anos de dados operacionais e pedagógicos (2021–2025). O objetivo é apoiar a coordenação pedagógica na compreensão da evolução das aprovações no vestibular, no impacto da frequência escolar, no desempenho por curso/matéria e na identificação de recomendações estratégicas baseadas em dados.

---

## 2. Diagnóstico da Base Bruta e Qualidade dos Dados

A análise inicial identificou 9 tabelas relacionais com excelente integridade referencial entre as chaves (`aluno_id`), sem inconsistências de relacionamento. No entanto, foram identificados e tratados os seguintes problemas de qualidade de dados:

- **Inconsistências Categóricas**: Variações de caixa e ortografia em nomes de matérias (mais de 28 variações para 11 matérias reais), universidades (`uece`, `Ufc` vs `UECE`, `UFC`), escolas de origem e cidades.
- **Heterogeneidade de Datas**: Formatos mistos de datas (`YYYY-MM-DD`, `MM-DD-YYYY` e `DD/MM/YYYY HH:MM`) padronizados para o padrão ISO 8601.
- **Registros Suspeitos**: Trata e saneamento de 15 aprovações marcadas com o rótulo `"Cadastro duplicado?"`.
- **Tratamento de Nulos**: Preenchimento correto de bolsas percentuais (0%) e presenças ausentes sem distorção dos cálculos de médias acadêmicas.

---

## 3. Respostas às Análises Obrigatórias

### 3.1. Evolução da taxa de aprovação ao longo dos anos

### 3.2. Relação entre presença nas aulas e aprovação no vestibular

### 3.3. Cursos ou matérias com melhor desempenho

### 3.4. Recomendações práticas para a coordenação pedagógica

---

## 4. Desempenho do Modelo Preditivo

---

## 5. Conclusões Gerais
