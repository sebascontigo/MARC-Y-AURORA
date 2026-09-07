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

    # === NOTIFICACIONES PUSH ===
    page.goto('https://www.instagram.com/push/web/settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('=== NOTIFICACIONES PUSH ===')
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText')
    idx = body.find('Notificaciones push')
    print(repr(body[idx:idx+600]) if idx >= 0 else repr(body[100:700]))
    # checkboxes/radios
    ctrls = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=checkbox],input[type=radio],select')).map(e=>({tag:e.tagName, type:e.type||'', al:e.getAttribute('aria-label')||'', name:e.name||'', checked:e.checked, dis:e.disabled}))""")
    print('  CONTROLES:')
    for c in ctrls:
        print('   ', c)

    # === NOTIFICACIONES EMAIL ===
    page.goto('https://www.instagram.com/emails/settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== NOTIFICACIONES EMAIL ===')
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText')
    idx = body.find('Notificaciones por correo')
    print(repr(body[idx:idx+500]) if idx >= 0 else repr(body[100:600]))
    ctrls = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=checkbox],input[type=radio],select')).map(e=>({tag:e.tagName, type:e.type||'', al:e.getAttribute('aria-label')||'', name:e.name||'', checked:e.checked, dis:e.disabled}))""")
    print('  CONTROLES:')
    for c in ctrls:
        print('   ', c)
