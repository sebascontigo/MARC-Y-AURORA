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

    # Busqueda GLOBAL de botones tipo guardar en todo el documento (incluso ocultos)
    hits = page.evaluate("""() => {
        const rx = /listo|guardar|done|save|confirmar|aplicar|enviar|siguiente|continuar|next|submit/i;
        const out = [];
        document.querySelectorAll('button,[role=button],input[type=submit],a,div[tabindex],span[role=button]').forEach(e => {
            const t = (e.innerText || e.value || '').trim();
            const al = e.getAttribute('aria-label') || '';
            if ((t && rx.test(t) && t.length < 30) || (al && rx.test(al))) {
                out.push({tag: e.tagName, txt: t.slice(0,25), al: al.slice(0,25), vis: e.offsetParent !== null, dis: e.disabled});
            }
        });
        return out;
    }""")
    print('=== BOTONES GUARDAR EN TODO EL DOC ===')
    for h in hits:
        print(h)
    if not hits:
        print('(ninguno)')
