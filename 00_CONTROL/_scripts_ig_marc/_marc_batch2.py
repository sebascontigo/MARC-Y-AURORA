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

    # === 1) BANDEJA DE DMs ===
    page.goto('https://www.instagram.com/direct/inbox/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)
    print('=== DM INBOX ===')
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 600)')
    print(repr(body[:500]))

    # === 2) CODIGO QR ===
    page.goto('https://www.instagram.com/qr/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== CODIGO QR ===')
    print('URL:', page.url)
    qr = page.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('img[src*="qr"], canvas, img'));
        const out = [];
        imgs.forEach(i => {
            const src = i.src || i.toDataURL && 'canvas';
            if (src) out.push({tag: i.tagName, src: (src||'').slice(0,80), alt: i.alt||''});
        });
        return out.slice(0,5);
    }""")
    print('Elementos QR:', qr)
    body = page.evaluate('() => document.body.innerText.slice(0, 300)')
    print(repr(body[:250]))

    # === 3) ESTADO DE LA CUENTA (elegibilidad para recomendacion/ads) ===
    page.goto('https://www.instagram.com/settings/help/account_status/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== ESTADO DE LA CUENTA ===')
    print('URL:', page.url)
    body = page.evaluate('() => document.body.innerText.slice(0, 800)')
    print(repr(body[:700]))

    # === 4) COMPARTIR Y REUTILIZAR ===
    page.goto('https://www.instagram.com/accounts/settings/v2/sharing_and_reuse/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)
    print('\n=== COMPARTIR Y REUTILIZAR ===')
    print('URL:', page.url)
    checks = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=checkbox],input[type=radio]')).map(e=>({type:e.type, al:e.getAttribute('aria-label')||'', checked:e.checked}))""")
    for c in checks:
        print('  ', c)
    body = page.evaluate('() => document.body.innerText')
    idx = body.find('Compartir y reutilizar', 200)
    print(repr(body[idx:idx+400]) if idx >= 0 else repr(body[300:700]))
