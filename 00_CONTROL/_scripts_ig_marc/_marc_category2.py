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

    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    # Click nativo en "Cambiar" (categoria)
    try:
        loc = page.locator('text=Cambiar').first
        print('Count Cambiar:', page.locator('text=Cambiar').count())
        loc.click(timeout=8000)
        print('Click nativo Cambiar ok')
    except Exception as e:
        print('Click nativo fallo:', str(e)[:90])
        # fallback JS
        page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('button,[role=button],div,span'));
            const m = els.find(e => (e.innerText||'').trim() === 'Cambiar');
            if (m) m.click();
        }""")
        print('Click JS Cambiar')
    time.sleep(3)

    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 1200)')
    print('=== BODY TRAS CLICK CAMBIAR ===')
    print(repr(body[:1100]))
    print()
    # buscar input de busqueda de categoria
    fields = page.evaluate("""() => Array.from(document.querySelectorAll('input,textarea')).map(e=>({type:e.type||'', ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', vis:e.offsetParent!==null}))""")
    print('=== CAMPOS ===')
    for f in fields:
        print(f)
