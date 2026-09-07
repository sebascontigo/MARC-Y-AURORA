from playwright.sync_api import sync_playwright
import time

EMAIL_MARC = "info@marcsouza.com"
TEL_MARC = "642666972"

def enviar_disabled(page):
    return page.evaluate("""() => {
        const b = Array.from(document.querySelectorAll('[role=button],button')).find(e => (e.innerText||'').trim() === 'Enviar');
        return b ? b.getAttribute('aria-disabled') : 'no button';
    }""")

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

    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    # Rellenar email + telefono + TEXT + mostrar contacto
    page.fill('input[type="email"]', EMAIL_MARC, timeout=8000)
    time.sleep(0.5)
    page.fill('input[placeholder="Número de teléfono"]', TEL_MARC, timeout=8000)
    time.sleep(0.5)
    page.evaluate('() => { const r=document.querySelector(\'input[aria-label="TEXT"]\'); if(r && !r.checked) r.click(); }')
    time.sleep(0.5)
    page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Mostrar información de contacto"]\'); if(c && !c.checked) c.click(); }')
    time.sleep(1)

    # Esperar a que el boton se habilite
    enabled = enviar_disabled(page)
    print('Enviar aria-disabled tras rellenar:', enabled)
    waits = 0
    while enabled == 'true' and waits < 10:
        time.sleep(1)
        enabled = enviar_disabled(page)
        waits += 1
    print('Enviar aria-disabled final:', enabled, '(esperas:', waits, ')')

    if enabled != 'true':
        # Monitoreo de red
        posts = []
        def on_response(resp):
            try:
                if resp.request.method == 'POST' and 'instagram' in resp.url:
                    posts.append({'url': resp.url[:90], 'status': resp.status})
            except Exception:
                pass
        page.on('response', on_response)

        # Click nativo
        try:
            page.locator('[role=button]:has-text("Enviar")').first.click(timeout=8000)
            print('Click Enviar ok')
        except Exception as e:
            print('Click fallo:', str(e)[:100])
        time.sleep(6)
        print('=== POST REQUESTS ===')
        for r in posts:
            print(r)
        if not posts:
            print('(ningun POST)')
    else:
        print('BOTON SIGUE DESHABILITADO - no se envia')
