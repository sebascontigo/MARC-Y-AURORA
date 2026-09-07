from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222', timeout=90000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if 'instagram.com' in pg.url and 'facebook' not in pg.url:
            page = pg
            break
    if page is None:
        page = ctx.new_page()
    page.bring_to_front()
    page.goto('https://www.instagram.com/marcsouza.7/p/DZkutW4Ck7i/', wait_until='domcontentloaded', timeout=60000)
    time.sleep(5)
    print('URL:', page.url)

    js_click_menu = """() => {
        const s = document.querySelector('svg[aria-label="Más opciones"]');
        if (s) { const b = s.closest('button,div[role=button]') || s; b.click(); return 'ok'; }
        return 'no';
    }"""
    res = page.evaluate(js_click_menu)
    print('Click menu:', res)
    time.sleep(2.5)

    js_dialog = """() => {
        const ds = document.querySelectorAll('[role=dialog]');
        if (!ds.length) return 'SIN DIALOG';
        return ds[ds.length-1].innerText;
    }"""
    dlg = page.evaluate(js_dialog)
    print('=== MENU POST (modo movil) ===')
    print(repr(dlg))
    print()
    print('Contiene Fijar/Anclar?', any(k in dlg for k in ['Fijar', 'fijar', 'Anclar', 'anclar', 'Pin', 'Destacar']))
