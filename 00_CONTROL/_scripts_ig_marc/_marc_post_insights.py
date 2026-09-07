from playwright.sync_api import sync_playwright
import time

POSTS = {
    'DZkutW4Ck7i': 'Krishnamurti (autoridad)',
    'DZsG6BHit2z': 'Miedos (dolor)',
    'DZsHrfPihsS': 'Te atreves (CTA)',
    'DZsII8dCupd': 'Oliva (personal)',
}

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222', timeout=90000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if 'instagram.com' in pg.url:
            page = pg
            break
    if page is None:
        page = ctx.new_page()
    page.bring_to_front()

    for code, desc in POSTS.items():
        try:
            page.goto(f'https://www.instagram.com/marcsouza.7/p/{code}/', wait_until='domcontentloaded', timeout=30000)
            time.sleep(4)
            # buscar "Ver insights" en el post
            insights_btn = page.evaluate("""() => {
                const els = Array.from(document.querySelectorAll('a,button,[role=button],div,span'));
                const m = els.find(e => /Ver insights|insights/i.test(e.innerText||'') && (e.innerText||'').length < 30);
                return m ? (m.innerText||'').trim() : null;
            }""")
            # leer metricas visibles del post (likes, comentarios, fecha)
            body = page.evaluate('() => document.body.innerText')
            # extraer likes
            likes = page.evaluate("""() => {
                const m = document.body.innerText.match(/(\\d+)\\s*Me gusta/);
                return m ? m[1] : null;
            }""")
            print(f'[{code}] {desc}')
            print(f'   likes: {likes} | insights_btn: {insights_btn}')
        except Exception as e:
            print(f'[{code}] error:', str(e)[:60])
        print()
