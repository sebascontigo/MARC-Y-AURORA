# ROADMAP 30 DÍAS — MARC Y AURORA
> Proyecto: gestión de redes sociales, marketing y auditoría documental para Marc y Aurora.
> Dueño de agencia: Sebastián. Clientes: Marc (formación premium) y Aurora (metodología/contenido).
> Fecha inicio: 2026-08-16 · Generado por perfil LAB

---

## ESTADO ACTUAL (punto de partida real)

| Área | Estado | Detalle |
|---|---|---|
| Auditoría local MARC | ✅ Completada | MDs, PDFs, DOCX, XLSX clasificados (`MARC/00_AUDITORIA_MAESTRA`) |
| Auditoría local AURORA | ✅ Completada | 36 fichas en `AURORA/00_AUDITORIA_MAESTRA` |
| AUDITORIA_GLOBAL | ⚠️ Parcial | Índice y mapas creados; subcarpetas 03-15 vacías (placeholders) |
| Google Drive | 🚫 Bloqueado | Faltan credenciales/acceso compartido |
| Audios WhatsApp (27 OPUS) | ⚠️ Pendiente |Convertidos a WAV ya; falta transcripción (ASR/Whisper) |
| Imágenes (≈13 JPG) | ⚠️ Pendiente | Falta análisis visual |
| Duplicados / contradicciones | ⚠️ Parcial | `05_DUPLICADOS` y `06_CONTRADICCIONES` sin resolver |
| Alcance/KPI/contrato | 🚫 No definido | Riesgo #1: alcance ampliado sin límites |

---

## SEMANA 1 (Días 1-7): AUDITORÍA COMPLETA + ORGANIZACIÓN

**Meta: cerrar todos los pendientes de la auditoría y dejar la estructura de carpetas operativa.**

| Día | Tarea | Responsable |
|---|---|---|
| 1 | Reunión kickoff con Marc: confirmar alcance, objetivos y prioridades | Sebastián + Marc |
| 1 | Instalar Whisper local (`pip install openai-whisper`) y transcribir los 27 WAV ya convertidos | Sebastián (agente) |
| 2 | Reunión con Aurora: accesos a Google Drive y alcance | Sebastián + Aurora |
| 2 | Autenticar Google Drive (MCP o credenciales) y lanzar comparación Local vs Drive | Sebastián (agente) |
| 3 | Analizar las ≈13 imágenes JPG (visión/OCR) y documentar hallazgos | Sebastián (agente) |
| 3 | Integrar transcripciones al inventario maestro y actualizar `08_LINEA_TIEMPO` | Sebastián (agente) |
| 4 | Resolver duplicados (mover a `05_DUPLICADOS` tras validar) | Sebastián + Marc |
| 4 | Resolver contradicciones documentadas (decisión con cliente) | Sebastián + Marc |
| 5 | Completar subcarpetas vacías de AUDITORIA_GLOBAL (03-15) con contenido real | Sebastián (agente) |
| 5 | Regenerar `20_INVENTARIO_TOTAL_ARCHIVOS.csv` definitivo | Sebastián (agente) |
| 6 | Definir estructura de carpetas definitiva por cliente (reorganización física) | Sebastián |
| 6 | Documentar la nueva estructura en `00_MAPA_MAESTRO_MARC_AURORA.md` | Sebastián (agente) |
| 7 | **Hito W1:** entregar informe de auditoría cerrada a Marc y Aurora | Sebastián |

---

## SEMANA 2 (Días 8-14): BASES DEL NEGOCIO

**Meta: contrato claro, alcance cerrado, KPI definidos y propiedad de canales asignada.**

| Día | Tarea | Responsable |
|---|---|---|
| 8 | Redactar alcance cerrado por cliente (qué SÍ / qué NO incluye) | Sebastián |
| 9 | Firmar/actualizar contrato con Marc con alcance cerrado | Marc |
| 10 | Definir KPI por canal (Instagram, ads, embudo) y línea base | Sebastián + Marc |
| 10 | Definir presupuesto por categoría (ads, herramientas, contenido) | Marc |
| 11 | Auditoría de accesos: Instagram, Meta Ads, Drive, dominios (quién tiene qué) | Sebastián + Aurora |
| 12 | Definir propiedad de cada tarea/canal (matriz RACI) | Sebastián |
| 13 | Definir stack de herramientas definitivo (edición, programación, CRM, reporting) | Sebastián |
| 14 | **Hito W2:** documento `PLAN_NEGOCIO_Y_KPI.md` aprobado por ambos clientes | Sebastián |

---

## SEMANA 3 (Días 15-21): CONTENIDO Y REDES SOCIALES

**Meta: sistema de contenido en marcha para Marc (Instagram) y Aurora.**

| Día | Tarea | Responsable |
|---|---|---|
| 15 | Auditoría extensa del perfil de Instagram de Marc (bio, feed, insights, competencia) | Sebastián (agente) |
| 16 | Definir pilares de contenido y tono de voz por cliente | Sebastián |
| 17 | Calendario editorial mes 1 (20 piezas Marc / 12 Aurora) | Sebastián |
| 18 | Producción lote 1: guiones + grabación (Marc) / curación (Aurora) | Marc + Sebastián |
| 19 | Edición y programación de publicaciones semana 1 | Sebastián |
| 20 | Auditoría de Instagram de Aurora + propuesta de posicionamiento | Sebastián (agente) |
| 21 | **Hito W3:** primer lote publicado y calendario cargado en herramienta de programación | Sebastián |

---

## SEMANA 4 (Días 22-28): VENTAS, ADS Y AUTOMATIZACIÓN

**Meta: embudo activo, campañas de ads y automatizaciones clave.**

| Día | Tarea | Responsable |
|---|---|---|
| 22 | Revisar embudo actual de Marc (captación → venta) y detectar fugas | Sebastián |
| 23 | Diseñar campaña de ads de pago (segmentación, copys, presupuesto) | Sebastián |
| 24 | Publicar campaña y configurar píxel/conversiones | Sebastián + Marc |
| 25 | Automatizar: bienvenida DM, respuestas, registro de leads | Sebastián (agente) |
| 26 | Script de ventas y materiales de cierre (oferta premium de Marc) | Sebastián |
| 27 | Testimonios: recopilar y producir contenido social proof (Aurora tiene material en Drive) | Aurora + Sebastián |
| 28 | **Hito W4:** embudo + ads activos con seguimiento semanal | Sebastián |

---

## CIERRE (Días 29-30)

| Día | Tarea | Responsable |
|---|---|---|
| 29 | Informe de resultados mes 1: KPI reales vs línea base | Sebastián (agente) |
| 30 | Reunión de revisión con Marc y Aurora + plan mes 2 | Sebastián + Marc + Aurora |

---

## RIESGOS Y MITIGACIÓN

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Alcance ampliado sin límites (Marc) | 🔴 Alto | Contrato cerrado semana 2; cambios vía change request |
| Google Drive inaccesible | 🔴 Alto | Solicitar acceso día 2; alternativa: export del cliente |
| Transcripciones atrasadas | 🟡 Medio | Whisper local ya preparado (WAVs convertidos) |
| Tareas fuera de contrato ya detectadas | 🟡 Medio | Matriz RACI día 12 |
| Mezcla de documentación entre clientes | 🟡 Medio | Estructuras separadas obligatorias (regla del proyecto) |

---

## REGLAS DE ORGANIZACIÓN DE CARPETAS (vigentes desde ya)

1. MARC y AURORA siempre separados: nunca mezclar materiales ni conclusiones.
2. Todo lo compartido/maestro va en `AUDITORIA_GLOBAL`.
3. Cada cliente mantiene su carpeta con numeración consistente (`00_AUDITORIA_MAESTRA`, `01_...`).
4. Los agentes solo reorganizan previa validación en esta hoja de decisiones.
5. No renombrar `00_CONTINUIDAD_ESTADO.md` ni `00_MAPA_MAESTRO_MARC_AURORA.md`: son los anclas de estado.
