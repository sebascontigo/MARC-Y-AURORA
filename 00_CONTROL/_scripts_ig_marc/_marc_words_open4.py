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

    # Encontrar el contenedor scrollable que CONTIENE el texto "Administrar palabras"
    info = page.evaluate("""() => {
        // buscar el elemento de texto
        const spans = Array.from(document.querySelectorAll('span,div')).filter(e => (e.innerText||'').trim() === 'Administrar palabras y frases personalizadas');
        if (!spans.length) return {err: 'no text element'};
        const target = spans[spans.length-1];
        // subir por el arbol hasta encontrar un ancestro scrollable
        let node = target;
        let scrollContainer = null;
        while (node && node !== document.body) {
            const cs = getComputedStyle(node);
            if ((cs.overflowY === 'auto' || cs.overflowY === 'scroll') && node.scrollHeight > node.clientHeight + 50) {
                scrollContainer = node;
                break;
            }
            node = node.parentElement;
        }
        if (scrollContainer) {
            // hacer scroll del target al centro del contenedor
            const cRect = scrollContainer.getBoundingClientRect();
            const tRect = target.getBoundingClientRect();
            scrollContainer.scrollTop += (tRect.top - cRect.top) - cRect.height/2;
            return {found: true, scrolled: true, containerTag: scrollContainer.tagName};
        }
        return {found: true, scrolled: false, msg: 'no scrollable ancestor'};
    }""")
    print('Scroll info:', info)
    time.sleep(1.2)

    # Ahora leer posicion del target
    pos = page.evaluate("""() => {
        const spans = Array.from(document.querySelectorAll('span,div')).filter(e => (e.innerText||'').trim() === 'Administrar palabras y frases personalizadas');
        if (!spans.length) return null;
        const t = spans[spans.length-1];
        const r = t.getBoundingClientRect();
        return {x: r.x + r.width/2, y: r.y + r.height/2, w: r.width, h: r.height, vis: t.offsetParent !== null};
    }""")
    print('Pos target:', pos)

    if pos and pos.get('vis') and 0 < pos['y'] < 1100:
        page.mouse.click(pos['x'], pos['y'])
        print('>>> Click ok')
        time.sleep(3)
        print('URL:', page.url)
        ta = page.evaluate("""() => Array.from(document.querySelectorAll('textarea,input[type=text]')).map(e=>({tag:e.tagName, ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', vis:e.offsetParent!==null}))""")
        print('=== CAMPOS ===')
        for t in ta:
            print('  ', t)
        body = page.evaluate('() => document.body.innerText.slice(0, 500)')
        print('=== BODY ===')
        print(repr(body[:450]))
    else:
        print('Target no clicable en viewport')
