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

    page.goto('https://www.instagram.com/marcsouza.7/p/DZkutW4Ck7i/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    # Click en "Ver insights" con locator nativo
    try:
        page.locator('text=Ver insights').first.click(timeout=6000)
        print('Click nativo ok')
    except Exception as e:
        print('Click nativo fallo:', str(e)[:60])
        page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('a,button,[role=button],div,span'));
            const m = els.find(e => (e.innerText||'').trim() === 'Ver insights');
            if (m) m.click();
        }""")
        print('Click JS')
    time.sleep(5)

    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText')
    print('Body length:', len(body))
    # buscar metricas
    for kw in ['Visualizaciones', 'Alcance', 'Cuentas alcanzadas', 'Interacciones', 'Guardados', 'Compartidos', 'Me gusta']:
        idx = body.find(kw)
        if idx > 0:
            print(f'\n[{kw}]:')
            print(repr(body[idx:idx+200]))
