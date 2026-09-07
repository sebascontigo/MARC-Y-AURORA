import urllib.request, urllib.parse, os, time

OUT = r"C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA IA\MARC Y AURORA\AURORA\04_Instagram\ASSETS\IA_DRAFTS"
os.makedirs(OUT, exist_ok=True)

# Dirección de arte Soberanía Vital: vitalidad, desintoxicación, alimentación, naturaleza.
# DIFERENCIADA de Marc (que es oscuro/amanecer mental). Aurora = fresco, verde, luz natural, cuerpo.
BASE = ("fresh natural light, clean and airy, space for text overlay, no text, no words, no letters, "
        "wellness detox nutrition vitality aesthetic, professional instagram design background")

JOBS = [
    # --- Fondos carrusel 4:5 ---
    ("carrusel_fondo_01.jpg", (1080,1350),
     "clean bright background, fresh green leaves and soft natural light, gentle negative space at center, " + BASE, 211),
    ("carrusel_fondo_02.jpg", (1080,1350),
     "minimal fresh composition, sliced citrus and green vegetables on light surface, top soft daylight, elegant space for text, " + BASE, 223),

    # --- Posts por pilar 4:5 ---
    ("post_dolor_01.jpg", (1080,1350),
     "muted scene of fatigue, a person holding their head with low energy, soft desaturated tones, gentle light, " + BASE, 231),
    ("post_metodo_01.jpg", (1080,1350),
     "clean composition of colorful whole foods, greens, fruits and seeds arranged neatly, bright natural light, nourishing theme, " + BASE, 247),
    ("post_autoridad_01.jpg", (1080,1350),
     "warm professional atmosphere, soft daylight on a clean wellness workspace with a glass of green juice, calm and trustworthy, " + BASE, 259),
    ("post_oferta_01.jpg", (1080,1350),
     "vibrant sunrise light over fresh natural elements, sense of renewal and energy, silhouette of a woman standing tall, vitality theme, " + BASE, 271),

    # --- Stories por pilar 9:16 ---
    ("story_dolor_01.jpg", (1080,1920),
     "vertical soft muted background, gentle fog with a faint warm light at top, roomy center for text, " + BASE, 283),
    ("story_metodo_01.jpg", (1080,1920),
     "vertical clean bright background, subtle green botanical elements at edges, large space for text, " + BASE, 297),
    ("story_prueba_01.jpg", (1080,1920),
     "vertical warm hopeful background, soft natural bokeh, gentle gradient, space for a testimonial quote, " + BASE, 313),
    ("story_autoridad_01.jpg", (1080,1920),
     "vertical personal warm scene, soft morning light, minimalist kitchen counter with fresh ingredients, authentic feel, " + BASE, 331),
    ("story_oferta_01.jpg", (1080,1920),
     "vertical fresh dawn, natural light breaking through, inspiring, large empty center for announcement text, " + BASE, 349),

    # --- Portada reel 9:16 ---
    ("reel_cover_01.jpg", (1080,1920),
     "vertical cinematic hook cover, a burst of fresh green and warm light at center, bold clean contrast, " + BASE, 367),
]

ok, fail = 0, 0
for name, (w,h), prompt, seed in JOBS:
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
           + f"?width={w}&height={h}&nologo=true&seed={seed}")
    path = os.path.join(OUT, name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(path,"wb") as f:
            f.write(r.read())
        print(f"OK  {name}  {os.path.getsize(path)} bytes")
        ok += 1
    except Exception as e:
        print(f"FALLO {name}: {str(e)[:120]}")
        fail += 1
    time.sleep(1)

print(f"\nTotal: {ok} generadas, {fail} fallidas -> {OUT}")
