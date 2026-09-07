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
    time.sleep(2)

    # Tipear lentamente "Coaching" caracter a caracter
    inp = page.query_selector('input[placeholder="Búsqueda"]')
    if inp is None:
        print('NO HAY INPUT DE BUSQUEDA - quizas el selector se cerro')
        # reabrir
        page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('button,[role=button],div,span'));
            const m = els.find(e => (e.innerText||'').trim() === 'Cambiar');
            if (m) m.click();
        }""")
        time.sleep(2)
        inp = page.query_selector('input[placeholder="Búsqueda"]')

    if inp:
        inp.click()
        inp.fill('')
        time.sleep(0.5)
        page.keyboard.type('Coaching', delay=120)
        time.sleep(3)

        # Buscar el contenedor de resultados (listbox, options)
        results = page.evaluate("""() => {
            const out = [];
            // buscar elementos tipo opcion/lista
            document.querySelectorAll('[role=option],[role=listbox] *,li, [class*="result"], [class*="option"]').forEach(e => {
                const t = (e.innerText||'').trim();
                if (t && t.length < 50 && t.length > 2) out.push(t);
            });
            return [...new Set(out)].slice(0, 30);
        }""")
        print('=== RESULTADOS DOM (Coaching) ===')
        for r in results:
            print(' -', r)
        if not results:
            print('(vacio)')
            # dump body corto
            body = page.evaluate('() => document.body.innerText.slice(0, 400)')
            print(repr(body[:350]))
    else:
        print('Sin input tras reabrir')
