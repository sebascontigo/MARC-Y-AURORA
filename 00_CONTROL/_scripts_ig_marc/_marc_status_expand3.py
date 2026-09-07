from playwright.sync_api import sync_playwright
import time

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

    page.goto('https://www.instagram.com/settings/help/account_status/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    for kw in ['menores de 18', 'Funciones que no puedes usar']:
        clicked = page.evaluate("""(kw) => {
            const els = Array.from(document.querySelectorAll('div,span,button,[role=button]'));
            const cands = els.filter(e => {
                const t = (e.innerText||'').trim();
                return t.includes(kw) && t.length < 80;
            });
            if (!cands.length) return 'not found';
            // el mas interno
            let t = cands[cands.length-1];
            t.scrollIntoView({block:'center'});
            t.click();
            return 'clicked (' + cands.length + ' cands)';
        }""", kw)
        time.sleep(2.5)
        print(f'[{kw}] -> {clicked}')
        body = page.evaluate('() => document.body.innerText')
        idx = body.rfind(kw)
        if idx >= 0:
            print('   contenido:', repr(body[idx:idx+320]))
        print()
