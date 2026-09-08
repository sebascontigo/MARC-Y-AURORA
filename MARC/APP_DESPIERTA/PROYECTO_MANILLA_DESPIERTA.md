# PROYECTO DESPIERTA EN TU MUÑECA — reloj + manilla antistrés
> Visión 31/8/2026 · Petición de Marc: que la app sirva en el reloj y que una manilla detecte el estrés y suene su voz para ayudar en el momento exacto.
> Principio rector: **ayudar de verdad en el momento de necesidad**, sin dependencia del móvil, con privacidad total (los datos del cuerpo nunca salen del dispositivo sin permiso).

## LO QUE YA EXISTE (hoy)
| Pieza | Estado |
|---|---|
| Módulo CALMA en la app PWA (SOS + respiración 4-4-6 + anclaje 5-4-3-2-1 + audio de voz) | ✅ en `APP_DESPIERTA/index.html` pestaña Calma |
| Versión reloj (UI redonda, SOS gigante, misma voz) | ✅ `APP_DESPIERTA/watch/index.html` → https://despierta-app.netlify.app/watch |
| Audios de voz (calma + fortaleza) | ✅ `APP_DESPIERTA/audios/*.mp3` (TTS provisional → clon ElevenLabs con OK de Marc) |

## CÓMO SE USA EN UN WEAR OS HOY (Samsung/Pixel Watch)
1. Abrir Samsung Internet en el reloj → `despierta-app.netlify.app/watch`.
2. Añadir a favoritos / atajo. Botón redondo → voz de Marc + respiración guiada con vibración.
3. Funciona offline si el reloj guardó la página (y el audio está en el servidor — fase 2 lo empaqueta offline).

## FASE 1 — PWA WATCH OFFLINE (1-2 semanas)
- Service worker del watch con precarga de audio y manifest redondo (`icons` maskable 192/512).
- Botón «añadir a pantalla de reloj». Instalación tipo app en Wear OS 4+.
- Criterio de hecho: funciona sin conexión tras la primera visita.

## FASE 2 — APP NATIVA WEAR OS (4-6 semanas)
- APK Wear OS (Kotlin) con **Health Services API**: detección de estrés por HRV/frecuencia en reposo + detección manual (SOS).
- Acciones al detectar estrés: vibración suave → pantalla CALMA → voz de Marc → respiración guiada.
- Sincronización con la app PWA (check-in automático del episodio de calma).
- Distribución: APK directo a los alumnos del programa (sin Play Store al inicio).

## FASE 3 — MANILLA (hardware)
| Opción | Qué permite | Coste aproximado | Comentario |
|---|---|---|---|
| **Mi Band / Amazfit + app Notify** | Automatización: pulso alto → notificación/acción (abrir audio de Marc) | ya en el mercado (~30-60€) | vía rápida, sin desarrollo |
| **Samsung Galaxy Watch** | Estrés nativo + rutinas (Bixby Routines: estrés alto → reproducir audio) | ya en el mercado | integración inmediata |
| **Banda propia (BLE + HRV)** | Control total del flujo, marca Despierta | prototipo 50-150€ (ESP32 + sensor) | fase empresa, certificación médica NO (bienestar) |
- **Regla de oro:** la manilla NO diagnostica nada. Solo detecta señales y ofrece calma. Enfoque de bienestar y ayuda real.

## VOZ DE MARC
1. Grabación limpia de 5 min (lectura en calma) + consentimiento firmado.
2. Clon en ElevenLabs → sustituye los MP3 provisionales en `audios/`.
3. Biblioteca creciente: calma 1-2 min, fortaleza, micro-lección diaria (la misma del clon).

## MÉTRICA DE ÉXITO REAL
- Nº de episodios de calma completados por alumno (la ayuda que llega a tiempo), no descargas.
