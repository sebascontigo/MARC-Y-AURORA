# INVENTARIO MAESTRO — WORKSPACE MARC Y AURORA

> **Fecha de generación:** 2026-08-18
> **Agente:** Agente Operativo Principal (sesión ZCode/Qwen3.8-Max)
> **Método:** escaneo recursivo completo del workspace + lectura/verificación de documentos clave
> **Inventario completo (425 filas, una por archivo):** `00_CONTROL/INVENTARIO_COMPLETO.csv`
> **Regenerar CSV:** `python 00_CONTROL/_gen_inventario.py` (desde la raíz del workspace)

---

## 1. RESUMEN CUANTITATIVO

| Métrica | Valor |
|---|---|
| Total de archivos | **425** |
| Tamaño total | ~84 MB |
| Archivos MARC | 359 |
| Archivos AURORA | 37 |
| Archivos COMPARTIDO (AUDITORIA_GLOBAL + chat nuevo) | 28 |
| Archivos INFRA (scripts de este control) | 1 |
| Archivos vacíos (0 bytes) | 3 |
| Archivos con sensibilidad ALTA | 9 |

### Clasificación A–F (según PROMPT 3)

| Cat. | Significado | Nº | Detalle |
|---|---|---|---|
| **A** | Documentos clave del negocio | 35 | Doc1/2/3, contrato IE6, XLSX oferta, IMPODERATE, análisis APP, CVs, DOCX operativos |
| **B** | Conversaciones y audios | 237 | 2 exports de WhatsApp con Marc (TXT+OPUS+WAV+transcripts), chat Aurora (+34 722…), ZIP |
| **C** | Imágenes y multimedia | 32 | JPG/PNG del proyecto MARC |
| **D** | Documentación de trabajo/auditoría | 90 | Auditorías Cline/Copilot, fichas AURORA, mapas, entregables, prompts |
| **E** | Infraestructura/config | 28 | .github agents/hooks/skills, CSVs, configs, scripts |
| **F** | Vacíos/corruptos | 3 | Ver §5 Anomalías |

---

## 2. CATEGORÍA A — DOCUMENTOS CLAVE (tabla completa)

> Regla de lectura: cuando un documento existe en varias copias, la **fuente de verdad vigente** se indica en la columna "Estado". Los duplicados se conservan (principio de no-borrado) pero no se usan como referencia.

| # | Archivo | Ruta | Tipo | Tamaño | Fecha | Proyecto | Persona | Contenido | Importancia | Sensibilidad | Estado | Relación |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | Doc1_Informe_Sesion_Marc(1).md | MARC/02_Informes_Sesiones/ | MD | 8,5KB | 05/08 | MARC | Marc | Acta sesión #1 (04/08): perfil Marc, dolor IG, APP crítica, acuerdos | CRÍTICA | MEDIA | ✅ VIGENTE (versión completa) | A2 es versión previa más corta; A4-A7 son exportaciones PDF |
| A2 | Doc1_Informe_Sesion_Marc.md | MARC/02_Informes_Sesiones/ | MD | 7,4KB | 05/08 | MARC | Marc | Versión previa del acta sesión #1 | ALTA | MEDIA | ⚠️ SUPERADA por A1 | Duplicado parcial |
| A3 | Doc1_Informe_Sesion_Marc.pdf | MARC/02_Informes_Sesiones/ | PDF | 17KB | 05/08 | MARC | Marc | Export PDF del acta | MEDIA | MEDIA | ⚠️ COPIA | — |
| A4 | Doc1_Informe_Sesion_Marc_04-05-26.pdf | MARC/1 DÍA 04-05-2026/ | PDF | 98KB | 05/08 | MARC | Marc | PDF entregado a Marc (diseño final) | ALTA | MEDIA | ✅ COPIA DE ENTREGA | Idéntico en 3 rutas (SHA256 igual según auditoría Cline) |
| A5 | Doc2_Plan_Operativo_Marc.md | MARC/01_Contexto_Alineacion/ | MD | 12KB | 05/08 | MARC | Marc | Plan operativo 3 fases: IG agosto, lanzamiento sept, APP oct | CRÍTICA | MEDIA | ✅ VIGENTE (con salvedad: precios §5 superados por XLSX) | A6 PDF entrega |
| A6 | Doc2_Plan_Operativo_Marc_04-05-26.pdf | MARC/1 DÍA 04-05-2026/ | PDF | 188KB | 05/08 | MARC | Marc | PDF entregado del plan | ALTA | MEDIA | ✅ COPIA DE ENTREGA | Duplicado en 3 rutas |
| A7 | Doc3_Contexto_Escala_Marc.md | MARC/01_Contexto_Alineacion/ | MD | 7,4KB | 05/08 | MARC | Marc | Inteligencia Escala con Ads: Aythami, TheFitDos, método, GHL | CRÍTICA | MEDIA | ✅ VIGENTE | A8 PDF entrega |
| A8 | Doc3_Contexto_Escala_Marc_04-05-26.pdf | MARC/1 DÍA 04-05-2026/ | PDF | 135KB | 05/08 | MARC | Marc | PDF entregado del contexto Escala | ALTA | MEDIA | ✅ COPIA DE ENTREGA | Duplicado en 3 rutas |
| A9 | Plan_Marc_Operativo_Final(1).md | MARC/01_Contexto_Alineacion/ | MD | 5,5KB | 05/08 | MARC | Marc | Unificación Doc1+2+3 resumida | ALTA | MEDIA | ✅ VIGENTE (resumen) | — |
| A10 | Plan_Marc_Operativo_Final.md | MARC/01_Contexto_Alineacion/ | MD | **0B** | 05/08 | MARC | Marc | VACÍO | — | — | 🔴 ANOMALÍA (ver §5) | A9 es la versión válida |
| A11 | Documento_Alineacion_MARC_Sebastian.pdf | MARC/01_Contexto_Alineacion/ | PDF | 161KB | 13/08 | MARC | Marc+Sebastián | Documento de alineación enviado por Marc 11/8 | CRÍTICA | ALTA | 🟡 PENDIENTE LECTURA COMPLETA | Referenciado en chat 11/8 |
| A12 | Marc.pdf | MARC/01_Contexto_Alineacion/ | PDF | 1,2MB | 13/08 | MARC | Marc | Documento extenso enviado por Marc 11/8 | CRÍTICA | ALTA | 🟡 PENDIENTE LECTURA COMPLETA | Posible dossier de negocio |
| A13 | 5.0 IE6 - Contrato de prestación de servicios y garantía de resultados.pdf | MARC/Chat de WhatsApp con MARC (ÚLTIMO…)/ | PDF | 133KB | 11/8 | MARC | Escala/Marc | Contrato Quality Products Fusion LLC: 6 meses, oferta HT, embudo, GHL, ads, 3 sesiones/sem, garantía | CRÍTICA | ALTA (contractual) | ✅ LEÍDO PARCIAL (vía DOC-WA0062) | Duplicado en chat antiguo |
| A14 | INFORME - IMPODERATE.pdf | idem | PDF | 1,2MB | 03/08 | MARC | Marc | Estudio mercado InPodera.ai: programa reprogramación mental a US$1.700, veredicto SÍ 70/100, proyecciones | CRÍTICA | MEDIA | ✅ LEÍDO COMPLETO (537 líneas, por Cline) | Valida viabilidad high-ticket |
| A15 | Info básic para Sebastian.docx | idem | DOCX | 15KB | 11/08 | MARC | Marc | Brief de Marc: Despierta 1.497€/4m, SV 997€/3m, Escala promete ~7.000€ (5+7 ventas), 750€ ads/lanzamiento, sept=2 lanzamientos, oct=4 con Facebook, YouTube a 7-9 meses, web a renovar | CRÍTICA | MEDIA | ✅ LEÍDO COMPLETO (esta sesión) | Fuente de verdad de precios y roadmap comercial |
| A16 | Oferta_Colaboracion_Sebastian.xlsx | idem | XLSX | 16KB | 12/08 | MARC | Sebastián | Estructura retributiva: 400€ fijo + comisiones por canal/producto. **REGLA MARC: solo valen las casillas VIOLETAS** | CRÍTICA | ALTA (contractual) | ✅ LEÍDO COMPLETO + COLORES VERIFICADOS (esta sesión) | Ver §3 desglose violeta |
| A17 | DOC-20260812-WA0062.docx | idem | DOCX | 54KB | 12/08 | MARC | Sebastián | Análisis estratégico Reconecta-T: separar Escala vs Sebastián, 400€ = piloto 30 días, proteger alcance | CRÍTICA | MEDIA | ✅ LEÍDO PARCIAL (esta sesión) | Complemento de A16 |
| A18 | DOC-20260812-WA0125.docx | idem | DOCX | 51KB | 12/08 | MARC | Todos | Documento maestro 27 secciones: funnel, productos, tech, roles, comisiones, KPIs, presupuesto, onboarding 17 items | CRÍTICA | MEDIA | ✅ LEÍDO COMPLETO (por Cline, 1.194 líneas) | El más extenso del proyecto |
| A19 | Analisis App GEMINI.pdf | idem | PDF | 26KB | 17/08 | MARC | Marc | Análisis estratégico APP Despierta: viable, "diamante escondido", B2C 9,99-19,99€/mes, garantía condicionada, clon IA | CRÍTICA | MEDIA | ✅ LEÍDO COMPLETO (esta sesión) | Requisitos APP en Doc2 §3.1 |
| A20 | CVREDES.pdf | idem | PDF | ~9KB | — | MARC | Sebastián | CV de Sebastián para el puesto (ejecutor IG) | ALTA | ALTA (datos personales) | ✅ LEÍDO COMPLETO (esta sesión) | — |
| A21 | Doc1/2/3 + contrato + IMPODERATE + Info básic + XLSX + DOCX (copias) | MARC/Chat de WhatsApp con MARC/ | varios | — | 15/08 | MARC | — | **Export antiguo del chat**: duplicados exactos de A13-A18 | MEDIA | MEDIA | ⚠️ DUPLICADOS (conservar, no usar) | El export "(ÚLTIMO EL MÁS RECIENTE)" es el vigente |
| A22 | Doc2_Plan_Operativo_Marc.md | MARC_Proyecto_Entrega_2026/01_OFICIAL/OPERACION/ | MD | 12KB | 18/08 | MARC | Marc | Copia de entrega del plan | MEDIA | MEDIA | ⚠️ COPIA DE ENTREGA | Igual a A5 |
| A23 | Doc3_Contexto_Escala_Marc.md | MARC_Proyecto_Entrega_2026/02_CONTEXTO/NEGOCIO/ | MD | 7,4KB | 18/08 | MARC | Marc | Copia de entrega del contexto Escala | MEDIA | MEDIA | ⚠️ COPIA DE ENTREGA | Igual a A7 |
| A24 | Doc1_Informe_Sesion_Marc.md | MARC_Proyecto_Entrega_2026/04_AUDITORIAS/ | MD | 8,5KB | 18/08 | MARC | Marc | Copia de entrega del acta | MEDIA | MEDIA | ⚠️ COPIA DE ENTREGA | Igual a A1 |
| A25 | CV_SEBASTIAN.txt | MARC_Proyecto_Entrega_2026/09_REFERENCIA/ | TXT | 2,2KB | 18/08 | MARC | Sebastián | CV "Director de Ejecución Digital" (versión estratégica) | ALTA | ALTA (personal) | ✅ LEÍDO | El manifiesto lo llama "credenciales del operador" ⚠️ revisar redacción |

### ⚠️ DOCUMENTOS AUSENTES [NO ENCONTRADO EN WORKSPACE]

Marc envió por WhatsApp el 17/08 estos PDFs que **NO están exportados al workspace** (solo existen dentro de la app de WhatsApp de Sebastián):

| Documento | Estado | Acción |
|---|---|---|
| 01_Despierta_Analisis_Estrategico_y_Mercado.pdf | [NO ENCONTRADO EN WORKSPACE] | Exportar desde WhatsApp a `MARC/03_Despierta/` |
| 02_Despierta_Oferta_Precio_1497_y_Modelo_Rentable.pdf | [NO ENCONTRADO EN WORKSPACE] | Exportar desde WhatsApp |
| 03_Despierta_App_IA_Marketing_y_Riesgos.pdf | [NO ENCONTRADO EN WORKSPACE] | Exportar desde WhatsApp |

Nota: `Analisis App GEMINI.pdf` (A19) SÍ está y parece ser el análisis de la APP; los 3 listados arriba son documentos distintos según el chat del 17/8.

---

## 3. DESGLOSE DE LA OFERTA ECONÓMICA (A16 — XLSX verificado celda a celda)

> [CONFIRMADO] Extracción directa del XLSX con openpyxl, incluyendo colores de relleno. Regla de Marc (chat 12/08): **"A TENER SOLO EN CUENTA LO QUE ESTÁ EN LAS CASILLAS DE COLOR VIOLETA"**. El violeta es el color `#DB91CD`.

### Celdas VIOLETAS = estructura vigente [CONFIRMADO]

| Concepto | Precio | Comisión | Por venta | Ventas est. | Ganancia est. |
|---|---|---|---|---|---|
| Fijo base mensual ("Mano Derecha & Gestor Operativo") | — | — | — | — | **400 €** |
| MARC · Instagram · Despierta (Setter IA) | 1.497 € | 3% | 45 € | 5 | 225 € |
| MARC · Instagram · Consultas/Intervenciones | 75 € | 6% | 4,50 € | 15 | 67,50 € |
| AURORA · Instagram · Soberanía Vital (Setter IA) | (celda vacía; 997€ según A15) | 3% | 30 € | 7 | 210 € |
| AURORA · Instagram · Consultas Especializadas | 75 € | 6% | 4,50 € | 15 | 67,50 € |
| **TOTAL estimado** | | | | | **970 €/mes** |

### Celdas NO violetas (sin validez según regla de Marc) [CONFIRMADO]

- Facebook (2), YouTube (3), Otros Medios → mismas comisiones listadas pero **sin estimaciones** (colores naranja/rojo/amarillo)
- Catálogo Web (verde): "Ventas Automatizadas — POR DEFINIR"
- Nota: D18 (precio Soberanía Vital en Instagram) está **vacía** en el XLSX; el precio 997€ procede de A15 [INFERENCIA sólida]

### Entregables de Sebastián (hoja XLSX, filas 31-35) [CONFIRMADO]

1. **IA & Automatización** — Setter Virtual IA (cualificación y agendamiento)
2. **App Despierta** — desarrollo técnico, estructuración e implementación
3. **Mantenimiento Web** — tiendas web de Marc y Aurora (catálogos y pagos)
4. **Soporte Lanzamientos** — coordinación técnica y logística
5. **Mano Derecha** — asistencia operativa directa e incidencias

---

## 4. CATEGORÍA B — CONVERSACIONES Y AUDIOS (resumen)

| Bloque | Ruta | Contenido | Estado |
|---|---|---|---|
| Chat WhatsApp Marc — export VIGENTE | MARC/Chat de WhatsApp con MARC (ÚLTIMO EL MÁS RECIENTE)/ | 781 líneas, 24/07→18/08/26. Fuente primaria de decisiones | ✅ LEÍDO COMPLETO |
| Chat WhatsApp Marc — export antiguo | MARC/Chat de WhatsApp con MARC/ | Versión hasta 15/08 | ⚠️ SUPERADO (conservar) |
| Audios OPUS export antiguo | …/Chat de WhatsApp con MARC/*.opus | 27 notas de voz | Convertidos a WAV |
| WAV convertidos | …/Chat de WhatsApp con MARC/wav/ | 27 WAV | ✅ Existen |
| Transcripciones (27) | …/Chat de WhatsApp con MARC/transcripts/*.txt | ASR generado por Copilot 16/8 | ✅ VERIFICADAS como reales (muestra PTT-20260804-WA0125) |
| **Audios NUEVOS 17/8 SIN transcribir** | export vigente, PTT-20260817-WA0006…WA0024 | **13 OPUS nuevos** | 🔵 PENDIENTE TRANSCRIPCIÓN |
| Chat WhatsApp Aurora (+34 722 39 89 89) | raíz/Chat de WhatsApp con +34 722 39 89 89/ | Búsqueda habitación (9/7) + **credenciales IG/correo Aurora (17/8)** + 1 multimedia omitido | 🔴 SENSIBILIDAD ALTA — ver §6 |

---

## 5. ANOMALÍAS Y ARCHIVOS DEFECTUOSOS

| Archivo | Problema | Acción recomendada |
|---|---|---|
| MARC/01_Contexto_Alineacion/Plan_Marc_Operativo_Final.md | 0 bytes | La versión válida es `Plan_Marc_Operativo_Final(1).md`; no borrar, documentado aquí |
| MARC/.mcp-sqlite/marc-data.db | 0 bytes | Base de datos MCP vacía (infraestructura agente anterior); sin datos que recuperar |
| AUDITORIA_GLOBAL/OTROS DOCUMENTES POR ORDENAR/MARC_IMAGENES | 0 bytes, sin extensión | Posible carpeta fallida; las imágenes reales están en MARC/ |
| 20_INVENTARIO_TOTAL_ARCHIVOS.csv.bak | Backup del inventario Cline | Conservar como histórico |
| Duplicados Doc1/Doc2/Doc3 + adjuntos entre los 2 exports de chat | SHA256 idénticos (verificado por Cline) | Conservar ambos exports; el vigente es "(ÚLTIMO EL MÁS RECIENTE)" |
| Copias de entrega en MARC_Proyecto_Entrega_2026/ | Duplican Doc1/2/3 | Estructura de entrega a Marc; conservar |

---

## 6. ⚠️ HALLAZGO DE SEGURIDAD CRÍTICO

**[CONFIRMADO]** Se han detectado **dos** archivos con credenciales en texto plano:

1. `Chat de WhatsApp con +34 722 39 89 89.txt` (raíz) — Aurora envió el 17/08/2026 a las 13:15 usuario y contraseña de su Instagram, y correo y contraseña de Soberanía Vital.
2. `MARC/Chat…(ÚLTIMO EL MÁS RECIENTE)/…/Chat de WhatsApp con Marc Souza Gil.txt` (línea 640) — Marc envió el 15/08/2026 a las 19:21 el correo del proyecto Despierta (proyectodespierta7@gmail.com) con su contraseña.

**Acciones aplicadas inmediatamente por este agente (sin tocar el archivo original):**
1. Las credenciales **NO se copian ni se citan** en ningún documento de este sistema. Solo se registra: SERVICIO / TIPO / UBICACIÓN / ESTADO.
2. Se marca el archivo con `[CREDENCIALES SENSIBLES DETECTADAS]` en el CSV de inventario.
3. **REQUIERE AUTORIZACIÓN / DECISIÓN DE SEBASTIÁN:** (a) mover ese archivo a una ubicación fuera de cualquier sincronización/GitHub, (b) recomendar a Aurora cambio de contraseñas tras el uso, (c) nunca pegar esas credenciales en documentos, prompts ni repositorios.

Registro de acceso (sin valores):

| Servicio | Usuario | Contraseña | Ubicación | Estado |
|---|---|---|---|---|
| Instagram Aurora | [EN ARCHIVO ORIGINAL] | [EN ARCHIVO ORIGINAL] | Chat +34 722… .txt, línea 19-20 | Recibido 17/8 13:15 |
| Correo Soberanía Vital (Gmail) | [EN ARCHIVO ORIGINAL] | [EN ARCHIVO ORIGINAL] | Chat +34 722… .txt, línea 21-22 | Recibido 17/8 13:15 |
| Gmail proyecto Despierta | proyectodespierta7@gmail.com [C] | [EN ARCHIVO ORIGINAL] | Chat Marc vigente, línea 640 | Recibido 15/8 19:21 |

Nota adicional: en ese chat, ante el envío de credenciales, apareció una respuesta automática anómala ("No puedo ayudarte con eso") — [INFERENCIA] un bot/respuesta rápida rechazó el mensaje; sin impacto operativo.

---

## 7. FUENTES DE VERDAD (jerarquía)

1. **Chat WhatsApp vigente** (24/7→18/8) — decisiones de última hora (precios, acuerdos, urgencias)
2. **Oferta_Colaboracion_Sebastian.xlsx (celdas violetas)** — estructura económica vigente
3. **Info básic para Sebastian.docx** — precios de productos y roadmap comercial de Marc
4. **Doc1/Doc2/Doc3 (MD)** — contexto, plan e inteligencia (con salvedades donde el chat posterior las actualiza)
5. **Contrato IE6** — qué entrega exactamente Escala con Ads
6. **Auditorías previas (Cline/Copilot)** — histórico, no reemplazan a este inventario

Cualquier conflicto entre fuentes se registra en `00_CONTROL/DECISIONS.md` y se resuelve por antigüedad (la más reciente confirmada por Marc gana) o se marca [PENDIENTE DE CONFIRMACIÓN].
