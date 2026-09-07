from playwright.sync_api import sync_playwright
import time

def enviar_disabled(page):
    return page.evaluate("""() => {
        const b = Array.from(document.querySelectorAll('[role=button],button')).find(e => (e.innerText||'').trim() === 'Enviar');
        return b ? b.getAttribute('aria-disabled') : 'no button';
    }""")

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

    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    # Activar "Mostrar etiqueta de categoria"
    page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Mostrar etiqueta de categoría"]\'); if(c && !c.checked) c.click(); }')
    time.sleep(1)
    cat_label = page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Mostrar etiqueta de categoría"]\'); return c? c.checked : "none"; }')
    print('Mostrar etiqueta categoria:', cat_label)

    # Rellenar email+tel para habilitar Enviar (si se reseteo)
    email_val = page.evaluate('() => document.querySelector(\'input[type="email"]\').value')
    if not email_val:
        page.fill('input[type="email"]', 'info@marcsouza.com', timeout=8000)
        time.sleep(0.5)
    tel_val = page.evaluate('() => document.querySelector(\'input[placeholder="Número de teléfono"]\').value')
    if not tel_val:
        page.fill('input[placeholder="Número de teléfono"]', '642666972', timeout=8000)
        time.sleep(0.5)
    # TEXT
    page.evaluate('() => { const r=document.querySelector(\'input[aria-label="TEXT"]\'); if(r && !r.checked) r.click(); }')
    time.sleep(1)

    print('Enviar aria-disabled:', enviar_disabled(page))
    waits = 0
    while enviar_disabled(page) == 'true' and waits < 8:
        time.sleep(1); waits += 1
    print('Enviar final:', enviar_disabled(page))

    if enviar_disabled(page) != 'true':
        posts = []
        def on_response(resp):
            try:
                if resp.request.method == 'POST' and 'instagram' in resp.url:
                    posts.append({'url': resp.url[:90], 'status': resp.status})
            except Exception:
                pass
        page.on('response', on_response)
        # click via JS en el div role=button Enviar
        page.evaluate("""() => {
            const b = Array.from(document.querySelectorAll('[role=button],button')).find(e => (e.innerText||'').trim() === 'Enviar');
            if (b) b.click();
        }""")
        print('>>> Click Enviar (JS)')
        time.sleep(6)
        print('=== POST ===')
        for r in posts:
            print(r)
        if not posts:
            print('(ningun POST)')
    else:
        print('Enviar deshabilitado')
