from playwright.sync_api import sync_playwright
import time

EMAIL_MARC = "info@marcsouza.com"
TEL_MARC = "642666972"  # numero real de Marc (del Centro de Cuentas), sin prefijo ES

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

    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)

    # 1) Email
    page.fill('input[type="email"]', EMAIL_MARC, timeout=8000)
    time.sleep(0.5)
    # 2) Telefono
    try:
        page.fill('input[placeholder="Número de teléfono"]', TEL_MARC, timeout=8000)
        print('Telefono rellenado')
    except Exception as e:
        print('Telefono fallo:', str(e)[:60])
    time.sleep(0.5)
    # 3) Metodo TEXT
    page.evaluate('() => { const r=document.querySelector(\'input[aria-label="TEXT"]\'); if(r) r.click(); }')
    time.sleep(0.5)
    # 4) Mostrar contacto ON
    page.evaluate('() => { const c=document.querySelector(\'input[aria-label="Mostrar información de contacto"]\'); if(c && !c.checked) c.click(); }')
    time.sleep(0.5)

    estado = page.evaluate("""() => ({
        email: document.querySelector('input[type="email"]').value,
        tel: document.querySelector('input[placeholder="Número de teléfono"]').value,
        text_checked: document.querySelector('input[aria-label="TEXT"]').checked,
        mostrar: document.querySelector('input[aria-label="Mostrar información de contacto"]').checked
    })""")
    print('=== ANTES DE ENVIAR ===', estado)

    # 5) Click Enviar (usar el button real)
    clicked = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const m = btns.find(b => (b.innerText||'').trim() === 'Enviar');
        if (m) { m.click(); return 'button clicked'; }
        const divs = Array.from(document.querySelectorAll('[role=button],div,span'));
        const d = divs.find(e => (e.innerText||'').trim() === 'Enviar');
        if (d) { d.click(); return 'div clicked'; }
        return 'not found';
    }""")
    print('Enviar:', clicked)
    time.sleep(5)

    # Capturar dialog/error/toast
    dlg = page.evaluate("""() => {
        const d = document.querySelector('[role=dialog],[role=alertdialog],[role=alert]');
        return d ? d.innerText.slice(0,400) : 'SIN DIALOG';
    }""")
    print('=== DIALOG/ERROR TRAS ENVIAR ===')
    print(repr(dlg))
    print('URL:', page.url)
