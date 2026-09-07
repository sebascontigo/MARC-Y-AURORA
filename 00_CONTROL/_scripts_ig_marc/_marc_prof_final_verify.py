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

    # Estado completo en la pagina de config
    page.goto('https://www.instagram.com/accounts/professional_account_settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)
    estado = page.evaluate("""() => ({
        email: document.querySelector('input[type="email"]') ? document.querySelector('input[type="email"]').value : 'none',
        whatsapp: document.querySelector('input[placeholder="Número de WhatsApp Business"]') ? document.querySelector('input[placeholder="Número de WhatsApp Business"]').value : 'none',
        tel: document.querySelector('input[placeholder="Número de teléfono"]') ? document.querySelector('input[placeholder="Número de teléfono"]').value : 'none',
        text_checked: document.querySelector('input[aria-label="TEXT"]') ? document.querySelector('input[aria-label="TEXT"]').checked : 'none',
        call_checked: document.querySelector('input[aria-label="CALL"]') ? document.querySelector('input[aria-label="CALL"]').checked : 'none',
        mostrar: document.querySelector('input[aria-label="Mostrar información de contacto"]') ? document.querySelector('input[aria-label="Mostrar información de contacto"]').checked : 'none',
        mostrar_cat: document.querySelector('input[aria-label="Mostrar etiqueta de categoría"]') ? document.querySelector('input[aria-label="Mostrar etiqueta de categoría"]').checked : 'none'
    })""")
    print('=== ESTADO CONFIG PROFESIONAL ===')
    for k, v in estado.items():
        print(f'  {k}: {v}')

    # Verificar en el perfil publico si aparece el contacto
    page.goto('https://www.instagram.com/marcsouza.7/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(5)
    body = page.evaluate('() => document.body.innerText.slice(0, 900)')
    print()
    print('=== PERFIL (buscando contacto/categoria) ===')
    print(repr(body[:800]))
    print()
    print('Aparece email?', 'info@marcsouza.com' in body or 'Correo' in body or 'Email' in body)
    print('Aparece boton contacto?', any(k in body for k in ['Contacto', 'Enviar mensaje', 'Llamar', 'Texto', 'WhatsApp']))
