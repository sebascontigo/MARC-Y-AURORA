import os, json, time

ROOT = r"C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA IA\MARC Y AURORA"
SKIP = {".mimosa", ".git", "node_modules", "__pycache__"}

dirs = []
files = []
for base, dnames, fnames in os.walk(ROOT):
    dnames[:] = [d for d in dnames if d not in SKIP]
    rel = os.path.relpath(base, ROOT)
    if rel == ".":
        rel = ""
    for d in dnames:
        dirs.append(os.path.join(rel, d) if rel else d)
    for f in fnames:
        p = os.path.join(base, f)
        try:
            sz = os.path.getsize(p)
            mt = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(p)))
        except Exception:
            sz, mt = -1, "?"
        files.append((os.path.join(rel, f) if rel else f, sz, mt))

print("=== DIRECTORIOS (%d) ===" % len(dirs))
for d in sorted(dirs):
    print("  [D]", d)

print("\n=== ARCHIVOS (%d) ===" % len(files))
# agrupar por carpeta top-level
from collections import defaultdict
by_top = defaultdict(list)
for path, sz, mt in files:
    top = path.split(os.sep)[0] if os.sep in path else "(raiz)"
    by_top[top].append((path, sz, mt))
for top in sorted(by_top):
    items = by_top[top]
    tot = sum(s for _, s, _ in items if s > 0)
    print(f"\n## {top}  ({len(items)} archivos, {tot/1024:.0f} KB)")
    for path, sz, mt in sorted(items):
        print(f"   {mt}  {sz:>9d}  {path}")
