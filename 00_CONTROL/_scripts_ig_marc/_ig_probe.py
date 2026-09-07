from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=30000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if "instagram.com" in pg.url:
            page = pg; break
    if page is None:
        print("Sin pestaña IG"); raise SystemExit

    # Lectura rápida de marcadores de automatización (sin recargar, sin tocar captcha)
    info = page.evaluate("""
      () => ({
        webdriver: navigator.webdriver,
        languages: navigator.languages,
        plugins_len: navigator.plugins.length,
        ua: navigator.userAgent.slice(0,60),
        has_chrome: typeof window.chrome !== 'undefined',
        url: location.href.slice(0,60)
      })
    """)
    print("webdriver =", info["webdriver"], "  <-- clave")
    print("plugins_len =", info["plugins_len"])
    print("has_chrome =", info["has_chrome"])
    print("url =", info["url"])
    if info["webdriver"]:
        print(">>> La página SÍ está marcada como automatizada. El captcha no renderizará para clic humano aquí.")
        print(">>> Solución: reiniciar Brave sin puerto de depuración y login manual limpio.")
    else:
        print(">>> La página NO está marcada como automatizada. Tu clic manual en F5 + casilla debería funcionar.")
