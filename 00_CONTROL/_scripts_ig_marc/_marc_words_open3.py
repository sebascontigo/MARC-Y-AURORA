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

    # Scroll del contenedor interno que contiene el contenido de settings
    page.evaluate("""() => {
        // buscar el contenedor scrollable principal
        const all = Array.from(document.querySelectorAll('div'));
        const scrollables = all.filter(d => d.scrollHeight > d.clientHeight + 100 && d.clientHeight > 200);
        scrollables.forEach(d => { d.scrollTop = d.scrollHeight; });
        window.scrollTo(0, document.body.scrollHeight);
    }""")
    time.sleep(1.5)

    # Ahora buscar el elemento y su rect
    info = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => /Administrar palabras y frases/i.test((e.innerText||'').trim()) && (e.innerText||'').trim().length < 60);
        const results = els.map(el => {
            const r = el.getBoundingClientRect();
            return {tag: el.tagName, txt: (el.innerText||'').trim().slice(0,40), x: r.x+r.width/2, y: r.y+r.height/2, w: r.width, h: r.height, vis: el.offsetParent !== null};
        }).filter(x => x.w > 30 && x.h > 5 && x.h < 150);
        return results;
    }""")
    print('=== CANDIDATOS ===')
    for i in info:
        print(' ', i)

    # Clicar el primero visible dentro del viewport
    target = None
    for i in info:
        if i['vis'] and 0 < i['y'] < 1100:
            target = i
            break
    if target:
        page.mouse.click(target['x'], target['y'])
        print('>>> Click en', target['x'], target['y'])
        time.sleep(3)
        print('URL:', page.url)
        ta = page.evaluate("""() => Array.from(document.querySelectorAll('textarea,input[type=text]')).map(e=>({tag:e.tagName, ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', vis:e.offsetParent!==null}))""")
        print('=== CAMPOS ===')
        for t in ta:
            print('  ', t)
    else:
        print('Sin candidato visible en viewport')
