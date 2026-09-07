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

    # Click en Cambiar (categoria)
    js = """() => {
        const els = Array.from(document.querySelectorAll('button,[role=button],div,span'));
        const m = els.find(e => (e.innerText||'').trim() === 'Cambiar');
        if (m) { m.click(); return 'clicked'; }
        return 'not found';
    }"""
    print('Click Cambiar:', page.evaluate(js))
    time.sleep(3)
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 1500)')
    print(repr(body[:1400]))
    print()
    # inputs de busqueda de categoria
    fields = page.evaluate("""() => Array.from(document.querySelectorAll('input,textarea')).map(e=>({type:e.type||'', ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', dis:e.disabled, vis:e.offsetParent!==null}))""")
    print('=== CAMPOS ===')
    for f in fields:
        print(f)
