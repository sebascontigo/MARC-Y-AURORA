from playwright.sync_api import sync_playwright
import time

EMAIL_MARC = "info@marcsouza.com"
TEL_MARC = "642666972"

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

    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    # Inspeccionar el boton Enviar en detalle
    btn_info = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('button,[role=button],div,span').forEach(e => {
            if ((e.innerText||'').trim() === 'Enviar') {
                out.push({
                    tag: e.tagName,
                    role: e.getAttribute('role'),
                    disabled: e.disabled,
                    ariaDisabled: e.getAttribute('aria-disabled'),
                    cls: (e.className||'').toString().slice(0,60),
                    type: e.type || '',
                    parent: e.parentElement ? e.parentElement.tagName : ''
                });
            }
        });
        return out;
    }""")
    print('=== BOTONES ENVIAR ===')
    for b in btn_info:
        print(b)

    # Rellenar campos
    page.fill('input[type="email"]', EMAIL_MARC, timeout=8000)
    time.sleep(0.3)
    page.fill('input[placeholder="Número de teléfono"]', TEL_MARC, timeout=8000)
    time.sleep(0.3)
    page.evaluate('() => { const r=document.querySelector(\'input[aria-label="TEXT"]\'); if(r) r.click(); }')
    time.sleep(0.3)

    # Capturar requests de red al enviar
    requests_log = []
    def on_request(req):
        if 'instagram' in req.url and req.method == 'POST':
            requests_log.append({'url': req.url[:80], 'method': req.method})
    def on_response(resp):
        if 'instagram' in resp.url and resp.request.method == 'POST':
            requests_log.append({'url': resp.url[:80], 'status': resp.status})
    page.on('request', on_request)
    page.on('response', on_response)

    # Click nativo de Playwright en el boton Enviar (el <button> real si existe)
    try:
        btn = page.locator('button:has-text("Enviar")').first
        print('Locator button count:', page.locator('button:has-text("Enviar")').count())
        btn.click(timeout=8000)
        print('Click nativo en <button> ok')
    except Exception as e:
        print('Click nativo fallo:', str(e)[:80])
        # fallback: role=button
        try:
            page.locator('[role=button]:has-text("Enviar")').first.click(timeout=8000)
            print('Click en role=button ok')
        except Exception as e2:
            print('Click role=button fallo:', str(e2)[:80])

    time.sleep(5)
    print('=== REQUESTS POST ===')
    for r in requests_log:
        print(r)
    if not requests_log:
        print('(ningun POST capturado)')
