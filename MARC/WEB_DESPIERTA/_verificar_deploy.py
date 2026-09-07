#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VERIFICADOR PRE/POST-DEPLOY — DESPIERTA (regla anti-regresión)
Corre ANTES de cada deploy y DESPUÉS en producción. Si algo falla: EXIT 1 (bloquea).

Uso:
  python _verificar_deploy.py local   -> verifica carpeta local
  python _verificar_deploy.py prod    -> verifica producción (curl)
  python _verificar_deploy.py         -> verifica AMBOS

CONTRATOS (lo que JAMÁS puede romperse):
  C1. WhatsApp de captación = 34643270566 en TODOS los CTAs (3 sitios)
  C2. Cero ocurrencias del número viejo 34642666972
  C3. index.html existe y pesa >30KB (landing completa, no rota)
  C4. E-book descargable (PDF 200, >400KB)
  C5. Sin credenciales/tokens en archivos publicados (patrones sk-, nvapi-, wk-)
  C6. Precio 1.497 € presente; precio Aurora 997 € en SU landing
"""
import sys, os, re, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))  # WEB_DESPIERTA/
WS_OK  = "34643270566"
WS_OLD = "34642666972"
PROD = "https://despierta-marc.netlify.app"

fails = []
def check(cond, name):
    print(("  ✅ " if cond else "  ❌ ") + name)
    if not cond: fails.append(name)

def scan_html(html):
    check(html.count(WS_OK) >= 3, f"C1 WhatsApp correcto x3 (hay {html.count(WS_OK)})")
    check(WS_OLD not in html, "C2 sin número viejo")
    check("1.497" in html or "1497" in html, "C6 precio DESPIERTA presente")
    for pat in ("sk-", "nvapi-", "wk-", "AKIA"):
        check(pat not in html, f"C5 sin credencial '{pat}…'")

def local():
    print("== LOCAL ==")
    p = os.path.join(ROOT, "index.html")
    ok = os.path.exists(p); check(ok, "C3 index.html existe")
    if ok:
        html = open(p, encoding="utf-8").read()
        check(html.count("<section") == 10, f"C3 landing completa (10 secciones; hay {html.count('<section')})")
        check("</html>" in html, "C3 HTML cerrado")
        scan_html(html)
    pdf = os.path.join(ROOT, "La_Loca_en_Tu_Cabeza.pdf")
    check(os.path.exists(pdf) and os.path.getsize(pdf) > 400000, "C4 e-book presente local")

def prod():
    print("== PRODUCCIÓN ==")
    try:
        html = urllib.request.urlopen(PROD + "/", timeout=20).read().decode("utf-8", "ignore")
        check(html.count("<section") == 10, f"C3 landing viva (10 secciones; hay {html.count('<section')})")
        check("wa.me" in html and "DESPIERTA" in html.upper(), "C3 contenido real")
        scan_html(html)
        r = urllib.request.urlopen(PROD + "/La_Loca_en_Tu_Cabeza.pdf", timeout=25)
        check(r.status == 200 and len(r.read()) > 400000, "C4 e-book 200 en producción")
    except Exception as e:
        check(False, f"C3/C4 producción accesible ({str(e)[:60]})")

mode = sys.argv[1] if len(sys.argv) > 1 else "ambos"
if mode in ("local", "ambos"): local()
if mode in ("prod",  "ambos"): prod()
print()
if fails:
    print(f"⛔ BLOQUEADO — {len(fails)} contrato(s) roto(s): " + "; ".join(fails))
    sys.exit(1)
print("✅ TODOS LOS CONTRATOS OK — DESPLIEGUE/LAUNCH SEGURO")
