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

    # Verificar persistencia del filtro avanzado
    page.goto('https://www.instagram.com/accounts/settings/v2/hidden_words/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    filtro = page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Filtro avanzado de comentarios"]\'); return c? c.checked : "none"; }')
    ocultar_com = page.evaluate('() => { const cs=document.querySelectorAll(\'input[aria-label="Ocultar comentarios"]\'); return cs.length? cs[0].checked : "none"; }')
    print('=== HIDDEN WORDS TRAS RECARGA ===')
    print('  Filtro avanzado comentarios:', filtro)
    print('  Ocultar comentarios (1ro):', ocultar_com)

    # Mapear controles de Comentarios con mas detalle (radios de "Permitir comentarios de")
    page.goto('https://www.instagram.com/accounts/comments/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== COMENTARIOS - radios ===')
    radios = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=radio]')).map(e=>({al:e.getAttribute('aria-label')||'', checked:e.checked, dis:e.disabled}))""")
    for r in radios:
        print('  ', r)
    # checkboxes (GIF etc)
    checks = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=checkbox]')).map(e=>({al:e.getAttribute('aria-label')||'', checked:e.checked, dis:e.disabled}))""")
    print('  CHECKBOXES:')
    for c in checks:
        print('   ', c)
