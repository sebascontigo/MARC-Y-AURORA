import time
from playwright.sync_api import sync_playwright

NUEVO_NOMBRE = "Marc Souza · Despierta"
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
    try:
        page.wait_for_selector('textarea', timeout=30000)
    except Exception:
        pass
    time.sleep(8)

    # Dump completo de valores de inputs (el nombre puede cargar tarde)
    vals = page.evaluate("""
      () => Array.from(document.querySelectorAll('input, textarea, [contenteditable="true"]')).map((el,i) => ({
        i, tag: el.tagName, type: el.type||'', val: (el.value !== undefined ? el.value : el.innerText).slice(0,80),
        aria: el.getAttribute('aria-label')||'', ph: el.placeholder||''
      }))
    """)
    print("=== CAMPOS (dump) ===")
    for v in vals:
        print(f"  [{v['i']}] {v['tag']} t={v['type']} aria={v['aria'][:30]!r} ph={v['ph'][:20]!r} val={v['val'][:50]!r}")

    # BIO
    bio = page.query_selector('textarea')
    if bio:
        bio.click()
        bio.fill(NUEVA_BIO)
        print("\nBio rellenada")

    # NOMBRE: buscar input cuyo valor contenga 'Despierta' o el primer text input junto al avatar
    nombre_ok = False
    for el in page.query_selector_all('input'):
        try:
            v = el.input_value()
            if "Despierta" in v or "Marc" in v:
                el.click(); el.fill(NUEVO_NOMBRE)
                print("Nombre actualizado desde input con valor:", repr(v[:40]))
                nombre_ok = True; break
        except Exception:
            pass
    if not nombre_ok:
        # contenteditable
        for el in page.query_selector_all('[contenteditable="true"]'):
            try:
                t = el.inner_text()
                if "Despierta" in t or "Marc" in t:
                    el.click(); page.keyboard.press("Control+a"); page.keyboard.type(NUEVO_NOMBRE)
                    print("Nombre actualizado desde contenteditable:", repr(t[:40]))
                    nombre_ok = True; break
            except Exception:
                pass
    if not nombre_ok:
        print("AVISO: campo nombre no localizado; solo se guardará la bio")

    time.sleep(1)
    # SUBMIT
    sub = page.query_selector('button[type="submit"]')
    if sub:
        sub.click()
        print(">>> Submit clicado")
    time.sleep(8)
    print("URL tras submit:", page.url[:70])

    # VERIFICACIÓN: recargar perfil
    page.goto("https://www.instagram.com/marcsouza.7/", wait_until="commit", timeout=90000)
    time.sleep(8)
    header = page.evaluate("""
      () => {
        const h = document.querySelector('header');
        return h ? h.innerText.slice(0, 500) : document.body.innerText.slice(0, 500);
      }
    """)
    print("\n=== PERFIL TRAS CAMBIO ===")
    print(header)
