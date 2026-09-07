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

    page.goto('https://www.instagram.com/accounts/settings/v2/hidden_words/', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    # Inspeccionar la estructura del elemento y sus ancestros clicables
    info = page.evaluate("""() => {
        const spans = Array.from(document.querySelectorAll('span,div')).filter(e => (e.innerText||'').trim() === 'Administrar palabras y frases personalizadas');
        if (!spans.length) return {err: 'none'};
        const t = spans[spans.length-1];
        // subir 5 niveles y reportar cada uno
        const chain = [];
        let node = t;
        for (let i = 0; i < 6 && node; i++) {
            const r = node.getBoundingClientRect();
            chain.push({
                lvl: i, tag: node.tagName,
                role: node.getAttribute('role'),
                tabindex: node.getAttribute('tabindex'),
                cls: (node.className||'').toString().slice(0,40),
                w: Math.round(r.width), h: Math.round(r.height),
                clickable: node.onclick !== null || node.getAttribute('role') === 'button' || node.tagName === 'A' || node.tagName === 'BUTTON'
            });
            node = node.parentElement;
        }
        return {chain};
    }""")
    print('=== CADENA DE ANCESTROS ===')
    for c in info.get('chain', []):
        print(' ', c)

    # Buscar el primer ancestro con role=button o tabindex y clicarlo
    clicked = page.evaluate("""() => {
        const spans = Array.from(document.querySelectorAll('span,div')).filter(e => (e.innerText||'').trim() === 'Administrar palabras y frases personalizadas');
        if (!spans.length) return 'no text';
        let node = spans[spans.length-1];
        while (node && node !== document.body) {
            if (node.getAttribute('role') === 'button' || node.tagName === 'BUTTON' || node.tagName === 'A' || node.getAttribute('tabindex') === '0') {
                node.scrollIntoView({block:'center'});
                node.click();
                return 'clicked ' + node.tagName + ' role=' + node.getAttribute('role');
            }
            node = node.parentElement;
        }
        return 'no clickable ancestor';
    }""")
    print('Resultado click:', clicked)
    time.sleep(3)
    print('URL:', page.url)
    ta = page.evaluate('() => document.querySelectorAll("textarea").length')
    print('Textareas:', ta)
    if ta > 0:
        body = page.evaluate('() => document.body.innerText.slice(0, 400)')
        print(repr(body[:350]))
