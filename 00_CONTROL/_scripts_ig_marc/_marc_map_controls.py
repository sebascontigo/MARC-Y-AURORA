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

    # 1) Estado etiqueta categoria
    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    cat = page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Mostrar etiqueta de categoría"]\'); return c? c.checked : "none"; }')
    print('Etiqueta categoria (mostrar):', cat)

    # 2) Mapear controles de interaccion
    rutas = {
        'hidden_words': 'https://www.instagram.com/accounts/settings/v2/hidden_words/',
        'comments': 'https://www.instagram.com/accounts/comments/',
        'tags_mentions': 'https://www.instagram.com/accounts/settings/v2/tags_and_mentions/',
        'messages': 'https://www.instagram.com/accounts/messages_and_story_replies/',
    }
    for nombre, url in rutas.items():
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            time.sleep(4)
            print(f'\n=== {nombre} ===')
            print('URL:', page.url)
            body = page.evaluate('() => document.body.innerText.slice(0, 700)')
            print(repr(body[:650]))
            # checkboxes/radios
            ctrls = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=checkbox],input[type=radio]')).map(e=>({type:e.type, al:e.getAttribute('aria-label')||'', checked:e.checked, dis:e.disabled})).filter(x=>x.al)""")
            if ctrls:
                print('  CONTROLES:')
                for c in ctrls:
                    print('   ', c)
        except Exception as e:
            print(f'{nombre} error:', str(e)[:70])
