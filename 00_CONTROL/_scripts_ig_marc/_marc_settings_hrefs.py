from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222', timeout=90000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if 'instagram.com' in pg.url and 'facebook' not in pg.url:
            page = pg
            break
    if page is None:
        page = ctx.new_page()
    page.bring_to_front()

    page.goto('https://www.instagram.com/accounts/settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    # Todos los hrefs de la pagina de settings
    hrefs = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('a[href]').forEach(a => {
            const h = a.getAttribute('href') || '';
            const t = (a.innerText || '').trim();
            if (h && !h.startsWith('http') || h.includes('instagram.com')) {
                out.push({href: h.slice(0,70), txt: t.slice(0,40)});
            }
        });
        return out;
    }""")
    print('=== HREFS EN SETTINGS ===')
    for h in hrefs:
        print(h)
