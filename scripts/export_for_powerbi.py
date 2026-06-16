"""Exporta dados do SQLite para CSV — pronto para importar no Power BI."""

import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "chamados_ti.db"
OUTPUT = BASE_DIR / "data" / "chamados_ti_clean.csv"


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Banco não encontrado: {DB_PATH}\nExecute: python scripts/etl_pipeline.py"
        )

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM chamados", conn)
    conn.close()

    df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    print(f"Exportado: {OUTPUT}")
    print(f"Registros: {len(df)}")


if __name__ == "__main__":
    main()
