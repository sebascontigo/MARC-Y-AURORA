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

    # === MENSAJES: cuerpo completo para ver opciones ===
    page.goto('https://www.instagram.com/accounts/messages_and_story_replies/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    body = page.evaluate('() => document.body.innerText')
    # extraer tras el menu lateral (buscar "Mensajes" como seccion)
    idx = body.find('Quién puede enviarte mensajes')
    if idx < 0:
        idx = body.find('Mensajes')
        # saltar el del menu
        idx2 = body.find('Mensajes', idx+10)
        if idx2 > 0: idx = idx2
    print('=== MENSAJES (seccion) ===')
    print(repr(body[idx:idx+500]) if idx >= 0 else repr(body[-500:]))
    # todos los radios/checkbox con texto de label cercano
    ctrls = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('input[type=radio],input[type=checkbox]').forEach(e => {
            // buscar texto asociado
            let label = e.getAttribute('aria-label') || '';
            let parent = e.closest('label,div,span');
            let txt = parent ? (parent.innerText||'').trim().slice(0,50) : '';
            out.push({type:e.type, al:label, txt:txt, checked:e.checked, dis:e.disabled});
        });
        return out;
    }""")
    print('  CONTROLES con texto:')
    for c in ctrls:
        print('   ', c)

    # === HIDDEN WORDS: buscar campo de palabras personalizadas ===
    page.goto('https://www.instagram.com/accounts/settings/v2/hidden_words/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== HIDDEN WORDS - inputs de texto ===')
    inputs = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=text],textarea')).map(e=>({ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', vis:e.offsetParent!==null}))""")
    for i in inputs:
        print('  ', i)
    body2 = page.evaluate('() => document.body.innerText')
    idx = body2.find('Palabras y frases personalizadas')
    if idx < 0:
        idx = body2.find('personalizadas')
    print('  seccion personalizadas:', repr(body2[idx:idx+300]) if idx >= 0 else '(no hallada)')
