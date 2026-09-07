import time
from playwright.sync_api import sync_playwright

NUEVA_BIO = ("🧠 +10 años de transformaciones reales\n"
             "Psicoterapia · Coaching · Metafísica\n"
             "DESPIERTA · 4 meses para dominar tu mente\n"
             "👇 Plazas septiembre")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=60000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if "instagram.com" in pg.url:
            page = pg; break
    if page is None:
        page = ctx.new_page()

    page.goto("https://www.instagram.com/accounts/edit/", wait_until="commit", timeout=90000)
    page.wait_for_selector('textarea', timeout=30000)
    time.sleep(5)

    # fill() nativo de Playwright dispara correctamente los eventos de React
    page.fill('textarea', NUEVA_BIO)
    time.sleep(2)
    print("campo:", repr(page.input_value('textarea')[:50]))

    # Click NATIVO de Playwright en el botón por texto 'Enviar'
    try:
        page.click('div[role="button"]:has-text("Enviar")', timeout=8000)
        print(">>> click nativo en div[role=button] Enviar")
    except Exception as e:
        print("div role=button falló:", str(e)[:60])
        try:
            page.click('text=Enviar', timeout=8000)
            print(">>> click nativo en text=Enviar")
        except Exception as e2:
            print("text=Enviar falló:", str(e2)[:60])

    # Esperar a que la red se calme
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    time.sleep(5)

    # Verificar
    page.goto("https://www.instagram.com/marcsouza.7/", wait_until="commit", timeout=90000)
    time.sleep(8)
    header = page.evaluate("() => { const h=document.querySelector('header'); return h?h.innerText.slice(0,500):document.body.innerText.slice(0,500); }")
    print("=== PERFIL ===")
    print(header[:350])
    if "+10 años" in header:
        print("OK_BIO_VERIFICADA")
    else:
        print("BIO_SIN_CAMBIO")
