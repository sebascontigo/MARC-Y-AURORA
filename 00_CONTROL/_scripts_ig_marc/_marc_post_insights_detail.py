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
    time.sleep(4)

    # Click en "Ver insights"
    clicked = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('a,button,[role=button],div,span'));
        const m = els.find(e => (e.innerText||'').trim() === 'Ver insights');
        if (m) { m.click(); return 'clicked'; }
        return 'not found';
    }""")
    print('Click Ver insights:', clicked)
    time.sleep(3)

    # Leer el panel de insights
    body = page.evaluate('() => document.body.innerText')
    # buscar la seccion de insights del post
    for kw in ['Visualizaciones', 'Alcance', 'Interacciones', 'Me gusta', 'Guardados', 'Compartidos']:
        idx = body.find(kw)
        if idx > 0:
            print(f'\n[{kw}] en {idx}:')
            print(repr(body[idx:idx+250]))
            break
    else:
        print('\n=== BODY (zona media) ===')
        print(repr(body[300:900]))
