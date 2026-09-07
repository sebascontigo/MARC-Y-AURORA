from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222', timeout=90000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if 'instagram.com' in pg.url:
            page = pg
            break
    if page is None:
        page = ctx.new_page()
    page.bring_to_front()

    # Recargar el gestor de palabras
    page.goto('https://www.instagram.com/accounts/hide_custom_words/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    val = page.evaluate('() => { const t=document.querySelector("textarea"); return t? t.value : "none"; }')
    print('=== TEXTAREA TRAS RECARGA ===')
    print('Longitud:', len(val) if val else 0)
    print('Contenido (primeros 200):', repr(val[:200]) if val else val)
    print()
    print('Contiene crypto?', 'crypto' in (val or ''))
    print('Contiene forex?', 'forex' in (val or ''))
    print('Contiene follow for follow?', 'follow for follow' in (val or ''))
