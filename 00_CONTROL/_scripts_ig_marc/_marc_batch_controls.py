from playwright.sync_api import sync_playwright
import time

PALABRAS_ANTISPAM = "crypto, forex, inversion, gana dinero, trabaja desde casa, multinivel, mlm, dropshipping, hazte rico, dinero facil, bitcoin, trading, apuesta, casino, prestamo, credito rapido, bajar de peso rapido, milagro, cura, gratis, sorteo, ganador, premio, click aqui, enlace en bio spam, follow for follow, f4f, l4l, dm for promo"

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

    resultados = {}

    # === 1) PRIVACIDAD DE CUENTA (debe ser PUBLICA para ads) ===
    try:
        page.goto('https://www.instagram.com/accounts/settings/v2/account_privacy/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
        priv = page.evaluate("""() => {
            const c = document.querySelector('input[type=checkbox]');
            const body = document.body.innerText;
            const esPrivada = /cuenta privada/i.test(body);
            return {checkbox: c ? {checked: c.checked, al: c.getAttribute('aria-label')} : null,
                    menciona_privada: esPrivada};
        }""")
        resultados['privacidad'] = priv
        print('=== PRIVACIDAD ===', priv)
    except Exception as e:
        print('privacidad error:', str(e)[:60])

    # === 2) PALABRAS FILTRADAS PERSONALIZADAS ===
    try:
        page.goto('https://www.instagram.com/accounts/settings/v2/hidden_words/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
        # buscar el enlace/boton administrar y su href
        href = page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('a[href],button,[role=button],div,span'));
            const m = els.find(e => /Administrar palabras/i.test(e.innerText||''));
            if (m) return {tag: m.tagName, href: m.getAttribute('href')||'', txt: (m.innerText||'').slice(0,40)};
            return null;
        }""")
        print('=== ADMIN PALABRAS elemento ===', href)
        if href and href.get('href'):
            page.goto('https://www.instagram.com' + href['href'], wait_until='domcontentloaded', timeout=30000)
            time.sleep(4)
            print('URL admin palabras:', page.url)
            # buscar textarea/input para palabras
            ta = page.evaluate("""() => Array.from(document.querySelectorAll('textarea,input[type=text]')).map(e=>({tag:e.tagName, ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', vis:e.offsetParent!==null}))""")
            print('  campos:', ta)
            resultados['admin_palabras_url'] = page.url
            resultados['admin_palabras_campos'] = ta
    except Exception as e:
        print('palabras error:', str(e)[:60])

    # === 3) MENSAJES: verificar que DMs estan abiertos ===
    try:
        page.goto('https://www.instagram.com/accounts/messages_and_story_replies/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
        body = page.evaluate('() => document.body.innerText')
        # buscar la seccion de control de mensajes
        idx = body.find('Tus seguidores')
        if idx < 0:
            idx = body.find('Otras personas')
        resultados['mensajes_seccion'] = body[idx:idx+400] if idx >= 0 else body[-400:]
        print('=== MENSAJES seccion ===')
        print(repr(resultados['mensajes_seccion'][:350]))
    except Exception as e:
        print('mensajes error:', str(e)[:60])

    print('\n=== RESUMEN ===')
    for k, v in resultados.items():
        print(f'{k}: {str(v)[:200]}')
