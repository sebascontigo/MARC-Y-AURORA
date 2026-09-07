import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=60000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if "instagram.com" in pg.url:
            page = pg; break
    if page is None:
        page = ctx.new_page()

    # === EDIT PROFILE: leer todos los campos ===
    page.goto("https://www.instagram.com/accounts/edit/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)
    fields = page.evaluate("""
      () => {
        const out = {inputs: [], textareas: []};
        document.querySelectorAll('input').forEach(i => {
          out.inputs.push({name: i.name||i.getAttribute('aria-label')||'', type: i.type, value: (i.value||'').slice(0,200), placeholder: i.placeholder||''});
        });
        document.querySelectorAll('textarea').forEach(t => {
          out.textareas.push({name: t.name||t.getAttribute('aria-label')||'', value: (t.value||'').slice(0,300)});
        });
        return out;
      }
    """)
    print("=== INPUTS en /accounts/edit/ ===")
    for f in fields["inputs"]:
        if f["value"] or f["name"]:
            print(f"  [{f['name']}] type={f['type']} value={repr(f['value'])}")
    print("=== TEXTAREAS ===")
    for t in fields["textareas"]:
        print(f"  [{t['name']}] value={repr(t['value'])}")

    # === POSTS: abrir cada uno y leer caption/fecha ===
    posts = ["DZsII8dCupd", "DZsHrfPihsS", "DZsG6BHit2z", "DZkutW4Ck7i"]
    for code in posts:
        page.goto(f"https://www.instagram.com/marcsouza.7/p/{code}/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(4)
        info = page.evaluate("""
          () => {
            const out = {};
            const t = document.querySelector('time');
            out.fecha = t ? t.getAttribute('datetime') : '';
            // caption: suele estar en un div con role presentation o en h1/h2
            const spans = Array.from(document.querySelectorAll('h1, h2, h3, span')).map(s=>s.innerText).filter(Boolean);
            out.caption = '';
            // buscar el bloque de caption (junto al nombre de usuario)
            const capEl = document.querySelector('div._aade') || document.querySelector('ul li div span') ;
            if (capEl) out.caption = capEl.innerText.slice(0,500);
            // video o imagen?
            out.has_video = !!document.querySelector('video');
            out.img_alts = Array.from(document.querySelectorAll('img[alt]')).map(i=>i.alt).filter(a=>a.length>20).slice(0,2);
            // likes / comentarios
            const sect = document.querySelector('section');
            out.section_text = sect ? sect.innerText.slice(0,200) : '';
            return out;
          }
        """)
        print(f"\n=== POST {code} ===")
        print("  fecha:", info["fecha"])
        print("  video:", info["has_video"])
        print("  caption:", repr(info["caption"][:300]))
        print("  img_alts:", info["img_alts"])
        print("  section:", repr(info["section_text"][:150]))
