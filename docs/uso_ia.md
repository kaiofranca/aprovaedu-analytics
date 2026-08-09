# Transparência sobre o Uso de Inteligência Artificial

---

## 1. Declaração de Uso

Neste projeto, utilizei ferramentas de inteligência artificial generativa como **apoio ao desenvolvimento**, mantendo total responsabilidade sobre as decisões técnicas, a arquitetura do sistema e a produção do código-fonte.

As ferramentas de IA foram empregadas como assistentes de programação e **não** como substitutas do raciocínio analítico ou da tomada de decisão.

---

## 2. Ferramentas de IA Utilizadas

| Ferramenta | Provedor | Uso no Projeto |
|---|---|---|
| **Claude Opus 4.6** | Anthropic | Assistência principal na revisão de código, estruturação de módulos e geração de visualizações |
| **Gemini Flash 3.6** | Google DeepMind | Consultas pontuais sobre bibliotecas, validação de lógica e apoio em tarefas repetitivas |

---

## 3. Decisões Técnicas Tomadas por Mim

Todas as decisões estratégicas e arquiteturais foram tomadas por mim com base na análise dos dados e nos requisitos do desafio. As principais decisões incluem:

1. **Escolha do banco de dados**: Optei pelo SQLite em vez do DuckDB após avaliar que um banco embarcado sem dependências externas era mais adequado ao escopo do projeto.
2. **Criação do ambiente virtual (`venv`)**: Decidi isolar as dependências do projeto em um ambiente virtual para garantir reprodutibilidade.
3. **Seleção do algoritmo de ML (Random Forest)**: Avaliei as opções disponíveis (Regressão Logística, Random Forest, ambos) e optei pelo Random Forest por fornecer ranking de importância de features e ser robusto ao tamanho da base (812 amostras).
4. **Definição das 9 features do modelo preditivo**: Selecionei as variáveis de entrada com base nas dimensões comportamentais e acadêmicas disponíveis no banco de dados, garantindo cobertura de engajamento, rendimento, persistência e perfil do aluno.
5. **Hiperparâmetros do modelo**: Defini a configuração de 100 árvores, profundidade máxima 10, balanceamento de classes e split 80/20 estratificado.
6. **Estrutura do Dashboard (4 abas)**: Organizei a interface em Visão Geral, Desempenho Acadêmico, Frequência e Simulador Preditivo, com o simulador como funcionalidade opcional ativada por botão.
7. **Containerização com Docker**: Defini que o `main.py` deveria ser executado durante o build da imagem para que o container já contivesse os dados tratados e o modelo treinado.

---

## 4. Como a IA Foi Utilizada na Prática

### O que a IA fez:
- **Revisão de código**: Identificação de erros de lógica, sugestões de refatoração e validação de queries SQL.
- **Correção e padronização**: Ajustes em formatação de texto, consistência de estilo nos gráficos (títulos em *sentence case*) e conjugação verbal no relatório.
- **Automação de tarefas repetitivas**: Geração de estruturas de notebooks (células markdown + código), templates de gráficos com Matplotlib/Plotly e boilerplate de configuração (Dockerfile, .gitignore).
- **Explicações didáticas**: Apoio na compreensão de conceitos técnicos.

### O que eu fiz:
- **Análise exploratória dos dados brutos**: Investiguei cada uma das 9 tabelas, identifiquei as inconsistências e defini as regras de limpeza.
- **Decisões de negócio**: Interpretei os resultados das análises e formulei as recomendações para a coordenação pedagógica.
- **Validação cruzada de resultados**: Comparei os números gerados pelo pipeline com cálculos manuais para garantir correção.
- **Fluxo de trabalho Git**: Gerenciei branches (`feat/etl`, `feat/analises`, `feat/prediction`, `feat/bi`), pull requests e merges no repositório.
- **Todas as decisões técnicas**: Conforme detalhado na Seção 3, cada escolha de tecnologia, algoritmo e estrutura foi feita por mim após avaliação das alternativas.

---

## 5. Conclusão

A inteligência artificial foi uma ferramenta de **produtividade e aprendizado**, não de substituição. Todas as decisões críticas do projeto (desde a escolha do banco de dados até os hiperparâmetros do modelo) foram tomadas por mim com base na análise dos dados e nos requisitos do desafio. O uso de IA permitiu acelerar tarefas operacionais e aprofundar meu entendimento técnico, mantendo total transparência sobre o processo.
