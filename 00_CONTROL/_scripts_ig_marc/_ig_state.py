import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=30000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if "instagram.com" in pg.url:
            page = pg; break
    if page is None:
        print("No hay pestaña de Instagram"); raise SystemExit

    page.bring_to_front()
    print("URL:", page.url[:80])
    time.sleep(3)

    # Estado de frames SIN recargar (para no re-trigger detección)
    print("\nFrames:")
    anchor_found = False
    for fr in page.frames:
        if not fr.url: continue
        tag = ""
        if "anchor" in fr.url: tag = " << ANCHOR (casilla)"; anchor_found = True
        if "bframe" in fr.url: tag = " << BFRAME (reto visual)"
        if "fbsbx" in fr.url: tag = " << contenedor FB"
        print(f"   {fr.url[:95]}{tag}")
        if "anchor" in fr.url:
            try:
                has = fr.evaluate("!!document.querySelector('#recaptcha-anchor')")
                if has:
                    vis = fr.eval_on_selector("#recaptcha-anchor", "el => { const r=el.getBoundingClientRect(); return r.width+'x'+r.height+' visible='+(r.width>0); }")
                    print("      #recaptcha-anchor:", vis)
            except Exception as e:
                print("      err:", str(e)[:80])

    if not anchor_found:
        print("\n>>> El widget anchor NO está presente ahora mismo.")
        print(">>> La página está en el captcha pero el widget se ha auto-eliminado (detección de automatización).")
