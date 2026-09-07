from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222', timeout=90000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if 'instagram.com' in pg.url and 'facebook' not in pg.url:
            page = pg
            break
    if page is None:
        page = ctx.new_page()
    page.bring_to_front()

    # Recargar para ver si persistio
    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    estado = page.evaluate("""() => ({
        email: document.querySelector('input[type="email"]') ? document.querySelector('input[type="email"]').value : 'none',
        whatsapp: document.querySelector('input[placeholder="Número de WhatsApp Business"]') ? document.querySelector('input[placeholder="Número de WhatsApp Business"]').value : 'none',
        tel: document.querySelector('input[placeholder="Número de teléfono"]') ? document.querySelector('input[placeholder="Número de teléfono"]').value : 'none',
        text_checked: document.querySelector('input[aria-label="TEXT"]') ? document.querySelector('input[aria-label="TEXT"]').checked : 'none',
        call_checked: document.querySelector('input[aria-label="CALL"]') ? document.querySelector('input[aria-label="CALL"]').checked : 'none',
        mostrar_checked: document.querySelector('input[aria-label="Mostrar información de contacto"]') ? document.querySelector('input[aria-label="Mostrar información de contacto"]').checked : 'none',
        categoria: (function(){ const els=Array.from(document.querySelectorAll('div,span')); const c=els.find(e=>(e.innerText||'').trim()==='Producto/servicio'); return c? 'found' : 'not found'; })()
    })""")
    print('=== ESTADO TRAS RECARGA ===')
    for k, v in estado.items():
        print(f'{k}: {v}')
