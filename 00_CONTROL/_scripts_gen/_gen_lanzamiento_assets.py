# -*- coding: utf-8 -*-
# Piezas visuales de LANZAMIENTO (31/8) — MARC (oscuro/ámbar) + AURORA (claro/verde)
# Salidas: post 1080x1080 + story 1080x1920 para cada cliente
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r"C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA TECNOLOGÍA\CLIENTES\MARC Y AURORA"
OUT_MARC = os.path.join(ROOT, "MARC", "04_Instagram", "ASSETS", "LANZAMIENTO")
OUT_AUR = os.path.join(ROOT, "AURORA", "04_Instagram", "ASSETS", "LANZAMIENTO")
os.makedirs(OUT_MARC, exist_ok=True)
os.makedirs(OUT_AUR, exist_ok=True)

F_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
F_BLACK = r"C:\Windows\Fonts\ariblk.ttf"
F_REG = r"C:\Windows\Fonts\arial.ttf"

def font(path, size):
    return ImageFont.truetype(path if os.path.exists(path) else r"C:\Windows\Fonts\arialbd.ttf", size)

def vgrad(size, top, bottom):
    w, h = size
    img = Image.new("RGB", (1, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        d.point((0, y), fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img.resize((w, h))

def glow_center(img, color, radius=1.15, alpha=70):
    w, h = img.size
    ov = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(ov)
    d.ellipse([w/2 - w*radius/2, h/2 - h*radius/2, w/2 + w*radius/2, h/2 + h*radius/2], fill=alpha)
    ov = ov.filter(ImageFilter.GaussianBlur(120))
    layer = Image.new("RGB", (w, h), color)
    img.paste(layer, (0, 0), ov)
    return img

def draw_center(d, img_w, y, text, f, fill, tracking=0):
    if tracking:
        widths = [d.textlength(c, font=f) for c in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (img_w - total) / 2
        for c, cw in zip(text, widths):
            d.text((x, y), c, font=f, fill=fill)
            x += cw + tracking
    else:
        tw = d.textlength(text, font=f)
        d.text(((img_w - tw) / 2, y), text, font=f, fill=fill)

def gen_marc(w, h, out):
    img = vgrad((w, h), (16, 14, 11), (34, 24, 12))
    img = glow_center(img, (255, 122, 26), alpha=60)
    d = ImageDraw.Draw(img)
    gold = (255, 138, 40)
    white = (242, 238, 230)
    # marco
    m = int(w * 0.045)
    d.rounded_rectangle([m, m, w - m, h - m], radius=int(w * 0.05), outline=(255, 122, 26, 120), width=3)
    scale = w / 1080.0
    draw_center(d, w, int(h * 0.10), "D E S P I E R T A", font(F_BLACK, int(72 * scale)), gold)
    draw_center(d, w, int(h * 0.185), "MARC SOUZA", font(F_BOLD, int(34 * scale)), white)
    d.line([w*0.25, int(h*0.25), w*0.75, int(h*0.25)], fill=gold, width=3)
    draw_center(d, w, int(h * 0.30), "PLAZAS", font(F_BLACK, int(110 * scale)), white)
    draw_center(d, w, int(h * 0.40), "SEPTIEMBRE", font(F_BLACK, int(110 * scale)), gold)
    draw_center(d, w, int(h * 0.53), "13 módulos · 4 meses · grupo reducido", font(F_REG, int(34 * scale)), (200, 195, 185))
    fases = ["VER", "DESMONTAR", "REPROGRAMAR", "DOMINAR"]
    fx = w * 0.5 - (len(fases) - 1) * w * 0.115
    for i, fa in enumerate(fases):
        bx = fx + i * w * 0.23
        bw = w * 0.20
        d.rounded_rectangle([bx, int(h*0.60), bx + bw, int(h*0.60) + int(56*scale)], radius=14, outline=gold, width=2)
        tw = d.textlength(fa, font=font(F_BOLD, int(24 * scale)))
        d.text((bx + (bw - tw) / 2, int(h*0.60) + int(14*scale)), fa, font=font(F_BOLD, int(24 * scale)), fill=white)
        if i < len(fases) - 1:
            d.text((bx + bw + w*0.012, int(h*0.60) + int(14*scale)), "→", font=font(F_BOLD, int(24*scale)), fill=gold)
    draw_center(d, w, int(h * 0.74), "Escríbeme «DESPIERTA»", font(F_BOLD, int(44 * scale)), white)
    draw_center(d, w, int(h * 0.785), "por WhatsApp y te regalo el e-book", font(F_REG, int(30 * scale)), (200, 195, 185))
    draw_center(d, w, h - int(90 * scale) - int(h * 0.045), "despierta-marc.netlify.app", font(F_BOLD, int(30 * scale)), gold)
    img.save(out, quality=92)
    print("OK", out)

def gen_aurora(w, h, out):
    img = vgrad((w, h), (244, 248, 242), (222, 235, 222))
    d = ImageDraw.Draw(img)
    deep = (46, 93, 63)
    soft = (110, 140, 115)
    m = int(w * 0.045)
    d.rounded_rectangle([m, m, w - m, h - m], radius=int(w * 0.05), outline=deep, width=3)
    scale = w / 1080.0
    draw_center(d, w, int(h * 0.12), "S O B E R A N Í A   V I T A L", font(F_BOLD, int(56 * scale)), deep)
    draw_center(d, w, int(h * 0.19), "AURORA VELAV", font(F_REG, int(30 * scale)), soft)
    d.line([w*0.25, int(h*0.245), w*0.75, int(h*0.245)], fill=deep, width=3)
    draw_center(d, w, int(h * 0.30), "TU CUERPO,", font(F_BLACK, int(78 * scale)), deep)
    draw_center(d, w, int(h * 0.375), "TU TERRITORIO", font(F_BLACK, int(78 * scale)), deep)
    draw_center(d, w, int(h * 0.50), "Transformación física y emocional", font(F_REG, int(34 * scale)), soft)
    draw_center(d, w, int(h * 0.55), "Higienismo · hábitos · energía", font(F_REG, int(34 * scale)), soft)
    d.rounded_rectangle([w*0.22, int(h*0.63), w*0.78, int(h*0.63) + int(110*scale)], radius=18, outline=deep, width=3)
    draw_center(d, w, int(h * 0.63) + int(18*scale), "SOBERANÍA VITAL · 997€", font(F_BOLD, int(40 * scale)), deep)
    draw_center(d, w, int(h * 0.63) + int(66*scale), "3 meses de acompañamiento", font(F_REG, int(26 * scale)), soft)
    draw_center(d, w, int(h * 0.78), "Consultas individuales · 75€/sesión", font(F_BOLD, int(32 * scale)), deep)
    draw_center(d, w, h - int(80 * scale) - int(h * 0.045), "Escríbeme por Instagram → @auroravelav", font(F_BOLD, int(30 * scale)), deep)
    img.save(out, quality=92)
    print("OK", out)

gen_marc(1080, 1080, os.path.join(OUT_MARC, "POST_PLAZAS_SEPTIEMBRE_1080.jpg"))
gen_marc(1080, 1920, os.path.join(OUT_MARC, "STORY_PLAZAS_SEPTIEMBRE_1080x1920.jpg"))
gen_aurora(1080, 1080, os.path.join(OUT_AUR, "POST_SOBERANIA_VITAL_1080.jpg"))
gen_aurora(1080, 1920, os.path.join(OUT_AUR, "STORY_SOBERANIA_VITAL_1080x1920.jpg"))
print("DONE")