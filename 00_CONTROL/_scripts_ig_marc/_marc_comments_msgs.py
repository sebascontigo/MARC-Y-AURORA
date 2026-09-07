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

    # === COMENTARIOS: quien puede comentar ===
    page.goto('https://www.instagram.com/accounts/comments/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('=== COMENTARIOS ===')
    # los radios no tienen aria-label; leer el texto y el checked
    body = page.evaluate('() => document.body.innerText')
    idx = body.find('Permitir comentarios de')
    print(repr(body[idx:idx+200]) if idx >= 0 else '(seccion no hallada)')
    # estado de los radios
    radios = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=radio]')).map((e,i)=>({i, checked:e.checked}))""")
    print('  radios:', radios)

    # === MENSAJES: cuerpo completo ===
    page.goto('https://www.instagram.com/accounts/messages_and_story_replies/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== MENSAJES (cuerpo) ===')
    body = page.evaluate('() => document.body.innerText')
    # buscar seccion de control de mensajes (saltar menu lateral)
    idx = body.find('Mensajes')
    # encontrar la segunda ocurrencia (la seccion, no el menu)
    idx2 = body.find('Quién puede', idx)
    if idx2 < 0:
        idx2 = body.find('Tus seguidores', idx)
    print(repr(body[idx2:idx2+500]) if idx2 >= 0 else repr(body[400:900]))
    radios = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=radio]')).map((e,i)=>({i, checked:e.checked, al:e.getAttribute('aria-label')||''}))""")
    print('  radios:', radios)

    # === ETIQUETAS Y MENCIONES ===
    page.goto('https://www.instagram.com/accounts/settings/v2/tags_and_mentions/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== ETIQUETAS Y MENCIONES ===')
    radios = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=radio]')).map(e=>({al:e.getAttribute('aria-label')||'', checked:e.checked}))""")
    for r in radios:
        print('  ', r)
