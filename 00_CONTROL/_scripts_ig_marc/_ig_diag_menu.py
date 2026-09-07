#!/usr/bin/env python3
"""Diagnóstico del menú de opciones del post para encontrar 'Fijar'."""
import time
from _ig_toolkit import IGSession

ig = IGSession()
if not ig.connect():
    print("FALLO CONEXION")
    exit(1)

page = ig.get_page("instagram.com")
print("URL:", page.url[:70])

# Asegurar que estamos en el post
if "DZkutW4Ck7i" not in page.url:
    page.goto("https://www.instagram.com/marcsouza.7/p/DZkutW4Ck7i/", wait_until="commit", timeout=90000)
    time.sleep(6)

# Abrir menú
menu = page.query_selector('[aria-label="Más opciones"]')
if menu:
    menu.click()
    print(">>> menú abierto")
    time.sleep(3)
else:
    print("No se encontró [aria-label='Más opciones']")
    # Buscar alternativas
    labels = page.evaluate('''() => Array.from(document.querySelectorAll('[aria-label]'))
        .map(e => ({label: e.getAttribute('aria-label'), tag: e.tagName}))
        .filter(x => x.label)''')
    print("aria-labels disponibles:", labels[:20])
    ig.close()
    exit(1)

# Buscar CUALQUIER overlay/popup que apareció
result = page.evaluate('''() => {
    const overlays = [];
    document.querySelectorAll('div, section').forEach(el => {
        const style = window.getComputedStyle(el);
        if ((style.position === 'fixed' || style.position === 'absolute') &&
            style.display !== 'none' &&
            el.offsetWidth > 100 && el.offsetHeight > 100 &&
            el.innerText && el.innerText.trim().length > 5) {
            overlays.push({
                tag: el.tagName,
                cls: (el.className||'').toString().slice(0,60),
                text: el.innerText.trim().slice(0, 400),
                w: el.offsetWidth,
                h: el.offsetHeight
            });
        }
    });
    return overlays;
}''')

print("=== OVERLAYS VISIBLES ===")
for o in result:
    print(f"  [{o['tag']}] {o['w']}x{o['h']} cls={o['cls'][:40]}")
    print(f"    text: {repr(o['text'][:300])}")
    print()

# También buscar role=dialog, role=menu, role=listbox
roles = page.evaluate('''() => {
    const els = document.querySelectorAll('[role="dialog"], [role="menu"], [role="listbox"], [role="presentation"]');
    return Array.from(els).map(e => ({
        role: e.getAttribute('role'),
        text: (e.innerText||'').trim().slice(0, 300),
        vis: e.offsetParent !== null || window.getComputedStyle(e).display !== 'none'
    }));
}''')
print("=== ELEMENTOS CON ROLE ===")
for r in roles:
    if r['text']:
        print(f"  role={r['role']} vis={r['vis']} text={repr(r['text'][:200])}")

ig.close()
