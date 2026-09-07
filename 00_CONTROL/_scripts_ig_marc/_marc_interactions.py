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

    # Ir a configuracion y entrar en "Como pueden interactuar contigo los demas"
    page.goto('https://www.instagram.com/accounts/settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    js_click = """(label) => {
        const els = Array.from(document.querySelectorAll('a,button,[role=button],div,span'));
        const m = els.find(e => (e.innerText||'').trim() === label);
        if (m) { m.click(); return 'clicked'; }
        return 'not found';
    }"""
    print('Click interacciones:', page.evaluate(js_click, 'Cómo pueden interactuar contigo los demás'))
    time.sleep(3)
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 900)')
    print(repr(body[:800]))
