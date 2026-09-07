# -*- coding: utf-8 -*-
"""Valida rápida de HTMLs: apertura/cierre de etiquetas clave + ids referenciados."""
import re, sys
from pathlib import Path

def check(path):
    txt = Path(path).read_text(encoding="utf-8")
    errors = []
    # balance simple de div/section
    for tag in ["div", "section", "details", "button"]:
        opens = len(re.findall(r"<%s[\s>]" % tag, txt))
        closes = len(re.findall(r"</%s>" % tag, txt))
        if opens != closes:
            errors.append(f"tag {tag}: {opens} aperturas vs {closes} cierres")
    # ids referenciados por getElementById / onclick go('x') -> v-x
    ids = set(re.findall(r'id="([^"]+)"', txt))
    refs = set(re.findall(r'getElementById\("([^"]+)"\)', txt))
    missing = refs - ids
    if missing:
        errors.append(f"getElementById sin id: {missing}")
    # data-go -> v- existente
    gos = set(re.findall(r'data-go="([^"]+)"', txt))
    for g in list(gos):
        if ("v-" + g) not in ids:
            errors.append(f"data-go '{g}' sin vista v-{g}")
    print(("OK " if not errors else "FAIL ") + str(path))
    for e in errors:
        print("   -", e)
    return not errors

ok = True
for p in [
    r"MARC\WEB_DESPIERTA\index.html",
    r"MARC\APP_DESPIERTA\index.html",
    r"AURORA\WEB_SOBERANIA_VITAL\index.html",
]:
    ok = check(Path(p)) and ok
sys.exit(0 if ok else 1)