# Guia do Dashboard Power BI

Este guia explica passo a passo como criar o dashboard no Power BI Desktop usando os dados do SQLite.

## Pré-requisitos

- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) instalado
- Pipeline ETL executado (`python scripts/etl_pipeline.py`)
- Banco gerado em `data/chamados_ti.db`

## Passo 1 — Conectar ao SQLite

O Power BI não conecta nativamente ao SQLite. Use uma destas opções:

### Opção A (recomendada para iniciantes): exportar para CSV

Execute no terminal, na raiz do projeto:

```bash
python -c "import sqlite3, pandas as pd; conn=sqlite3.connect('data/chamados_ti.db'); pd.read_sql('SELECT * FROM chamados', conn).to_csv('data/chamados_ti_clean.csv', index=False, encoding='utf-8-sig'); conn.close(); print('Exportado!')"
```

No Power BI: **Obter dados → Texto/CSV** → selecione `data/chamados_ti_clean.csv`.

### Opção B: conector SQLite

Instale um conector ODBC para SQLite ou use o conector **SQLite** da Microsoft AppSource, se disponível na sua versão.

## Passo 2 — Preparar os dados no Power Query

1. Clique em **Transformar dados**.
2. Verifique os tipos das colunas:
   - `data_abertura` e `data_fechamento` → Data/Hora
   - `tempo_resolucao_horas` → Número decimal
3. Clique em **Fechar e aplicar**.

## Passo 3 — Criar as medidas DAX

Na aba **Modelagem**, crie as medidas abaixo:

```dax
Total Chamados = COUNTROWS(chamados)

Tempo Medio Resolucao (h) =
    AVERAGE(chamados[tempo_resolucao_horas])

Chamados Fechados =
    CALCULATE(
        [Total Chamados],
        chamados[status] = "Fechado"
    )

Chamados Abertos =
    CALCULATE(
        [Total Chamados],
        chamados[status] IN {"Aberto", "Em andamento"}
    )
```

## Passo 4 — Montar o dashboard

Organize os visuais na página:

| Visual | Tipo sugerido | Campo |
|--------|---------------|-------|
| Total de chamados | Cartão | `Total Chamados` |
| Tempo médio de resolução | Cartão | `Tempo Medio Resolucao (h)` |
| Chamados por categoria | Gráfico de barras | Eixo: `categoria`, Valores: `Total Chamados` |
| Chamados por status | Gráfico de pizza ou barras | Legenda: `status`, Valores: `Total Chamados` |
| Top 5 analistas | Gráfico de barras | Eixo: `analista`, Valores: `Total Chamados`, Filtro Top N = 5 |

### Dica de filtro para Top 5 analistas

1. Adicione um gráfico de barras com `analista` e `Total Chamados`.
2. No painel de filtros do visual, em **Filtros neste visual**:
   - Arraste `analista`
   - Tipo: **Top N**
   - Mostrar itens: **Top 5**
   - Por valor: `Total Chamados`

## Passo 5 — Formatação

- Título da página: **Dashboard de Chamados de TI — TechNova**
- Use cores consistentes (ex.: verde para Fechado, laranja para Em andamento, vermelho para Aberto).
- Formate `Tempo Medio Resolucao (h)` com 1 casa decimal.

## Passo 6 — Salvar e exportar print

1. Salve o arquivo como `dashboard/chamados_ti_dashboard.pbix`.
2. Tire um print da tela e salve em `screenshots/dashboard_powerbi.png`.
3. Adicione o print no README do GitHub.

## Conceitos de Engenharia de Dados praticados aqui

| Etapa | Conceito |
|-------|----------|
| Conexão com dados | **Data ingestion** — consumir dados do repositório |
| Power Query | **Data preparation** — tipagem e limpeza visual |
| Medidas DAX | **Camada semântica** — métricas de negócio reutilizáveis |
| Dashboard | **Data visualization** — comunicar insights para stakeholders |
