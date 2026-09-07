# -*- coding: utf-8 -*-
"""Genera portadas de HISTORIAS DESTACADAS (IG) para MARC y AURORA. 1080x1080."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W = H = 1080

def font(size, bold=True):
    path = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
    return ImageFont.truetype(path, size)

def cover_round_text(draw, cx, cy, text, f, fill, w):
    draw.ellipse([cx - w // 2, cy - w // 2, cx + w // 2, cy + w // 2], outline=fill, width=8)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), text, font=f, fill=fill)

def make(path, bg_top, bg_bot, accent, title, sub, seed):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = tuple(int(bg_top[i] + (bg_bot[i] - bg_top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    # círculo decorativo
    d.ellipse([W // 2 - 380, H // 2 - 380, W // 2 + 380, H // 2 + 380], outline=accent, width=6)
    d.ellipse([W // 2 - 250, H // 2 - 250, W // 2 + 250, H // 2 + 250], outline=accent, width=4)
    # monograma
    cover_round_text(d, W // 2, H // 2 - 130, "D", font(150), accent, 240)
    cover_round_text(d, W // 2, H // 2 + 110, "S", font(150), accent, 240)
    # línea
    d.line([(W // 2 - 200, H // 2 + 235), (W // 2 + 200, H // 2 + 235)], fill=accent, width=4)
    # título
    f_t = font(96)
    bbox = d.textbbox((0, 0), title, font=f_t)
    d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], 570), title, font=f_t, fill=(255, 255, 255) if seed == "marc" else (34, 48, 31))
    # sub
    f_s = font(44, bold=False)
    bbox2 = d.textbbox((0, 0), sub, font=f_s)
    d.text(((W - (bbox2[2] - bbox2[0])) / 2 - bbox2[0], 720), sub, font=f_s, fill=(164, 156, 141) if seed == "marc" else (93, 107, 87))
    img.save(path, "PNG")
    print("GENERATED", path.name)

# MARC: oscuro + ámbar
marc_dark = (20, 20, 24)
marc_accent = (232, 165, 75)
out_marc = Path(r"MARC\04_Instagram\ASSETS\HIGHLIGHT_COVERS")
out_marc.mkdir(parents=True, exist_ok=True)
for name, title, sub in [
    ("INICIO", "DESPIERTA", "Tu proceso en 4 meses"),
    ("METODO", "EL MÉTODO", "VER · DESMONTAR · REPROGRAMAR · DOMINAR"),
    ("PROGRAMA", "13 MÓDULOS", "El mapa completo del programa"),
    ("TESTIMONIOS", "TESTIMONIOS", "ANA · ELENA · GABI · VICENT"),
    ("PODCAST", "PODCAST", "Reconecta-t con Marc Souza"),
    ("CONTACTO", "HABLEMOS", "Plazas septiembre abiertas"),
]:
    make(out_marc / (name + ".png"), marc_dark, (34, 28, 18), marc_accent, title, sub, "marc")

# AURORA: claro + verde
aur_bg = (247, 245, 239)
aur_accent = (62, 107, 58)
out_aur = Path(r"AURORA\04_Instagram\ASSETS\HIGHLIGHT_COVERS")
out_aur.mkdir(parents=True, exist_ok=True)
for name, title, sub in [
    ("INICIO", "SOBERANÍA VITAL", "Recupera tu energía"),
    ("METODO", "EL MÉTODO", "Desintoxicación · Alimentación · Acompañamiento"),
    ("CONTACTO", "HABLEMOS", "Plazas septiembre abiertas"),
]:
    make(out_aur / (name + ".png"), aur_bg, (238, 240, 228), aur_accent, title, sub, "aurora")