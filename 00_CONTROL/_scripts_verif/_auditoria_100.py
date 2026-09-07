#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AUDITORIA 100 — inventario, duplicados y anomalias del workspace MARC Y AURORA.
Solo LECTURA. No mueve, no borra, no renombra. Escribe CSVs en la carpeta de salida.

Uso: python _auditoria_100.py
"""

import os, csv, hashlib, collections, datetime, sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # MARC Y AURORA/
OUT = os.path.join(WS, "00_CONTROL", "AUDITORIA_100_2026-09-05")
os.makedirs(OUT, exist_ok=True)

SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".ruff_cache",
    ".mimosa",
    ".netlify",
    ".mcp-sqlite",
    "SCAN_TMP",
    ".venv",
}
IGNORE_NAMES = {"desktop.ini", "Thumbs.db"}

MEDIA = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico"}
VIDEO = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
AUDIO = {".mp3", ".opus", ".wav", ".m4a", ".ogg"}
DOCS = {
    ".md",
    ".txt",
    ".pdf",
    ".docx",
    ".doc",
    ".odt",
    ".xlsx",
    ".csv",
    ".pptx",
    ".rtf",
}
CODE = {
    ".py",
    ".ps1",
    ".html",
    ".js",
    ".css",
    ".json",
    ".jsonc",
    ".webmanifest",
    ".sh",
    ".toml",
    ".yml",
    ".yaml",
}

# firmas reales (magic numbers) para detectar extension que no coincide
SIGS = [
    (b"%PDF", ".pdf"),
    (b"\xff\xd8\xff", ".jpg"),
    (b"\x89PNG\r\n\x1a\n", ".png"),
    (b"GIF8", ".gif"),
    (b"PK\x03\x04", ".zip-like"),
    (b"ID3", ".mp3"),
]


def categoria(ext):
    if ext in MEDIA:
        return "imagen"
    if ext in VIDEO:
        return "video"
    if ext in AUDIO:
        return "audio"
    if ext in DOCS:
        return "documento"
    if ext in CODE:
        return "codigo"
    if ext == ".zip":
        return "paquete"
    if ext.startswith(".bak") or "bak_" in ext:
        return "backup"
    return "otro"


def proyecto(rel):
    p = rel.replace("\\", "/").split("/")[0]
    if p in (
        "MARC",
        "AURORA",
        "03_ESCALA",
        "00_CONTROL",
        "AUDITORIA_GLOBAL",
        "ARCHIVO_DOCUMENTAL",
        "MARC_Proyecto_Entrega_2026",
        "04_ACUERDOS",
        "03_ESCALA",
    ):
        return p
    return "RAIZ" if "/" not in rel.replace("\\", "/") else p


def sha256(path, limit=None):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                b = f.read(1 << 20)
                if not b:
                    break
                h.update(b)
    except Exception:
        return ""
    return h.hexdigest()


rows, empties, name_issues, mismatch, backups, big = [], [], [], [], [], []
by_size = collections.defaultdict(list)
total_bytes = 0

for root, dirs, files in os.walk(WS):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fn in files:
        if fn in IGNORE_NAMES:
            continue
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, WS)
        try:
            st = os.stat(full)
        except Exception:
            continue
        ext = os.path.splitext(fn)[1].lower()
        cat = categoria(ext)
        rows.append(
            {
                "ruta_relativa": rel,
                "nombre": fn,
                "ext": ext,
                "categoria": cat,
                "proyecto": proyecto(rel),
                "bytes": st.st_size,
                "modificado": datetime.datetime.fromtimestamp(st.st_mtime).strftime(
                    "%Y-%m-%d %H:%M"
                ),
            }
        )
        total_bytes += st.st_size
        if st.st_size == 0:
            empties.append(rel)
        if st.st_size > 20 * 1024 * 1024:
            big.append((round(st.st_size / 1048576, 1), rel))
        if ".bak" in fn.lower() or fn.lower().endswith("~"):
            backups.append(rel)
        # nombres problematicos: corchetes, dobles espacios, parentesis duplicados, ruta larga
        probs = []
        if "[" in fn or "]" in fn:
            probs.append("corchetes")
        if "  " in fn:
            probs.append("doble-espacio")
        if fn.count("(") > 1:
            probs.append("copias-(1)(1)")
        if len(full) > 240:
            probs.append("ruta-larga")
        if any(ord(c) > 0x2500 for c in fn):
            probs.append("emoji-en-nombre")
        if probs:
            name_issues.append((rel, ";".join(probs)))
        if st.st_size > 0:
            by_size[st.st_size].append(full)
        # extension vs firma real
        if ext in (".pdf", ".jpg", ".jpeg", ".png", ".gif", ".mp3") and st.st_size > 8:
            try:
                head = open(full, "rb").read(12)
            except Exception:
                head = b""
            hit = None
            for sig, e in SIGS:
                if head.startswith(sig):
                    hit = e
                    break
            norm = ".jpg" if ext == ".jpeg" else ext
            if (
                hit
                and hit != norm
                and not (hit == ".zip-like" and ext in (".docx", ".xlsx", ".pptx"))
            ):
                mismatch.append((rel, ext, hit))

# duplicados reales: mismo tamano -> comparar hash
dups = collections.defaultdict(list)
for size, paths in by_size.items():
    if len(paths) < 2:
        continue
    for p in paths:
        dups[(size, sha256(p))].append(p)
dup_groups = {k: v for k, v in dups.items() if len(v) > 1 and k[1]}


def wcsv(name, header, data):
    p = os.path.join(OUT, name)
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(header)
        w.writerows(data)
    return p


wcsv(
    "INVENTARIO.csv",
    ["ruta_relativa", "nombre", "ext", "categoria", "proyecto", "bytes", "modificado"],
    [
        [
            r["ruta_relativa"],
            r["nombre"],
            r["ext"],
            r["categoria"],
            r["proyecto"],
            r["bytes"],
            r["modificado"],
        ]
        for r in sorted(rows, key=lambda x: x["ruta_relativa"])
    ],
)

wcsv(
    "DUPLICADOS.csv",
    ["sha256_corto", "bytes", "copias", "rutas"],
    [
        [k[1][:12], k[0], len(v), " | ".join(os.path.relpath(x, WS) for x in sorted(v))]
        for k, v in sorted(dup_groups.items(), key=lambda kv: -kv[0][0] * len(kv[1]))
    ],
)

wcsv(
    "ANOMALIAS.csv",
    ["tipo", "ruta", "detalle"],
    [["vacio", r, "0 bytes"] for r in sorted(empties)]
    + [["nombre", r, d] for r, d in sorted(name_issues)]
    + [["extension", r, f"ext={e} firma={h}"] for r, e, h in sorted(mismatch)]
    + [["backup", r, "archivo .bak/~ (conservar)"] for r in sorted(backups)]
    + [["pesado", r, f"{mb} MB"] for mb, r in sorted(big, reverse=True)],
)

# resumen por categoria y proyecto
cat = collections.Counter(r["categoria"] for r in rows)
proj = collections.Counter(r["proyecto"] for r in rows)
proj_bytes = collections.Counter()
for r in rows:
    proj_bytes[r["proyecto"]] += r["bytes"]

print("== AUDITORIA 100 ==")
print(f"archivos: {len(rows)}   peso total: {round(total_bytes / 1048576, 1)} MB")
print("por categoria:", dict(cat.most_common()))
print("por proyecto :", dict(proj.most_common()))
print(
    "MB por proyecto:", {k: round(v / 1048576, 1) for k, v in proj_bytes.most_common()}
)
print(
    f"vacios: {len(empties)}  nombres-problematicos: {len(name_issues)}  "
    f"ext-mismatch: {len(mismatch)}  backups: {len(backups)}  >20MB: {len(big)}"
)
print(
    f"grupos duplicados: {len(dup_groups)}  archivos implicados: {sum(len(v) for v in dup_groups.values())}  "
    f"bytes recuperables: {round(sum(k[0] * (len(v) - 1) for k, v in dup_groups.items()) / 1048576, 1)} MB"
)
print("salida:", OUT)
