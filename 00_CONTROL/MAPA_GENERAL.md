# MAPA GENERAL — WORKSPACE MARC Y AURORA

> **Fecha:** 2026-08-18 · **Agente:** Agente Operativo Principal
> **Regla:** este mapa describe lo que HAY. Lo que falta se marca `[NO ENCONTRADO EN WORKSPACE]` o `[PENDIENTE CREAR]` — nunca se inventa.
> **Compañero de este documento:** `INVENTARIO_MAESTRO.md` (el qué) y `CENTRO_DE_CONTROL.md` (el estado vivo).

---

## 1. ESTRUCTURA ACTUAL (lo que existe hoy)

```
MARC Y AURORA/                          ← raíz del workspace
│
├── 00_CONTROL/                         ← 🆕 CREADO ESTA SESIÓN (sistema de control maestro)
│   ├── INVENTARIO_MAESTRO.md           ← inventario clasificado A-F + hallazgos
│   ├── INVENTARIO_COMPLETO.csv         ← 425 filas, una por archivo (regenerable)
│   ├── MAPA_GENERAL.md                 ← este documento
│   └── _gen_inventario.py              ← script de regeneración del CSV
│
├── AUDITORIA_GLOBAL/                   ← trabajo de auditoría previo (Cline 16/8 + Copilot)
│   ├── 00_AUDITORIA_MAESTRA_COMPLETA.md   ← auditoría Cline (~61% completada)
│   ├── 00_INDICE_AUDITORIA.md / 00_INDICE_MAESTRO/
│   ├── 01_MAPA_CARPETAS.md … 16_CONCLUSIONES.md   ← mapas temáticos Cline
│   ├── 17_ANALISIS_IMAGENES_FASE2.md
│   ├── 18_DOCUMENTOS_RECUPERADOS_FASE2.md  ← IMPODERATE + DOC-WA0125 completos
│   ├── 20_INVENTARIO_TOTAL_ARCHIVOS.csv (+.bak)  ← inventario Cline (pre-18/8)
│   ├── 01_MARC/ … 15_PENDIENTES/       ← subcarpetas mayormente PLACEHOLDER
│   └── OTROS DOCUMENTOS POR ORDENAR/
│       ├── 00_CONTINUIDAD_ESTADO.md    ← ⚓ ANCLA DE ESTADO (no renombrar)
│       ├── 00_MAPA_MAESTRO_MARC_AURORA.md  ← ⚓ ANCLA (no renombrar)
│       ├── ROADMAP_30_DIAS.md          ← plan 30 días desde 16/8
│       └── 01_PROMPTS_PARA_AGENTES.md  ← prompts para chats recuperados
│
├── MARC/                               ← cliente MARC (359 archivos)
│   ├── AGENTS.md                       ← instrucciones maestras de agentes (entorno anterior)
│   ├── 00_AUDITORIA_MAESTRA/           ← fichas de auditoría MARC
│   ├── 01_Contexto_Alineacion/         ← Doc2, Doc3, Plan Final, Alineación, Marc.pdf
│   ├── 02_Informes_Sesiones/           ← Doc1 (acta sesión #1)
│   ├── 1 DÍA 04-05-2026/               ← PDFs de entrega a Marc (Doc1/2/3 diseño final)
│   ├── Chat de WhatsApp con MARC (ÚLTIMO EL MÁS RECIENTE)/  ← ⭐ FUENTE PRIMARIA VIGENTE
│   │   └── Chat de WhatsApp con Marc Souza Gil/
│   │       ├── Chat…txt (781 líneas, 24/7→18/8)
│   │       ├── Adjuntos: contrato IE6, IMPODERATE, Info básic, XLSX oferta,
│   │       │   DOC-WA0062, DOC-WA0125, Analisis App GEMINI, CVREDES, Doc1/2/3 PDF
│   │       └── 13 OPUS nuevos del 17/8 (SIN transcribir)
│   ├── Chat de WhatsApp con MARC/      ← export antiguo (hasta 15/8) + wav/ + transcripts/ (27)
│   ├── .github/                        ← agents (01_SUPER_AGENT + 13), hooks, skills (infra anterior)
│   ├── .mcp-sqlite/marc-data.db        ← 0 bytes (sin datos)
│   ├── 13_PREGUNTAS_PARA_MARC.md / 15_REUNION_BRIEF_MARC.md / MARC_REUNION_BRIEF.md
│   └── ~13 imágenes JPG del proyecto
│
├── AURORA/                             ← cliente AURORA (37 archivos)
│   └── 00_AUDITORIA_MAESTRA/           ← 36 fichas MD (220-916 bytes, formato esqueleto)
│       (00_RESUMEN … 18_FUENTES_Y_EVIDENCIAS)
│
├── MARC_Proyecto_Entrega_2026/         ← estructura de ENTREGA a Marc (17-18/8)
│   ├── 00_INDEX/MANIFIESTO_WORKSPACE.md
│   ├── 01_OFICIAL/OPERACION/Doc2…md
│   ├── 02_CONTEXTO/NEGOCIO/Doc3…md
│   ├── 04_AUDITORIAS/Doc1…md
│   ├── 06_PROMPTS/ENTREGA_MENSAJE_1/2/3.md
│   └── 09_REFERENCIA/CV_SEBASTIAN.txt
│
├── Chat de WhatsApp con +34 722 39 89 89/   ← 🔴 chat Aurora (credenciales en texto plano)
├── Chat de WhatsApp con +34 722 39 89 89.zip
└── .mimosa/                            ← infraestructura de escaneo (no tocar)
```

---

## 2. QUÉ HAY EN CADA ZONA (resumen ejecutivo)

| Zona | Qué contiene | Estado |
|---|---|---|
| MARC/01_Contexto_Alineacion | Los 3 documentos fundacionales + alineación 13/8 | 🟢 OPERATIVO |
| MARC/Chat…(ÚLTIMO) | Toda la historia reciente: decisión, precios, Escala, urgencia IG | 🟢 FUENTE DE VERDAD |
| MARC/Chat…(antiguo) | Historia + 27 audios + 27 transcripciones | 🟢 HISTÓRICO |
| AURORA/00_AUDITORIA_MAESTRA | 36 fichas esqueleto: la mayoría dice [NO CONSTA] | 🟡 EN PROGRESO (plantilla, sin sustancia) |
| AUDITORIA_GLOBAL | Auditoría Cline/Copilot: mapas, duplicados, contradicciones, línea de tiempo | 🟡 EN PROGRESO (~61%) |
| MARC_Proyecto_Entrega_2026 | Paquete entregable Doc1/2/3 + mensajes de entrega + CV | 🟢 OPERATIVO |
| Chat +34 722… | Credenciales Aurora + búsqueda de habitación | 🔴 SENSIBLE |

---

## 3. LO QUE FALTA (marcado, no inventado)

### Documentos/activos NO presentes en el workspace

| Elemento | Dónde debería estar | Estado |
|---|---|---|
| 01_Despierta_Analisis_Estrategico_y_Mercado.pdf (enviado 17/8) | MARC/03_Despierta/ | [NO ENCONTRADO EN WORKSPACE] — solo en WhatsApp |
| 02_Despierta_Oferta_Precio_1497_y_Modelo_Rentable.pdf (17/8) | MARC/03_Despierta/ | [NO ENCONTRADO EN WORKSPACE] |
| 03_Despierta_App_IA_Marketing_y_Riesgos.pdf (17/8) | MARC/03_Despierta/ | [NO ENCONTRADO EN WORKSPACE] |
| Contenido Google Drive (carpeta Escala + Documentos Aurora) | — | [BLOQUEADO — sin acceso/credenciales] |
| Google Doc Escala (docs.google.com/document/d/1Tp5-…) | — | [BLOQUEADO — requiere login] |
| Acceso Instagram Marc (usuario) | — | [PENDIENTE — Marc preguntó 3× por la intención; no consta handle en workspace] |
| Acceso GHL | — | [PENDIENTE] |
| Acceso Meta Business / Ads | — | [PENDIENTE] |
| Web reconecta-t.net (credenciales hosting) | — | [PENDIENTE] |
| 8 vídeos/ángulos de Escala | — | [NO ENCONTRADO EN WORKSPACE] |
| Testimonios de alumnos | — | [NO ENCONTRADO EN WORKSPACE] (Aurora tiene material en Drive según mapa maestro) |
| Brand kit / assets de marca | — | [NO ENCONTRADO EN WORKSPACE] |
| Contrato firmado Sebastián-Marc | — | [NO ENCONTRADO EN WORKSPACE] — riesgo #1 de la auditoría Cline |

### Carpetas/entregables pendientes de crear (aprobados en prompts del operador)

`00_CONTROL/` ampliación (CENTRO_DE_CONTROL, TASKS, DECISIONS, CHANGELOG, SESION_2026-08-18, INFORME_AUDITORIA_INICIAL), `MARC/03_Despierta/`, `MARC/04_Instagram/`, `03_ESCALA/`, `06_WEB/`, `07_APP_DESPIERTA/`, `08_AUTOMATIZACIONES/`, `09_OPERACIONES/` — se crean en FASE B ampliada e I/J de esta sesión.

---

## 4. REGLAS DE ESTRUCTURA (vigentes)

1. **MARC y AURORA siempre separados.** Lo compartido va a AUDITORIA_GLOBAL o 00_CONTROL con etiqueta SHARED.
2. **No renombrar ni mover** `00_CONTINUIDAD_ESTADO.md`, `00_MAPA_MAESTRO_MARC_AURORA.md` (anclas de estado del sistema anterior).
3. **No borrar duplicados**: se marcan en el inventario y se conserva la copia; la fuente de verdad se declara en `INVENTARIO_MAESTRO.md` §7.
4. **Credenciales**: nunca copiarlas a documentos. Solo SERVICIO/TIPO/UBICACIÓN/ESTADO.
5. **Los exports de WhatsApp no se editan**: son evidencia bruta. Cualquier procesamiento (transcripciones, resúmenes) va en archivos aparte.
6. Todo cambio de estructura se registra en `00_CONTROL/CHANGELOG.md`.
