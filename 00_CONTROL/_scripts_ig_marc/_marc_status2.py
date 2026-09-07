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

    page.goto('https://www.instagram.com/settings/help/account_status/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    # El contenido principal suele estar en el ultimo panel; dump completo y tomar desde la ultima ocurrencia de "Estado de la cuenta"
    body = page.evaluate('() => document.body.innerText')
    last = body.rfind('Estado de la cuenta')
    print('=== ESTADO DE LA CUENTA (contenido principal) ===')
    print(repr(body[last:last+900]))
