#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CHEQUEO TECNICO DE ENTREGABLES — MARC Y AURORA (solo lectura).
1) Reels 9:16: dimensiones, duracion, audio, peso (ffprobe).
2) Assets de lanzamiento y portadas: dimensiones reales (Pillow).
3) Barrido de secretos por PATRON: reporta SOLO ruta y tipo, nunca el valor.
4) Riesgo de versionado: rutas sensibles que git podria capturar.

Salida: 00_CONTROL/AUDITORIA_100_2026-09-05/CHEQUEO_TECNICO.txt
"""

import os, re, sys, json, glob, subprocess, io, atexit

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
        os.path.join(OUT_DIR, "CHEQUEO_TECNICO.txt"), "w", encoding="utf-8"
    ).write(_buf.getvalue())
)


def ffprobe(path):
    try:
        out = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-print_format",
                "json",
                "-show_streams",
                "-show_format",
                path,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        ).stdout
        d = json.loads(out)
        v = [s for s in d["streams"] if s["codec_type"] == "video"]
        a = [s for s in d["streams"] if s["codec_type"] == "audio"]
        dur = float(d["format"]["duration"])
        return (
            v[0]["width"],
            v[0]["height"],
            round(dur, 1),
            len(a),
            v[0]["codec_name"],
        )
    except Exception as e:
        return ("ERR", str(e)[:60], 0, 0, "")


print("=== 1. REELS FINALES 9:16 (deben ser 1080x1920, ~30s, con audio) ===")
reels = sorted(
    glob.glob(os.path.join(WS, "MARC", "21_TESTIMONIOS", "REELS_FINALES", "*.mp4"))
)
for f in reels:
    w, h, dur, na, codec = ffprobe(f)
    mb = round(os.path.getsize(f) / 1048576, 2)
    ok = "OK " if (w == 1080 and h == 1920 and na >= 1) else "REV"
    print(
        f"  [{ok}] {os.path.basename(f):32s} {w}x{h}  {dur}s  audio={na}  {codec}  {mb} MB"
    )

print("\n=== 2. VIDEOS FUENTE / VERSIONES WEB (formato original) ===")
for f in sorted(
    glob.glob(os.path.join(WS, "MARC", "21_TESTIMONIOS", "VERSIONES_WEB", "*.mp4"))
):
    w, h, dur, na, codec = ffprobe(f)
    mb = round(os.path.getsize(f) / 1048576, 2)
    print(f"  {os.path.basename(f):36s} {w}x{h}  {dur}s  audio={na}  {mb} MB")

print("\n=== 3. IMAGENES CLAVE (dimensiones reales) ===")
try:
    from PIL import Image

    grupos = {
        "LANZAMIENTO MARC": os.path.join(
            WS, "MARC", "04_Instagram", "ASSETS", "LANZAMIENTO", "*.jpg"
        ),
        "LANZAMIENTO AURORA": os.path.join(
            WS, "AURORA", "04_Instagram", "ASSETS", "LANZAMIENTO", "*.jpg"
        ),
        "PORTADAS MARC": os.path.join(
            WS, "MARC", "04_Instagram", "ASSETS", "HIGHLIGHT_COVERS", "*.png"
        ),
        "PORTADAS AURORA": os.path.join(
            WS, "AURORA", "04_Instagram", "ASSETS", "HIGHLIGHT_COVERS", "*.png"
        ),
        "BRAND KIT MARC": os.path.join(
            WS, "MARC", "27_BRAND_KIT", "PLANTILLAS", "*.jpg"
        ),
        "QR": os.path.join(WS, "MARC", "04_Instagram", "ASSETS", "QR_*.png"),
    }
    for nombre, patron in grupos.items():
        fs = sorted(glob.glob(patron))
        print(f"  -- {nombre} ({len(fs)} archivos)")
        for f in fs:
            try:
                with Image.open(f) as im:
                    print(
                        f"     {os.path.basename(f):46s} {im.width}x{im.height} {im.mode}"
                    )
            except Exception as e:
                print(f"     {os.path.basename(f):46s} ERROR {str(e)[:40]}")
except ImportError:
    print("  Pillow no disponible")

print("\n=== 4. BARRIDO DE SECRETOS POR PATRON (solo ruta + tipo, nunca el valor) ===")
PATRONES = [
    ("api_key_openai", re.compile(r"\bsk-[A-Za-z0-9]{20,}")),
    ("api_key_nvidia", re.compile(r"\bnvapi-[A-Za-z0-9_\-]{20,}")),
    ("token_github", re.compile(r"\bgh[pous]_[A-Za-z0-9]{20,}")),
    ("token_notion", re.compile(r"\bntn_[A-Za-z0-9]{20,}")),
    ("aws_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("bearer", re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{20,}")),
    (
        "password_campo",
        re.compile(r"(?i)\b(contrase[nñ]a|password|passwd|pwd)\s*[:=]\s*\S{4,}"),
    ),
    (
        "credencial_generica",
        re.compile(
            r"(?i)\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._\-]{16,}"
        ),
    ),
]
TEXTO = {
    ".md",
    ".txt",
    ".json",
    ".jsonc",
    ".py",
    ".ps1",
    ".html",
    ".js",
    ".css",
    ".yml",
    ".yaml",
    ".toml",
    ".env",
    ".csv",
}
SKIP = {
    ".git",
    "node_modules",
    "__pycache__",
    ".ig-profile",
    ".ruff_cache",
    ".mimosa",
    "SCAN_TMP",
    ".venv",
}

hallazgos = {}
revisados = 0
for root, dirs, files in os.walk(WS):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for fn in files:
        if os.path.splitext(fn)[1].lower() not in TEXTO:
            continue
        full = os.path.join(root, fn)
        if os.path.abspath(full) == os.path.abspath(__file__):
            continue
        try:
            if os.path.getsize(full) > 6_000_000:
                continue
            txt = open(full, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        revisados += 1
        tipos = sorted({n for n, rx in PATRONES if rx.search(txt)})
        if tipos:
            hallazgos[os.path.relpath(full, WS)] = tipos

print(f"  archivos de texto revisados: {revisados}")
if hallazgos:
    print(f"  ARCHIVOS CON PATRON SENSIBLE: {len(hallazgos)}  (valores NO mostrados)")
    for k, v in sorted(hallazgos.items()):
        print(f"     [{','.join(v)}]  {k}")
else:
    print("  Sin coincidencias de patron en archivos de texto revisados.")

print("\n=== 5. RIESGO DE VERSIONADO (rutas que NO deben entrar en git) ===")
riesgos = [
    ("00_CONTROL/.ig-profile", "perfil de navegador con datos de sesion/cookies"),
    (".netlify", "estado de despliegue"),
    (".mcp-sqlite", "base local de herramientas"),
    ("SCAN_TMP", "temporales de escaneo"),
]
for rel, motivo in riesgos:
    p = os.path.join(WS, rel.replace("/", os.sep))
    existe = os.path.exists(p)
    n = 0
    if existe and os.path.isdir(p):
        for r, d, f in os.walk(p):
            n += len(f)
    print(f"  {'EXISTE' if existe else 'no    '}  {rel:28s} archivos={n:5d}  {motivo}")
print("\nFIN")
