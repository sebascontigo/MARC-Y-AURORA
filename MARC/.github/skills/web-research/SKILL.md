---
name: web-research
description: "Investigación en internet: búsqueda web, lectura de páginas y plataformas sociales (Reddit, X, YouTube, V2EX, blogs). Usar para investigar temas, noticias, reputación o datos de mercado."
---

# Skill: Web Research

Orquesta las capacidades de investigación instaladas. **No duplica herramientas**: enruta al canal correcto.

## Enrutamiento

| Necesidad | Herramienta |
|---|---|
| Leer una URL concreta | `web_fetch` (built-in) o MCP `web-fetch/*` (@kazuph/mcp-fetch) |
| Interacción real con página (formularios, JS, descargas) | MCP `playwright/*` → agente `07_BROWSER_AGENT` |
| Plataformas sociales/comunidades (Reddit, X, YouTube, blogs, GitHub) | skill **agent-reach** (instalada en ~/.agents/skills, 15 plataformas) |
| Síntesis multi-fuente | agente `02_RESEARCHER` |

## Método

1. Descomponer la pregunta en subconsultas verificables.
2. Priorizar fuentes oficiales/primarias; citar siempre la URL.
3. Contrastar cifras importantes con una segunda fuente.
4. Reportar: hallazgos + fuentes + qué quedó sin verificar.

## Reglas

- Respetar robots.txt y términos de la web; sin elusión de paywalls/anti-bot.
- Sin datos personales sin motivo legítimo (PII).
