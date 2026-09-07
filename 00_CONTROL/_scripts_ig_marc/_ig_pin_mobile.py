#!/usr/bin/env python3
"""Intentar fijar post desde la vista móvil de Instagram (m.instagram.com)."""
import time
from _ig_toolkit import IGSession, MOBILE_UA

ig = IGSession()
if not ig.connect():
    print("FALLO CONEXION")
    exit(1)

# Crear nueva página con UA móvil
page = ig.ctx.new_page()
ig._page = page

# Override UA via CDP
page.set_extra_http_headers({"User-Agent": MOBILE_UA})

# Navegar al post en vista móvil
page.goto("https://www.instagram.com/marcsouza.7/p/DZkutW4Ck7i/", wait_until="commit", timeout=90000)
time.sleep(8)

print("URL:", page.url[:80])
print("Title:", page.title())

# Buscar botón de menú (tres puntos) en vista móvil
menu = page.query_selector('[aria-label="Más opciones"]')
if not menu:
    menu = page.query_selector('button[aria-label*="opciones"]')
if not menu:
    menu = page.query_selector('[data-testid="more-button"]')
if not menu:
    # Buscar cualquier botón con svg de tres puntos
    menu = page.query_selector('button:has(svg circle)')

if menu:
    menu.click()
    print(">>> menú abierto (vista móvil)")
    time.sleep(3)
    
    # Leer todo el texto visible
    body_text = page.evaluate("() => document.body.innerText")
    print("=== TEXTO PÁGINA (primeros 800 chars) ===")
    print(body_text[:800])
    
    # Buscar dialog/overlay
    dialog = page.evaluate('''() => {
        const d = document.querySelector('[role="dialog"], [role="menu"], [role="listbox"]');
        return d ? d.innerText : 'SIN DIALOG';
    }''')
    print("\n=== DIALOG ===")
    print(dialog[:500])
    
    # Buscar fijar/anclar
    if "Fijar" in body_text or "Anclar" in body_text or "Pin" in body_text:
        print("\n*** OPCIÓN DE FIJADO ENCONTRADA EN VISTA MÓVIL ***")
    else:
        print("\n>>> Opción Fijar NO disponible tampoco en vista móvil web")
else:
    print("No se encontró botón de menú en vista móvil")
    # Listar todos los botones
    btns = page.evaluate('''() => Array.from(document.querySelectorAll('button, [role="button"]'))
        .map(b => ({text: (b.innerText||b.getAttribute('aria-label')||'').trim().slice(0,40), vis: b.offsetParent!==null}))
        .filter(b => b.text)''')
    print("Botones:", btns[:20])

ig.close()
