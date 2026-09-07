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

    # Ruta 1: Centro de cuentas (Meta Accounts Center) - perfiles
    print('=== RUTA 1: accounts_center ===')
    for url in [
        'https://www.instagram.com/accounts/accounts_center/',
        'https://accountscenter.instagram.com/',
    ]:
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            time.sleep(4)
            print('URL:', page.url)
            body = page.evaluate('() => document.body.innerText.slice(0, 600)')
            print(repr(body[:500]))
            print('---')
        except Exception as e:
            print('Error en', url, str(e)[:80])

    # Ruta 2: Panel profesional / professional dashboard
    print('=== RUTA 2: professional dashboard ===')
    try:
        page.goto('https://www.instagram.com/marcsouza.7/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
        # buscar boton panel profesional
        js = """() => {
            const els = Array.from(document.querySelectorAll('a,button,[role=button]'));
            const m = els.find(e => /panel|profesional|insights|dashboard/i.test((e.innerText||'') + (e.getAttribute('aria-label')||'')));
            if (m) { return (m.innerText||'') + '|' + (m.getAttribute('aria-label')||'') + '|' + (m.getAttribute('href')||''); }
            return 'NO ENCONTRADO';
        }"""
        print('Panel prof:', page.evaluate(js))
    except Exception as e:
        print('Error ruta2', str(e)[:80])
