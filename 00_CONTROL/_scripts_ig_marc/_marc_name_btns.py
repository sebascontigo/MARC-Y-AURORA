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

    # Dump completo del dialog/modal
    dlg = page.evaluate("""() => {
        const d = document.querySelector('[role=dialog], [role=alertdialog], .x1n2onr6');
        if (!d) return 'SIN DIALOG';
        return d.innerText;
    }""")
    print('=== DIALOG ===')
    print(repr(dlg))
    print()

    # TODOS los elementos clicables con texto corto, incluyendo ocultos
    all_click = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('button, [role=button], a, [role=link], input[type=submit]').forEach(e => {
            const t = (e.innerText || e.value || '').trim();
            out.push({tag: e.tagName, txt: t.slice(0,30), dis: e.disabled, vis: e.offsetParent !== null, cls: (e.className||'').toString().slice(0,40)});
        });
        return out;
    }""")
    print('=== TODOS LOS CLICABLES ===')
    for c in all_click:
        print(c)
