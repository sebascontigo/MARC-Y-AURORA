#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ACCESIBILIDAD Y CALIDAD WEB (calculo real, sin captura de pantalla).
- Contraste WCAG de los pares de color declarados en el CSS de cada landing.
- Comprobaciones estructurales: idioma, un solo H1, alt en imagenes, target de enlaces,
  viewport, prefers-reduced-motion, tamano de fuente base.
Salida: 00_CONTROL/AUDITORIA_100_2026-09-05/ACCESIBILIDAD.txt
"""

import os, re, sys, io, atexit

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(WS, "00_CONTROL", "AUDITORIA_100_2026-09-05")
os.makedirs(OUT_DIR, exist_ok=True)
_buf = io.StringIO()
_real = sys.stdout


class _Tee:
    def write(self, s):
        _real.write(s)
        _buf.write(s)

    def flush(self):
        _real.flush()


sys.stdout = _Tee()
atexit.register(
    lambda: open(
        os.path.join(OUT_DIR, "ACCESIBILIDAD.txt"), "w", encoding="utf-8"
    ).write(_buf.getvalue())
)


def hex2rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (f(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(c1, c2):
    l1, l2 = lum(hex2rgb(c1)), lum(hex2rgb(c2))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def vars_css(html):
    out = {}
    for m in re.finditer(r"--([a-z0-9\-]+)\s*:\s*(#[0-9a-fA-F]{3,6})", html):
        out[m.group(1)] = m.group(2)
    return out


PAGINAS = [
    (
        "LANDING DESPIERTA (Marc)",
        "MARC/WEB_DESPIERTA/index.html",
        [
            ("ink", "bg", "texto normal sobre fondo"),
            ("ink-dim", "bg", "texto secundario sobre fondo"),
            ("accent", "bg", "acento sobre fondo"),
            ("ink-dim", "bg2", "texto secundario en tarjeta"),
            ("accent", "bg2", "acento en tarjeta"),
        ],
    ),
    (
        "LANDING SOBERANIA VITAL (Aurora)",
        "AURORA/WEB_SOBERANIA_VITAL/index.html",
        [
            ("ink", "bg", "texto normal sobre fondo"),
            ("ink-dim", "bg", "texto secundario sobre fondo"),
            ("accent", "bg", "acento sobre fondo"),
            ("ink-dim", "bg2", "texto secundario en tarjeta"),
            ("accent", "bg2", "acento en tarjeta"),
        ],
    ),
    ("APP DESPIERTA", "MARC/APP_DESPIERTA/index.html", None),
]

for titulo, rel, pares in PAGINAS:
    p = os.path.join(WS, rel.replace("/", os.sep))
    print(f"=== {titulo} — {rel} ===")
    if not os.path.exists(p):
        print("  NO EXISTE\n")
        continue
    html = open(p, encoding="utf-8", errors="ignore").read()
    v = vars_css(html)
    print(f"  variables de color detectadas: {len(v)} -> {', '.join(sorted(v))}")

    objetivo = pares
    if objetivo is None:
        claves = [k for k in v if k in ("ink", "ink-dim", "muted", "text", "accent")]
        fondos = [k for k in v if k in ("bg", "bg2", "card", "panel", "surface")]
        objetivo = [(a, b, f"{a} sobre {b}") for a in claves for b in fondos]

    print("  -- CONTRASTE WCAG (AA normal>=4.5, AA grande>=3.0)")
    for fg, bg, desc in objetivo:
        if fg in v and bg in v:
            r = ratio(v[fg], v[bg])
            veredicto = (
                "AA-normal"
                if r >= 4.5
                else ("AA-grande" if r >= 3.0 else "INSUFICIENTE")
            )
            print(f"     {r:5.2f}:1  {veredicto:12s} {desc}  ({fg} vs {bg})")
        else:
            print(f"     n/d  {desc} (falta {fg if fg not in v else bg})")

    print("  -- ESTRUCTURA")
    checks = [
        (
            "idioma declarado (lang)",
            bool(re.search(r'<html[^>]+lang="[a-z\-]+"', html)),
        ),
        ("un solo <h1>", html.count("<h1") == 1),
        ("viewport responsive", 'name="viewport"' in html),
        ("respeta reduced-motion", "prefers-reduced-motion" in html),
        (
            "imagenes con alt",
            all('alt="' in m for m in re.findall(r"<img[^>]*>", html))
            if re.findall(r"<img[^>]*>", html)
            else True,
        ),
        (
            "enlaces externos con rel=noopener",
            all(
                "rel=" in m
                for m in re.findall(r'<a[^>]+href="https?://[^"]+"[^>]*>', html)
            ),
        ),
        ("titulo <title> presente", "<title>" in html),
        ("descripcion meta presente", 'name="description"' in html),
        ("datos estructurados", "application/ld+json" in html),
        ("tema de color declarado", 'name="theme-color"' in html),
    ]
    for nombre, ok in checks:
        print(f"     {'OK ' if ok else 'REV'}  {nombre}")

    imgs = re.findall(r"<img[^>]*>", html)
    print(
        f"     imagenes: {len(imgs)}  h2: {html.count('<h2')}  details/FAQ: {html.count('<details')}"
    )
    m = re.search(r"body\{[^}]*font-size:\s*([0-9]+)px", html)
    if m:
        print(
            f"     fuente base: {m.group(1)}px  ({'OK' if int(m.group(1)) >= 16 else 'pequena'})"
        )
    print()

print("FIN")
