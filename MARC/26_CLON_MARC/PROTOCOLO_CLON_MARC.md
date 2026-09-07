# PROTOCOLO CLON DE MARC — historias diarias con UN SOLO PROMPT
> Versión 1.0 · 31/8/2026 · Objetivo: que Sebastián escriba UNA línea al día y el sistema produzca la historia de Instagram lista para publicar.
> Ética: el clon SIEMPRE se anuncia como contenido generado con el avatar de Marc y aprobado por él. Nada se publica sin su OK (o el OK permanente que él firme).

## 1. EL FLUJO (un prompt → historia publicada)
```
Sebastián escribe:  «HOY: [tema] [producto o CTA]»
        │
        ▼
AGENTE: 1. Genera el GUION (40-60 palabras, estilo Marc: directo, sin humo, CTA final)
        2. FASE 0 (hoy): genera la HISTORIA visual con plantilla Despierta + texto
           FASE 1 (con vídeo base): genera VÍDEO del avatar con la voz clonada
        3. Exporta a  HISTORIAS/YYYY-MM-DD/  (9:16, listo para subir)
        4. Escribe el CAPTION/sticker y el checklist de publicación
        5. Publica (con sesión IG) o deja la pieza lista para subir manualmente
```

### Ejemplo real de prompt único
> **HOY:** plazas de septiembre + e-book gratis
Resultado: historia 9:16 con hook «Tu mente no está rota. Está programada.» + texto de oferta + CTA «escríbeme DESPIERTA».

## 2. FASE 0 — FUNCIONA HOY, COSTE 0€ (fallback operativo)
- Script: `_gen_historia_diaria.py` (este mismo directorio).
- Uso: `python _gen_historia_diaria.py --hook "TU HOOK" --texto "Tu texto corto" --cta "Escríbeme DESPIERTA"`
- Salida: `HISTORIAS/2026-08-31/HISTORIA_9x16.jpg` (1080×1920) + caption sugerido.
- Estética idéntica a la marca (oscuro/ámbar serif) — coherente con la landing y los reels.

## 3. FASE 1 — AVATAR REAL (cuando Marc graba el vídeo base)
| Paso | Herramienta | Estado |
|---|---|---|
| 1. Vídeo base de Marc (2 min, frontal, buena luz, silencio de fondo) | móvil | ⏳ Marc lo graba |
| 2. Clon de voz (5 min de audio limpio + consentimiento firmado) | ElevenLabs | ⏳ autorización |
| 3. Guion → locución con la voz clonada | ElevenLabs API | listo al tener la voz |
| 4. Avatar hablando el guion (lip-sync) | HeyGen / D-ID / Hedra vía **KIE** (créditos ya disponibles: Seedance, Veo 3.1, Kling 3.0, GPT Image 2) | 🔑 cuenta KIE activa (80 créditos) |
| 5. Post-producción 9:16 + subtítulos | ffmpeg (hook + CTA como en REELS_FINALES) | ✅ automatizado |
| 6. Fila de montaje y publicación | este protocolo | ✅ |

## 4. REGLAS DE ORO
1. **Un prompt, cero fricción:** si Sebastián tiene que explicar más de una línea, el sistema está mal.
2. **Voz de Marc validada:** los guiones siguen sus frases reales (transcripciones de MARC/24_MEDIA y charlas). Nada que Marc no diría.
3. **Salud primero:** nada de promesas médicas o de resultados garantizados. El clon informa y acompaña (proyecto enfocado a AYUDAR).
4. **Trazabilidad:** cada historia guarda guion + prompt + asset en su carpeta del día.
5. **Aurora tiene su propio protocolo espejo:** `AURORA/05_CLON_AURORA/` (misma mecánica, estética verde).
