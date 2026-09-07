---
name: xlsx-csv
description: "Procesar hojas de cálculo Excel y CSV: leer, analizar, transformar y generar .xlsx/.csv con pandas/openpyxl. Usar ante libros Excel, CSV o análisis tabular."
---

# Skill: XLSX / CSV

Stack verificado: `pandas 3.0.5`, `openpyxl 3.1.5`.

## Lectura y análisis

```python
import pandas as pd
df = pd.read_excel("libro.xlsx", sheet_name=None)   # dict hojas -> DataFrame (None = todas)
df = pd.read_csv("datos.csv", sep=None, encoding="utf-8-sig")
print(df.shape); print(df.dtypes); print(df.describe())
```

## Escritura

```python
df.to_excel("salida.xlsx", index=False, sheet_name="Datos")
df.to_csv("salida.csv", index=False, encoding="utf-8-sig")  # utf-8-sig para Excel
```

## Formato avanzado (openpyxl)

```python
from openpyxl import Workbook
wb = Workbook(); ws = wb.active
ws["A1"] = "Total"; ws["B1"] = 42
wb.save("formato.xlsx")
```

## Reglas

- Perfilar datos (nulos, duplicados, tipos) antes de transformar.
- Fórmulas en Excel se preservan al reescribir solo con openpyxl; pandas las convierte en valores.
- CSV con acentos/ñ: usar `utf-8-sig` para compatibilidad con Excel.
