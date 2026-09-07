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

    if 'account_status' not in page.url:
        page.goto('https://www.instagram.com/settings/help/account_status/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(5)

    secciones = ['Contenido suprimido y problemas con los mensajes',
                 'Disponibilidad para menores de 18 años',
                 'Funciones que no puedes usar']
    for s in secciones:
        # click en la seccion (por JS, buscando el elemento clicable)
        clicked = page.evaluate("""(label) => {
            const els = Array.from(document.querySelectorAll('div,span,button,[role=button],a'));
            const cands = els.filter(e => (e.innerText||'').trim() === label);
            if (!cands.length) return 'not found';
            // tomar el ultimo (el mas interno) y subir a un ancestro clicable si es necesario
            let t = cands[cands.length-1];
            t.scrollIntoView({block:'center'});
            t.click();
            return 'clicked';
        }""", s)
        time.sleep(2)
        print(f'[{s}] -> {clicked}')
        # leer el contenido expandido: dump body y extraer tras la seccion
        body = page.evaluate('() => document.body.innerText')
        idx = body.rfind(s)
        if idx >= 0:
            print('   contenido:', repr(body[idx:idx+350]))
        print()
