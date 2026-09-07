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

    if 'professional_account_settings' not in page.url:
        page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
    time.sleep(2)

    # Verificar que los campos siguen rellenos (puede haberse reseteado)
    estado = page.evaluate("""() => ({
        email: document.querySelector('input[type="email"]') ? document.querySelector('input[type="email"]').value : 'none',
        text_checked: document.querySelector('input[aria-label="TEXT"]') ? document.querySelector('input[aria-label="TEXT"]').checked : 'none',
        mostrar_checked: document.querySelector('input[aria-label="Mostrar información de contacto"]') ? document.querySelector('input[aria-label="Mostrar información de contacto"]').checked : 'none'
    })""")
    print('Estado actual:', estado)

    # Si se reseteo, rellenar de nuevo
    if estado.get('email') != 'info@marcsouza.com':
        page.fill('input[type="email"]', 'info@marcsouza.com', timeout=8000)
        print('Email re-rellenado')
        time.sleep(0.5)
    if not estado.get('text_checked'):
        page.evaluate('() => { const r=document.querySelector(\'input[aria-label="TEXT"]\'); if(r) r.click(); }')
        print('TEXT re-marcado')
        time.sleep(0.5)

    # Click Enviar
    js = """() => {
        const els = Array.from(document.querySelectorAll('button,[role=button],div,span'));
        const m = els.find(e => (e.innerText||'').trim() === 'Enviar');
        if (m) { m.click(); return 'clicked'; }
        return 'not found';
    }"""
    print('Click Enviar:', page.evaluate(js))
    time.sleep(4)

    # Verificar resultado: mensaje de exito o error, y estado de la pagina
    print('URL tras enviar:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 1000)')
    print('=== BODY TRAS ENVIAR ===')
    print(repr(body[:900]))
