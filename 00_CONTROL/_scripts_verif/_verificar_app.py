#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VERIFICADOR DE LA APP DESPIERTA (PWA) — contratos que no pueden romperse.
  P1. index.html, manifest y service worker presentes y coherentes
  P2. El service worker cachea SOLO archivos que existen
  P3. El manifest declara iconos que existen y arranque valido
  P4. Los audios referenciados existen
  P5. Sin credenciales en los archivos publicados
  P6. Accesibilidad minima: idioma, viewport, respeta reduced-motion
  P7. Aviso de privacidad: la app declara que los datos se quedan en el dispositivo
  P8. Produccion responde 200 en todas las rutas declaradas

Uso: python _verificar_app.py [local|prod|ambos]
"""

import os, re, sys, json, urllib.request

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(WS, "MARC", "APP_DESPIERTA")
PROD = "https://despierta-app.netlify.app"

fails = []


def check(cond, nombre):
    print(("  OK   " if cond else "  FALLA ") + nombre)
    if not cond:
        fails.append(nombre)


def local():
    print("== LOCAL ==")
    idx = os.path.join(APP, "index.html")
    man = os.path.join(APP, "manifest.webmanifest")
    sw = os.path.join(APP, "sw.js")
    check(os.path.exists(idx), "P1a index.html existe")
    check(os.path.exists(man), "P1b manifest existe")
    check(os.path.exists(sw), "P1c service worker existe")
    if not (os.path.exists(idx) and os.path.exists(man) and os.path.exists(sw)):
        return

    html = open(idx, encoding="utf-8").read()
    swtxt = open(sw, encoding="utf-8").read()
    mtxt = open(man, encoding="utf-8").read()

    # P2 — el sw solo cachea lo que existe
    activos = re.findall(r"'\./([^']+)'", swtxt)
    faltan = [
        a
        for a in activos
        if a and not os.path.exists(os.path.join(APP, a.replace("/", os.sep)))
    ]
    check(
        not faltan,
        f"P2 service worker sin rutas fantasma {('-> falta ' + ', '.join(faltan)) if faltan else ''}",
    )

    # P3 — manifest
    try:
        m = json.loads(mtxt)
        iconos = [i.get("src", "") for i in m.get("icons", [])]
        faltan_i = [
            i
            for i in iconos
            if not os.path.exists(
                os.path.join(APP, i.replace("./", "").replace("/", os.sep))
            )
        ]
        check(
            not faltan_i,
            f"P3a iconos del manifest existen {('-> falta ' + ', '.join(faltan_i)) if faltan_i else ''}",
        )
        check(
            bool(m.get("name")) and bool(m.get("start_url")),
            "P3b manifest con nombre y arranque",
        )
        check(
            m.get("display") in ("standalone", "fullscreen", "minimal-ui"),
            "P3c manifest instalable (display)",
        )
    except Exception as e:
        check(False, f"P3 manifest es JSON valido ({str(e)[:40]})")

    # P4 — audios
    for a in re.findall(r'src="(audios/[^"]+)"', html):
        check(
            os.path.exists(os.path.join(APP, a.replace("/", os.sep))),
            f"P4 audio existe: {a}",
        )

    # P5 — credenciales
    for pat in ("sk-", "nvapi-", "ghp_", "ntn_", "AKIA"):
        check(pat not in html and pat not in swtxt, f"P5 sin credencial '{pat}...'")

    # P6 — accesibilidad minima
    check('lang="es"' in html, "P6a idioma declarado")
    check('name="viewport"' in html, "P6b viewport responsive")
    check("prefers-reduced-motion" in html, "P6c respeta reduced-motion")

    # P7 — aviso de privacidad real
    bajo = html.lower()
    check(
        ("en tu dispositivo" in bajo)
        or ("solo en tu" in bajo)
        or ("no sale de tu" in bajo),
        "P7 declara que los datos se quedan en el dispositivo",
    )

    # coherencia: version de cache anunciada
    ver = re.search(r"CACHE\s*=\s*'([^']+)'", swtxt)
    print(f"  info: version de cache = {ver.group(1) if ver else 'no declarada'}")


def prod():
    print("== PRODUCCION ==")
    rutas = [
        "/",
        "/manifest.webmanifest",
        "/sw.js",
        "/watch/",
        "/assets/icon-192.png",
        "/assets/icon-512.png",
        "/audios/calma_marc.mp3",
        "/audios/fuerte_marc.mp3",
    ]
    for r in rutas:
        try:
            resp = urllib.request.urlopen(PROD + r, timeout=25)
            datos = resp.read()
            check(
                resp.status == 200 and len(datos) > 0,
                f"P8 {r} responde 200 ({len(datos):,} B)",
            )
        except Exception as e:
            check(False, f"P8 {r} accesible ({str(e)[:40]})")


modo = sys.argv[1] if len(sys.argv) > 1 else "ambos"
if modo in ("local", "ambos"):
    local()
if modo in ("prod", "ambos"):
    prod()

print()
if fails:
    print(f"BLOQUEADO — {len(fails)} contrato(s) roto(s): " + "; ".join(fails))
    sys.exit(1)
print("TODOS LOS CONTRATOS DE LA APP OK")
