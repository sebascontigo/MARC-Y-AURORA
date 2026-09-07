from playwright.sync_api import sync_playwright
import time

def buscar(page, termino):
    try:
        page.fill('input[placeholder="Búsqueda"]', termino, timeout=6000)
    except Exception:
        page.evaluate("""(t) => {
            const i = document.querySelector('input[placeholder="Búsqueda"]');
            if (i) {
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(i, t);
                i.dispatchEvent(new Event('input', {bubbles:true}));
            }
        }""", termino)
    time.sleep(2)
    # Leer solo la zona de resultados (antes de "Cuenta profesional" que es el form de abajo)
    body = page.evaluate('() => document.body.innerText')
    # Extraer la seccion de resultados
    idx = body.find('No se han encontrado')
    if idx >= 0:
        return f'[{termino}] SIN RESULTADOS'
    # Los resultados aparecen entre el input y el form. Tomar primeras lineas
    lines = [l.strip() for l in body.split('\n') if l.strip()]
    # Buscar lineas que parezcan categorias (cortas, tras "Búsqueda")
    return f'[{termino}] primeras lineas: ' + ' | '.join(lines[:25])

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
    time.sleep(2)

    for t in ['Salud', 'Entrenador', 'Educación', 'Bienestar']:
        print(buscar(page, t))
        print()
