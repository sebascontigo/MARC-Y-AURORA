#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ORDEN DE LA RAIZ DEL WORKSPACE (2026-09-06) — mueve SOLO informes fechados.
Reglas: nada se borra, nada se sobreescribe, manifiesto de cada movimiento,
verificacion de integridad (sha256 antes==despues), rollback documentado.

Qué mueve (4 archivos, todos informes fechados de sesiones pasadas):
  TAREAS_SEBASTIAN_HOY.md      -> ARCHIVO_DOCUMENTAL/02_INFORMES/
  ENTREGA_HOY_2026-08-25.md    -> ARCHIVO_DOCUMENTAL/02_INFORMES/
  INFORME_FINAL_2026-08-28.md   -> ARCHIVO_DOCUMENTAL/02_INFORMES/
  INFORME_100_2026-09-05.md     -> ARCHIVO_DOCUMENTAL/02_INFORMES/

Qué NO toca: MASTER_*.md, README, 00_EMPIEZA_AQUI, opencode.json, .gitignore,
todo MARC/, todo AURORA/, 00_CONTROL/, chats, entregas oficiales.

Uso:
  python _ordenar_raiz.py            -> ejecuta el movimiento
  python _ordenar_raiz.py --check    -> solo verifica estado sin mover
  python _ordenar_raiz.py --rollback -> devuelve cada archivo a su sitio
"""

import os, sys, hashlib, datetime, shutil

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(WS, "ARCHIVO_DOCUMENTAL", "02_INFORMES")
MANIFEST = os.path.join(DEST, "MANIFIESTO_MOVIMIENTO_2026-09-06.md")

MOVIMIENTOS = [
    (
        "TAREAS_SEBASTIAN_HOY.md",
        "Informe de tareas manuales de Sebastián (25-ago). Obsoleto: USB, hosting y webs ya resueltos.",
    ),
    (
        "ENTREGA_HOY_2026-08-25.md",
        "Informe de entrega del 25-ago (landings + app v1). Cumplió su ciclo.",
    ),
    (
        "INFORME_FINAL_2026-08-28.md",
        "Cierre de la operación montaje del 28-ago. Cumplió su ciclo.",
    ),
    (
        "INFORME_100_2026-09-05.md",
        "Informe de las 100 tareas del 5-sep. Contenido ya integrado en MASTER_STATUS/CHANGELOG.",
    ),
]

VIVOS = {
    "README.md",
    "00_EMPIEZA_AQUI.md",
    "MASTER_ACCESS.md",
    "MASTER_ASSETS.md",
    "MASTER_CHANGELOG.md",
    "MASTER_CONTEXT.md",
    "MASTER_DECISIONS.md",
    "MASTER_KPIS.md",
    "MASTER_ROADMAP.md",
    "MASTER_STATUS.md",
    "MASTER_TASKS.md",
    "opencode.json",
    ".gitignore",
    "desktop.ini",
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()[:16]


def main():
    os.makedirs(DEST, exist_ok=True)
    modo = sys.argv[1] if len(sys.argv) > 1 else "run"

    if modo == "--check":
        print("== MODO CHECK (no mueve nada) ==")
        for nombre, _ in MOVIMIENTOS:
            p = os.path.join(WS, nombre)
            d = os.path.join(DEST, nombre)
            print(
                f"  raiz={'SI' if os.path.exists(p) else 'no '}  destino={'SI' if os.path.exists(d) else 'no '}  {nombre}"
            )
        return

    if modo == "--rollback":
        print("== ROLLBACK (devuelve a la raiz) ==")
        for nombre, _ in MOVIMIENTOS:
            d = os.path.join(DEST, nombre)
            p = os.path.join(WS, nombre)
            if os.path.exists(d) and not os.path.exists(p):
                os.rename(d, p)
                print(f"  devuelto: {nombre}")
            else:
                print(f"  nada que devolver: {nombre}")
        return

    print("== MOVIMIENTO raiz -> ARCHIVO_DOCUMENTAL/02_INFORMES ==")
    hechos = []
    for nombre, motivo in MOVIMIENTOS:
        p = os.path.join(WS, nombre)
        d = os.path.join(DEST, nombre)
        if not os.path.exists(p):
            print(f"  ya movido o no existe: {nombre}")
            continue
        if os.path.exists(d):
            print(f"  CONFLICTO: ya existe en destino {nombre} — NO se toca")
            continue
        antes = sha(p)
        os.rename(p, d)
        despues = sha(d)
        ok = antes == despues
        print(f"  {'OK ' if ok else 'FALLO INTEGRIDAD'} {nombre}")
        hechos.append((nombre, motivo, antes, ok))

    # manifiesto (apend, nunca machaca)
    with open(MANIFEST, "a", encoding="utf-8") as f:
        f.write(
            f"\n## Movimiento {datetime.datetime.now():%Y-%m-%d %H:%M} — orden de la raiz\n"
        )
        f.write(
            "> Motivo general: informes fechados fuera de la raiz del workspace. Ningun borrado; solo `os.rename` con verificacion sha256. Rollback: `python 00_CONTROL/_ordenar_raiz.py --rollback`\n\n"
        )
        for nombre, motivo, h, ok in hechos:
            f.write(
                f"- `{nombre}` (sha256 {h}) -> `ARCHIVO_DOCUMENTAL/02_INFORMES/{nombre}` — {motivo}\n"
            )
    print(f"\nManifiesto: {MANIFEST}")
    print(f"Movidos: {len(hechos)} de {len(MOVIMIENTOS)}")

    # verificacion post: la raiz solo contiene vivos + resto original
    resto = [
        f
        for f in os.listdir(WS)
        if os.path.isfile(os.path.join(WS, f)) and f not in VIVOS
    ]
    print(
        "Resto de archivos en raiz (deben ser 0):",
        resto if resto else "0 — raiz limpia",
    )


if __name__ == "__main__":
    main()
