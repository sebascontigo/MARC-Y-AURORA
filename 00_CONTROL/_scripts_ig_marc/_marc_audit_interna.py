import time, json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=30000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if "instagram.com" in pg.url:
            page = pg; break
    if page is None:
        print("ERROR: sin pestaña IG"); raise SystemExit

    # 1) Confirmar acceso de edición (prueba definitiva de sesión propia)
    page.goto("https://www.instagram.com/accounts/edit/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)
    print("URL edit:", page.url[:80])
    if "/accounts/login" in page.url:
        print(">>> SIN ACCESO DE EDICIÓN (redirige a login)"); raise SystemExit

    body = page.evaluate("document.body.innerText.slice(0, 1200)")
    print("=== PÁGINA DE EDICIÓN (primeros 1200 chars) ===")
    print(body)

    # 2) Volver al perfil y leer el grid completo
    page.goto("https://www.instagram.com/marcsouza.7/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)

    data = page.evaluate("""
      () => {
        const out = {};
        // header completo
        const header = document.querySelector('header');
        out.header = header ? header.innerText.slice(0,600) : '';
        // bio section
        const bioEl = document.querySelector('div.-vDIg') || document.querySelector('header section div');
        out.bio = bioEl ? bioEl.innerText : '';
        // links externos en bio
        out.links = Array.from(document.querySelectorAll('header a[href]')).map(a=>({href:a.href, txt:(a.innerText||'').slice(0,40)})).filter(l=>l.href.includes('http') && !l.href.includes('instagram.com'));
        // posts del grid
        out.posts = Array.from(document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]')).map(a => ({
          href: a.href,
          label: a.getAttribute('aria-label') || '',
          time: (a.querySelector('time')||{}).dateTime || ''
        }));
        // highlights
        out.highlights = Array.from(document.querySelectorAll('a[href*="/stories/highlights/"]')).map(a => a.getAttribute('aria-label') || a.innerText).filter(Boolean);
        // botones
        out.buttons = Array.from(document.querySelectorAll('header button, header [role="button"]')).map(b=>b.innerText.trim()).filter(Boolean).slice(0,10);
        return out;
      }
    """)
    print("\n=== HEADER ===")
    print(data["header"])
    print("\n=== BIO ===")
    print(data["bio"])
    print("\n=== LINKS EXTERNOS ===")
    for l in data["links"]: print(" ", l)
    print(f"\n=== POSTS ({len(data['posts'])}) ===")
    for p_ in data["posts"]:
        print(f"  {p_['time'] or '(sin fecha)'} | {p_['label'][:90]} | {p_['href'][:60]}")
    print(f"\n=== HIGHLIGHTS ({len(data['highlights'])}) ===")
    for h in data["highlights"]: print(" ", h)
    print("\n=== BOTONES ===")
    print(data["buttons"])
