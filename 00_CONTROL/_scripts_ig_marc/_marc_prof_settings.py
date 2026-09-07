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

    # Cuenta profesional
    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('=== CUENTA PROFESIONAL ===')
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 1200)')
    print(repr(body[:1100]))
    print()
    # hrefs internos
    hrefs = page.evaluate("""() => Array.from(document.querySelectorAll('a[href]')).map(a=>({href:(a.getAttribute('href')||'').slice(0,60), txt:(a.innerText||'').trim().slice(0,40)})).filter(x=>x.txt)""")
    print('=== HREFS ===')
    for h in hrefs:
        print(h)
