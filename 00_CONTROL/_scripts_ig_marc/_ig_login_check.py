import time
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp("http://localhost:9222")
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if 'instagram.com' in pg.url:
            page = pg
            break
    if page is None:
        page = ctx.pages[0]
    print("URL:", page.url)
    # texto visible principal
    body_text = page.eval_on_selector("body", "el => el.innerText")
    print("BODY TEXT (primeros 1200 chars):")
    print(body_text[:1200])
    print("---")
    # labels y headings
    heads = page.eval_on_selector_all("h1,h2,h3,label", "els => els.map(e => e.innerText.trim()).filter(Boolean)")
    print("HEADINGS/LABELS:", heads[:10])
    # links relevantes
    links = page.eval_on_selector_all("a", "els => els.map(e => ({t: e.innerText.trim(), h: e.href})).filter(x => x.t)")
    print("LINKS:", links[:10])
