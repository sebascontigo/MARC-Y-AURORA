from playwright.sync_api import sync_playwright
import time

EMAIL_MARC = "info@marcsouza.com"
TEL_MARC = "642666972"

def enviar_state(page):
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

    print('Estado inicial Enviar (aria-disabled):', enviar_state(page))

    # Test 1: solo email
    page.fill('input[type="email"]', EMAIL_MARC, timeout=8000)
    time.sleep(1)
    print('Tras solo email:', enviar_state(page))

    # Test 2: email + telefono
    page.fill('input[placeholder="Número de teléfono"]', TEL_MARC, timeout=8000)
    time.sleep(1)
    print('Tras email + tel:', enviar_state(page))

    # Test 3: email + tel + TEXT
    page.evaluate('() => { const r=document.querySelector(\'input[aria-label="TEXT"]\'); if(r) r.click(); }')
    time.sleep(1)
    print('Tras + TEXT:', enviar_state(page))

    # Test 4: volver a CALL
    page.evaluate('() => { const r=document.querySelector(\'input[aria-label="CALL"]\'); if(r) r.click(); }')
    time.sleep(1)
    print('Tras volver CALL:', enviar_state(page))

    # Test 5: mostrar categoria
    page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Mostrar etiqueta de categoría"]\'); if(c && !c.checked) c.click(); }')
    time.sleep(1)
    print('Tras mostrar categoria:', enviar_state(page))
