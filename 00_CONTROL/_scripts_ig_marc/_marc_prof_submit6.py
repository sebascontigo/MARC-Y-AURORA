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

    # Secuencia EXACTA del diagnostico que habilito el boton:
    # email -> esperar -> tel -> esperar -> TEXT
    page.fill('input[type="email"]', EMAIL_MARC, timeout=8000)
    time.sleep(1.2)
    print('1) email. Enviar:', enviar_disabled(page))

    page.fill('input[placeholder="Número de teléfono"]', TEL_MARC, timeout=8000)
    time.sleep(1.2)
    print('2) + tel. Enviar:', enviar_disabled(page))

    page.evaluate('() => { const r=document.querySelector(\'input[aria-label="TEXT"]\'); if(r) r.click(); }')
    time.sleep(1.2)
    print('3) + TEXT. Enviar:', enviar_disabled(page))

    # Si esta habilitado, enviar YA
    if enviar_disabled(page) != 'true':
        posts = []
        def on_response(resp):
            try:
                if resp.request.method == 'POST' and 'instagram' in resp.url:
                    posts.append({'url': resp.url[:90], 'status': resp.status})
            except Exception:
                pass
        page.on('response', on_response)
        try:
            page.locator('[role=button]:has-text("Enviar")').first.click(timeout=8000)
            print('>>> Click Enviar OK')
        except Exception as e:
            print('>>> Click fallo:', str(e)[:100])
        time.sleep(6)
        print('=== POST REQUESTS ===')
        for r in posts:
            print(r)
        if not posts:
            print('(ningun POST)')
        # Verificar
        time.sleep(2)
        page.reload(wait_until='domcontentloaded')
        time.sleep(5)
        estado = page.evaluate("""() => ({
            email: document.querySelector('input[type="email"]') ? document.querySelector('input[type="email"]').value : 'none',
            tel: document.querySelector('input[placeholder="Número de teléfono"]') ? document.querySelector('input[placeholder="Número de teléfono"]').value : 'none'
        })""")
        print('=== TRAS RECARGA ===', estado)
    else:
        print('BOTON DESHABILITADO - abortando')
