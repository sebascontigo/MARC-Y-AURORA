from playwright.sync_api import sync_playwright
import time

EMAIL_MARC = "info@marcsouza.com"
TEL_MARC = "642666972"
UA_MOVIL = "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36"

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

    # Restaurar emulacion movil via CDP
    try:
        cdp = ctx.new_cdp_session(page)
        cdp.send('Emulation.setUserAgentOverride', {
            'userAgent': UA_MOVIL,
            'platform': 'Linux armv8l',
        })
        cdp.send('Emulation.setDeviceMetricsOverride', {
            'width': 412, 'height': 915, 'deviceScaleFactor': 2.6, 'mobile': True
        })
        print('Emulacion movil restaurada via CDP')
    except Exception as e:
        print('CDP emulation fallo:', str(e)[:80])

    # Recargar para aplicar UA
    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)
    ua = page.evaluate('() => navigator.userAgent')
    print('UA ahora movil?', any(k in ua for k in ['Android', 'Mobile']))
    print('URL:', page.url)

    # Mapear campos
    fields = page.evaluate("""() => Array.from(document.querySelectorAll('input,textarea')).map(e=>({
        type: e.type||'', ph: e.placeholder||'', al: e.getAttribute('aria-label')||'', dis: e.disabled, vis: e.offsetParent!==null
    }))""")
    print('=== CAMPOS ===')
    for f in fields:
        print(f)
