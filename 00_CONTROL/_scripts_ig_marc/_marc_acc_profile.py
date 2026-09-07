from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222', timeout=90000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if 'accountscenter.instagram.com' in pg.url:
            page = pg
            break
    if page is None:
        for pg in ctx.pages:
            if 'instagram.com' in pg.url and 'facebook' not in pg.url:
                page = pg
                break
    if page is None:
        page = ctx.new_page()
    page.bring_to_front()

    if 'accountscenter.instagram.com/profiles' not in page.url:
        page.goto('https://accountscenter.instagram.com/profiles/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)

    # Click en el perfil marcsouza.7
    js = """() => {
        const els = Array.from(document.querySelectorAll('a,button,[role=button],div,span'));
        const m = els.find(e => (e.innerText||'').trim() === 'marcsouza.7');
        if (m) { m.click(); return 'clicked'; }
        return 'not found';
    }"""
    print('Click perfil:', page.evaluate(js))
    time.sleep(3)
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 1000)')
    print(repr(body[:900]))
    print()
    # inputs disponibles
    fields = page.evaluate("""() => Array.from(document.querySelectorAll('input,textarea,[contenteditable=true]')).map(e=>({tag:e.tagName, ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', val:(e.value||e.innerText||'').slice(0,50), dis:e.disabled}))""")
    print('=== CAMPOS ===')
    for f in fields:
        print(f)
