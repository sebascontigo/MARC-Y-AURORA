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
    time.sleep(2)

    # Buscar categoria "Coach"
    try:
        page.fill('input[placeholder="Búsqueda"]', 'Coach', timeout=8000)
        print('Busqueda Coach rellenada')
    except Exception as e:
        print('Fill fallo:', str(e)[:70])
        page.evaluate("""() => {
            const i = document.querySelector('input[placeholder="Búsqueda"]');
            if (i) {
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(i, 'Coach');
                i.dispatchEvent(new Event('input', {bubbles:true}));
            }
        }""")
        print('Busqueda Coach via JS')
    time.sleep(2.5)

    # Leer resultados
    body = page.evaluate('() => document.body.innerText.slice(0, 1500)')
    print('=== RESULTADOS ===')
    print(repr(body[:1400]))
