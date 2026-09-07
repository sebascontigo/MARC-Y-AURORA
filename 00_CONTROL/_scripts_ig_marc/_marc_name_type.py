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

    # Enfocar el input via JS y seleccionar todo
    page.evaluate("""() => {
        const i = document.querySelector('input[value]');
        if (i) { i.focus(); i.select(); }
    }""")
    time.sleep(0.5)
    # Borrar con teclado
    page.keyboard.press('Control+A')
    page.keyboard.press('Delete')
    time.sleep(0.5)
    # Escribir caracter a caracter
    page.keyboard.type(NUEVO_NOMBRE, delay=40)
    time.sleep(1.5)

    val = page.evaluate('() => { const i=document.querySelector(\'input[value]\'); return i? i.value : "none"; }')
    print('Valor tras tipeo:', repr(val))

    # Buscar boton guardar de nuevo
    hits = page.evaluate("""() => {
        const rx = /listo|guardar|done|save|confirmar|aplicar|enviar|siguiente|continuar|next|submit/i;
        const out = [];
        document.querySelectorAll('button,[role=button],input[type=submit],a,div[tabindex],span[role=button]').forEach(e => {
            const t = (e.innerText || e.value || '').trim();
            const al = e.getAttribute('aria-label') || '';
            if ((t && rx.test(t) && t.length < 30) || (al && rx.test(al))) {
                out.push({tag: e.tagName, txt: t.slice(0,25), al: al.slice(0,25), vis: e.offsetParent !== null, dis: e.disabled});
            }
        });
        return out;
    }""")
    print('=== BOTONES GUARDAR tras tipeo ===')
    for h in hits:
        print(h)
    if not hits:
        print('(ninguno - el formulario no expone guardar)')
