#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ANALISIS DE CONTINUIDAD — sesiones exportadas de agentes + configuracion de agentes.
Solo lectura. No imprime valores sensibles: solo metadatos (fecha, tema, tamano).
Salida: 00_CONTROL/AUDITORIA_100_2026-09-05/CONTINUIDAD.txt
"""

import os, re, sys, io, json, atexit, collections, datetime

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
    lambda: open(os.path.join(OUT_DIR, "CONTINUIDAD.txt"), "w", encoding="utf-8").write(
        _buf.getvalue()
    )
)

SES = os.path.join(WS, "00_CONTROL", "HISTORIAL_SESIONES")
print("=== 1. SESIONES EXPORTADAS DE AGENTES ===")
if not os.path.isdir(SES):
    print("  carpeta no encontrada")
else:
    files = [
        f for f in os.listdir(SES) if f.endswith(".md") and not f.startswith("00_")
    ]
    por_mes = collections.Counter()
    tot = 0
    grandes = []
    for f in files:
        p = os.path.join(SES, f)
        sz = os.path.getsize(p)
        tot += sz
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})_", f)
        if m:
            por_mes[f"{m.group(1)}-{m.group(2)}"] += 1
        grandes.append((sz, f))
    grandes.sort(reverse=True)
    print(f"  sesiones exportadas: {len(files)}   peso total: {tot / 1048576:.1f} MB")
    print(f"  por mes: {dict(sorted(por_mes.items()))}")
    fechas = sorted(
        mm.group(1)
        for mm in (re.match(r"(\d{4}-\d{2}-\d{2})_", f) for f in files)
        if mm
    )
    if fechas:
        print(f"  rango: {fechas[0]} -> {fechas[-1]}")
    print("  -- 15 sesiones mas extensas (probable trabajo real, no saludos)")
    for sz, f in grandes[:15]:
        print(f"     {sz / 1024:8.0f} KB  {f}")
    triviales = [f for sz, f in grandes if sz < 1500]
    print(f"  -- sesiones triviales (<1,5 KB, ruido): {len(triviales)}")

print("\n=== 2. CONFIGURACION DE AGENTES EN ESTE WORKSPACE ===")
CFG = [
    ("opencode.json (proyecto)", "opencode.json"),
    ("AGENTS.md (MARC)", "MARC/AGENTS.md"),
    ("MCP MARC", "MARC/.mcp.json"),
]
for nombre, rel in CFG:
    p = os.path.join(WS, rel.replace("/", os.sep))
    if not os.path.exists(p):
        print(f"  {nombre}: NO EXISTE")
        continue
    txt = open(p, encoding="utf-8", errors="ignore").read()
    print(f"  -- {nombre}  ({len(txt)} car.)")
    if rel.endswith(".json"):
        try:
            d = json.loads(re.sub(r"^\s*//.*$", "", txt, flags=re.M))

            def claves(o, pref="", prof=0):
                if prof > 1 or not isinstance(o, dict):
                    return []
                out = []
                for k, v in o.items():
                    out.append(pref + k)
                    if isinstance(v, dict) and prof < 1:
                        out += claves(v, pref + k + ".", prof + 1)
                return out

            ks = claves(d)
            print(f"     claves: {', '.join(ks[:40])}")
            # nombres de modelos/proveedores SIN valores sensibles
            if "provider" in d and isinstance(d["provider"], dict):
                for prov, cfg in d["provider"].items():
                    ms = list((cfg or {}).get("models", {}).keys())
                    print(f"     provider '{prov}': {len(ms)} modelos")
            for campo in ("model", "small_model", "agent", "permission", "mcp"):
                if campo in d:
                    v = d[campo]
                    print(
                        f"     {campo}: {list(v.keys()) if isinstance(v, dict) else v}"
                    )
        except Exception as e:
            print(f"     (no parseable como JSON: {str(e)[:60]})")

print("\n=== 3. AGENTES/SKILLS DECLARADOS DENTRO DE MARC/.github ===")
gh = os.path.join(WS, "MARC", ".github")
if os.path.isdir(gh):
    for root, dirs, files in os.walk(gh):
        for f in sorted(files):
            p = os.path.join(root, f)
            print(f"  {os.path.relpath(p, gh):58s} {os.path.getsize(p):>8,} B")
else:
    print("  no existe")

print("\n=== 4. AUTOMATIZACIONES ACTIVAS DETECTADAS ===")
aut = os.path.join(WS, "AUTOMATIZACION")
if os.path.isdir(aut):
    for root, dirs, files in os.walk(aut):
        for f in sorted(files):
            p = os.path.join(root, f)
            print(
                f"  {os.path.relpath(p, WS):64s} {os.path.getsize(p):>8,} B  mod={datetime.datetime.fromtimestamp(os.path.getmtime(p)):%Y-%m-%d %H:%M}"
            )
    est = os.path.join(aut, "VIGIA_EXPERIENTIAL", "ESTADO.md")
    if os.path.exists(est):
        t = open(est, encoding="utf-8").read()
        sem = re.search(r"Semaforo:\s*(.+)", t)
        rev = re.search(r"Ultima revision:\s*(.+)", t)
        print(
            f"  VIGIA: semaforo={sem.group(1).strip() if sem else '?'} | ultima revision={rev.group(1).strip() if rev else '?'}"
        )
        print(
            "  NOTA: es una tarea programada que se ejecuta sin intervencion (revisar si sigue siendo deseada)."
        )
else:
    print("  sin carpeta AUTOMATIZACION")

print("\n=== 5. DOCUMENTOS RECTORES Y SU FRESCURA ===")
RECTORES = [
    "README.md",
    "00_EMPIEZA_AQUI.md",
    "MASTER_CONTEXT.md",
    "MASTER_STATUS.md",
    "MASTER_TASKS.md",
    "MASTER_DECISIONS.md",
    "MASTER_CHANGELOG.md",
    "MASTER_ASSETS.md",
    "MASTER_ACCESS.md",
    "MASTER_KPIS.md",
    "MASTER_ROADMAP.md",
    "MARC/00_DONDE_ESTA_TODO.md",
    "AURORA/00_DONDE_ESTA_TODO.md",
    "MARC/PENDIENTE_SEBASTIAN.md",
    "MARC/KIT_PUBLICACION_10MIN.md",
    "MARC/COLA_VERIFICADA_2026-09-04.md",
    "TAREAS_SEBASTIAN_HOY.md",
    "INFORME_FINAL_2026-08-28.md",
    "HANDOFF_ZED.md",
]
hoy = datetime.date.today()
for rel in RECTORES:
    p = os.path.join(WS, rel.replace("/", os.sep))
    if not os.path.exists(p):
        print(f"  FALTA  {rel}")
        continue
    mt = datetime.date.fromtimestamp(os.path.getmtime(p))
    txt = open(p, encoding="utf-8", errors="ignore").read()
    m = re.search(
        r"(?:Actualizad[oa]|Última actualización|Ultima actualizacion|Generado|Creado)[:*\s]*([0-9]{4}-[0-9]{2}-[0-9]{2})",
        txt,
    )
    declarada = m.group(1) if m else "sin fecha declarada"
    dias = (hoy - mt).days
    print(f"  disco={mt} ({dias:2d}d)  declarada={declarada:22s} {rel}")
print("\nFIN")
