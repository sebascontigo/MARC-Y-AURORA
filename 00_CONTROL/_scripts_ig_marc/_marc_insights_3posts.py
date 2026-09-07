from playwright.sync_api import sync_playwright
import time

POSTS = {
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
            # Click Ver insights
            try:
                page.locator('text=Ver insights').first.click(timeout=5000)
            except Exception:
                page.evaluate("""() => {
                    const els = Array.from(document.querySelectorAll('a,button,[role=button],div,span'));
                    const m = els.find(e => (e.innerText||'').trim() === 'Ver insights');
                    if (m) m.click();
                }""")
            time.sleep(4)
            body = page.evaluate('() => document.body.innerText')
            # extraer metricas clave
            vistas = None
            for kw in ['Visualizaciones\n', 'Cuentas alcanzadas']:
                idx = body.find(kw)
                if idx >= 0:
                    # tomar el numero tras el keyword
                    seg = body[idx:idx+60]
                    import re
                    m = re.search(r'(\d+)', seg.split('\n')[1] if '\n' in seg else seg)
                    if m:
                        vistas = m.group(1)
                    break
            likes = None
            m = __import__('re').search(r'Me gusta\n(\d+)', body)
            if m: likes = m.group(1)
            guardados = None
            m = __import__('re').search(r'guardado\n(\d+)', body)
            if m: guardados = m.group(1)
            compartidos = None
            m = __import__('re').search(r'compartido\n(\d+)', body)
            if m: compartidos = m.group(1)
            print(f'[{code}] {desc}')
            print(f'   vistas={vistas} likes={likes} guardados={guardados} compartidos={compartidos}')
        except Exception as e:
            print(f'[{code}] error:', str(e)[:70])
        print()
