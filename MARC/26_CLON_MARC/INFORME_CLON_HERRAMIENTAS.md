# 🎭 INFORME CLON IA DE MARC — qué NO sirve, qué SÍ, y la ruta definitiva
> 31/8/2026 · Agente (GLM-5.3). Fuentes: compendio BAYONA_COMPENDIO_IA_2026 (investigación con verificación primaria, ago 2026) + estado del proyecto (PROTOCOLO_CLON_MARC v1).
> Objetivo: que Marc tenga su clon hablando (voz + cara) para historias/reels diarios, con budget 0€ o mínimo, y que Sebastián solo escriba una línea al día.

## 1. LO QUE NO SIRVE (descartado, con motivo)

| Herramienta | Por qué NO |
|---|---|
| **ElevenLabs FREE** | ⛔ El tier gratis **NO incluye clonación de voz** — solo voces stock. Además exige atribución y te da licencia perpetua sobre la voz. Para clonar exige Starter $6/mes. |
| **Argil** | $39/mes — caro para validar la idea. |
| **Creatify** (clon desde 1 foto) | Calidad de avatar "foto estática" no transmite la autoridad de un terapeuta. Rejected para marca seria. |
| **Resemble AI trial** | Solo ~5s de audio para probar. Inútil para 40-60 palabras diarias. |
| **Hola/Hello2, LatentSync, EchoMimic, InfiniteTalk, EMO, OmniHuman** | Requieren 12-24GB+ de VRAM. El portátil (RTX 3050 4GB) no puede correrlos. |
| **Clonar la voz sin consentimiento firmado** | ⛔ Legal: 12+ estados EEUU con leyes de clonación + ética del proyecto. Marc firma autorización ANTES de generar nada con su voz. |

## 2. LO MEJOR GRATIS / CASI GRATIS (la ruta recomendada)

### Ruta A — 0€ TOTAL (hoy mismo, Fase 0 vigente)
| Pieza | Herramienta | Coste |
|---|---|---|
| Guion diario | Agente (frases reales de Marc de transcripciones) | 0 |
| Imagen historia 9:16 | `_gen_historia_diaria.py` (plantilla marca) | 0 |
| Voz TTS provisional | `calma_marc.mp3` (edge-tts es-CO, ya en producción) | 0 |
| Publicación | Kit manual 10-min o sesión IG | 0 |
**Estado: FUNCIONANDO HOY** (verificada la historia del 31/8 en `26_CLON_MARC/HISTORIAS/`).

### Ruta B — CLON DE VOZ real (calidad Marc, ~0€)
1. **Qwen3-TTS** (self-host, Apache 2.0) — clona desde **3 segundos de audio** (ideal: 5 min limpios). 0€.
2. **Chatterbox Multilingual v3** (Resemble, open) — **gana a ElevenLabs en A/B ciego con 63.75-65%** de preferencia. 0€ self-host (marca un watermark detectable — irrelevante para uso propio con consentimiento).
3. **Fish Audio S2 Pro** — #1 open weights (Elo 1124, 83 idiomas) con tier de API gratis.
**Recomendada: Qwen3-TTS** (menos fricción para clonar con poco audio). Corre local sin GPU.

### Ruta C — AVATAR HABLANDO (cara + voz, el clon completo)
| Herramienta | Free tier | Veredicto |
|---|---|---|
| **HeyGen** | **3 vídeos/mes de 1 min a 1080p** — gratis, sin tarjeta | ⭐ RECOMENDADO para empezar: 3 historias/semana con el avatar de Marc |
| **Vidnoz** | ~3 min/día de 720p renovables, sin tarjeta | ⭐ Plan B diario: más volumen, algo menos de calidad |
| **KIE (cuenta activa, 80 créditos)** | Ya pagado (créditos existentes: Seedance, Veo 3.1, Kling 3.0) | ⭐ Vía ya disponible en el arsenal para vídeo premium |
| **Wav2Lip** (open) | Gratis self-host, **4GB VRAM — el ÚNICO que cabe en tu RTX 3050** | Para volumen alto: lip-sync sobre vídeo base de Marc, local |
| **Google Vids** | 25 generaciones avatar/mes | Reserva |

**Combinación ganadora (0€ validación → escala):**
1. **Hoy:** HeyGen free (3/mes) para 3 historias semanales del avatar de Marc.
2. **Volumen diario:** Vidnoz free (3 min/día) o Wav2Lip local sobre 2 min de vídeo base.
3. **Audio diario no-avatar:** Ruta A (plantillas + TTS provisional).
4. **Cuando el embudo facture:** ElevenLabs Starter $6/mes (voz) + HeyGen pagado si el free se queda corto.

## 3. LO QUE HACE FALTA DE MARC (checklist humano, 30 min total)
1. ☐ **Vídeo base 2 min**: frontal, buena luz, silencio, mirando a cámara (móvil vale).
2. ☐ **Audio limpio 5 min**: leyendo algo en voz natural (para Qwen3-TTS).
3. ☐ **Consentimiento firmado** de voz+imagen (plantilla en §5).
4. ☐ Aprobar el primer guion generado con sus frases reales.

## 4. FLUJO "UNA LÍNEA" (ya operativo — v1 del protocolo)
Sebastián escribe: `HOY: [tema] [CTA]` → guion (estilo Marc validado con transcripciones) → historia/avatar → caption + checklist → pieza lista en `HISTORIAS/YYYY-MM-DD/`.

## 5. PLANTILLA DE CONSENTIMIENTO (borrador legal para firma)
> Yo, **Marc Souza Gil**, autorizo a SEVISIONARI (Sebastián Bayona) a clonar mi voz y mi imagen con IA **exclusivamente** para contenido de las marcas DESPIERTA y Marc Souza, en Instagram y webs propias. La autorización cubre: generación, edición y publicación de vídeos/avatar con mi likeness. **Exclusiones:** terceros, política, contenido ajeno a mis marcas. **Duración:** 1 año desde la firma, revocable por escrito. El avatar se etiquetará siempre como contenido generado con IA aprobado por Marc.
> Valencia, ____ de ______ 2026. Firma: ________

## 6. CONCLUSIÓN PARA SEBASTIÁN (1 línea)
**No gastes un euro**: Qwen3-TTS (voz) + HeyGen free (avatar, 3/mes) + Vidnoz/Wav2Lip (volumen) + lo que YA funciona (Fase 0). Solo necesitas 30 min de Marc (vídeo + audio + firma) y el clon queda montado.
