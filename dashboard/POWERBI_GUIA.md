# Guia do Dashboard Power BI — Passo a Passo

Este guia monta o dashboard completo no **Power BI Desktop** usando os dados do projeto TechNova.

## Pré-requisitos

1. [Power BI Desktop](https://powerbi.microsoft.com/desktop/) instalado
2. Pipeline ETL executado:

```bash
python scripts/etl_pipeline.py
python scripts/export_for_powerbi.py
```

O arquivo `data/chamados_ti_clean.csv` será usado como fonte.

---

## Passo 1 — Importar os dados

1. Abra o **Power BI Desktop**
2. Clique em **Obter dados** (ou **Get data**)
3. Selecione **Texto/CSV**
4. Navegue até `data/chamados_ti_clean.csv` do projeto
5. Clique em **Abrir**
6. Na pré-visualização, clique em **Carregar** (se os tipos estiverem corretos)  
   **ou** em **Transformar dados** (recomendado na primeira vez)

> **Por que CSV e não SQLite?** O Power BI não conecta nativamente ao SQLite sem conectores extras. Exportar para CSV é a forma mais simples para iniciantes.

---

## Passo 2 — Ajustar tipos no Power Query

Se clicou em **Transformar dados**:

| Coluna | Tipo correto |
|--------|--------------|
| `id_chamado` | Texto |
| `cliente` | Texto |
| `analista` | Texto |
| `categoria` | Texto |
| `prioridade` | Texto |
| `status` | Texto |
| `data_abertura` | Data/Hora |
| `data_fechamento` | Data/Hora |
| `tempo_resolucao_horas` | Número decimal |

1. Clique no ícone à esquerda de cada coluna para alterar o tipo
2. Clique em **Fechar e aplicar** (canto superior esquerdo)

> **Conceito:** isso é **data preparation** — garantir que cada campo tenha o tipo certo antes de criar visuais.

---

## Passo 3 — Renomear a tabela (opcional)

No painel **Dados** (à direita), clique com o botão direito na tabela importada e renomeie para `chamados`.

---

## Passo 4 — Criar medidas DAX

Medidas são cálculos reutilizáveis (KPIs). Na aba **Modelagem**:

1. Clique em **Nova medida**
2. Cole cada medida abaixo (uma por vez):

```dax
Total Chamados = COUNTROWS(chamados)
```

```dax
Tempo Medio Resolucao (h) =
    AVERAGE(chamados[tempo_resolucao_horas])
```

```dax
Chamados Fechados =
    CALCULATE(
        [Total Chamados],
        chamados[status] = "Fechado"
    )
```

```dax
Chamados Abertos =
    CALCULATE(
        [Total Chamados],
        chamados[status] IN {"Aberto", "Em andamento"}
    )
```

> **Conceito:** camada **semântica** — você define a métrica uma vez e usa em vários gráficos.

---

## Passo 5 — Montar os visuais

Ative a visualização em **Exibição → Layout de página → Tamanho 16:9**.

### 5.1 Total de chamados (Cartão)

1. Clique em área vazia do relatório
2. No painel **Visualizações**, escolha **Cartão**
3. Arraste a medida `Total Chamados` para o campo **Campos**

### 5.2 Tempo médio de resolução (Cartão)

1. Adicione outro **Cartão**
2. Arraste `Tempo Medio Resolucao (h)`
3. Formate: selecione o visual → **Formatar** → **Rótulo de chamada** → 1 casa decimal → sufixo ` h`

### 5.3 Chamados por categoria (Barras)

1. Escolha **Gráfico de barras agrupadas**
2. **Eixo Y:** `categoria`
3. **Eixo X:** `Total Chamados`
4. Ordene: clique nos `...` do visual → **Ordenar eixo** → por valor decrescente

### 5.4 Chamados por status (Pizza ou barras)

1. Escolha **Gráfico de pizza** ou **Barras**
2. **Legenda:** `status`
3. **Valores:** `Total Chamados`
4. Cores sugeridas:
   - Fechado → verde
   - Em andamento → laranja
   - Aberto → vermelho

### 5.5 Top 5 analistas (Barras + filtro Top N)

1. Escolha **Gráfico de barras**
2. **Eixo Y:** `analista`
3. **Eixo X:** `Total Chamados`
4. No painel **Filtros neste visual**:
   - Arraste `analista` para o filtro
   - Tipo de filtro: **Top N**
   - Mostrar itens: **Top** `5`
   - Por valor: `Total Chamados`

> **Dica:** para "analistas que mais resolveram", adicione um filtro no visual: `status` = `Fechado`.

---

## Passo 6 — Layout e título

1. **Inserir → Caixa de texto** → título: `Dashboard de Chamados de TI — TechNova`
2. Alinhe os cartões no topo e os gráficos abaixo
3. Use **Exibição → Grade de alinhamento** para organizar

---

## Passo 7 — Salvar e publicar no portfólio

1. **Arquivo → Salvar como** → `dashboard/chamados_ti_dashboard.pbix`
2. Tire um print: `Win + Shift + S`
3. Salve em `screenshots/dashboard_powerbi.png`
4. Faça commit do print no GitHub (o `.pbix` pode ficar fora do Git por ser binário grande)

---

## Valores esperados (referência)

Após o ETL, você deve ver aproximadamente:

| Métrica | Valor esperado |
|---------|----------------|
| Total de chamados | ~1177 |
| Tempo médio resolução | ~185 horas |
| Status Fechado | ~785 |
| Status Em andamento | ~220 |
| Status Aberto | ~172 |

---

## Conceitos de Engenharia de Dados

| Etapa no Power BI | Conceito |
|-------------------|----------|
| Importar CSV | **Data consumption** |
| Power Query | **Data preparation** |
| Medidas DAX | **Semantic layer / métricas de negócio** |
| Visuais | **Data storytelling** |
| Dashboard | **Self-service BI** |

---

## Problemas comuns

| Problema | Solução |
|----------|---------|
| Medida DAX com erro | Verifique se a tabela se chama `chamados` |
| Tempo médio em branco | Confirme tipo decimal em `tempo_resolucao_horas` |
| Datas erradas | Reimporte com **Transformar dados** e tipo Data/Hora |
| CSV não encontrado | Execute `python scripts/export_for_powerbi.py` |
