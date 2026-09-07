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

    # === INSIGHTS 30 DIAS (baseline) ===
    page.goto('https://www.instagram.com/accounts/insights/?timeframe=30', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)
    body = page.evaluate('() => document.body.innerText')
    # extraer desde "Insights"
    idx = body.find('Visualizaciones')
    print('=== INSIGHTS 30 DIAS ===')
    print(repr(body[idx:idx+700]) if idx >= 0 else repr(body[:700]))
