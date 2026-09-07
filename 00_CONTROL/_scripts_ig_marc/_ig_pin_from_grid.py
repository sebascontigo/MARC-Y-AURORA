#!/usr/bin/env python3
"""Intentar fijar post desde el grid del perfil (ruta alternativa)."""
import time
from _ig_toolkit import IGSession

ig = IGSession()
if not ig.connect():
    print("FALLO CONEXION")
    exit(1)

page = ig.get_page("instagram.com")

# Navegar al perfil
page.goto("https://www.instagram.com/marcsouza.7/", wait_until="commit", timeout=90000)
time.sleep(6)

# Buscar el post en el grid (por link que contenga el shortcode)
post_link = page.query_selector('a[href*="DZkutW4Ck7i"]')
if post_link:
    post_link.click()
    print(">>> Post abierto desde grid")
    time.sleep(4)
else:
    print("Post no encontrado en grid, navegando directo")
    page.goto("https://www.instagram.com/marcsouza.7/p/DZkutW4Ck7i/", wait_until="commit", timeout=90000)
    time.sleep(6)

# Abrir menú
menu = page.query_selector('[aria-label="Más opciones"]')
if menu:
    menu.click()
    time.sleep(3)
    # Leer dialog
    dialog_text = page.evaluate('''() => {
        const d = document.querySelector('[role="dialog"]');
        return d ? d.innerText : 'SIN DIALOG';
    }''')
    print("=== MENÚ DESDE GRID ===")
    print(dialog_text)
    
    # Buscar fijar/anclar
    if "Fijar" in dialog_text or "Anclar" in dialog_text or "Pin" in dialog_text:
        print("\n*** OPCIÓN DE FIJADO ENCONTRADA ***")
        pin = page.query_selector('[role="dialog"] div:has-text("Fijar")')
        if not pin:
            pin = page.query_selector('[role="dialog"] div:has-text("Anclar")')
        if pin:
            pin.click()
            print(">>> FIJADO EJECUTADO")
            time.sleep(3)
    else:
        print("\n>>> Opción Fijar NO está disponible tampoco desde grid")
else:
    print("No se encontró botón de menú")

ig.close()
