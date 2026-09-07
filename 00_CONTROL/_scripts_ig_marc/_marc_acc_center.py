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

    page.goto('https://accountscenter.instagram.com/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    # Click en Perfiles y datos personales
    js = """() => {
        const els = Array.from(document.querySelectorAll('a,button,[role=button],div'));
        const m = els.find(e => (e.innerText||'').trim() === 'Perfiles y datos personales');
        if (m) { m.click(); return 'clicked'; }
        return 'not found';
    }"""
    print('Click perfiles:', page.evaluate(js))
    time.sleep(3)
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 800)')
    print(repr(body[:700]))
