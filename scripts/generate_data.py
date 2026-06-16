"""
Gera um arquivo CSV fictício com chamados de TI da empresa TechNova.

Por que este script existe?
- Em projetos reais, os dados vêm de sistemas externos (APIs, bancos, planilhas).
- Aqui simulamos essa fonte com dados sintéticos para praticar o pipeline ETL.
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

# Caminhos relativos ao diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "chamados_ti_raw.csv"

# Domínios fictícios da TechNova
CLIENTES = [
    "TechNova Matriz",
    "TechNova Filial SP",
    "TechNova Filial RJ",
    "TechNova Filial BH",
    "TechNova Remoto",
]

ANALISTAS = [
    "Ana Silva",
    "Bruno Costa",
    "Carla Mendes",
    "Diego Alves",
    "Elena Rocha",
    "Felipe Nunes",
    "Gabriela Lima",
    "Henrique Dias",
]

CATEGORIAS = [
    "Hardware",
    "Software",
    "Rede",
    "Acesso",
    "E-mail",
    "Impressora",
]

PRIORIDADES = ["Baixa", "Média", "Alta", "Crítica"]
STATUS = ["Aberto", "Em andamento", "Fechado"]

# Pesos para distribuição mais realista
PESO_PRIORIDADE = [0.35, 0.35, 0.20, 0.10]
PESO_STATUS = [0.15, 0.20, 0.65]  # maioria fechada


def gerar_data_abertura() -> datetime:
    """Gera uma data de abertura nos últimos 12 meses."""
    inicio = datetime.now() - timedelta(days=365)
    dias_aleatorios = random.randint(0, 364)
    hora = random.randint(8, 18)
    minuto = random.choice([0, 15, 30, 45])
    return inicio + timedelta(days=dias_aleatorios, hours=hora, minutes=minuto)


def gerar_data_fechamento(abertura: datetime, status: str) -> str | None:
    """
    Chamados abertos/em andamento não têm data de fechamento.
    Chamados fechados recebem uma data entre 1h e 15 dias após abertura.
    """
    if status != "Fechado":
        return None

    horas_resolucao = random.randint(1, 15 * 24)
    fechamento = abertura + timedelta(hours=horas_resolucao)
    return fechamento.strftime("%Y-%m-%d %H:%M:%S")


def gerar_chamados(quantidade: int = 1200) -> pd.DataFrame:
    """Cria o DataFrame com os chamados fictícios."""
    registros = []

    for i in range(1, quantidade + 1):
        status = random.choices(STATUS, weights=PESO_STATUS, k=1)[0]
        abertura = gerar_data_abertura()
        fechamento = gerar_data_fechamento(abertura, status)

        registros.append(
            {
                "id_chamado": f"CH-{i:05d}",
                "cliente": random.choice(CLIENTES),
                "analista": random.choice(ANALISTAS),
                "categoria": random.choice(CATEGORIAS),
                "prioridade": random.choices(PRIORIDADES, weights=PESO_PRIORIDADE, k=1)[0],
                "status": status,
                "data_abertura": abertura.strftime("%Y-%m-%d %H:%M:%S"),
                "data_fechamento": fechamento,
            }
        )

    # Inserir alguns registros inválidos propositalmente para praticar limpeza no ETL
    # (~2% dos dados com problemas)
    for j in range(int(quantidade * 0.02)):
        idx = random.randint(0, len(registros) - 1)
        tipo_erro = random.choice(["data_invalida", "campo_vazio", "status_invalido"])

        if tipo_erro == "data_invalida":
            registros[idx]["data_abertura"] = "data-invalida"
        elif tipo_erro == "campo_vazio":
            registros[idx]["cliente"] = ""
        else:
            registros[idx]["status"] = "Cancelado"  # status fora do domínio esperado

    return pd.DataFrame(registros)


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df = gerar_chamados(1200)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Arquivo gerado com sucesso: {OUTPUT_FILE}")
    print(f"Total de registros: {len(df)}")
    print(f"Colunas: {list(df.columns)}")


if __name__ == "__main__":
    main()
