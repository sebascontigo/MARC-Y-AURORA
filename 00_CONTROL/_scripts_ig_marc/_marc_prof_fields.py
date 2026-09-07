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

    if 'professional_account_settings' not in page.url:
        page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
    time.sleep(2)

    # Mapear inputs, checkboxes, botones
    fields = page.evaluate("""() => Array.from(document.querySelectorAll('input,textarea,select')).map(e=>({
        tag: e.tagName, type: e.type||'', ph: e.placeholder||'', al: e.getAttribute('aria-label')||'',
        val: (e.value||'').slice(0,50), dis: e.disabled, checked: e.checked, vis: e.offsetParent !== null
    }))""")
    print('=== CAMPOS ===')
    for f in fields:
        print(f)
    print()
    btns = page.evaluate("""() => Array.from(document.querySelectorAll('button,[role=button]')).map(b=>({
        txt: (b.innerText||'').trim().slice(0,40), dis: b.disabled, vis: b.offsetParent !== null
    })).filter(x=>x.txt)""")
    print('=== BOTONES ===')
    for b in btns:
        print(b)
