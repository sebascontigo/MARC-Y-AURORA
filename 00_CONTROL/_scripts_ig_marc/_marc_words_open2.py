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

    # Encontrar el elemento VISIBLE y hacer scrollIntoView + click
    info = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => (e.innerText||'').trim() === 'Administrar palabras y frases personalizadas');
        // filtrar a los visibles con rect razonable
        const vis = els.map(el => {
            const r = el.getBoundingClientRect();
            return {el, r, visible: el.offsetParent !== null};
        }).filter(x => x.visible && x.r.width > 50 && x.r.height < 200);
        if (!vis.length) return {found: false, total: els.length};
        const target = vis[0];
        target.el.scrollIntoView({block: 'center'});
        const r2 = target.el.getBoundingClientRect();
        return {found: true, x: r2.x + r2.width/2, y: r2.y + r2.height/2, w: r2.width, h: r2.height, tag: target.el.tagName};
    }""")
    print('Elemento visible:', info)

    if info.get('found'):
        time.sleep(0.8)  # esperar scroll
        # re-leer posicion tras scroll
        pos = page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('*')).filter(e => (e.innerText||'').trim() === 'Administrar palabras y frases personalizadas');
            const vis = els.map(el => {const r = el.getBoundingClientRect(); return {el, r};}).filter(x => x.el.offsetParent !== null && x.r.width > 50 && x.r.height < 200);
            if (!vis.length) return null;
            const r = vis[0].r;
            return {x: r.x + r.width/2, y: r.y + r.height/2};
        }""")
        if pos:
            page.mouse.click(pos['x'], pos['y'])
            print('Click en', pos)
            time.sleep(3)
            print('URL:', page.url)
            # buscar textarea/input
            ta = page.evaluate("""() => Array.from(document.querySelectorAll('textarea,input[type=text]')).map(e=>({tag:e.tagName, ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', vis:e.offsetParent!==null}))""")
            print('=== CAMPOS ===')
            for t in ta:
                print('  ', t)
            body = page.evaluate('() => document.body.innerText.slice(0, 600)')
            print('=== BODY ===')
            print(repr(body[:500]))
    else:
        print('No hay elemento visible. Total matches:', info.get('total'))
