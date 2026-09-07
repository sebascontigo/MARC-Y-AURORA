#!/usr/bin/env python3
"""
SOLUCIONES A ERRORES DE AUTOMATIZACIÓN IG — Sesión MARC 2026-08-19
===================================================================

Este documento resume los errores encontrados y sus soluciones.
Usar _ig_toolkit.py como base para futuras automatizaciones.

ERROR 1: CDP se cuelga repetidamente
-------------------------------------
CAUSA: Brave DevTools backend se satura tras múltiples conexiones.
SOLUCIÓN: IGSession.connect() ahora:
  - Detecta CDP colgado (timeout en connect_over_cdp)
  - Limpia la instancia de Playwright (evita "Sync API inside asyncio loop")
  - Mata Brave y lo relanza con --remote-debugging-port=9222
  - Reintenta hasta 3 veces
  - Timeout reducido a 30s (antes 60s causaba esperas largas)

ERROR 2: React no registra keyboard.type()
-------------------------------------------
CAUSA: React usa un sistema de eventos sintéticos. keyboard.type() dispara
  eventos nativos que React NO intercepta correctamente en inputs controlados.
SOLUCIÓN: IGSession.react_fill() usa:
  1. el.click() para enfocar
  2. Ctrl+A + Backspace para limpiar
  3. el.fill(text) que SÍ dispara eventos React (input + change)
  4. Fallback: setter nativo + dispatchEvent si fill() no registra
  VERIFICADO: La bio se guardó correctamente con este método.

ERROR 3: Campo "Nombre" no editable en vista web
-------------------------------------------------
CAUSA: Instagram Web muestra el nombre como texto estático, no como input.
  La edición del nombre solo está disponible en la app móvil.
SOLUCIÓN: BLOQUEADO en web. Opciones:
  a) Usar la app móvil manualmente (1 click)
  b) Intentar con UA móvil + m.instagram.com (no verificado)
  c) API privada de Instagram (riesgo de baneo, NO recomendado)
ESTADO: BLOQUEADO — limitación de plataforma.

ERROR 4: Opción "Fijar/Anclar" no aparece en menú del post
-----------------------------------------------------------
CAUSA: La función de fijar posts es EXCLUSIVA de la app móvil de Instagram.
  Instagram Web (desktop Y móvil) NO la ofrece.
  Verificado en 3 rutas:
  - URL directa del post → menú: Eliminar, Editar, Ocultar MG, Desactivar
    comentarios, Información, Compartir, Copiar enlace, Código de inserción
  - Grid del perfil → menú: Ver insights, Promocionar publicación
  - Vista móvil (m.instagram.com) → overlay bloquea, sin opción de fijar
SOLUCIÓN: BLOQUEADO en web. Solo posible desde la app móvil.
ESTADO: BLOQUEADO — limitación de plataforma.

ERROR 5: Playwright "Sync API inside asyncio loop"
---------------------------------------------------
CAUSA: Si connect_over_cdp() da timeout, la instancia de sync_playwright()
  queda viva con su loop asyncio interno. Al reintentar, Playwright detecta
  el loop activo y rechaza crear otra instancia sync.
SOLUCIÓN: IGSession._stop_pw() llama pw.stop() antes de cada reintento,
  liberando el loop asyncio. Implementado en connect().

RESUMEN DE HERRAMIENTAS CREADAS
================================
- _ig_toolkit.py: IGSession con auto-recuperación CDP, react_fill, react_submit
- _ig_diag_menu.py: Diagnóstico del menú de opciones del post
- _ig_pin_from_grid.py: Intento de fijar desde grid (confirmado: no existe)
- _ig_pin_mobile.py: Intento de fijar desde vista móvil (confirmado: no existe)

PRÓXIMOS PASOS PARA EL AGENTE
==============================
1. Bio: YA VERIFICADA como guardada. No repetir.
2. Nombre: Informar a Sebastián que solo se puede cambiar desde la app móvil.
3. Fijar post: Informar que solo se puede desde la app móvil.
4. Para futuras ediciones: usar _ig_toolkit.py (IGSession + react_fill).
5. Si CDP se cuelga: el toolkit lo resuelve automáticamente.
"""

if __name__ == "__main__":
    print(__doc__)
