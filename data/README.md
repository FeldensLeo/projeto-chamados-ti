# Pasta de dados

Arquivos gerados pelos scripts (não versionados no Git):

| Arquivo | Gerado por |
|---------|------------|
| `chamados_ti_raw.csv` | `python scripts/generate_data.py` |
| `chamados_ti.db` | `python scripts/etl_pipeline.py` |
| `chamados_ti_clean.csv` | `python scripts/export_for_powerbi.py` |
