#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHIVISTA DIGITAL — MARC Y AURORA
Copia documentos clave a la estructura numerada ARCHIVO_DOCUMENTAL (originales intactos)
y genera el ÍNDICE MAESTRO cronológico.
Reglas: NO borra, NO sobrescribe originales, NO inventa fechas.
"""
import os, re, shutil, csv, hashlib
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raíz del proyecto MARC Y AURORA
ARCH = os.path.join(ROOT, "ARCHIVO_DOCUMENTAL")

DOC_EXT = {'.md','.pdf','.docx','.xlsx','.txt','.csv','.odt'}
SKIP_DIRS = {'.git','.mimosa','__pycache__','.mcp-sqlite','.github','ARCHIVO_DOCUMENTAL'}

# ---------- 1. Recolectar todos los documentos ----------
docs = []
for r, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in DOC_EXT:
            full = os.path.join(r, f)
            rel = os.path.relpath(full, ROOT)
            docs.append({'file': f, 'rel': rel, 'full': full, 'ext': ext})

print(f"Documentos encontrados: {len(docs)}")

# ---------- 2. Clasificar por persona ----------
def clasify(rel):
    u = rel.replace('\\','/')
    if '/AURORA/' in u or u.startswith('AURORA/'):
        return 'AURORA'
    if '/MARC/' in u or u.startswith('MARC/') or u.startswith('MARC_Proyecto_Entrega_2026/'):
        return 'MARC'
    # compartido
    return 'COMPARTIDO'

# ---------- 3. Extraer fecha (de nombre o carpeta; si no, por confirmar) ----------
def extract_date(rel, full):
    u = rel.replace('\\','/')
    # YYYYMMDD
    m = re.search(r'(20\d{2})(\d{2})(\d{2})', u)
    if m:
        y,mo,d = m.groups()
        if 1 <= int(mo) <= 12 and 1 <= int(d) <= 31:
            return f"{y}-{mo}-{d}"
    # YYYY-MM-DD
    m = re.search(r'(20\d{2})-(\d{2})-(\d{2})', u)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    # DD-MM-YYYY o DD_MM_YYYY
    m = re.search(r'(\d{2})[-_](\d{2})[-_](20\d{2})', u)
    if m:
        d,mo,y = m.groups()
        if 1 <= int(mo) <= 12 and 1 <= int(d) <= 31:
            return f"{y}-{mo}-{d}"
    # fallback: mtime del archivo
    try:
        mt = datetime.fromtimestamp(os.path.getmtime(full))
        return mt.strftime('%Y-%m-%d') + ' (mtime)'
    except:
        return 'Fecha_por_confirmar'

# ---------- 4. Tema por palabras clave ----------
def topic(rel, f):
    u = (rel + ' ' + f).lower()
    if any(k in u for k in ['contrato','ie6','contract']): return 'Contrato'
    if any(k in u for k in ['cv','hoja_de_vida','perfil']): return 'CV/Perfil'
    if any(k in u for k in ['beca','alegacion','subsanacion','regulariz','extranjer','nie','pasaporte']): return 'Legal/Extranjería'
    if any(k in u for k in ['instagram','ig_','note','insights','reel','carrusel','stor','contenido','hashtag']): return 'Instagram/Contenido'
    if any(k in u for k in ['escala','reunion','agenda','brief']): return 'Escala/Reuniones'
    if any(k in u for k in ['auditoria','inventario','mapa']): return 'Auditoría'
    if any(k in u for k in ['financ','precio','oferta','comision','xlsx','deuda','bank']): return 'Finanzas'
    if any(k in u for k in ['kpi','metrica','riesgo','oportunidad','plan_30','roadmap']): return 'Estrategia/KPI'
    if any(k in u for k in ['chat','whatsapp','ptt','transcript','wav','opus']): return 'Chat/Audios'
    if any(k in u for k in ['master_','readme','context','status','tasks','decision','changelog']): return 'Sistema MASTER'
    if any(k in u for k in ['casa','alquiler','luz','naturgy','transfer']): return 'Casa'
    if any(k in u for k in ['app','gemini','glide','automatiz','goHighLevel','ghl']): return 'Tech/APP'
    return 'General'

# ---------- 5. Asignar número cronológico y construir índice ----------
for d in docs:
    d['persona'] = clasify(d['rel'])
    d['fecha'] = extract_date(d['rel'], d['full'])
    d['tema'] = topic(d['rel'], d['file'])
    try:
        d['size'] = os.path.getsize(d['full'])
    except:
        d['size'] = 0

# orden cronológico (fecha limpia), luego por persona y nombre
def sortkey(d):
    f = d['fecha'][:10]
    if not re.match(r'20\d{2}-\d{2}-\d{2}$', f):
        f = '9999-99-99'  # por confirmar al final
    return (f, d['persona'], d['file'].lower())

docs.sort(key=sortkey)
for i, d in enumerate(docs, 1):
    d['num'] = f"{i:03d}"

# ---------- 6. Escribir ÍNDICE MAESTRO (CSV + MD) ----------
os.makedirs(os.path.join(ARCH, '00_INDICE'), exist_ok=True)
csv_path = os.path.join(ARCH, '00_INDICE', 'INDICE_MAESTRO.csv')
with open(csv_path, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.writer(fh)
    w.writerow(['NUM','FECHA','PERSONA','TEMA','ARCHIVO','UBICACION_ORIGINAL','EXT','TAM_KB'])
    for d in docs:
        w.writerow([d['num'], d['fecha'], d['persona'], d['tema'], d['file'], d['rel'], d['ext'], round(d['size']/1024,1)])
print(f"CSV escrito: {csv_path}")

# MD legible
md_path = os.path.join(ARCH, '00_INDICE', 'INDICE_MAESTRO.md')
with open(md_path, 'w', encoding='utf-8') as fh:
    fh.write("# ÍNDICE MAESTRO — MARC Y AURORA\n\n")
    fh.write(f"> Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')} · Total documentos: {len(docs)}\n")
    fh.write("> Sistema numerado y cronológico. Los ORIGINALES no se mueven; este índice los localiza.\n\n")
    fh.write("| NUM | FECHA | PERSONA | TEMA | ARCHIVO | UBICACIÓN ORIGINAL |\n")
    fh.write("|-----|-------|---------|------|---------|--------------------|\n")
    for d in docs:
        fh.write(f"| {d['num']} | {d['fecha']} | {d['persona']} | {d['tema']} | {d['file']} | `{d['rel']}` |\n")
print(f"MD escrito: {md_path}")

# ---------- 7. Resumen por persona/tema ----------
from collections import Counter
cp = Counter(d['persona'] for d in docs)
ct = Counter(d['tema'] for d in docs)
print("\nPor persona:", dict(cp))
print("Por tema:", dict(ct.most_common()))

# guardar metadatos para el siguiente paso (copias)
import json
with open(os.path.join(ARCH, '00_INDICE', '_docs_meta.json'), 'w', encoding='utf-8') as fh:
    json.dump(docs, fh, ensure_ascii=False, indent=1)
print("\nMetadatos guardados. Listo para el paso de copias.")
