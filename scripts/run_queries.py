"""Executa as consultas analíticas e exibe os resultados no terminal."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "chamados_ti.db"


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("1. Total de chamados:")
    print(cur.execute("SELECT COUNT(*) FROM chamados").fetchone()[0])

    print("\n2. Analista com mais chamados resolvidos:")
    print(
        cur.execute(
            """
            SELECT analista, COUNT(*) AS total
            FROM chamados
            WHERE status = 'Fechado'
            GROUP BY analista
            ORDER BY total DESC
            LIMIT 1
            """
        ).fetchone()
    )

    print("\n3. Categoria com mais chamados:")
    print(
        cur.execute(
            """
            SELECT categoria, COUNT(*) AS total
            FROM chamados
            GROUP BY categoria
            ORDER BY total DESC
            LIMIT 1
            """
        ).fetchone()
    )

    print("\n4. Tempo médio de resolução (horas):")
    print(
        cur.execute(
            """
            SELECT ROUND(AVG(tempo_resolucao_horas), 2)
            FROM chamados
            WHERE status = 'Fechado'
            """
        ).fetchone()[0]
    )

    print("\n5. Chamados por status:")
    for row in cur.execute(
        "SELECT status, COUNT(*) FROM chamados GROUP BY status ORDER BY 2 DESC"
    ):
        print(f"   {row[0]}: {row[1]}")

    conn.close()


if __name__ == "__main__":
    main()
