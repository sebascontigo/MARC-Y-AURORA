from playwright.sync_api import sync_playwright
import time

PALABRAS = "crypto, forex, inversion, gana dinero, trabaja desde casa, multinivel, mlm, dropshipping, hazte rico, dinero facil, bitcoin, trading, apuesta, casino, prestamo, credito rapido, bajar de peso rapido, milagro, cura milagrosa, gratis, sorteo, ganador, premio, click aqui, follow for follow, f4f, l4l, dm for promo, promo your post, buy followers, compra seguidores"

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

    if 'hide_custom_words' not in page.url:
        page.goto('https://www.instagram.com/accounts/hide_custom_words/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
    time.sleep(2)
    print('URL:', page.url)

    # Ver estado actual del textarea
    antes = page.evaluate('() => { const t=document.querySelector("textarea"); return t? t.value : "none"; }')
    print('Textarea ANTES:', repr(antes[:100]) if antes else antes)

    # Rellenar con la lista de palabras
    try:
        page.fill('textarea', PALABRAS, timeout=8000)
        print('fill ok')
    except Exception as e:
        print('fill fallo:', str(e)[:60])
        page.evaluate("""(v) => {
            const t = document.querySelector('textarea');
            if (t) {
                const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                setter.call(t, v);
                t.dispatchEvent(new Event('input', {bubbles:true}));
            }
        }""", PALABRAS)
        print('fill via JS')
    time.sleep(1)

    despues = page.evaluate('() => { const t=document.querySelector("textarea"); return t? t.value : "none"; }')
    print('Textarea DESPUES (primeros 120):', repr(despues[:120]) if despues else despues)

    # Buscar boton de guardar/anadir
    btns = page.evaluate("""() => Array.from(document.querySelectorAll('button,[role=button]')).map(b=>({txt:(b.innerText||'').trim().slice(0,30), dis:b.disabled, ariaDis:b.getAttribute('aria-disabled'), vis:b.offsetParent!==null})).filter(x=>x.txt)""")
    print('=== BOTONES ===')
    for b in btns:
        print('  ', b)
