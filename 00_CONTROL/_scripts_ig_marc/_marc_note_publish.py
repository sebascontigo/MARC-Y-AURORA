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

    if 'direct/inbox' not in page.url:
        page.goto('https://www.instagram.com/direct/inbox/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(5)

    # Verificar que la nota sigue escrita
    val = page.evaluate('() => { const e=document.querySelector(\'div[aria-label="Obsesión del momento…"]\'); return e? e.innerText : "none"; }')
    print('Nota actual:', repr(val))
    if not val or 'DESPIERTA' not in val:
        print('La nota no esta escrita - abortando')
        raise SystemExit

    # Monitoreo de red
    posts = []
    def on_response(resp):
        try:
            if resp.request.method == 'POST' and 'instagram' in resp.url:
                posts.append({'url': resp.url[:90], 'status': resp.status})
        except Exception:
            pass
    page.on('response', on_response)

    # Click en Compartir (el boton exacto)
    clicked = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('button,[role=button],div,span'));
        const cands = els.filter(e => (e.innerText||'').trim() === 'Compartir');
        if (!cands.length) return 'not found';
        const t = cands[cands.length-1];
        t.click();
        return 'clicked (' + cands.length + ' cands)';
    }""")
    print('Click Compartir:', clicked)
    time.sleep(5)

    print('=== POST REQUESTS ===')
    for r in posts:
        print('  ', r)
    if not posts:
        print('  (ningun POST)')

    # Verificar resultado
    dlg = page.evaluate('() => { const d=document.querySelector("[role=dialog],[role=alertdialog],[role=alert]"); return d? d.innerText.slice(0,200) : "SIN DIALOG"; }')
    print('Dialog:', repr(dlg))
    print('URL:', page.url)
