from playwright.sync_api import sync_playwright
import time

NUEVO_NOMBRE = "Marc Souza | DESPIERTA"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222', timeout=90000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if 'accountscenter.instagram.com' in pg.url:
            page = pg
            break
    if page is None:
        page = ctx.new_page()
    page.bring_to_front()

    if '/name/' not in page.url:
        page.goto('https://accountscenter.instagram.com/profiles/17841440004587806/name/?entrypoint=fb_account_center', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
    time.sleep(2)

    # Rellenar de nuevo (por si se reseteo)
    try:
        page.fill('input[value]', NUEVO_NOMBRE, timeout=8000)
    except Exception:
        pass
    time.sleep(1)
    val = page.evaluate('() => { const i=document.querySelector(\'input[value]\'); return i? i.value : "none"; }')
    print('Valor en campo:', repr(val))

    # Buscar si aparecio algun boton de guardar/listo/done/save
    js_btns = """() => Array.from(document.querySelectorAll('button,[role=button],input[type=submit]')).map(b=>({txt:(b.innerText||b.value||'').trim().slice(0,30), dis:b.disabled, vis:b.offsetParent!==null})).filter(x=>x.txt)"""
    print('=== BOTONES tras fill ===')
    for b in page.evaluate(js_btns):
        print(b)

    # Intentar Enter en el input
    try:
        page.press('input[value]', 'Enter', timeout=5000)
        print('Enter enviado')
    except Exception as e:
        print('Enter fallo:', str(e)[:60])
    time.sleep(3)

    # Re-leer dialog y URL
    print('URL tras Enter:', page.url)
    dlg = page.evaluate("""() => { const d=document.querySelector('[role=dialog],[role=alertdialog]'); return d? d.innerText.slice(0,500) : 'SIN DIALOG'; }""")
    print('=== DIALOG tras Enter ===')
    print(repr(dlg))
