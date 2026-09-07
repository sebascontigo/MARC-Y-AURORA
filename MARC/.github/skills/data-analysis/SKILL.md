---
name: data-analysis
description: "Análisis de datos: perfilado, limpieza, agregaciones y generación de informes a partir de CSV/Excel/JSON/SQLite con pandas y SQL. Usar ante preguntas sobre datos del proyecto MARC."
---

# Skill: Data Analysis

Stack verificado: Python 3.12, `pandas 3.0.5`, `openpyxl 3.1.5`; SQLite vía MCP `sqlite-marc` (workspace) y `sqlite` (usuario), además del módulo estándar `sqlite3`.

## Pipeline estándar

```python
import pandas as pd
df = pd.read_csv("datos.csv")
# 1. Perfil
print(df.info()); print(df.isna().sum())
# 2. Limpieza (sobre copia)
df = df.drop_duplicates().astype({"fecha": "datetime64[ns]"})
# 3. Agregación
resumen = df.groupby("categoria")["valor"].agg(["count", "mean", "sum"])
# 4. Salida
resumen.to_csv("resumen.csv", encoding="utf-8-sig")  # o to_xlsx / sqlite
```

## SQLite (MCP sqlite-marc)

Base de datos del workspace: `.mcp-sqlite/marc-data.db`. Usar las tools del servidor MCP para consultas rápidas; para análisis pesado, exportar a DataFrame:

```python
import sqlite3, pandas as pd
con = sqlite3.connect(".mcp-sqlite/marc-data.db")
df = pd.read_sql_query("SELECT * FROM tabla", con)
```

## Reglas

- No destruir el original: analizar sobre copias o en solo lectura.
- Declarar el tratamiento de nulos/duplicados en el informe.
- Cifras clave: doble verificación por una vía independiente cuando sea barato.
