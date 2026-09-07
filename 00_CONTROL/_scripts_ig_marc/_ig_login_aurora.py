import re, time
from playwright.sync_api import sync_playwright

CHAT = r"C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA IA\MARC Y AURORA\Chat de WhatsApp con +34 722 39 89 89\Chat de WhatsApp con +34 722 39 89 89.txt"
with open(CHAT, encoding="utf-8") as f:
    txt = f.read()
user = re.search(r"Usuario-\s*(\S+)", txt).group(1)
pw = re.search(r"Contraseña\+\s*(\S+)", txt).group(1)
print(f"Usuario Aurora: {user}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=30000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if "instagram.com" in pg.url or "about:blank" in pg.url:
            page = pg; break
    if page is None:
        page = ctx.new_page()

    page.goto("https://www.instagram.com/accounts/login/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(4)
    if "/accounts/login" in page.url:
        page.fill('input[name="email"]', user, timeout=15000)
        page.fill('input[name="pass"]', pw, timeout=15000)
        time.sleep(1)
        page.press('input[name="pass"]', "Enter")
        print("Credenciales de Aurora enviadas")
    time.sleep(6)
    print("URL tras enviar:", page.url[:70])
    page.bring_to_front()
    print(">>> SEBASTIÁN: si aparece captcha, pásalo con un clic. Yo retomo cuando estés dentro.")
