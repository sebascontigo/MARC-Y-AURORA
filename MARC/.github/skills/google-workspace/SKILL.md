---
name: google-workspace
description: "Operar Google Drive, Docs, Sheets, Gmail y Calendar mediante el MCP google-workspace (workspace-mcp). Usar para listar/leer/crear archivos de Drive y documentos compartidos del cliente."
---

# Skill: Google Workspace

Servidor MCP: `google-workspace` (`uvx workspace-mcp`, ~122 tools: Drive, Docs, Sheets, Gmail, Calendar...).

## Estado de autorización

El servidor requiere **OAuth completado por el usuario** (Google Cloud client + consentimiento del navegador). Si una herramienta responde con error de autorización:

1. NO inventar tokens ni credenciales.
2. Informar al usuario los pasos exactos (ver SUPER_AGENT_SETUP.md § Google Drive).

## Recursos del cliente MARC

- Carpeta Drive: `https://drive.google.com/drive/folders/1ApLPxr-2uAzoJRyClGLQlghDBtQc88rJ`
- Doc: `https://docs.google.com/document/d/1Tp5-ayqaYAnaan_ITdZ8vhq-lXr-qJvYCGanCM8JzSQ/edit?tab=t.0`

## Buenas prácticas

- Leer/listar siempre antes de escribir.
- Mover a la papelera de Drive en vez de borrado duro; borrados solo con autorización explícita.
- Al compartir: no cambiar permisos de acceso público sin confirmación.
