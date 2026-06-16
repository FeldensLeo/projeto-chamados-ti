"""
Pipeline ETL simples para chamados de TI da TechNova.

ETL = Extract (Extrair) + Transform (Transformar) + Load (Carregar)

Fluxo:
  CSV bruto  -->  limpeza e enriquecimento  -->  SQLite
"""

import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_CSV = BASE_DIR / "data" / "chamados_ti_raw.csv"
DB_PATH = BASE_DIR / "data" / "chamados_ti.db"
SQL_SCHEMA = BASE_DIR / "sql" / "create_tables.sql"

STATUS_VALIDOS = {"Aberto", "Em andamento", "Fechado"}
PRIORIDADES_VALIDAS = {"Baixa", "Média", "Alta", "Crítica"}


def extract(csv_path: Path) -> pd.DataFrame:
    """EXTRACT: lê os dados da fonte (arquivo CSV)."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {csv_path}\n"
            "Execute primeiro: python scripts/generate_data.py"
        )

    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    print(f"[EXTRACT] {len(df)} registros lidos de {csv_path.name}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """TRANSFORM: limpa, padroniza e enriquece os dados."""
    original = len(df)
    df = df.copy()

    # Remover linhas com campos obrigatórios vazios
    df = df.dropna(subset=["id_chamado", "cliente", "analista", "categoria"])
    df = df[df["cliente"].astype(str).str.strip() != ""]

    # Padronizar texto
    for col in ["cliente", "analista", "categoria", "prioridade", "status"]:
        df[col] = df[col].astype(str).str.strip()

    # Filtrar valores fora do domínio esperado
    df = df[df["status"].isin(STATUS_VALIDOS)]
    df = df[df["prioridade"].isin(PRIORIDADES_VALIDAS)]

    # Padronizar datas (registros inválidos viram NaT e são removidos)
    df["data_abertura"] = pd.to_datetime(df["data_abertura"], errors="coerce")
    df["data_fechamento"] = pd.to_datetime(df["data_fechamento"], errors="coerce")

    df = df.dropna(subset=["data_abertura"])

    # Calcular tempo de resolução em horas (apenas para chamados fechados)
    df["tempo_resolucao_horas"] = None
    mask_fechado = df["status"] == "Fechado"
    df.loc[mask_fechado, "tempo_resolucao_horas"] = (
        (df.loc[mask_fechado, "data_fechamento"] - df.loc[mask_fechado, "data_abertura"])
        .dt.total_seconds()
        / 3600
    ).round(2)

    # Remover fechados sem data de fechamento ou com tempo negativo
    invalidos_fechados = mask_fechado & (
        df["data_fechamento"].isna() | (df["tempo_resolucao_horas"] < 0)
    )
    df = df[~invalidos_fechados]

    removidos = original - len(df)
    print(f"[TRANSFORM] {removidos} registros inválidos removidos")
    print(f"[TRANSFORM] {len(df)} registros prontos para carga")
    return df


def load(df: pd.DataFrame, db_path: Path, schema_path: Path) -> None:
    """LOAD: grava os dados no banco SQLite."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)

    try:
        with open(schema_path, encoding="utf-8") as f:
            conn.executescript(f.read())

        df_load = df.copy()
        df_load["data_abertura"] = df_load["data_abertura"].dt.strftime("%Y-%m-%d %H:%M:%S")
        df_load["data_fechamento"] = df_load["data_fechamento"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        df_load.to_sql("chamados", conn, if_exists="append", index=False)

        total = conn.execute("SELECT COUNT(*) FROM chamados").fetchone()[0]
        print(f"[LOAD] {total} registros carregados em {db_path.name}")
    finally:
        conn.close()


def main() -> None:
    print("=" * 50)
    print("Pipeline ETL - TechNova Chamados de TI")
    print("=" * 50)

    df_raw = extract(RAW_CSV)
    df_clean = transform(df_raw)
    load(df_clean, DB_PATH, SQL_SCHEMA)

    print("=" * 50)
    print("ETL concluído com sucesso!")
    print("=" * 50)


if __name__ == "__main__":
    main()
