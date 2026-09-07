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
    print('URL:', page.url)

    # fill directo sin click
    try:
        page.fill('input[value="Despierta"]', NUEVO_NOMBRE, timeout=8000)
        print('fill por selector ok')
    except Exception as e:
        print('fill por selector fallo:', str(e)[:60])
        # fallback: JS
        page.evaluate("""(v) => {
            const i = document.querySelector('input[value="Despierta"]') || document.querySelector('input');
            if (i) {
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(i, v);
                i.dispatchEvent(new Event('input', {bubbles:true}));
            }
        }""", NUEVO_NOMBRE)
        print('fill por JS ok')

    time.sleep(1)
    val = page.evaluate('() => { const i=document.querySelector(\'input[value]\'); return i? i.value : "none"; }')
    print('Valor en campo ahora:', repr(val))

    # Botones
    js_btns = """() => Array.from(document.querySelectorAll('button,[role=button]')).map(b=>({txt:(b.innerText||'').trim().slice(0,30), dis:b.disabled, vis:b.offsetParent!==null})).filter(x=>x.txt)"""
    print('=== BOTONES ===')
    for b in page.evaluate(js_btns):
        print(b)
