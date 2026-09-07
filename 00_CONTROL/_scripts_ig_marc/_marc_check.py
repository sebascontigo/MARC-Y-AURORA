from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=30000)
    ctx = browser.contexts[0]
    print(f"Pestañas abiertas: {len(ctx.pages)}")
    ig_page = None
    for i, pg in enumerate(ctx.pages):
        u = pg.url
        print(f"  [{i}] {u[:100]}")
        if "instagram.com" in u:
            ig_page = pg

    if ig_page is None:
        print("\nNo hay pestaña de Instagram. Abriendo perfil público de Marc...")
        ig_page = ctx.new_page()
        ig_page.goto("https://www.instagram.com/centro_de_bienestar_inanis/", wait_until="domcontentloaded", timeout=45000)

    import time
    time.sleep(4)
    print("\nURL IG:", ig_page.url[:90])

    # Detectar sesión: ¿aparece el avatar de perfil propio o botón de login?
    estado = ig_page.evaluate("""
      () => {
        const out = {};
        out.title = document.title;
        // botón de login presente?
        out.login_form = !!document.querySelector('input[name="password"]');
        // nav con iconos de home/DM = sesión iniciada
        out.nav_svg = document.querySelectorAll('svg[aria-label]').length;
        // enlace a /accounts/login/?
        out.login_link = !!document.querySelector('a[href*="/accounts/login"]');
        // avatar propio en nav (sesión iniciada)
        const imgs = Array.from(document.querySelectorAll('img')).map(i=>i.alt||'');
        out.img_alts = imgs.slice(0,8);
        // texto del body (primeros 300)
        out.body = document.body ? document.body.innerText.slice(0,400) : '';
        return out;
      }
    """)
    print("title:", estado["title"])
    print("login_form:", estado["login_form"], "| login_link:", estado["login_link"], "| svgs:", estado["nav_svg"])
    print("body:", repr(estado["body"][:300]))

    if estado["login_form"] or "login" in ig_page.url:
        print("\n>>> ESTADO: SIN SESIÓN (login/captcha pendiente)")
    else:
        print("\n>>> ESTADO: posible sesión iniciada — verificar con navegación a /accounts/edit/")
