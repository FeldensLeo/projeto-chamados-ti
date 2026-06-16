-- ============================================================
-- Schema do banco de dados - TechNova Chamados de TI
-- ============================================================
-- SQLite foi escolhido por ser leve, gratuito e não exigir
-- instalação de servidor — ideal para aprendizado e portfólio.
-- ============================================================

DROP TABLE IF EXISTS chamados;

CREATE TABLE chamados (
    id_chamado            TEXT PRIMARY KEY,
    cliente               TEXT NOT NULL,
    analista              TEXT NOT NULL,
    categoria             TEXT NOT NULL,
    prioridade            TEXT NOT NULL,
    status                TEXT NOT NULL,
    data_abertura         TEXT NOT NULL,
    data_fechamento       TEXT,
    tempo_resolucao_horas REAL
);

-- Índices para acelerar consultas frequentes no dashboard
CREATE INDEX idx_chamados_status    ON chamados (status);
CREATE INDEX idx_chamados_categoria ON chamados (categoria);
CREATE INDEX idx_chamados_analista  ON chamados (analista);
