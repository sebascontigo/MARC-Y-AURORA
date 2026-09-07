from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222', timeout=90000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if 'accountscenter.instagram.com' in pg.url:
            page = pg
            break
    if page is None:
        page = ctx.new_page()
    page.bring_to_front()
    time.sleep(2)
    print('URL:', page.url)

    # Click en la fila "Nombre"
    js = """() => {
        const els = Array.from(document.querySelectorAll('a,button,[role=button],div,span'));
        // buscar el elemento clicable cuya etiqueta sea exactamente 'Nombre' (no 'Nombre de usuario')
        const cands = els.filter(e => (e.innerText||'').trim() === 'Nombre');
        if (cands.length) { cands[cands.length-1].click(); return 'clicked ' + cands.length + ' cands'; }
        return 'not found';
    }"""
    print('Click Nombre:', page.evaluate(js))
    time.sleep(3)
    print('URL tras click:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 800)')
    print(repr(body[:700]))
    print()
    fields = page.evaluate("""() => Array.from(document.querySelectorAll('input,textarea,[contenteditable=true]')).map(e=>({tag:e.tagName, ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', val:(e.value||e.innerText||'').slice(0,50), dis:e.disabled}))""")
    print('=== CAMPOS ===')
    for f in fields:
        print(f)
