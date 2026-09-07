# LÍNEA DE TIEMPO — MARC Y AURORA

> Construida a partir del CONTENIDO REAL de los documentos maestros (MASTER_DECISIONS, MASTER_CHANGELOG, MASTER_CONTEXT, ACCIONES_EJECUTADAS_MARC).
> Etiquetas: [C]=CONFIRMADO en documento · [A]=fecha según nombre de archivo (ambigua) · [M]=fecha de modificación del archivo (mtime).
> NO se inventan fechas. Las ambiguas se marcan.

---

## FASE 0 — ANTECEDENTES (mayo 2026)

| Fecha | Acontecimiento | Fuente |
|---|---|---|
| 2026-05-04 [A] | Documentos Doc1 (Informe Sesión), Doc2 (Plan Operativo), Doc3 (Contexto Escala) fechados "04-05-26" en el nombre. Carpeta `MARC/1 DÍA 04-05-2026/`. ⚠️ Fecha ambigua: podría ser 4-mayo o 4-agosto; el nombre dice 04-05-26. | `MARC/1 DÍA 04-05-2026/*.pdf` |

---

## FASE 1 — ARRANQUE DEL PROYECTO (4-5 agosto 2026)

| Fecha | Acontecimiento | Fuente |
|---|---|---|
| 2026-08-04 [C] | **SESIÓN INICIAL** con Marc. Informe de sesión generado. Primeras notas de voz (PTT-20260804). | `INFORME_SESION INICIAL_04-08-2026.pdf`, transcripts |
| 2026-08-05 [C] | **D-001:** Marc elige a Sebastián como operador digital (tras 3 candidatos). | MASTER_DECISIONS |
| 2026-08-07 / 08-10 [M] | Más notas de voz de Marc (PTT-20260807, PTT-20260810). | transcripts |

---

## FASE 2 — ACUERDO ECONÓMICO Y PLANIFICACIÓN (12-15 agosto 2026)

| Fecha | Acontecimiento | Fuente |
|---|---|---|
| 2026-08-12 [C] | **D-002:** Estructura económica fijada: 400€/mes fijo + comisiones SOLO casillas violetas del XLSX. Informes de Sebastián (DOC-20260812-WA0062/WA0125). | MASTER_DECISIONS, `Oferta_Colaboracion_Sebastian.xlsx` |
| 2026-08-14 [C] | **D-003:** Se confirma reunión con Escala con Ads para el miércoles 20/8 a las 16:00. Notas de voz (PTT-20260814). | MASTER_DECISIONS |
| 2026-08-15 [M] | Notas de voz (PTT-20260815). | transcripts |

---

## FASE 3 — AUDITORÍA Y ESTRATEGIA (16-17 agosto 2026)

| Fecha | Acontecimiento | Fuente |
|---|---|---|
| 2026-08-16 [C] | **Auditoría documental global** (agente Cline/Copilot): mapas, inventario, duplicados, contradicciones. Creada estructura `AUDITORIA_GLOBAL/`. | `AUDITORIA_GLOBAL/00_INDICE_AUDITORIA.md` |
| 2026-08-17 [C] | **D-004:** Marc aprueba la estructura MARC-PROJECT del agente ("me parece perfecto"). **D-013/14/15:** metodología preservar→ordenar→verificar→decidir→ejecutar. **Credenciales de Aurora recibidas.** Notas de voz (PTT-20260817). | MASTER_DECISIONS, MASTER_CONTEXT |
| 2026-08-17 [C] | **Estrategia por fases aceptada por Marc:** FASE 1 (agosto) Instagram vivo · FASE 2 (septiembre) lanzamiento con Escala · FASE 3 (octubre+) APP/web/setter. | MASTER_CONTEXT §4 |

---

## FASE 4 — EJECUCIÓN INSTAGRAM MARC (18-19 agosto 2026)

| Fecha | Acontecimiento | Fuente |
|---|---|---|
| 2026-08-18 [C] | **D-005:** Instagram = prioridad absoluta (Marc lo reclama 3×). **D-006:** perfil de negocio = @centro_de_bienestar_inanis. **D-007/008:** seguridad de credenciales + preservar docs previos. | MASTER_DECISIONS |
| 2026-08-18 [C] | **Login IG Marc RESUELTO** (cuenta real = @marcsouza.7). **BIO optimizada y verificada.** Consolidación del workspace a sistema MASTER (README + 9 MASTER_*.md). 12 imágenes IA generadas. Reunión con Marc por la noche. | MASTER_CHANGELOG, ACCIONES #001-#009 |
| 2026-08-19 [C] | **Configuración profesional completa** (email, tel, contacto, visibilidad, categoría). **Protección anti-spam** (filtro + 30 palabras). **NOTA de Instagram publicada.** QR descargado. Baseline de insights (29 visualizaciones/30d). Post Krishnamurti = 11 vistas, 81.8% no-seguidores. 31-32 acciones registradas. | MASTER_CHANGELOG, ACCIONES #018-#032 |

---

## FASE 5 — REUNIÓN ESCALA Y CONTINUIDAD (20-23 agosto 2026)

| Fecha | Acontecimiento | Fuente |
|---|---|---|
| 2026-08-20 [C] | **Reunión con Escala con Ads** (16:00). Guía de reunión preparada. | `03_ESCALA/GUIA_REUNION_ESCALA_2026-08-20.md` |
| 2026-08-23 [C] | **NOTA renovada** (ciclo 24h). Crecimiento detectado: visualizaciones 29→41 (+41%). Lotes de contenido 2 y 3 creados (C-006..C-009, R-002, R-003, stories semana 2). Acciones #033-#045. **Sistema de archivo documental creado (este documento).** | ACCIONES #033-#045, MASTER_STATUS |

---

## HITOS FUTUROS PLANIFICADOS [C — MASTER_CONTEXT]

| Fecha prevista | Hito |
|---|---|
| Septiembre 2026 | Lanzamiento DESPIERTA (Marc, 1.497€) y SOBERANÍA VITAL (Aurora, 997€) con Escala. Inversión ads ~750€/lanzamiento. |
| Octubre 2026+ | APP MVP (Glide), renovación web, setter, Facebook, YouTube. |

---

## ⚠️ AMBIGÜEDADES DE FECHA DETECTADAS

1. **Carpeta `MARC/1 DÍA 04-05-2026/`** y archivos `*_04-05-26.pdf`: la fecha literal es 4-mayo-2026, pero el proyecto arranca el 4-agosto-2026. Posible error de tipeo (04-05 vs 04-08) o convención distinta. **Requiere confirmación de Marc/Sebastián.** No se asume ninguna.
2. **187 documentos** usan fecha de modificación del archivo (mtime) como aproximación porque el nombre no contiene fecha. Son fechas reales del disco, no del contenido.

---

*Generado: 2026-08-23 · Archivista digital. Los originales no fueron modificados.*
