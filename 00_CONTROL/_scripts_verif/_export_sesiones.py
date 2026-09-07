#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exporta el historial COMPLETO de sesiones de OpenCode a Markdown legible.

- Lee la base local en modo SOLO LECTURA (mode=ro): no altera ninguna sesión.
- Redacta credenciales (keys, tokens, cookies, JWT) antes de escribir a disco.
- Omite imágenes base64 y razonamiento interno del modelo.
- Salida: 00_CONTROL/HISTORIAL_SESIONES/ (1 índice + 1 archivo por sesión).

Uso:  python 00_CONTROL/_export_sesiones.py
"""

import datetime
import json
import os
import re
import sqlite3
import sys
import unicodedata

DB = os.path.expanduser("~/.local/share/opencode/opencode.db").replace("\\", "/")
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "HISTORIAL_SESIONES")

MAX_TEXT = 14000  # tope por bloque de texto de usuario/agente
MAX_TOOL_OUT = 500  # tope de salida por herramienta
MAX_TOOL_IN = 300  # tope de parámetros por herramienta

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

# --- Redacción de secretos (el VALOR nunca se escribe; el nombre sí) ---------
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"ntn_[A-Za-z0-9]{16,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{16,}"),
    re.compile(r"xai-[A-Za-z0-9]{16,}"),
    re.compile(r"nvapi-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"AIza[0-9A-Za-z_\-]{25,}"),
    re.compile(r"eyJ[A-Za-z0-9_\-]{15,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{20,}"),
    re.compile(r"(?i)\b(csrftoken|sessionid|ds_user_id|ig_did|mid)=[^\s;\"']{8,}"),
    re.compile(r"data:image/[a-z]+;base64,[A-Za-z0-9+/=]{40,}"),
]
KV_SECRET = re.compile(
    r"(?i)\b([A-Za-z0-9_\-]*(?:api[_-]?key|apikey|access[_-]?token|refresh[_-]?token"
    r"|secret|password|passwd|contrasena|token|authorization)[A-Za-z0-9_\-]*)"
    r"(\s*[:=]\s*)(\"|')?([^\s,\"'}]{8,})"
)


def redact(text: str) -> str:
    if not text:
        return ""
    out = ANSI.sub("", text)
    for pat in SECRET_PATTERNS:
        out = pat.sub("[REDACTADO]", out)
    out = KV_SECRET.sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTADO]", out)
    return out


def clip(text: str, limit: int) -> str:
    if text is None:
        return ""
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n… [recortado, {len(text) - limit} caracteres más]"


def ts(value, fmt="%Y-%m-%d %H:%M"):
    if not value:
        return "-"
    value = int(value)
    if value > 10**12:
        value //= 1000
    return datetime.datetime.fromtimestamp(value).strftime(fmt)


def slugify(text: str, limit=48) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return text[:limit] or "sin-titulo"


def model_of(raw):
    if not raw:
        return "-"
    try:
        data = json.loads(raw)
        mid = data.get("id") or data.get("modelID") or "-"
        pid = data.get("providerID") or ""
        return f"{pid}/{mid}" if pid else mid
    except Exception:
        return str(raw)[:40]


def short_dir(path: str) -> str:
    if not path:
        return "-"
    path = path.replace("\\", "/")
    return path.replace("C:/SEVISIONARI/04 Proyectos/01 Grupo Bayona/", "…/")


def main():
    if not os.path.exists(DB):
        sys.exit(f"No encuentro la base: {DB}")
    os.makedirs(OUT, exist_ok=True)
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row

    projects = {
        r["id"]: r["worktree"] for r in con.execute("select id, worktree from project")
    }
    sessions = list(
        con.execute(
            "select id, project_id, parent_id, slug, directory, title, agent, model, cost,"
            " tokens_input, tokens_output, time_created, time_updated, time_archived"
            " from session order by time_updated desc"
        )
    )

    rows = []
    total_bytes = 0
    for pos, s in enumerate(sessions, 1):
        msgs = list(
            con.execute(
                "select id, time_created, data from message where session_id=?"
                " order by time_created, id",
                (s["id"],),
            )
        )
        parts_by_msg = {}
        for p in con.execute(
            "select message_id, data from part where session_id=? order by time_created, id",
            (s["id"],),
        ):
            parts_by_msg.setdefault(p["message_id"], []).append(p["data"])

        lines = []
        n_user = n_asst = n_tool = 0
        first_user = ""
        for m in msgs:
            try:
                md = json.loads(m["data"])
            except Exception:
                md = {}
            role = md.get("role", "?")
            body = []
            for raw in parts_by_msg.get(m["id"], []):
                try:
                    pd = json.loads(raw)
                except Exception:
                    continue
                ptype = pd.get("type")
                if ptype == "text":
                    txt = clip(redact(pd.get("text", "")), MAX_TEXT)
                    if txt:
                        body.append(txt)
                elif ptype == "tool":
                    n_tool += 1
                    tool = pd.get("tool", "?")
                    st = pd.get("state") or {}
                    inp = clip(
                        redact(json.dumps(st.get("input", {}), ensure_ascii=False)),
                        MAX_TOOL_IN,
                    )
                    outp = clip(redact(str(st.get("output", ""))), MAX_TOOL_OUT)
                    block = f"`[{tool}]` {inp}"
                    if outp:
                        block += f"\n```\n{outp}\n```"
                    body.append(block)
                elif ptype == "file":
                    body.append(
                        f"_[archivo adjunto: {pd.get('filename', '?')} ({pd.get('mime', '?')}) — contenido omitido]_"
                    )
                elif ptype == "patch":
                    files = ", ".join(short_dir(f) for f in (pd.get("files") or []))
                    body.append(f"_[parche aplicado: {files}]_")
                elif ptype == "compaction":
                    body.append("_[compactación automática de contexto]_")
                elif ptype == "agent":
                    body.append(f"_[subagente: {pd.get('name', '?')}]_")
            if not body:
                continue
            if role == "user":
                n_user += 1
                if not first_user:
                    first_user = " ".join(body[0].split())[:160]
                lines.append(f"### Usuario · {ts(m['time_created'], '%d-%m %H:%M')}\n")
            else:
                n_asst += 1
                lines.append(
                    f"### Agente ({md.get('modelID', '-')}) · {ts(m['time_created'], '%d-%m %H:%M')}\n"
                )
            lines.append("\n\n".join(body) + "\n")

        title = (s["title"] or "").strip() or first_user or s["slug"] or "sin título"
        if title.startswith("New session"):
            title = first_user or title
        fname = (
            f"{ts(s['time_updated'], '%Y-%m-%d')}_{slugify(title)}_{s['id'][-6:]}.md"
        )

        header = [
            f"# {title}",
            "",
            f"- **id:** `{s['id']}` · **slug:** {s['slug'] or '-'}",
            f"- **carpeta:** `{short_dir(s['directory'])}`",
            f"- **proyecto:** `{short_dir(projects.get(s['project_id'], s['project_id'] or '-'))}`",
            f"- **agente:** {s['agent'] or '-'} · **modelo:** {model_of(s['model'])}",
            f"- **creada:** {ts(s['time_created'])} · **último mensaje:** {ts(s['time_updated'])}",
            f"- **mensajes:** {n_user} de Sebastián / {n_asst} del agente · **herramientas usadas:** {n_tool}",
            f"- **tokens:** entrada {s['tokens_input'] or 0} · salida {s['tokens_output'] or 0} · **coste:** {s['cost'] or 0}",
            "",
            "> Exportado en modo solo lectura. Credenciales redactadas. Razonamiento interno e imágenes omitidos.",
            "",
            "---",
            "",
        ]
        content = "\n".join(header) + "\n".join(lines)
        path = os.path.join(OUT, fname)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        total_bytes += len(content.encode("utf-8"))

        rows.append(
            {
                "n": pos,
                "title": title,
                "file": fname,
                "dir": short_dir(s["directory"]),
                "created": ts(s["time_created"]),
                "updated": ts(s["time_updated"]),
                "user": n_user,
                "asst": n_asst,
                "tool": n_tool,
                "model": model_of(s["model"]),
                "agent": s["agent"] or "-",
                "archived": bool(s["time_archived"]),
                "id": s["id"],
            }
        )

    # --- índice --------------------------------------------------------------
    now = datetime.datetime.now()
    cut3 = now - datetime.timedelta(days=3)

    per_day = {}
    per_model = {}
    for r in rows:
        per_day[r["updated"][:10]] = per_day.get(r["updated"][:10], 0) + 1
        per_model[r["model"]] = per_model.get(r["model"], 0) + 1
    top_models = sorted(per_model.items(), key=lambda kv: -kv[1])[:8]
    days_sorted = sorted(per_day.items(), reverse=True)[:10]

    idx = [
        "# HISTORIAL DE SESIONES — OpenCode (todas)",
        "",
        f"> Generado: {now.strftime('%Y-%m-%d %H:%M')} · Fuente: base local de OpenCode leída en SOLO LECTURA.",
        f"> Total sesiones: **{len(rows)}** · un archivo .md por sesión en esta carpeta · tamaño: {total_bytes / 1048576:.1f} MB.",
        "> Credenciales redactadas automáticamente. Sesiones de Zed migradas aparte en `../SESIONES_ZED/`.",
        f"> Regenerar cuando quieras: `python 00_CONTROL/{os.path.basename(__file__)}`",
        "",
        "## Resumen",
        "",
        "| Actividad por día (últimos 10) | Sesiones |   | Modelo más usado | Sesiones |",
        "|---|---|---|---|---|",
    ]
    for i in range(max(len(days_sorted), len(top_models))):
        d = (
            f"{days_sorted[i][0]} | {days_sorted[i][1]}"
            if i < len(days_sorted)
            else " | "
        )
        m = f"{top_models[i][0]} | {top_models[i][1]}" if i < len(top_models) else " | "
        idx.append(f"| {d} |  | {m} |")
    idx += [
        "",
        "## Últimos 3 días",
        "",
        "| Nº | Título | Último mensaje | Carpeta | Mensajes | Archivo |",
        "|---|---|---|---|---|---|",
    ]
    recent = [
        r
        for r in rows
        if r["updated"] != "-"
        and datetime.datetime.strptime(r["updated"], "%Y-%m-%d %H:%M") >= cut3
    ]
    for i, r in enumerate(recent, 1):
        idx.append(
            f"| {i} | {r['title'][:60]} | {r['updated']} | {r['dir'][-40:]} | "
            f"{r['user']}/{r['asst']} | [{r['file']}]({r['file']}) |"
        )
    idx += [
        "",
        f"## Todas las sesiones ({len(rows)})",
        "",
        "| Nº | Último mensaje | Título | Carpeta | Msj (tú/agente) | Modelo | Archivo |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        idx.append(
            f"| {r['n']} | {r['updated']} | {r['title'][:60]} | {r['dir'][-38:]} | "
            f"{r['user']}/{r['asst']} | {r['model'][-28:]} | [{r['file']}]({r['file']}) |"
        )

    with open(
        os.path.join(OUT, "00_INDICE_SESIONES.md"), "w", encoding="utf-8", newline="\n"
    ) as fh:
        fh.write("\n".join(idx) + "\n")

    con.close()
    print(
        f"OK sesiones={len(rows)} recientes={len(recent)} MB={total_bytes / 1048576:.1f} dir={OUT}"
    )


if __name__ == "__main__":
    main()
