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

    if 'direct/inbox' not in page.url:
        page.goto('https://www.instagram.com/direct/inbox/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(5)

    # Click en "Tu nota" (el avatar con el +)
    page.mouse.click(64, 275)
    time.sleep(3)

    # Ver que se abrio (dialog con textarea/input para la nota)
    dlg = page.evaluate("""() => {
        const d = document.querySelector('[role=dialog],[role=alertdialog]');
        return d ? d.innerText.slice(0,400) : 'SIN DIALOG';
    }""")
    print('=== DIALOG ===')
    print(repr(dlg))
    print()
    # inputs
    inputs = page.evaluate("""() => Array.from(document.querySelectorAll('input[type=text],textarea,[contenteditable=true]')).map(e=>({tag:e.tagName, ph:e.placeholder||'', al:e.getAttribute('aria-label')||'', vis:e.offsetParent!==null}))""")
    print('=== INPUTS ===')
    for i in inputs:
        print('  ', i)
