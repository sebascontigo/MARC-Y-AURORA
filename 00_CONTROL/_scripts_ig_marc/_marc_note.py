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

    # Ir a la bandeja de DMs donde esta la Nota
    page.goto('https://www.instagram.com/direct/inbox/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)
    print('URL:', page.url)

    # Buscar el elemento "Nota..." / "Tu nota"
    nota_info = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('div,span,button,[role=button],a'));
        const cands = els.filter(e => {
            const t = (e.innerText||'').trim();
            return (t === 'Tu nota' || t === 'Nota...' || t === 'Añadir nota' || /nota/i.test(t)) && t.length < 30;
        });
        return cands.map(e => {
            const r = e.getBoundingClientRect();
            return {tag: e.tagName, txt: (e.innerText||'').trim().slice(0,25), x: r.x+r.width/2, y: r.y+r.height/2, w: r.width, h: r.height, vis: e.offsetParent!==null};
        }).filter(x => x.w > 10 && x.h > 5);
    }""")
    print('=== ELEMENTOS NOTA ===')
    for n in nota_info:
        print('  ', n)
