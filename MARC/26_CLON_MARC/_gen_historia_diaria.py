# -*- coding: utf-8 -*-
# FASE 0 del clon: historia diaria 9:16 con plantilla de marca (0€, sin avatar)
# Uso:
#   python _gen_historia_diaria.py --hook "TU HOOK" --texto "Texto de oferta" --cta "Escríbeme DESPIERTA" [--cliente aurora]
import argparse, os, datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
F_BLACK = r"C:\Windows\Fonts\ariblk.ttf"
F_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
F_REG = r"C:\Windows\Fonts\arial.ttf"

THEMES = {
    "marc": dict(top=(16,14,11), bottom=(34,24,12), glow=(255,122,26), accent=(255,138,40),
                 ink=(242,238,230), dim=(200,195,185), brand="D E S P I E R T A", author="MARC SOUZA",
                 handle="@marcsouza.7", outdir=os.path.join(HERE, "HISTORIAS")),
    "aurora": dict(top=(244,248,242), bottom=(222,235,222), glow=(46,93,63), accent=(46,93,63),
                   ink=(46,93,63), dim=(110,140,115), brand="S O B E R A N Í A   V I T A L", author="AURORA VELAV",
                   handle="@auroravelav", outdir=os.path.join(HERE, "..", "HISTORIAS")),
}

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook", required=True)
    ap.add_argument("--texto", default="")
    ap.add_argument("--cta", default="Escríbeme «DESPIERTA» por WhatsApp")
    ap.add_argument("--cliente", choices=["marc","aurora"], default="marc")
    ap.add_argument("--fecha", default=None, help="YYYY-MM-DD para planificar dias futuros")
    a = ap.parse_args()
    T = THEMES[a.cliente]
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H))
    d0 = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d0.line([(0, y), (W, y)], fill=tuple(int(T["top"][i] + (T["bottom"][i] - T["top"][i]) * t) for i in range(3)))
    ov = Image.new("L", (W, H), 0); dd = ImageDraw.Draw(ov)
    dd.ellipse([W*0.5-540, H*0.5-540, W*0.5+540, H*0.5+540], fill=55)
    img.paste(Image.new("RGB", (W, H), T["glow"]), (0, 0), ov.filter(ImageFilter.GaussianBlur(140)))
    d = ImageDraw.Draw(img)
    f_hook = ImageFont.truetype(F_BLACK, 88)
    f_txt = ImageFont.truetype(F_REG, 44)
    f_cta = ImageFont.truetype(F_BOLD, 46)
    f_small = ImageFont.truetype(F_BOLD, 30)
    d.text(((W - d.textlength(T["brand"], font=f_small)) / 2, 150), T["brand"], font=f_small, fill=T["accent"])
    d.text(((W - d.textlength(T["author"], font=ImageFont.truetype(F_BOLD, 26))) / 2, 200), T["author"], font=ImageFont.truetype(F_BOLD, 26), fill=T["dim"])
    # hook (centrado, envuelto)
    hl = wrap(d, a.hook.upper(), f_hook, W - 160)
    y = H * 0.28
    for ln in hl:
        d.text(((W - d.textlength(ln, font=f_hook)) / 2, y), ln, font=f_hook, fill=T["ink"])
        y += 100
    # texto medio
    if a.texto:
        d.line([W*0.3, y + 40, W*0.7, y + 40], fill=T["accent"], width=3)
        y += 90
        for ln in wrap(d, a.texto, f_txt, W - 220):
            d.text(((W - d.textlength(ln, font=f_txt)) / 2, y), ln, font=f_txt, fill=T["dim"])
            y += 58
    # CTA caja
    box_h = 120
    bx0, bx1 = W*0.10, W*0.90
    by0 = H - 380
    d.rounded_rectangle([bx0, by0, bx1, by0 + box_h], radius=24, outline=T["accent"], width=4)
    cl = wrap(d, a.cta, f_cta, (bx1 - bx0) - 80)
    cy = by0 + (box_h - len(cl)*54) / 2 + 8
    for ln in cl:
        d.text(((W - d.textlength(ln, font=f_cta)) / 2, cy), ln, font=f_cta, fill=T["ink"])
        cy += 54
    d.text(((W - d.textlength(T["handle"], font=f_small)) / 2, H - 170), T["handle"], font=f_small, fill=T["accent"])
    day = (ap.fecha if ap.fecha else datetime.date.today().isoformat()) if False else (a.fecha if hasattr(a, "fecha") else None) or datetime.date.today().isoformat()
    out = os.path.join(T["outdir"], day)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, f"HISTORIA_9x16_{a.cliente}.jpg")
    img.save(path, quality=92)
    print("OK", path)
    # caption sugerido
    with open(os.path.join(out, f"CAPTION_{a.cliente}.txt"), "w", encoding="utf-8") as f:
        f.write(a.hook + "\n\n" + (a.texto + "\n\n" if a.texto else "") + a.cta + "\n\n#" + ("despierta #marcsouza #mente #transformacion" if a.cliente=="marc" else "soberaniavital #auroravelav #habitos #salud"))

if __name__ == "__main__":
    main()