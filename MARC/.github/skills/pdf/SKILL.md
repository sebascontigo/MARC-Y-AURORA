---
name: pdf
description: "Leer, extraer texto/tablas y generar PDFs en Python. Usar cuando la tarea implique archivos .pdf: extracción de texto, tablas, metadatos, fusión/división o creación de PDFs."
---

# Skill: PDF

Stack verificado en este equipo (Python 3.12): `pdfplumber 0.11.10`, `pypdf 6.16.1`, `Pillow 12.3.0`.

## Extraer texto y tablas

```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
        tables = page.extract_tables()  # lista de listas
```

## Metadatos / fusión / división

```python
from pypdf import PdfReader, PdfWriter
reader = PdfReader("doc.pdf")
print(reader.metadata, len(reader.pages))
writer = PdfWriter()
writer.append("doc1.pdf"); writer.append("doc2.pdf")
with open("merged.pdf", "wb") as f: writer.write(f)
```

## Reglas

- PDFs escaneados sin capa de texto: informar que requiere OCR (no intentar extracción vacía).
- No modificar el original: trabajar sobre copias.
