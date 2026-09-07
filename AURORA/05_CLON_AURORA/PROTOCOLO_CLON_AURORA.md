# PROTOCOLO CLON DE AURORA — historias diarias (espejo de Marc)
> Versión 1.0 · 31/8/2026 · Misma mecánica que `MARC/26_CLON_MARC/PROTOCOLO_CLON_MARC.md`, con estética y voz propias de Aurora.

## Flujo de 1 prompt
> **HOY:** [tema] [CTA]
→ guion estilo Aurora (cercano, natural) → historia 9:16 verde → carpeta del día → checklist.

## Fase 0 (hoy, 0€)
```
python MARC\26_CLON_MARC\_gen_historia_diaria.py --cliente aurora --hook "..." --texto "..." --cta "..."
```
Salida: `AURORA/HISTORIAS/YYYY-MM-DD/HISTORIA_9x16_aurora.jpg` + caption.

## Fase 1 (avatar real) — requisitos
1. Vídeo base de Aurora (2 min, frontal, buena luz).
2. Consentimiento para clon de voz (ElevenLabs).
3. Avatar por prompt vía KIE (HeyGen/D-ID/Hedra).

## Ética
- Contenido del avatar siempre identificado y aprobado por Aurora.
- Sin promesas de salud garantizadas: informar y acompañar.
