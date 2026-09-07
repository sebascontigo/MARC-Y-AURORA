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
        for pg in ctx.pages:
            if 'instagram.com' in pg.url and 'facebook' not in pg.url:
                page = pg
                break
    if page is None:
        page = ctx.new_page()
    page.bring_to_front()

    # Cerrar dialog de nombre
    page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('div,button,[role=button]'));
        const c = els.find(e => (e.getAttribute('aria-label')||'') === 'Cerrar' || (e.innerText||'').trim() === 'Cerrar');
        if (c) c.click();
    }""")
    time.sleep(1.5)

    # Ir al perfil y explorar el panel profesional / herramientas
    page.goto('https://www.instagram.com/marcsouza.7/', wait_until='domcontentloaded', timeout=60000)
    time.sleep(5)
    print('URL:', page.url)

    # Explorar: buscar enlaces a professional dashboard, insights, business
    links = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('a[href]').forEach(a => {
            const h = a.getAttribute('href') || '';
            const t = (a.innerText || '').trim();
            if (/professional|insights|business|dashboard|ads|tools|promocion/i.test(h + t)) {
                out.push({href: h.slice(0,60), txt: t.slice(0,30)});
            }
        });
        return out;
    }""")
    print('=== ENLACES PROFESIONALES ===')
    for l in links:
        print(l)

    # Probar ir al professional dashboard directamente
    print()
    print('=== PROBANDO professional_dashboard ===')
    try:
        page.goto('https://www.instagram.com/professional_dashboard/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
        print('URL:', page.url)
        body = page.evaluate('() => document.body.innerText.slice(0, 800)')
        print(repr(body[:700]))
    except Exception as e:
        print('Error:', str(e)[:80])
