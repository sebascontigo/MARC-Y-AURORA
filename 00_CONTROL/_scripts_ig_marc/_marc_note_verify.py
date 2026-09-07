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

    # Recargar la bandeja
    page.goto('https://www.instagram.com/direct/inbox/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    # Leer la zona de la nota
    body = page.evaluate('() => document.body.innerText.slice(0, 500)')
    print('=== BANDEJA TRAS RECARGA ===')
    print(repr(body[:450]))
    print()
    print('Aparece la nota DESPIERTA?', 'DESPIERTA' in body)
    print('Sigue el editor (Obsesion del momento)?', 'Obsesión del momento' in body)

    # Buscar el texto de la nota en el avatar
    nota_txt = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('div,span'));
        const m = els.filter(e => /DESPIERTA/.test(e.innerText||'') && (e.innerText||'').length < 60);
        return m.map(e => (e.innerText||'').trim()).slice(0,5);
    }""")
    print('Elementos con DESPIERTA:', nota_txt)
