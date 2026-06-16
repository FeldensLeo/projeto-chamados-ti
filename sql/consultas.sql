-- ============================================================
-- Consultas analíticas - TechNova Chamados de TI
-- ============================================================
-- Execute com: sqlite3 data/chamados_ti.db < sql/consultas.sql
-- Ou abra o arquivo no DBeaver / DB Browser for SQLite.
-- ============================================================

-- 1. Quantos chamados existem?
SELECT COUNT(*) AS total_chamados
FROM chamados;


-- 2. Qual analista resolveu mais chamados?
-- Consideramos "resolvidos" os chamados com status Fechado.
SELECT
    analista,
    COUNT(*) AS chamados_resolvidos
FROM chamados
WHERE status = 'Fechado'
GROUP BY analista
ORDER BY chamados_resolvidos DESC
LIMIT 1;


-- 3. Qual categoria possui mais chamados?
SELECT
    categoria,
    COUNT(*) AS total
FROM chamados
GROUP BY categoria
ORDER BY total DESC
LIMIT 1;


-- 4. Qual é o tempo médio de resolução (em horas)?
SELECT
    ROUND(AVG(tempo_resolucao_horas), 2) AS tempo_medio_horas
FROM chamados
WHERE status = 'Fechado'
  AND tempo_resolucao_horas IS NOT NULL;


-- 5. Quantos chamados estão abertos e fechados?
SELECT
    status,
    COUNT(*) AS quantidade
FROM chamados
GROUP BY status
ORDER BY quantidade DESC;


-- ============================================================
-- Consultas extras para o dashboard Power BI
-- ============================================================

-- Top 5 analistas por volume de chamados resolvidos
SELECT
    analista,
    COUNT(*) AS chamados_resolvidos
FROM chamados
WHERE status = 'Fechado'
GROUP BY analista
ORDER BY chamados_resolvidos DESC
LIMIT 5;


-- Chamados por categoria
SELECT
    categoria,
    COUNT(*) AS total
FROM chamados
GROUP BY categoria
ORDER BY total DESC;


-- Chamados por prioridade
SELECT
    prioridade,
    COUNT(*) AS total
FROM chamados
GROUP BY prioridade
ORDER BY total DESC;
