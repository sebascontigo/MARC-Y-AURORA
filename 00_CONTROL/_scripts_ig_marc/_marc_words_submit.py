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

    if 'hide_custom_words' not in page.url:
        page.goto('https://www.instagram.com/accounts/hide_custom_words/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
    time.sleep(2)

    # Verificar que el textarea sigue relleno
    val = page.evaluate('() => { const t=document.querySelector("textarea"); return t? t.value : "none"; }')
    print('Textarea actual (len):', len(val) if val else 0)
    if not val or len(val) < 10:
        print('Textarea vacio - se reseteo. Abortando para no enviar vacio.')
        raise SystemExit

    # Monitoreo de red
    posts = []
    def on_response(resp):
        try:
            if resp.request.method == 'POST' and 'instagram' in resp.url:
                posts.append({'url': resp.url[:90], 'status': resp.status})
        except Exception:
            pass
    page.on('response', on_response)

    # Click Enviar (nativo primero, fallback JS)
    try:
        page.locator('button:has-text("Enviar")').first.click(timeout=6000)
        print('Click nativo button ok')
    except Exception:
        try:
            page.locator('[role=button]:has-text("Enviar")').first.click(timeout=6000)
            print('Click nativo role=button ok')
        except Exception as e:
            print('Click nativo fallo:', str(e)[:70])
            page.evaluate("""() => {
                const b = Array.from(document.querySelectorAll('button,[role=button]')).find(e => (e.innerText||'').trim() === 'Enviar');
                if (b) b.click();
            }""")
            print('Click JS')
    time.sleep(5)

    print('=== POST REQUESTS ===')
    for r in posts:
        print('  ', r)
    if not posts:
        print('  (ningun POST)')

    # Verificar resultado
    print('URL:', page.url)
    dlg = page.evaluate('() => { const d=document.querySelector("[role=dialog],[role=alertdialog],[role=alert]"); return d? d.innerText.slice(0,300) : "SIN DIALOG"; }')
    print('Dialog:', repr(dlg))
