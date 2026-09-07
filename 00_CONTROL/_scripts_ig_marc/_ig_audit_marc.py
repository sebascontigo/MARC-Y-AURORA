import time, json, re
from playwright.sync_api import sync_playwright

HANDLE = "centro_de_bienestar_inanis"
OUT = r"C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA IA\MARC Y AURORA\MARC\04_Instagram\AUDITORIA INTERNA_MARC.md"

def safe(fn, *a, **k):
    try:
        return fn(*a, **k)
    except Exception as e:
        return None

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=30000)
    ctx = browser.contexts[0]
    page = None
    for pg in ctx.pages:
        if "instagram.com" in pg.url:
            page = pg; break
    if page is None:
        print("ERROR: no hay pestaña de Instagram. Abre Instagram en Brave primero."); raise SystemExit

    # Confirmar sesión iniciada
    page.goto(f"https://www.instagram.com/{HANDLE}/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)
    cur = page.url
    print("URL actual:", cur[:80])
    if "/accounts/login" in cur:
        print("ERROR: sigue pidiendo login. La sesión no está autenticada todavía."); raise SystemExit

    data = {}
    # Meta tags
    og_desc = safe(page.eval_on_selector, 'meta[property="og:description"]', "el => el.content")
    og_title = safe(page.eval_on_selector, 'meta[property="og:title"]', "el => el.content")
    data["og_title"] = og_title
    data["og_description"] = og_desc

    # Contadores del header (posts / seguidores / seguidos)
    header_txt = safe(page.eval_on_selector, "header", "el => el.innerText")
    data["header_text"] = header_txt

    # Bio
    bio = safe(page.evaluate, "() => { const el = document.querySelector('header section div') || document.querySelector('div.-vDIg'); return el ? el.innerText : null; }")
    data["bio"] = bio

    # Botón de mensaje / estado
    data["body_head"] = safe(page.evaluate, "() => document.body.innerText.slice(0, 600)")

    # Scroll para cargar posts del grid y leer timestamps
    stamps = []
    for i in range(4):
        safe(page.evaluate, "() => window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2.5)
    # Links de posts
    links = safe(page.evaluate, """
      () => Array.from(document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]'))
        .map(a => ({href: a.href, time: (a.querySelector('time')||{}).dateTime || a.getAttribute('aria-label') || ''}))
        .slice(0, 40)
    """)
    data["recent_posts"] = links

    # Highlights
    highlights = safe(page.evaluate, """
      () => Array.from(document.querySelectorAll('[role="presentation"] a[href*="/stories/highlights/"]'))
        .map(a => a.getAttribute('aria-label') || a.innerText).filter(Boolean).slice(0, 20)
    """)
    data["highlights"] = highlights

    # Escribir informe
    lines = []
    lines.append("# AUDITORÍA INTERNA INSTAGRAM — MARC (@centro_de_bienestar_inanis)")
    lines.append("")
    lines.append(f"[CONFIRMADO] Fecha de extracción: {time.strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("## Datos del perfil (vista autenticada)")
    lines.append(f"- og:title: {data.get('og_title')}")
    lines.append(f"- og:description: {data.get('og_description')}")
    lines.append("")
    lines.append("## Header (contadores)")
    lines.append("```")
    lines.append(str(data.get("header_text"))[:800])
    lines.append("```")
    lines.append("")
    lines.append("## Bio")
    lines.append("```")
    lines.append(str(data.get("bio"))[:600])
    lines.append("```")
    lines.append("")
    lines.append(f"## Posts recientes detectados ({len(links or [])})")
    for l in (links or []):
        lines.append(f"- {l.get('time','(sin fecha)')}  {l.get('href','')[:70]}")
    lines.append("")
    lines.append(f"## Highlights ({len(highlights or [])})")
    for h in (highlights or []):
        lines.append(f"- {h}")
    lines.append("")
    lines.append("## Notas")
    lines.append("- [PENDIENTE] Insights / panel profesional: requiere navegar al dashboard; se extrae en segunda pasada si está disponible.")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("OK: informe escrito en", OUT)
    print("Posts detectados:", len(links or []))
    print("Header:", str(data.get('header_text'))[:200])
