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

    page.goto('https://www.instagram.com/push/web/settings/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    # Mapear cada grupo de radios a su etiqueta de texto cercana
    mapping = page.evaluate("""() => {
        const out = [];
        // buscar contenedores de setting: cada uno tiene un titulo y radios
        const radios = Array.from(document.querySelectorAll('input[type=radio]'));
        radios.forEach((r, i) => {
            // subir al contenedor fila
            let row = r.closest('div, label, li');
            let txt = '';
            let node = r;
            // buscar el texto de la opcion (sibling o label)
            let parent = r.parentElement;
            for (let k = 0; k < 4 && parent; k++) {
                const t = (parent.innerText||'').trim();
                if (t && t.length < 60) { txt = t; break; }
                parent = parent.parentElement;
            }
            out.push({i, checked: r.checked, optText: txt.replace(/\\n/g,' | ').slice(0,55)});
        });
        return out;
    }""")
    print('=== MAPPING RADIOS PUSH (solo los checked y su contexto) ===')
    # agrupar: mostrar solo checked=True con su texto
    for m in mapping:
        if m['checked']:
            print(f"  [{m['i']}] CHECKED -> {m['optText']}")
    print()
    print('=== TODOS con texto (primeros 40) ===')
    for m in mapping[:40]:
        print(f"  [{m['i']}] {'ON ' if m['checked'] else 'off'} {m['optText']}")
