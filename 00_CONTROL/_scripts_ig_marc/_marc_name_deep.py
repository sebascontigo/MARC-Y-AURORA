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

    # Scroll del dialog al fondo
    page.evaluate("""() => {
        document.querySelectorAll('[role=dialog],[role=alertdialog],div').forEach(d => {
            if (d.scrollHeight > d.clientHeight + 30 && d.clientHeight > 100) d.scrollTop = d.scrollHeight;
        });
    }""")
    time.sleep(1.5)

    # Estructura: hay <form>?
    form_info = page.evaluate("""() => {
        const forms = Array.from(document.querySelectorAll('form'));
        return forms.map(f => ({action: f.action, method: f.method, inputs: f.querySelectorAll('input,button').length}));
    }""")
    print('=== FORMS ===')
    print(form_info)

    # Botones dentro del dialog especificamente
    dlg_btns = page.evaluate("""() => {
        const d = document.querySelector('[role=dialog],[role=alertdialog]');
        if (!d) return 'SIN DIALOG';
        return Array.from(d.querySelectorAll('button,[role=button],input[type=submit],a')).map(b => ({
            tag: b.tagName, txt: (b.innerText||b.value||'').trim().slice(0,30),
            type: b.type||'', dis: b.disabled, vis: b.offsetParent !== null,
            al: b.getAttribute('aria-label')||''
        }));
    }""")
    print('=== BOTONES DENTRO DEL DIALOG ===')
    for b in dlg_btns:
        print(b)

    # Re-leer dialog tras scroll
    dlg = page.evaluate("""() => { const d=document.querySelector('[role=dialog],[role=alertdialog]'); return d? d.innerText : 'SIN DIALOG'; }""")
    print('=== DIALOG TRAS SCROLL ===')
    print(repr(dlg))
