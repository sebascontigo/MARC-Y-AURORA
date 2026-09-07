from playwright.sync_api import sync_playwright
import time

EMAIL_MARC = "info@marcsouza.com"
TEL_MARC = "642666972"

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

    if 'professional_account_settings' not in page.url:
        page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(5)
    time.sleep(2)

    # Inspeccionar boton Enviar
    btn_info = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('button,[role=button]').forEach(e => {
            if ((e.innerText||'').trim() === 'Enviar') {
                out.push({tag: e.tagName, role: e.getAttribute('role'), disabled: e.disabled,
                          ariaDisabled: e.getAttribute('aria-disabled'), type: e.type||''});
            }
        });
        return out;
    }""")
    print('=== BOTONES ENVIAR ===')
    for b in btn_info:
        print(b)

    # Rellenar
    page.fill('input[type="email"]', EMAIL_MARC, timeout=8000)
    time.sleep(0.3)
    page.fill('input[placeholder="Número de teléfono"]', TEL_MARC, timeout=8000)
    time.sleep(0.3)
    page.evaluate('() => { const r=document.querySelector(\'input[aria-label="TEXT"]\'); if(r) r.click(); }')
    time.sleep(0.3)

    # Monitoreo de red
    requests_log = []
    def on_response(resp):
        try:
            if resp.request.method == 'POST' and 'instagram' in resp.url:
                requests_log.append({'url': resp.url[:90], 'status': resp.status})
        except Exception:
            pass
    page.on('response', on_response)

    # Click nativo en <button> Enviar
    try:
        loc = page.locator('button:has-text("Enviar")')
        print('Count buttons Enviar:', loc.count())
        if loc.count() > 0:
            loc.first.click(timeout=8000)
            print('Click nativo <button> ok')
        else:
            page.locator('[role=button]:has-text("Enviar")').first.click(timeout=8000)
            print('Click nativo role=button ok')
    except Exception as e:
        print('Click nativo fallo:', str(e)[:100])

    time.sleep(6)
    print('=== POST REQUESTS ===')
    for r in requests_log:
        print(r)
    if not requests_log:
        print('(ningun POST)')

    # Verificar persistencia inmediata
    estado = page.evaluate("""() => ({
        email: document.querySelector('input[type="email"]').value,
        tel: document.querySelector('input[placeholder="Número de teléfono"]').value,
        text: document.querySelector('input[aria-label="TEXT"]').checked
    })""")
    print('=== ESTADO INMEDIATO ===', estado)
