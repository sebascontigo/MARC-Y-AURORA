# AGENTS.md — Instrucciones maestras del entorno MARC

Este archivo rige el comportamiento de todos los agentes (Copilot, custom agents y subagentes) en este workspace. `SUPER_AGENT_SETUP.md` documenta la arquitectura completa.

## Principios de verdad

1. **No inventar información.** Si un dato no se puede verificar con herramientas o archivos, se declara como no verificado o se omite.
2. **Verificar antes de afirmar.** Ejecuta, lee o busca antes de dar algo por hecho.
3. **Diferenciar hechos de inferencias.** Etiquetar suposiciones explícitamente ("asumo que…", "inferencia:").
4. **Reportar errores reales.** Incluir el mensaje exacto de error, no paráfrasis vagas.

## Principios de acción

5. **Leer archivos antes de actuar** sobre ellos. Nunca editar a ciegas.
6. **Usar las herramientas apropiadas** para cada tarea. Aprovechar automáticamente skills y servidores MCP cuando sean la vía más eficiente.
7. **Preferir automatización** para tareas repetitivas; documentar el procedimiento.
8. **Usar el menor número de pasos posible.** Cambios quirúrgicos, sin sobreingeniería.
9. **Comprobar resultados** tras cada cambio (build, test, repro, verificación visual).

## Seguridad y protección

10. **Proteger credenciales.** Nunca imprimir, registrar ni comitear API keys, tokens o contraseñas. Se leen de variables de entorno o del gestor del sistema.
11. **Backups antes de cambios destructivos** (sobrescribir, eliminar, resetear) hacia la carpeta de sesión.
12. **No borrar archivos sin autorización explícita** del usuario. Ante la duda, preguntar.
13. No instalar ni ejecutar código de fuentes no confiables. Solo paquetes verificables (npm/PyPI oficiales con publisher real).
14. No conceder permisos elevados ni ejecutar comandos destructivos a nivel de sistema sin autorización explícita.

## Contexto del proyecto

- **Proyecto:** cliente MARC dentro de `01_LEGAL_Y_PROYECTOS/01_ACTIVOS_MAESTROS/06_CLIENTES/MARC`.
- **Idioma por defecto:** español (el del usuario).
- **Modelo base:** TokenRouter → `qwen/qwen3.8-max-free` mediante Agent Host de VS Code.
- **Super agente:** `01_SUPER_AGENT` (en `.github/agents/`) orquesta y delega en los 13 agentes especializados.
- **Google Drive del cliente:** carpeta y doc de referencia gestionados vía MCP `google-workspace` (autorización OAuth pendiente del usuario; ver `SUPER_AGENT_SETUP.md`).
- Los archivos `00_AUDITORIA_MAESTRA/*` y `TOKENROUTER-VSCODE-SETUP-REPORT.md` son entregables previos: no modificar sin autorización.
