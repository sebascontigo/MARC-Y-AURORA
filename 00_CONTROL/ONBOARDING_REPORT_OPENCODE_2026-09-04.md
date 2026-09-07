# OPENCODE ONBOARDING REPORT — SEVISIONARI / EMPRESA IA
**Fecha:** 2026-09-04 · **Agente:** OpenCode + Muse Spark 1.3 (Tier contributor) · **Turno:** A (reconocimiento, solo lectura) · **Scope:** MARC Y AURORA + shallow resto (sin tocar nada)

## A. CONTEXTO ENTENDIDO
Ecosistema de Sebastián Bayona (Bogotá → España) operado como multiparque digital: empresas/marcas/productos/agentes bajo un futuro Holding Core. Misión activa a hoy: clientes MARC (Despierta 1.497€) y AURORA (Soberanía Vital 997€), lanzamiento septiembre 2026 con agencia Escala. Todo cuadra con el prompt maestro salvo fechas: docs rectores son del 18-31/8, hoy es 4/9 (posible desfase, ver E).

## B. REPOS ENCONTRADOS
- `C:\01_INFRAESTRUCTURA_DEL_SISTEMA\` → 01_BACKUPS, 02_ESCANEOS, 03_LIMPIEZA_PENDIENTE (con CUARENTENA_FINAL_20260818), 04_SCRIPTS_UTILITARIOS, **05_SISTEMA_DE_TRABAJO_AGENTES** (00 arquitectura, 01 flujos/handoffs, 02 prompts maestros, 03 SOPs, 04 prioridades, 05 resumen, 06 MAPA_MAESTRO_PC), **06_CEREBRO** (AGENTS/COSTS/LOGS/MCP/MODELS/PROVIDERS/ROUTING/SECURITY/SKILLS/POLICIES + README/RESUMEN/ESTADO_PRE/CHANGELOG/CREAR_CEREBRO.ps1), 07_LOGS_Y_AUDITORIAS.
- `C:\02_INFORMACION\` → 01_PERSONAL [NO ENTRADO, privado], 02_LEGAL_Y_DOCUMENTOS, 03_MULTIMEDIA, 99_BANDEJA, 99_PAPELERA.
- `C:\SEGURIDAD\` → historial incidente 2026 + CHECK-REGULAR.ps1 + estado final.
- `C:\03_PROYECTOS\01_GRUPO_BAYONA\` → CASO_OLGA, CASO_SEGURGLOB, COLOMBAI, EMPRESA FITNESS, EMPRESA TECNOLOGÍA, IDENTIDAD, LABORATORIO, **PARQUE INDUSTRIAL**, RECURSO MAESTRO (+ briefing agente, historial web 27/8).
- `C:\03_PROYECTOS\02_PRODUCTOS\BAYONA` [entidad producto].
- Workspace actual `.../CLIENTES/MARC Y AURORA/` → README + 9 MASTER_*.md + 00_CONTROL/ + 03_ESCALA/ + MARC/ + AURORA/ + MARC_Proyecto_Entrega_2026/ (00/01/02/04/06/09) + AUDITORIA_GLOBAL/ (historia, no tocar).

## C. GOBIERNO ENCONTRADO
README (reglas oro: no borrar historia, MARC/AURORA separados, etiquetado, no inventar, credenciales secretas, autorización previa, agente solo-texto) + MASTER_CONTEXT/STATUS/TASKS/DECISIONS/CHANGELOG/ASSETS/ACCESS/KPIS/ROADMAP + TAREAS_SEBASTIAN_HOY (25/8) + PENDIENTE_SEBASTIAN (tareas humanas). Sistema de tareas P0-P4 con estados. Regla continuidad: leer README→STATUS→TASKS, documentar en CHANGELOG. Todo coherente con prompt §§24-28.

## D. SISTEMAS REALES
- 3 webs publicadas 28/8 con HTTP 200 declarado: despierta-marc, despierta-app, soberania-vital (Netlify SEVISIONARI) [declarado, no re-verificado hoy].
- 43 acciones IG registradas (40 verificadas) sobre @marcsouza.7; NOTA 24h, QR, 12 imágenes IA 1080, 4 reels 9:16, lead magnet ebook ES+EN, tablero TABLERO.html.
- Repo GitHub sebascontigo/MARC-Y-AURORA verificado 31/8: privado VACÍO.
- Scripts: `00_CONTROL/_ig_audit_marc.py` listo; USB 116 archivos integrados 28/8.

## E. CONTRADICCIONES / DESFASES CON EL PROMPT
1. Docs al 18-31/8 vs hoy 4/9: estado IG (B-8 sesión expirada 25/8), aprobaciones contenido y Nota 24h pueden haber cambiado. [CONTRADICCIÓN temporal por resolver]
2. Prompt §8 Core 1A 26/26 tests y §§19-23 (BAYONA en EMPRESA FITNESS, VALLUNA, COLOMBAI C-001): entidades existen por nombre; tests y contenidos NO verificados en este turno. [PENDIENTE]
3. §31 base masiva Colombia: no localizada ni tocada en este turno. [ALERTA latente, no evidencia]
4. WhatsApp captación: 642666972 (landing) vs 643270566 (MASTER_ACCESS). [CONTRADICCIÓN abierta]

## F. SERVICIOS / APPS RELEVANTES
IG Marc/Aurora, Gmail Despierta/SoberaníaVital, WhatsApp Business, GHL y Meta Ads vía Escala (pendientes), Drive Escala/Aurora (bloqueados), dominio reconecta-t.net, Netlify, Glide futuro. Credenciales solo como metadatos (regla oro 5).

## G. ESTADO GIT
⚠️ Hallazgo operativo crítico: la raíz del repo es `C:\` (rama main). `git status` desde el workspace arrastra `$Recycle.Bin`, `.mimosa`, `.vscode` como untracked + warnings de permiso en carpetas sistema. Causa probada de la lentitud (comando colgado >3 min desde `C:\03_PROYECTOS`, segundos desde el workspace). Regla: NUNCA git en raíz; todo scoping a subcarpeta; ni reset ni force push jamás sin orden.

## H. RIESGOS
🔴 B-5 credenciales en texto plano (2 archivos) — requiere autorización, no tocar.
🔴 B-8 sesión IG expirada — bloquea Nota/CM/publicar; solo login humano.
🟡 Repo gigante en `C:\` — cualquier agente que abra raíz se cuelga (evidencia hoy).
🟡 Staleness 4-17 días en tableros.
🟡 Tier contributor: prompts entrenan a Meta — datos sensibles de clientes solo por estándar/local.

## I. QUÉ PUEDO OPERAR DESDE OPENCODE
Inventarios shallow, lectura/organización docs, código y webs estáticas, verificación HTTP, scripts de auditoría, contenido texto, MCP Playwright (conectado), changelogs y reportes. Todo con evidencia.

## J. QUÉ NO DEBO TOCAR TODAVÍA
Credenciales (B-5), login IG (B-8, humano), 01_PERSONAL, supuesta base masiva (§31), arquitectura Core/Holding, migraciones, despliegues, gasto (Metricool/Later), publicar sin OK, ramas/entrega oficial.

## K. RECOMENDACIÓN PRIMERA MISIÓN REAL
Turno A2: re-verificar tablero (¿sigue B-8? ¿aprobaron C-001..C-003?) + auditar solo-metadatos de PARQUE INDUSTRIAL y 06_CEREBRO-estado para alinear multiparque con Holding. Nada destructivo.

## NOTA 4-sep 17h — reorg ejecutada: todo lo operativo vive ahora en C:\SEVISIONARI (ver 99_ARCHIVO\REORG_LOG_2026-09-04.md). Rutas C:\ directas de este reporte quedan históricas.
