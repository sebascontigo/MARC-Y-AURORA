---
name: docx
description: "Crear y leer documentos Word (.docx) con python-docx. Usar para generar informes con títulos, tablas e imágenes o para extraer texto de .docx."
---

# Skill: DOCX

Stack verificado: `python-docx 1.2.0`.

## Crear documento

```python
from docx import Document
from docx.shared import Pt
doc = Document()
doc.add_heading("Informe MARC", level=0)
doc.add_paragraph("Texto normal.")
table = doc.add_table(rows=2, cols=2, style="Table Grid")
table.cell(0, 0).text = "Campo"
doc.save("informe.docx")
```

## Leer documento

```python
from docx import Document
doc = Document("informe.docx")
for p in doc.paragraphs:
    if p.text.strip(): print(p.text)
for t in doc.tables:
    for row in t.rows:
        print([c.text for c in row.cells])
```

## Reglas

- python-docx no lee .doc antiguo: si aparece .doc, informar que requiere conversión previa.
- Las imágenes se insertan con `doc.add_picture(ruta, width=...)`.
