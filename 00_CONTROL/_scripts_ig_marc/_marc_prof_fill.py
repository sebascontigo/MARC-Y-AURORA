from playwright.sync_api import sync_playwright
import time

EMAIL_MARC = "info@marcsouza.com"

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

    # 1) Rellenar email de empresa
    try:
        page.fill('input[type="email"]', EMAIL_MARC, timeout=8000)
        print('Email rellenado:', EMAIL_MARC)
    except Exception as e:
        print('Email fallo:', str(e)[:60])
    time.sleep(1)

    # 2) Seleccionar metodo de contacto TEXT (mejor para funnel que llamada)
    try:
        page.check('input[aria-label="TEXT"]', timeout=5000)
        print('Metodo contacto: TEXT')
    except Exception as e:
        # fallback click en el radio
        page.evaluate("""() => {
            const r = document.querySelector('input[aria-label="TEXT"]');
            if (r) { r.click(); }
        }""")
        print('Metodo contacto: TEXT (via JS)')
    time.sleep(1)

    # 3) Asegurar "Mostrar informacion de contacto" marcado
    try:
        page.check('input[aria-label="Mostrar información de contacto"]', timeout=5000)
        print('Mostrar info contacto: ON')
    except Exception as e:
        print('Mostrar info contacto fallo:', str(e)[:60])
    time.sleep(1)

    # Verificar estado de campos antes de enviar
    estado = page.evaluate("""() => ({
        email: document.querySelector('input[type="email"]') ? document.querySelector('input[type="email"]').value : 'none',
        text_checked: document.querySelector('input[aria-label="TEXT"]') ? document.querySelector('input[aria-label="TEXT"]').checked : 'none',
        mostrar_checked: document.querySelector('input[aria-label="Mostrar información de contacto"]') ? document.querySelector('input[aria-label="Mostrar información de contacto"]').checked : 'none'
    })""")
    print('=== ESTADO ANTES DE ENVIAR ===')
    print(estado)
