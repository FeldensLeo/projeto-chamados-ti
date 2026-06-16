Projeto Chamados de TI — TechNova

Projeto de portfólio, que simula o fluxo completo de tratamento de chamados de suporte técnico de uma empresa fictícia.

Do dado bruto (CSV) até a visualização em dashboard (Power BI), passando por limpeza, transformação e armazenamento em banco relacional.

---

-> Descrição do projeto

A TechNova possui uma equipe de suporte técnico que registra chamados diariamente. Este projeto:

1. Gera dados fictícios de chamados de TI
2. Executa um pipeline **ETL** (Extract, Transform, Load)
3. Armazena os dados em **SQLite**
4. Responde perguntas de negócio com **SQL**
5. Visualiza os resultados em um **dashboard Power BI**

> Objetivo pedagógico: demonstrar os fundamentos de Engenharia de Dados sem depender de cloud ou ferramentas avançadas.

---

-> Arquitetura simplificada

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  CSV (fonte)    │ ──► │  Python + Pandas │ ──► │  SQLite (DW)    │ ──► │  Power BI        │
│  dados brutos   │     │  Pipeline ETL    │     │  dados limpos   │     │  Dashboard       │
└─────────────────┘     └──────────────────┘     └─────────────────┘     └──────────────────┘
        ▲                         │
        │                         ▼
 generate_data.py           etl_pipeline.py
```

-> Fluxo de dados

| Etapa | Script / Arquivo | O que acontece |
|-------|------------------|----------------|
| Geração | `scripts/generate_data.py` | Cria CSV com ~1200 chamados (inclui dados inválidos de propósito) |
| Extract | `scripts/etl_pipeline.py` | Lê o CSV com Pandas |
| Transform | `scripts/etl_pipeline.py` | Remove inválidos, padroniza datas, calcula tempo de resolução |
| Load | `scripts/etl_pipeline.py` | Grava na tabela `chamados` do SQLite |
| Análise | `sql/consultas.sql` | Consultas SQL para métricas de negócio |
| Visualização | `dashboard/` | Dashboard Power BI |

---

-> Tecnologias utilizadas

| Tecnologia | Papel no projeto |
|------------|------------------|
| **Python** | Linguagem principal dos scripts |
| **Pandas** | Manipulação e transformação de dados |
| **SQLite** | Banco de dados relacional local |
| **SQL** | Consultas analíticas |
| **Power BI** | Dashboard e visualização |
| **Git/GitHub** | Versionamento e portfólio |

---

-> Estrutura do projeto

```
projeto-chamados-ti/
│
├── data/                  # Dados gerados (CSV bruto, banco SQLite)
├── scripts/
│   ├── generate_data.py   # Gera o CSV fictício
│   ├── etl_pipeline.py    # Pipeline ETL completo
│   ├── export_for_powerbi.py  # Exporta CSV para Power BI
│   └── run_queries.py     # Executa consultas e exibe resultados
├── sql/
│   ├── create_tables.sql  # Schema do banco
│   └── consultas.sql      # Consultas analíticas
├── dashboard/
│   └── POWERBI_GUIA.md    # Passo a passo do dashboard
├── screenshots/           # Prints do dashboard
├── requirements.txt
└── README.md
```

---

-> Como executar o projeto

-> 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/projeto-chamados-ti.git
cd projeto-chamados-ti
```

-> 2. Criar ambiente virtual (recomendado)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

-> 3. Instalar dependências

```bash
pip install -r requirements.txt
```

-> 4. Gerar os dados fictícios

```bash
python scripts/generate_data.py
```

Saída esperada: `data/chamados_ti_raw.csv` com ~1200 registros.

-> 5. Executar o pipeline ETL

```bash
python scripts/etl_pipeline.py
```

Saída esperada: `data/chamados_ti.db` com a tabela `chamados` populada.

-> 6. Validar consultas SQL

```bash
python scripts/run_queries.py
```

Ou, com [sqlite3](https://sqlite.org/cli.html) instalado:

```bash
sqlite3 data/chamados_ti.db < sql/consultas.sql
```

Ou abra o banco no [DB Browser for SQLite](https://sqlitebrowser.org/).

-> 7. Exportar dados para o Power BI

```bash
python scripts/export_for_powerbi.py
```

Gera `data/chamados_ti_clean.csv` — use este arquivo no Power BI.

-> 8. Criar o dashboard Power BI

Siga o guia em [`dashboard/POWERBI_GUIA.md`](dashboard/POWERBI_GUIA.md).

---

-> Consultas SQL — perguntas de negócio

| Pergunta | Arquivo |
|----------|---------|
| Quantos chamados existem? | `sql/consultas.sql` — consulta 1 |
| Qual analista resolveu mais chamados? | consulta 2 |
| Qual categoria possui mais chamados? | consulta 3 |
| Qual é o tempo médio de resolução? | consulta 4 |
| Quantos chamados abertos vs fechados? | consulta 5 |

---

-> Dashboard Power BI

O dashboard deve conter:

- Total de chamados
- Chamados por categoria
- Chamados por status
- Tempo médio de resolução
- Top 5 analistas

-> Print do dashboard

> Adicione aqui após criar o dashboard:

![Dashboard Power BI](screenshots/dashboard_powerbi.png)

---

-> Aprendizados obtidos

Ao concluir este projeto, você pratica:

- **Geração de dados sintéticos** para simular fontes reais
- **Pipeline ETL** com separação clara de Extract, Transform e Load
- **Data quality** — identificar e remover registros inválidos
- **Modelagem relacional** com tabelas, tipos e índices
- **SQL analítico** com agregações, filtros e ordenação
- **Visualização de dados** para comunicar insights
- **Versionamento com Git** para portfólio profissional

---

-> Conceitos de Engenharia de Dados por etapa

-> 1. Geração de dados (`generate_data.py`)

| Conceito | O que você pratica |
|----------|-------------------|
| Data sourcing | Simular uma fonte de dados externa |
| Data modeling| Definir schema (colunas e tipos) antes de gerar |
| Data realism | Distribuições ponderadas (mais chamados fechados que abertos) |
| Dirty data | Inserir erros propositais para praticar limpeza |

Por que inserir dados inválidos? Na vida real, dados nunca chegam 100% limpos. Aprender a lidar com isso é essencial.

-> 2. Extract (`etl_pipeline.py`)

| Conceito | O que você pratica |
|----------|-------------------|
| Data ingestion | Ler dados de uma fonte (CSV) |
| Decoupling | Separar leitura da transformação |

Por que CSV? É o formato mais universal para troca de dados. APIs e bancos retornam dados que frequentemente viram CSV/Parquet.

-> 3. Transform (`etl_pipeline.py`)

| Conceito | O que você pratica |
|----------|-------------------|
| **Data cleaning** | Remover nulos, campos vazios, valores inválidos |
| **Data validation** | Filtrar status e prioridades fora do domínio |
| **Data type casting** | Converter strings em datas |
| **Feature engineering** | Criar `tempo_resolucao_horas` a partir de duas datas |

**Por que calcular tempo de resolução?** Métricas derivadas são a base de KPIs. O dado bruto raramente responde perguntas de negócio diretamente.

-> 4. Load (`etl_pipeline.py` + `create_tables.sql`)

| Conceito | O que você pratica |
|----------|-------------------|
| **Data warehouse (simplificado)** | SQLite como repositório analítico |
| **Schema design** | PRIMARY KEY, NOT NULL, tipos adequados |
| **Indexing** | Índices em colunas usadas em filtros/agrupamentos |

**Por que SQLite e não PostgreSQL?** Para aprendizado, SQLite é zero-config. Os conceitos (SQL, tabelas, índices) são os mesmos.

-> 5. SQL analítico (`consultas.sql`)

| Conceito | O que você pratica |
|----------|-------------------|
| **Aggregation** | `COUNT`, `AVG`, `GROUP BY` |
| **Filtering** | `WHERE` para segmentar dados |
| **Ranking** | `ORDER BY` + `LIMIT` para top N |

**Por que SQL separado do Python?** Em empresas, analistas e engenheiros consultam o banco diretamente. Separar consultas facilita manutenção e reutilização.

-> 6. Dashboard Power BI

| Conceito | O que você pratica |
|----------|-------------------|
| **Data visualization** | Transformar números em insights visuais |
| **Semantic layer** | Medidas DAX reutilizáveis |
| **Self-service BI** | Usuários de negócio exploram dados sem código |

---

-> Próximos passos (evolução do projeto)

Quando se sentir confortável, evolua o projeto:

1. **Orquestração** — agendar o ETL com cron ou Task Scheduler
2. **Testes** — validar qualidade com `pytest` e `great_expectations`
3. **Logs** — registrar quantos registros foram removidos em cada execução
4. **Incremental load** — carregar apenas chamados novos
5. **dbt** — organizar transformações SQL em camadas (staging → mart)
6. **Cloud** — migrar para BigQuery, Snowflake ou PostgreSQL na nuvem

---

-> Licença

Projeto educacional / livre para uso em portfólio e estudos.

---

-> Autor

Projeto criado como exercício de aprendizado em Engenharia de Dados.
