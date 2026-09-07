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

    # === HERRAMIENTAS EMPRESARIALES ===
    page.goto('https://www.instagram.com/accounts/professional_account_tools/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('=== HERRAMIENTAS EMPRESARIALES ===')
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText')
    idx = body.find('Controles y herramientas')
    print(repr(body[idx:idx+500]) if idx >= 0 else repr(body[200:700]))

    # === NOTIFICACIONES (para no perder leads) ===
    page.goto('https://www.instagram.com/accounts/notifications/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== NOTIFICACIONES ===')
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText')
    idx = body.find('Notificaciones push')
    print(repr(body[idx:idx+400]) if idx >= 0 else repr(body[200:600]))
    # hrefs de subsecciones
    hrefs = page.evaluate("""() => Array.from(document.querySelectorAll('a[href]')).map(a=>({href:(a.getAttribute('href')||'').slice(0,60), txt:(a.innerText||'').trim().slice(0,40)})).filter(x=>x.txt && /mensaje|comentario|seguidor|push|correo/i.test(x.txt))""")
    print('  subsecciones:')
    for h in hrefs:
        print('   ', h)
