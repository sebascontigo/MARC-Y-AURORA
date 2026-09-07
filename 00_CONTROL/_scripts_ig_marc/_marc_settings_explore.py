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

    # Explorar rutas de configuracion relevantes para un CM
    rutas = {
        'insights': 'https://www.instagram.com/accounts/insights/?timeframe=30',
        'privacy': 'https://www.instagram.com/accounts/privacy_and_security/',
        'notifications': 'https://www.instagram.com/accounts/notifications/',
    }
    for nombre, url in rutas.items():
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            time.sleep(4)
            print(f'=== {nombre} ===')
            print('URL:', page.url)
            body = page.evaluate('() => document.body.innerText.slice(0, 700)')
            print(repr(body[:600]))
            print()
        except Exception as e:
            print(f'{nombre} error:', str(e)[:70])
            print()
