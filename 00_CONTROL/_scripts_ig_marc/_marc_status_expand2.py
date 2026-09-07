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

    if 'account_status' not in page.url:
        page.goto('https://www.instagram.com/settings/help/account_status/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(5)

    # Las secciones pueden ser enlaces; buscar hrefs
    hrefs = page.evaluate("""() => Array.from(document.querySelectorAll('a[href]')).map(a=>({href:(a.getAttribute('href')||'').slice(0,70), txt:(a.innerText||'').trim().slice(0,50)})).filter(x=>x.txt && /menores|funciones|suprimido/i.test(x.txt))""")
    print('=== HREFS de secciones ===')
    for h in hrefs:
        print('  ', h)

    # Navegar a cada una si tiene href
    for h in hrefs:
        if h['href'] and not h['href'].startswith('http'):
            try:
                page.goto('https://www.instagram.com' + h['href'], wait_until='domcontentloaded', timeout=20000)
                time.sleep(4)
                body = page.evaluate('() => document.body.innerText')
                last = body.rfind(h['txt'][:20])
                print(f"\n[{h['txt']}]")
                print(repr(body[last:last+300]) if last >= 0 else repr(body[200:500]))
            except Exception as e:
                print(f"[{h['txt']}] error:", str(e)[:60])
