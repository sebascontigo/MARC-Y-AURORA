# Instrucciones Copilot — workspace MARC

Las reglas maestras completas están en [AGENTS.md](../AGENTS.md) (raíz del workspace): verdad verificable, leer antes de actuar, credenciales protegidas, backups antes de cambios destructivos, mínimos pasos y verificación de resultados. Este archivo no las duplica.

Complementos específicos de Copilot en este workspace:

- Delega por defecto en `01_SUPER_AGENT` para tareas multi-herramienta; agentes especializados en `.github/agents/`.
- Skills bajo demanda en `.github/skills/` (se cargan solo cuando la tarea lo requiere).
- Servidores MCP: workspace (`.mcp.json`: filesystem del proyecto + SQLite MARC) y usuario (`~/.copilot/mcp-config.json`: memoria, pensamiento secuencial, fetch, sqlite, playwright, github, google-workspace).
- Responder en español salvo que el usuario cambie de idioma.
