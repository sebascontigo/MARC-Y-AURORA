# MASTER_ASSETS — INVENTARIO DE ACTIVOS

> **Actualizado:** 2026-09-06 (orden de la raíz: informes fechados a `ARCHIVO_DOCUMENTAL/02_INFORMES/`) · Revisado y ampliado **2026-09-05** (verificación por ejecución real).
> 3.729 archivos / 3,4 GB inventariados (carpetas sin medios binarios). Detalle completo fila a fila:
> catálogo: `00_CONTROL/AUDITORIA_100_2026-09-05/INVENTARIO.csv`
> Clasificación original: A=docs clave · B=conversaciones/audio · C=media · D=trabajo/auditoría · E=infra · F=vacíos

## UBICACIÓN DE LOS INFORMES FECHADOS (6-sep)

| Informe                            | Dónde estaba | Dónde está ahora                  |
| ---------------------------------- | ------------ | --------------------------------- |
| `TAREAS_SEBASTIAN_HOY.md` (25-ago) | raíz         | `ARCHIVO_DOCUMENTAL/02_INFORMES/` |
| `ENTREGA_HOY_2026-08-25.md`        | raíz         | `ARCHIVO_DOCUMENTAL/02_INFORMES/` |
| `INFORME_FINAL_2026-08-28.md`      | raíz         | `ARCHIVO_DOCUMENTAL/02_INFORMES/` |
| `INFORME_100_2026-09-05.md`        | raíz         | `ARCHIVO_DOCUMENTAL/02_INFORMES/` |

> Movimiento sin borrados, con verificación sha256 y manifiesto: `ARCHIVO_DOCUMENTAL/02_INFORMES/MANIFIESTO_MOVIMIENTO_2026-09-06.md` · Rollback: `python 00_CONTROL/_ordenar_raiz.py --rollback`

## VERIFICACIÓN DEL 5-SEP (assets clave comprobados por ejecución)

| Activo                                      | Verificación      | Resultado                                                                                         |
| ------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------- |
| 4 reels finales (GABI, VICENT, ELENA, ANA)  | `ffprobe`         | **OK**: 1080×1920, 30,1 s, H.264, con audio, 1,9-2,2 MB (+ `_v2` de 3,4-5,1 MB, 5-sep)            |
| Reels fuente `VERSIONES_WEB`                | `ffprobe`         | 720×406, 22-37 min (pista horizontal, NO publicable como reel)                                    |
| Post/story lanzamiento MARC y AURORA        | Pillow            | **OK**: ambos post 1080×1080, ambas stories 1080×1920                                             |
| 6 portadas MARC + 3 AURORA                  | Pillow            | **OK**: todas 1080×1080                                                                           |
| 4 plantillas brand kit MARC                 | Pillow            | **OK**: POST/CARRUSEL 1080×1350, STORY 1080×1920, QUOTE 1080×1080                                 |
| 12 fondos IA MARC + 12 AURORA (`IA_DRAFTS`) | existentes        | pendientes de revisión visual humana (sin cambios)                                                |
| QR `QR_MARCSOUZA7.png`                      | Pillow            | **OK** 235×270; **se sirve en producción de la landing (HTTP 200)**                               |
| Paquetes limpios de entrega                 | zipfile + testzip | **3 OK** (sin `.bak`, sin `.py` interno, sin `.netlify`): `00_CONTROL/PAQUETES_ENTREGA_20260905/` |
| Archivo interno en producción               | HTTP              | ⚠️ `_verificar_deploy.py` y `.bak_20260904_v1` responden 200 → **B-9** (redesplegar limpio)       |

## Resumen por categoría (inventario 18/8)

| Cat | Nº  | Descripción                                                                                      |
| --- | --- | ------------------------------------------------------------------------------------------------ |
| A   | 35  | Documentos clave (Doc1/2/3, XLSX oferta, Info básic, IMPODERATE, GEMINI, contrato IE6, CVREDES…) |
| B   | 252 | Conversaciones WhatsApp + 69 notas de voz OPUS (todas transcritas)                               |
| C   | 44  | Media: 14 imágenes de Marc + 12 imágenes IA generadas + PDFs visuales                            |
| D   | 120 | Trabajo de auditoría y entregables (AUDITORIA_GLOBAL, 00_CONTROL, fichas)                        |
| E   | 37  | Infraestructura (.github agents/skills/hooks, .mcp, scripts del agente)                          |
| F   | 3   | Vacíos (0 bytes): MARC_IMAGENES, marc-data.db, Plan_Marc_Operativo_Final.md                      |

## ACTIVOS DE CONTENIDO — MARC

| Activo                                                         | Ubicación                                                                               | Estado                                           |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **Programa completo DESPIERTA (13 módulos)**                   | `MARC/20_PRODUCTO_DESPIERTA/` (CURRICULO/HERRAMIENTAS/MENTORIA/CHARLAS/WEBINAR/PROCESO) | ✅ Integrado 28/8                                |
| **Testimonios en vídeo (ANA, ELENA, GABI, VICENT)**            | `MARC/21_TESTIMONIOS/VIDEOS/` + VERSIONES_WEB + CLIPS_REELS                             | ✅ Procesados 28/8                               |
| **E-book lead magnet «La Loca en Tu Cabeza»**                  | `MARC/22_LEAD_MAGNET_EBOOK/`                                                            | ✅ ES+EN+portadas                                |
| **6 análisis estratégicos IA (ofertas, gamificación, setter)** | `MARC/23_ESTRATEGIA_NEGOCIO/01_ANALISIS_IA/`                                            | ✅ 28/8                                          |
| **Podcasts Reconecta-t + taller Emprendimiento**               | `MARC/24_MEDIA/`                                                                        | ✅ 28/8                                          |
| **CV + diplomas de Marc**                                      | `MARC/25_MARCA_PERSONAL/`                                                               | ✅ 28/8                                          |
| **Portadas destacadas IG (6)**                                 | `MARC/04_Instagram/ASSETS/HIGHLIGHT_COVERS/`                                            | ✅ 28/8                                          |
| Chat vigente Marc (91 KB, hasta 18/8)                          | MARC/Chat…(ÚLTIMO EL MÁS RECIENTE)/                                                     | [C] fuente de verdad                             |
| 69 notas de voz + transcripts                                  | MARC/Chat…/transcripts*/                                                                | [C] todas transcritas                            |
| 14 imágenes recibidas de Marc (reels, info)                    | MARC/Chat…/IMG-*.jpg                                                                    | [C] sin analizar visualmente (agente solo-texto) |
| 3 PDFs Despierta + GEMINI + IMPODERATE                         | MARC/Chat…/                                                                             | [C]                                              |
| Contrato IE6 Escala (PDF)                                      | MARC/Chat…/                                                                             | [C]                                              |
| Oferta_Colaboracion_Sebastian.xlsx                             | MARC/Chat…/                                                                             | [C] celdas violetas = vinculantes                |
| **12 fondos IA generados (1080px)**                            | MARC/04_Instagram/ASSETS/IA_DRAFTS/                                                     | [C] pendiente revisión visual humana             |
| Calendario contenido sem 1-2                                   | MARC/04_Instagram/CONTENT_CALENDAR.md                                                   | Borrador                                         |
| 3 propuestas de bio                                            | MARC/04_Instagram/AUDITORIA_INSTAGRAM_MARC.md                                           | Borrador (D-009)                                 |

## ACTIVOS DE CONTENIDO — AURORA

| Activo                                                                 | Ubicación                    | Estado                   |
| ---------------------------------------------------------------------- | ---------------------------- | ------------------------ |
| Chat Aurora (1,7 KB, hasta 17/8)                                       | AURORA/Chat…/                | [C] muy escaso           |
| 1 multimedia omitido (17/8 17:07)                                      | NO EN WORKSPACE              | [P] identificar          |
| Drive "Documentos Aurora" (imágenes, testimonios, ventas, metodología) | Google Drive                 | [P] BLOQUEADO            |
| 36 fichas esqueleto auditoría                                          | AURORA/00_AUDITORIA_MAESTRA/ | [C] pero desactualizadas |

## ACTIVOS COMPARTIDOS / ESCALA

| Activo                                 | Ubicación                                | Estado        |
| -------------------------------------- | ---------------------------------------- | ------------- |
| Doc1/Doc2/Doc3 (entrega oficial)       | MARC_Proyecto_Entrega_2026/ + MARC/01-02 | [C]           |
| Documento Alineación + Marc.pdf        | MARC/01_Contexto_Alineacion/             | [C]           |
| Agenda reunión Escala 20/8             | 03_ESCALA/                               | [C]           |
| Drive Escala (Google Doc + materiales) | Google Drive                             | [P] BLOQUEADO |
| 8 ángulos de vídeo                     | NO ENTREGADOS                            | [P]           |
| Testimonios (Sony, Adriana)            | NO ENTREGADOS                            | [P]           |

## QUÉ FALTA (activos críticos ausentes)

1. 8 ángulos de vídeo de Escala [P]
2. Testimonios en vídeo/texto [P]
3. Brand kit de Marc (logo, colores, fuentes) [P]
4. Material primario de Aurora (Drive) [P]
5. Landing GHL (la construye Escala) [P]
