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

    page.goto('https://www.instagram.com/accounts/settings/v2/hidden_words/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    # Click en "Administrar palabras y frases personalizadas"
    try:
        page.locator('text=Administrar palabras y frases personalizadas').first.click(timeout=8000)
        print('Click nativo ok')
    except Exception as e:
        print('Click nativo fallo:', str(e)[:70])
        page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('button,[role=button],div,span,a'));
            const m = els.find(e => (e.innerText||'').trim() === 'Administrar palabras y frases personalizadas');
            if (m) m.click();
        }""")
        print('Click JS')
    time.sleep(3)

    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 1000)')
    print('=== BODY ===')
    print(repr(body[:900]))
    print()
    # inputs de texto / textarea para palabras
    inputs = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=text],textarea')).map(e=>({tag:e.tagName, ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', vis:e.offsetParent!==null}))""")
    print('=== INPUTS ===')
    for i in inputs:
        print('  ', i)
