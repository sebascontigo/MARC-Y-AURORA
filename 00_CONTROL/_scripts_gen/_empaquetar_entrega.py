#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EMPAQUETADOR LIMPIO DE ENTREGA — construye ZIPs solo con lo que debe publicarse.
Excluye: .netlify, backups .bak*, scripts internos (_*.py), desktop.ini, temporales.
NO borra nada: escribe ZIPs nuevos con sufijo de fecha y verifica su contenido.

Uso: python _empaquetar_entrega.py
"""

import os, zipfile, datetime, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOY = datetime.date.today().strftime("%Y%m%d")

PAQUETES = {
    "WEB_DESPIERTA": os.path.join(WS, "MARC", "WEB_DESPIERTA"),
    "APP_DESPIERTA": os.path.join(WS, "MARC", "APP_DESPIERTA"),
    "WEB_SOBERANIA_VITAL": os.path.join(WS, "AURORA", "WEB_SOBERANIA_VITAL"),
}
DESTINO = os.path.join(WS, "00_CONTROL", "PAQUETES_ENTREGA_" + HOY)
os.makedirs(DESTINO, exist_ok=True)

EXCLUIR_DIR = {".netlify", "__pycache__"}


def excluir(nombre):
    n = nombre.lower()
    if n == "desktop.ini":
        return True
    if ".bak" in n:
        return True
    if n.startswith("_") and n.endswith(".py"):
        return True
    if n.endswith((".tmp", ".log")):
        return True
    return False


total_ok = True
for nombre, carpeta in PAQUETES.items():
    if not os.path.isdir(carpeta):
        print(f"[FALTA] {nombre}: no existe {carpeta}")
        total_ok = False
        continue
    zpath = os.path.join(DESTINO, f"{nombre}_{HOY}.zip")
    incluidos = []
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(carpeta):
            dirs[:] = [d for d in dirs if d not in EXCLUIR_DIR]
            for f in sorted(files):
                if excluir(f):
                    continue
                p = os.path.join(root, f)
                arc = os.path.relpath(p, carpeta).replace(os.sep, "/")
                z.write(p, arc)
                incluidos.append((arc, os.path.getsize(p)))

    # verificacion del paquete recien creado
    with zipfile.ZipFile(zpath) as z:
        bad = z.testzip()
        nombres = z.namelist()
    tiene_index = "index.html" in nombres
    sin_basura = not any(
        (
            ".bak" in n.lower()
            or n.lower().endswith("desktop.ini")
            or n.startswith(".netlify")
            or n.endswith(".py")
        )
        for n in nombres
    )
    ok = bad is None and tiene_index and sin_basura
    total_ok = total_ok and ok
    print(
        f"[{'OK ' if ok else 'REV'}] {nombre}: {len(nombres)} archivos, {os.path.getsize(zpath):,} B"
    )
    print(
        f"      index.html={tiene_index}  integridad={'ok' if bad is None else bad}  sin_basura={sin_basura}"
    )
    for arc, sz in incluidos:
        print(f"      {arc:44s} {sz:>10,} B")

print()
print("Paquetes en:", DESTINO)
print(
    "RESULTADO:",
    "TODOS LOS PAQUETES LIMPIOS Y VERIFICADOS" if total_ok else "REVISAR AVISOS",
)
sys.exit(0 if total_ok else 1)
