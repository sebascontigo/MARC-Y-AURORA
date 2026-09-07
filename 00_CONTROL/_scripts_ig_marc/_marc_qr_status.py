from playwright.sync_api import sync_playwright
import time, base64, os

OUT = r"C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA IA\MARC Y AURORA\MARC\04_Instagram\ASSETS"

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

    # === DESCARGAR CODIGO QR ===
    page.goto('https://www.instagram.com/qr/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    # Extraer el canvas del QR como dataURL
    dataurl = page.evaluate("""() => {
        const c = document.querySelector('canvas');
        if (!c) return null;
        return c.toDataURL('image/png');
    }""")
    if dataurl and dataurl.startswith('data:image/png'):
        b64 = dataurl.split(',', 1)[1]
        raw = base64.b64decode(b64)
        os.makedirs(OUT, exist_ok=True)
        path = os.path.join(OUT, 'QR_MARCSOUZA7.png')
        with open(path, 'wb') as f:
            f.write(raw)
        print('QR guardado:', path, '| bytes:', len(raw))
    else:
        print('No se pudo extraer canvas QR. dataurl:', str(dataurl)[:60])
        # intentar boton descargar
        btn = page.evaluate("""() => {
            const b = Array.from(document.querySelectorAll('button,[role=button],div,span')).find(e => /Descargar código QR/i.test(e.innerText||''));
            if (b) { b.click(); return 'clicked'; }
            return 'not found';
        }""")
        print('Boton descargar:', btn)

    # === ESTADO DE LA CUENTA (profundidad) ===
    page.goto('https://www.instagram.com/settings/help/account_status/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)
    body = page.evaluate('() => document.body.innerText')
    # buscar contenido de estado (tras el menu)
    for kw in ['Recomendable', 'recomendación', 'Estado de la cuenta', 'infracciones', 'Infracciones', 'elegible', 'monetización', 'contenido']:
        idx = body.find(kw)
        if idx > 300:  # saltar el menu lateral
            print(f'\n[{kw}] en {idx}:')
            print(repr(body[idx:idx+300]))
            break
    else:
        # dump del final del body (contenido principal suele estar al final)
        print('\n=== BODY (zona final) ===')
        print(repr(body[-800:]))
