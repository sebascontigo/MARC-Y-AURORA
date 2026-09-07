#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Resumen legible de la auditoria: top carpetas, anomalias y duplicados grandes."""

import csv, collections, os, sys, io, atexit

BASE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "AUDITORIA_100_2026-09-05"
)

# Espejo de la salida a RESUMEN.txt (la consola del agente puede truncar)
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
    lambda: open(os.path.join(BASE, "RESUMEN.txt"), "w", encoding="utf-8").write(
        _buf.getvalue()
    )
)

rows = list(
    csv.DictReader(
        open(os.path.join(BASE, "INVENTARIO.csv"), encoding="utf-8-sig"), delimiter=";"
    )
)
n = collections.Counter()
b = collections.Counter()
for r in rows:
    key = "/".join(r["ruta_relativa"].replace("\\", "/").split("/")[:2])
    n[key] += 1
    b[key] += int(r["bytes"])

print("== TOP CARPETAS (nº archivos / MB) ==")
for k, c in n.most_common(20):
    print(f"{c:5d}  {b[k] / 1048576:9.1f} MB  {k}")

anom = list(
    csv.DictReader(
        open(os.path.join(BASE, "ANOMALIAS.csv"), encoding="utf-8-sig"), delimiter=";"
    )
)
print("\n== ANOMALIAS por tipo ==")
for t, c in collections.Counter(a["tipo"] for a in anom).most_common():
    print(f"{c:5d}  {t}")

print("\n== PESADOS (>20MB) ==")
for a in anom:
    if a["tipo"] == "pesado":
        print(f"  {a['detalle']:>10}  {a['ruta']}")

print("\n== VACIOS (primeros 25) ==")
vac = [a["ruta"] for a in anom if a["tipo"] == "vacio"]
for v in vac[:25]:
    print("  " + v)
print(f"  ... total {len(vac)}")

dups = list(
    csv.DictReader(
        open(os.path.join(BASE, "DUPLICADOS.csv"), encoding="utf-8-sig"), delimiter=";"
    )
)
print("\n== DUPLICADOS mas pesados (top 12) ==")
for d in dups[:12]:
    mb = int(d["bytes"]) / 1048576
    print(f"  {mb:8.2f} MB x{d['copias']}  {d['rutas'][:200]}")
