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

    page.goto('https://www.instagram.com/accounts/settings/v2/hidden_words/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    # Localizar el elemento exacto "Administrar palabras y frases personalizadas" y clicarlo por coordenadas del centro
    info = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('*'));
        const m = els.filter(e => (e.innerText||'').trim() === 'Administrar palabras y frases personalizadas');
        if (!m.length) return null;
        // tomar el mas pequeno (el span/div interno)
        const el = m[m.length-1];
        const r = el.getBoundingClientRect();
        return {tag: el.tagName, x: r.x + r.width/2, y: r.y + r.height/2, w: r.width, h: r.height, count: m.length};
    }""")
    print('Elemento administrar:', info)

    if info and info.get('w', 0) > 0:
        page.mouse.click(info['x'], info['y'])
        print('Click por coordenadas ok')
        time.sleep(3)
        print('URL:', page.url)
        body = page.evaluate('() => document.body.innerText.slice(0, 900)')
        print('=== BODY ===')
        print(repr(body[:800]))
        print()
        ta = page.evaluate("""() => Array.from(document.querySelectorAll('textarea,input[type=text]')).map(e=>({tag:e.tagName, ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', vis:e.offsetParent!==null}))""")
        print('=== CAMPOS ===')
        for t in ta:
            print('  ', t)
    else:
        print('No se encontro el elemento')
