#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VERIFICADOR DE LA LANDING DE AURORA (regla anti-regresion, espejo del de Marc).
Contratos que no pueden romperse en SOBERANIA VITAL:
  A1. CTA a Instagram @auroravelav presente al menos 3 veces
  A2. Precio 997 EUR y consulta 75 EUR presentes
  A3. Cero telefonos/CTA de Marc (no mezclar clientes)
  A4. Estructura minima: 6 secciones, HTML cerrado, idioma es
  A5. Sin credenciales ni tokens en el archivo publicado
  A6. Sin promesas de curacion (lenguaje sanitario prohibido)

Uso:  python _verificar_aurora.py [local|prod|ambos]
Salida: exit 1 si algun contrato falla.
"""

import os, re, sys, urllib.request

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL = os.path.join(WS, "AURORA", "WEB_SOBERANIA_VITAL", "index.html")
PROD = "https://soberania-vital.netlify.app"

PROHIBIDO_SALUD = [
    "cura ",
    "curar",
    "curación",
    "curacion",
    "elimina la enfermedad",
    "trata la enfermedad",
    "diagnostic",
    "garantizamos resultados",
    "resultados garantizados",
    "adelgaza sin esfuerzo",
    "milagro",
]
TEL_MARC = ["643270566", "642666972", "wa.me/34643"]

fails = []


def check(cond, nombre):
    print(("  OK   " if cond else "  FALLA ") + nombre)
    if not cond:
        fails.append(nombre)


def analizar(html, origen):
    print(f"== {origen} ==")
    check(
        html.count("instagram.com/auroravelav") >= 3,
        f"A1 CTA a @auroravelav x3 (hay {html.count('instagram.com/auroravelav')})",
    )
    check("997" in html, "A2a precio programa 997 EUR presente")
    check(
        "75 €" in html or "75 &euro;" in html or "75 EUR" in html,
        "A2b consulta 75 EUR presente",
    )
    check(
        not any(t in html for t in TEL_MARC),
        "A3 sin datos de contacto de Marc (clientes separados)",
    )
    n_sec = html.count("<section")
    check(n_sec >= 6, f"A4a al menos 6 secciones (hay {n_sec})")
    check("</html>" in html, "A4b HTML cerrado")
    check('lang="es"' in html, "A4c idioma declarado es")
    for pat in ("sk-", "nvapi-", "ghp_", "ntn_", "AKIA"):
        check(pat not in html, f"A5 sin credencial '{pat}...'")
    bajo = html.lower()
    encontrados = [p for p in PROHIBIDO_SALUD if p in bajo]
    check(
        not encontrados,
        f"A6 sin promesas sanitarias {('-> ' + ', '.join(encontrados)) if encontrados else ''}",
    )


modo = sys.argv[1] if len(sys.argv) > 1 else "ambos"

if modo in ("local", "ambos"):
    if os.path.exists(LOCAL):
        analizar(open(LOCAL, encoding="utf-8").read(), "LOCAL")
    else:
        check(False, "A4 index.html local existe")

if modo in ("prod", "ambos"):
    try:
        html = (
            urllib.request.urlopen(PROD + "/", timeout=25)
            .read()
            .decode("utf-8", "ignore")
        )
        analizar(html, "PRODUCCION " + PROD)
    except Exception as e:
        check(False, f"produccion accesible ({str(e)[:60]})")

print()
if fails:
    print(f"BLOQUEADO — {len(fails)} contrato(s) roto(s): " + "; ".join(fails))
    sys.exit(1)
print("TODOS LOS CONTRATOS DE AURORA OK")
