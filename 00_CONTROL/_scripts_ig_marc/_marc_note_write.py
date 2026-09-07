from playwright.sync_api import sync_playwright
import time

NOTA = "🧠 DESPIERTA · plazas septiembre abiertas"

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

    # Localizar el contenteditable de la nota
    sel = 'div[aria-label="Obsesión del momento…"]'
    el = page.query_selector(sel)
    if el is None:
        print('No se encontro el contenteditable de nota')
        raise SystemExit

    # Click para enfocar
    try:
        el.click(timeout=5000)
    except Exception:
        page.evaluate("""() => {
            const e = document.querySelector('div[aria-label="Obsesión del momento…"]');
            if (e) { e.focus(); e.click(); }
        }""")
    time.sleep(1)

    # Escribir la nota
    page.keyboard.type(NOTA, delay=30)
    time.sleep(1)

    # Verificar contenido
    val = page.evaluate('() => { const e=document.querySelector(\'div[aria-label="Obsesión del momento…"]\'); return e? e.innerText : "none"; }')
    print('Nota escrita:', repr(val))

    # Buscar boton de publicar/compartir
    btns = page.evaluate("""() => Array.from(document.querySelectorAll('button,[role=button],div,span')).map(b=>({txt:(b.innerText||'').trim().slice(0,30), vis:b.offsetParent!==null})).filter(x=>x.txt && x.vis && /compartir|publicar|listo|enviar|guardar/i.test(x.txt))""")
    print('=== BOTONES PUBLICAR ===')
    for b in btns:
        print('  ', b)
