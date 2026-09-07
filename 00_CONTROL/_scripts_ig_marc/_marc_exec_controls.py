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

    # === ACCION: activar Filtro avanzado de comentarios ===
    page.goto('https://www.instagram.com/accounts/settings/v2/hidden_words/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    antes = page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Filtro avanzado de comentarios"]\'); return c? c.checked : "none"; }')
    print('Filtro avanzado ANTES:', antes)

    if antes is False:
        # click nativo en el checkbox
        try:
            page.locator('input[aria-label="Filtro avanzado de comentarios"]').check(timeout=6000)
            print('check nativo ok')
        except Exception as e:
            print('check nativo fallo:', str(e)[:60])
            page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Filtro avanzado de comentarios"]\'); if(c) c.click(); }')
            print('click JS')
        time.sleep(2)
        despues = page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Filtro avanzado de comentarios"]\'); return c? c.checked : "none"; }')
        print('Filtro avanzado DESPUES:', despues)
    else:
        print('Ya estaba activo')

    # === Mapear controles de Comentarios (quien puede comentar) ===
    page.goto('https://www.instagram.com/accounts/comments/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== COMENTARIOS - controles ===')
    ctrls = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=radio],input[type=checkbox]')).map(e=>({type:e.type, al:e.getAttribute('aria-label')||'', checked:e.checked, dis:e.disabled})).filter(x=>x.al)""")
    for c in ctrls:
        print('  ', c)
    body = page.evaluate('() => document.body.innerText')
    # extraer seccion tras "Comentarios"
    idx = body.find('Permitir comentarios')
    if idx < 0:
        idx = body.find('Comentarios de')
    print('  texto relevante:', repr(body[idx:idx+300]) if idx >= 0 else '(no hallado)')

    # === Mapear controles de Mensajes ===
    page.goto('https://www.instagram.com/accounts/messages_and_story_replies/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== MENSAJES - controles ===')
    ctrls = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=radio],input[type=checkbox]')).map(e=>({type:e.type, al:e.getAttribute('aria-label')||'', checked:e.checked, dis:e.disabled})).filter(x=>x.al)""")
    for c in ctrls:
        print('  ', c)
