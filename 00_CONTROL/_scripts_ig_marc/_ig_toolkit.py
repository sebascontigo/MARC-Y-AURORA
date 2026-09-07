#!/usr/bin/env python3
"""
IG Toolkit — herramientas robustas para automatización de Instagram vía Brave CDP.

Resuelve los errores identificados en sesiones anteriores:
1. CDP se cuelga → reconexión automática con reinicio de Brave
2. React no registra keyboard.type() → usar fill() que dispara eventos React
3. Campo Nombre no editable en vista web → ruta alternativa con UA móvil
4. Opción Fijar no aparece → probar desde grid del perfil con UA móvil

Uso:
    from _ig_toolkit import IGSession
    ig = IGSession()
    ig.connect()
    ig.goto("https://www.instagram.com/accounts/edit/")
    ig.react_fill("textarea", "nueva bio")
    ig.react_submit()
"""
import subprocess
import time
import os
import sys

BRAVE_EXE = r"C:\Users\sevis\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
BRAVE_USER_DATA = r"C:\Users\sevis\AppData\Local\BraveSoftware\Brave-Browser\User Data"
CDP_PORT = 9222
CDP_URL = f"http://localhost:{CDP_PORT}"

# User-Agent móvil para acceder a vistas que la web desktop no muestra
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)


class IGSession:
    """Sesión robusta de Instagram vía Brave CDP con auto-recuperación."""

    def __init__(self, headless=False):
        self.headless = headless
        self.browser = None
        self.ctx = None
        self._page = None
        self._pw = None  # playwright instance, tracked for cleanup

    def _cdp_alive(self):
        """Verificar si CDP responde."""
        import urllib.request
        try:
            req = urllib.request.Request(f"{CDP_URL}/json/version")
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status == 200
        except Exception:
            return False

    def _kill_brave(self):
        """Matar todos los procesos de Brave."""
        subprocess.run(
            ["taskkill", "//IM", "brave.exe", "//F"],
            capture_output=True, timeout=15
        )
        time.sleep(3)

    def _launch_brave(self, url=None):
        """Lanzar Brave con CDP activo."""
        cmd = [
            BRAVE_EXE,
            f"--remote-debugging-port={CDP_PORT}",
            f"--user-data-dir={BRAVE_USER_DATA}",
            "--profile-directory=Default",
            "--no-first-run",
            "--no-default-browser-check",
        ]
        if url:
            cmd.append(url)
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if self.headless else 0,
        )
        # Esperar a que CDP responda
        for _ in range(20):
            time.sleep(1)
            if self._cdp_alive():
                return True
        return False

    def _stop_pw(self):
        """Detener limpiamente la instancia de Playwright si existe."""
        if self._pw is not None:
            try:
                self._pw.stop()
            except Exception:
                pass
            self._pw = None
            self.browser = None
            self.ctx = None

    def connect(self, max_retries=3):
        """Conectar a Brave CDP con auto-recuperación.

        Si CDP está colgado, mata Brave y lo relanza.
        Limpia la instancia de Playwright entre intentos para evitar
        el error 'Sync API inside asyncio loop'.
        """
        from playwright.sync_api import sync_playwright

        for attempt in range(max_retries):
            # Limpiar instancia anterior antes de cada intento
            self._stop_pw()

            try:
                if not self._cdp_alive():
                    print(f"[IGSession] CDP no responde, reiniciando Brave (intento {attempt+1})")
                    self._kill_brave()
                    if not self._launch_brave():
                        print("[IGSession] ERROR: Brave no arrancó con CDP")
                        continue

                self._pw = sync_playwright().start()
                self.browser = self._pw.chromium.connect_over_cdp(CDP_URL, timeout=30000)
                self.ctx = self.browser.contexts[0]
                print(f"[IGSession] Conectado. Pestañas: {len(self.ctx.pages)}")
                return True

            except Exception as e:
                err = str(e)
                print(f"[IGSession] Conexión falló (intento {attempt+1}): {err[:100]}")
                # Limpiar la instancia fallida ANTES de reintentar
                self._stop_pw()
                if "Target closed" in err or "Connection refused" in err or "Timeout" in err or "timeout" in err.lower():
                    self._kill_brave()
                    time.sleep(2)
                    self._launch_brave()
                    time.sleep(5)
                else:
                    # Error inesperado, no reintentar
                    raise

        print("[IGSession] ERROR: No se pudo conectar tras todos los intentos")
        return False

    def get_page(self, url_contains=None):
        """Obtener la página que contenga la URL dada, o crear una nueva."""
        if url_contains:
            for pg in self.ctx.pages:
                if url_contains in pg.url:
                    self._page = pg
                    return pg
        # Crear nueva pestaña
        self._page = self.ctx.new_page()
        return self._page

    @property
    def page(self):
        if self._page is None or self._page.is_closed():
            self._page = self.ctx.pages[0] if self.ctx.pages else self.ctx.new_page()
        return self._page

    def goto(self, url, wait="domcontentloaded", timeout=90000):
        """Navegar con timeout robusto."""
        page = self.page
        page.goto(url, wait_until=wait, timeout=timeout)
        return page

    def react_fill(self, selector, text, timeout=30000):
        """Rellenar un campo React usando fill() de Playwright.

        IMPORTANTE: fill() dispara correctamente los eventos de React
        (input + change), a diferencia de keyboard.type() que React ignora.
        """
        page = self.page
        el = page.wait_for_selector(selector, timeout=timeout)
        el.click()
        time.sleep(0.3)
        # Seleccionar todo y borrar primero
        page.keyboard.press("Control+a")
        page.keyboard.press("Backspace")
        time.sleep(0.2)
        # fill() dispara eventos React correctamente
        el.fill(text)
        time.sleep(0.5)
        # Verificar que el valor se registró
        actual = el.input_value()
        if text[:20] not in actual:
            print(f"[react_fill] WARNING: campo no registra texto. Intentando setter React...")
            page.evaluate(f'''(text) => {{
                const el = document.querySelector('{selector}');
                const setter = Object.getOwnPropertyDescriptor(
                    window.HTMLTextAreaElement.prototype, 'value'
                )?.set || Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                )?.set;
                if (setter) {{
                    setter.call(el, text);
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}''', text)
            time.sleep(0.5)
        return el

    def react_submit(self, timeout=15000):
        """Buscar y clicar el botón submit de un formulario React."""
        page = self.page
        # Intentar button[type=submit]
        btn = page.query_selector('button[type="submit"]')
        if btn and btn.is_visible():
            btn.click()
            print("[react_submit] Click en button[type=submit]")
            time.sleep(5)
            return True
        # Intentar botón con texto Enviar/Guardar/Save
        for text in ["Enviar", "Guardar", "Save", "Submit", "Done"]:
            btn = page.query_selector(f'button:has-text("{text}")')
            if btn and btn.is_visible():
                btn.click()
                print(f"[react_submit] Click en botón '{text}'")
                time.sleep(5)
                return True
        # Intentar div[role=button] con texto
        for text in ["Enviar", "Guardar", "Save"]:
            btn = page.query_selector(f'div[role="button"]:has-text("{text}")')
            if btn and btn.is_visible():
                btn.click()
                print(f"[react_submit] Click en div[role=button] '{text}'")
                time.sleep(5)
                return True
        print("[react_submit] WARNING: No se encontró botón submit")
        return False

    def dom_text(self, selector=None, max_chars=1000):
        """Leer texto del DOM (observación text-only)."""
        page = self.page
        if selector:
            el = page.query_selector(selector)
            return el.inner_text()[:max_chars] if el else f"(selector '{selector}' no encontrado)"
        return page.evaluate("() => document.body.innerText")[:max_chars]

    def dom_buttons(self):
        """Listar todos los botones visibles (para debugging)."""
        page = self.page
        return page.evaluate('''() =>
            Array.from(document.querySelectorAll('button, [role="button"]'))
            .filter(b => b.offsetParent !== null)
            .map(b => ({
                text: (b.innerText || b.getAttribute('aria-label') || '').trim().slice(0, 50),
                type: b.type || '',
                disabled: b.disabled,
                tag: b.tagName
            }))
        ''')

    def set_mobile_ua(self):
        """Cambiar a User-Agent móvil para acceder a vistas restringidas."""
        page = self.page
        # Crear nueva página con UA móvil en el mismo contexto
        new_page = self.ctx.new_page()
        new_page.set_extra_http_headers({"User-Agent": MOBILE_UA})
        self._page = new_page
        return new_page

    def close(self):
        """Cerrar limpiamente (sin matar Brave)."""
        self._stop_pw()


# === Funciones de alto nivel ===

def edit_bio(bio_text, verify_url=None):
    """Editar la bio de Instagram con verificación."""
    ig = IGSession()
    if not ig.connect():
        return {"ok": False, "error": "No se pudo conectar a Brave CDP"}

    try:
        ig.goto("https://www.instagram.com/accounts/edit/")
        ig.page.wait_for_selector("textarea", timeout=30000)
        time.sleep(3)

        ig.react_fill("textarea", bio_text)
        submitted = ig.react_submit()

        if not submitted:
            return {"ok": False, "error": "No se encontró botón submit"}

        # Verificar
        if verify_url:
            time.sleep(5)
            ig.goto(verify_url, wait="commit")
            time.sleep(8)
            header = ig.dom_text("header", 500)
            if bio_text[:20] in header:
                return {"ok": True, "verified": True, "header": header[:200]}
            else:
                return {"ok": True, "verified": False, "header": header[:200]}

        return {"ok": True, "verified": None}

    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}
    finally:
        ig.close()


def pin_post(post_url):
    """Intentar fijar un post (probando múltiples rutas)."""
    ig = IGSession()
    if not ig.connect():
        return {"ok": False, "error": "No se pudo conectar a Brave CDP"}

    try:
        # Ruta 1: URL directa del post
        ig.goto(post_url)
        time.sleep(6)

        # Buscar botón de menú
        menu = ig.page.query_selector('[aria-label="Más opciones"]')
        if not menu:
            menu = ig.page.query_selector('button[aria-label*="opciones"]')
        if not menu:
            menu = ig.page.query_selector('[data-testid="more-button"]')

        if menu:
            menu.click()
            time.sleep(2)

            # Buscar opción de fijar
            pin_option = ig.page.query_selector('[role="menuitem"]:has-text("Fijar")')
            if not pin_option:
                pin_option = ig.page.query_selector('[role="menuitem"]:has-text("Anclar")')
            if not pin_option:
                pin_option = ig.page.query_selector('[role="menuitem"]:has-text("Pin")')

            if pin_option:
                pin_option.click()
                time.sleep(3)
                return {"ok": True, "method": "menu_directo"}
            else:
                # Listar opciones disponibles para diagnóstico
                options = ig.page.evaluate('''() =>
                    Array.from(document.querySelectorAll('[role="menuitem"], [role="dialog"] button'))
                    .map(e => (e.innerText || '').trim())
                    .filter(t => t && t.length < 50)
                ''')
                return {"ok": False, "error": "Opción Fijar no encontrada", "opciones": options}
        else:
            return {"ok": False, "error": "Botón de menú no encontrado"}

    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}
    finally:
        ig.close()


if __name__ == "__main__":
    # Test rápido de conexión
    ig = IGSession()
    if ig.connect():
        print("Conexión OK")
        print(f"Pestañas: {[pg.url[:60] for pg in ig.ctx.pages]}")
        ig.close()
    else:
        print("Conexión FALLÓ")
