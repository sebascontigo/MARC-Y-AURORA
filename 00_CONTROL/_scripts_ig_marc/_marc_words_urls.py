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

    # Probar URLs directas del gestor de palabras personalizadas
    urls = [
        'https://www.instagram.com/accounts/settings/v2/hidden_words/custom_words/',
        'https://www.instagram.com/accounts/hidden_words/custom/',
        'https://www.instagram.com/accounts/settings/hidden_words/',
    ]
    for url in urls:
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=20000)
            time.sleep(3)
            body = page.evaluate('() => document.body.innerText.slice(0, 300)')
            has_ta = page.evaluate('() => document.querySelectorAll("textarea").length')
            print(f'[{url.split("instagram.com")[1]}]')
            print('  textareas:', has_ta, '| body:', repr(body[:120]))
            if has_ta > 0:
                print('  >>> TIENE TEXTAREA - URL correcta')
        except Exception as e:
            print(f'[{url}] error:', str(e)[:60])
        print()
