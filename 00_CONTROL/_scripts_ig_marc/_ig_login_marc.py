import re, time
from playwright.sync_api import sync_playwright

CHAT = r"C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA IA\MARC Y AURORA\MARC\Chat de WhatsApp con MARC (ÚLTIMO EL MÁS RECIENTE)\Chat de WhatsApp con Marc Souza Gil\Chat de WhatsApp con Marc Souza Gil.txt"
with open(CHAT, encoding="utf-8") as f:
    txt = f.read()
user = re.search(r"Usuario:\s*(\S+)", txt).group(1)
pw_ig = re.search(r'contraseña instagram\s*"([^"]+)"', txt, re.IGNORECASE).group(1)
print(f"Usuario: {user}")

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
        page.fill('input[name="pass"]', pw_ig, timeout=15000)
        time.sleep(1)
        page.press('input[name="pass"]', "Enter")
        print("Credenciales enviadas")
    time.sleep(8)
    print("URL tras enviar:", page.url[:70])

    # Buscar el frame anchor del reCAPTCHA y clicar la casilla
    clicked = False
    for fr in page.frames:
        if "anchor" in fr.url:
            try:
                cb = fr.wait_for_selector("#recaptcha-anchor", timeout=12000)
                print("Casilla encontrada. aria-checked =", cb.get_attribute("aria-checked"), "| visible =", cb.is_visible())
                cb.click(timeout=8000, force=True)
                clicked = True
                print(">>> Casilla clicada")
                break
            except Exception as e:
                print("No se pudo clicar la casilla:", str(e)[:120])
    if not clicked:
        print("No se encontró frame anchor. Frames actuales:")
        for fr in page.frames:
            if fr.url: print("   -", fr.url[:90])

    # Observar evolución 40s
    for i in range(8):
        time.sleep(5)
        try:
            u = page.url
            body = page.eval_on_selector("body", "el => el.innerText")
        except Exception:
            u, body = "?", ""
        print(f"[{(i+1)*5}s] URL={u[:70]} | body={len(body)} | head={repr(body[:90])}")
        if u and "recaptcha" not in u and "/accounts/login" not in u and u != "?":
            print(">>> ¡LOGIN COMPLETADO!")
            break

    # ¿Reto visual (bframe)?
    for fr in page.frames:
        if "bframe" in fr.url:
            print(">>> HAY RETO VISUAL (bframe) — requiere selección de imágenes.")
            try:
                t = fr.eval_on_selector("body", "el => el.innerText")
                print("    texto bframe:", repr(t[:150]))
            except Exception:
                pass
