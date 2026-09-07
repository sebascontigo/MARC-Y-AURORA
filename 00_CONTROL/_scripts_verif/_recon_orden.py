#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RECONOCIMIENTO PARA ORDENAR (solo lectura):
1) Archivos sueltos en la RAIZ del workspace (fuera de carpeta tematica).
2) Duplicados con nombre distinto en MARC/ (reunion brief, alineacion, CV, informes).
3) Zonas ya existentes para archivar informes (MARC/02_Informes_Sesiones).
Salida: 00_CONTROL/AUDITORIA_100_2026-09-05/RECON_ORDEN.txt
"""

import os, sys, io, atexit, hashlib

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(WS, "00_CONTROL", "AUDITORIA_100_2026-09-05")
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
    lambda: open(os.path.join(OUT, "RECON_ORDEN.txt"), "w", encoding="utf-8").write(
        _buf.getvalue()
    )
)

print("=== 1. ARCHIVOS SUELTOS EN LA RAIZ DEL WORKSPACE ===")
CARPETAS_VALIDAS = {
    "00_CONTROL",
    "03_ESCALA",
    "04_ACUERDOS",
    "ARCHIVO_DOCUMENTAL",
    "AUDITORIA_GLOBAL",
    "AURORA",
    "MARC",
    "MARC_Proyecto_Entrega_2026",
    "SCAN_TMP",
    "AUTOMATIZACION",
    ".git",
    ".mimosa",
    ".netlify",
    ".ruff_cache",
    "00_EMPIEZA_AQUI.md",
    "README.md",
}
raiz = [f for f in os.listdir(WS) if os.path.isfile(os.path.join(WS, f))]
for f in sorted(raiz):
    sz = os.path.getsize(os.path.join(WS, f))
    print(f"  {sz:>9,} B  {f}")

print("\n=== 2. CANDIDATOS A UNIFICAR/ARCHIVAR EN MARC/ ===")
PARES = [
    ("MARC/MARC_REUNION_BRIEF.md", "MARC/15_REUNION_BRIEF_MARC.md"),
    ("MARC/MARC_DOCUMENTO_ALINEACION.md", "MARC/16_DOCUMENTO_ALINEACION_MARC.md"),
    (
        "MARC/25_MARCA_PERSONAL/CV_Marc_Souza_Gil_v2.txt",
        "MARC/25_MARCA_PERSONAL/CV_Marc_Souza_Gil_v2_miner.txt",
    ),
]
for a, b in PARES:
    ha = hashlib.sha256(
        open(os.path.join(WS, a.replace("/", os.sep)), "rb").read()
    ).hexdigest()[:12]
    hb = hashlib.sha256(
        open(os.path.join(WS, b.replace("/", os.sep)), "rb").read()
    ).hexdigest()[:12]
    print(f"  {'IGUALES' if ha == hb else 'DISTINTOS'}  {a} ({ha}) vs {b} ({hb})")

print(
    "\n=== 3. INFORMES/SESIONES QUE ESTAN SUELTOS EN LA RAIZ (fechados, no vivos) ==="
)
FECHADOS = [
    f
    for f in raiz
    if any(
        x in f
        for x in ("2026-08", "2026-09", "INFORME", "ENTREGA_HOY", "HANDOFF", "COLA")
    )
]
for f in sorted(FECHADOS):
    print(f"  {os.path.getsize(os.path.join(WS, f)):>9,} B  {f}")

print("\n=== 4. DESTINOS EXISTENTES ===")
for d in [
    "MARC/02_Informes_Sesiones",
    "ARCHIVO_DOCUMENTAL/02_INFORMES",
    "ARCHIVO_DOCUMENTAL/00_INDICE",
]:
    p = os.path.join(WS, d.replace("/", os.sep))
    n = len(os.listdir(p)) if os.path.isdir(p) else -1
    print(f"  {'EXISTS' if n >= 0 else 'FALTA '}  {d}  ({n} elementos)")

print("\nFIN")
