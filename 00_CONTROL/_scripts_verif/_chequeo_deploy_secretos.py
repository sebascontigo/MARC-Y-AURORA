#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CHEQUEO 2 — paquetes de deploy, asset del QR, ZIPs, y barrido de credenciales en
castellano. NUNCA imprime valores: solo ruta, tipo de patron y numero de coincidencias.
Salida: 00_CONTROL/AUDITORIA_100_2026-09-05/CHEQUEO_DEPLOY_Y_SECRETOS.txt
"""

import os, re, sys, io, zipfile, atexit

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
        os.path.join(OUT_DIR, "CHEQUEO_DEPLOY_Y_SECRETOS.txt"), "w", encoding="utf-8"
    ).write(_buf.getvalue())
)

print("=== 1. CARPETAS DE DEPLOY (lo que se subiria tal cual) ===")
for rel in ["MARC/WEB_DESPIERTA", "MARC/APP_DESPIERTA", "AURORA/WEB_SOBERANIA_VITAL"]:
    d = os.path.join(WS, rel.replace("/", os.sep))
    print(f"  -- {rel}")
    if not os.path.isdir(d):
        print("     NO EXISTE")
        continue
    for root, dirs, files in os.walk(d):
        for f in sorted(files):
            if f == "desktop.ini":
                continue
            p = os.path.join(root, f)
            print(f"     {os.path.relpath(p, d):46s} {os.path.getsize(p):>10,} B")

print("\n=== 2. REFERENCIAS LOCALES DE index.html QUE DEBEN EXISTIR ===")
REF = re.compile(r'(?:src|href)="(?!https?:|#|mailto:|tel:|data:)([^"]+)"')
for rel in [
    "MARC/WEB_DESPIERTA/index.html",
    "MARC/APP_DESPIERTA/index.html",
    "MARC/APP_DESPIERTA/watch/index.html",
    "AURORA/WEB_SOBERANIA_VITAL/index.html",
]:
    p = os.path.join(WS, rel.replace("/", os.sep))
    if not os.path.exists(p):
        print(f"  {rel}: NO EXISTE")
        continue
    base = os.path.dirname(p)
    html = open(p, encoding="utf-8", errors="ignore").read()
    refs = sorted(set(REF.findall(html)))
    print(f"  -- {rel}  ({len(refs)} referencias locales)")
    for r in refs:
        target = os.path.normpath(os.path.join(base, r.split("?")[0]))
        ok = os.path.exists(target)
        print(f"     {'OK ' if ok else 'FALTA'}  {r}")

print("\n=== 3. ZIPS DE ENTREGA ===")
for rel in ["MARC/WEB_DESPIERTA.zip", "MARC/APP_DESPIERTA.zip"]:
    p = os.path.join(WS, rel.replace("/", os.sep))
    if not os.path.exists(p):
        print(f"  {rel}: NO EXISTE")
        continue
    z = zipfile.ZipFile(p)
    print(f"  -- {rel}  ({os.path.getsize(p):,} B, {len(z.infolist())} entradas)")
    for i in z.infolist():
        print(f"     {i.filename:46s} {i.file_size:>10,} B")

print("\n=== 4. BARRIDO DE CREDENCIALES EN CASTELLANO (solo ruta + tipo + nº) ===")
PAT = [
    (
        "clave/contrasena_con_valor",
        re.compile(r"(?i)\b(contrase[nñ]a|clave|password|pass|pwd)\s*[:=]\s*\S{4,}"),
    ),
    (
        "usuario_con_valor",
        re.compile(r"(?i)\b(usuario|user|login|correo)\s*[:=]\s*\S{4,}"),
    ),
    (
        "codigo_2fa",
        re.compile(
            r"(?i)\b(c[oó]digo|codigo)\s*(de)?\s*(verificaci[oó]n|2fa|sms)\s*[:=]?\s*\d{4,8}"
        ),
    ),
    (
        "token_generico",
        re.compile(r"(?i)\b(token|api[_-]?key|secret)\s*[:=]\s*\S{12,}"),
    ),
]
EXT = {
    ".txt",
    ".md",
    ".json",
    ".csv",
    ".log",
    ".py",
    ".ps1",
    ".html",
    ".yml",
    ".yaml",
    ".env",
    ".ini",
}
SKIP = {
    ".git",
    ".ig-profile",
    "node_modules",
    "__pycache__",
    ".ruff_cache",
    ".mimosa",
    ".venv",
}

hits = {}
revisados = 0
for root, dirs, files in os.walk(WS):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for fn in files:
        if os.path.splitext(fn)[1].lower() not in EXT:
            continue
        p = os.path.join(root, fn)
        if os.path.abspath(p) == os.path.abspath(__file__):
            continue
        try:
            if os.path.getsize(p) > 12_000_000:
                continue
            txt = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        revisados += 1
        found = {}
        for nombre, rx in PAT:
            n = len(rx.findall(txt))
            if n:
                found[nombre] = n
        if found:
            hits[os.path.relpath(p, WS)] = found

print(f"  archivos revisados: {revisados}")
print(f"  archivos con coincidencias: {len(hits)}")
for k, v in sorted(hits.items()):
    detalle = ", ".join(f"{a}x{b}" for a, b in v.items())
    print(f"     {detalle:52s} {k}")

print("\n=== 5. MASTER_ACCESS: estado del deposito de credenciales ===")
ma = os.path.join(WS, "MASTER_ACCESS.md")
if os.path.exists(ma):
    t = open(ma, encoding="utf-8").read()
    print(
        "  MASTER_ACCESS.md:",
        "apunta a boveda cifrada (DPAPI)"
        if "vault" in t or ".enc" in t
        else "REVISAR contenido",
    )
    print("  longitud:", len(t), "caracteres (si es corto = solo puntero, correcto)")
print("\nFIN")
