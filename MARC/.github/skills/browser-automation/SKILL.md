---
name: browser-automation
description: "Automatizar un navegador real (Chromium) con Playwright desde Python: navegar, click, formularios, screenshots y descarga de archivos. Usar cuando haga falta interacción web programática."
---

# Skill: Browser Automation (Playwright Python)

Stack verificado: `playwright 1.62.0` + Chromium instalado (smoke test superado).

## Patrón básico (síncrono)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com", wait_until="domcontentloaded")
    print(page.title())
    page.screenshot(path="captura.png", full_page=True)
    browser.close()
```

## Interacciones

```python
page.fill("#q", "texto")          # rellenar input
page.click("button[type=submit]") # click
page.wait_for_selector(".result") # esperar
links = page.eval_on_selector_all("a", "els => els.map(e => e.href)")
```

## Descargas

```python
with page.expect_download() as dl:
    page.click("a.descarga")
dl.value.save_as(r"out/archivo.zip")
```

## Cuándo usar qué

- **Este skill (Python)**: scripts robustos reutilizables, batch, pipelines.
- **MCP `playwright/*`**: interacción conversacional puntual desde el chat (agente 07).

## Reglas

- Siempre `headless=True` salvo que el usuario pida lo contrario.
- Verificar estado tras navegar (título/contenido) antes de afirmar éxito.
- No introducir credenciales reales ni eludir CAPTCHAs.
