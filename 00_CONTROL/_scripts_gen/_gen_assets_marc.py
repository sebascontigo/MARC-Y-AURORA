import urllib.request, urllib.parse, os, time

OUT = r"C:\03_PROYECTOS\01_GRUPO_BAYONA\EMPRESA IA\MARC Y AURORA\MARC\04_Instagram\ASSETS\IA_DRAFTS"
os.makedirs(OUT, exist_ok=True)

# Estilo base coherente con la marca Despierta: oscuro, amanecer, despertar mental
BASE = ("cinematic, high contrast, space for text overlay, no text, no words, no letters, "
        "wellness mental transformation aesthetic, professional instagram design background")

# (nombre, dimensiones, prompt, seed)
JOBS = [
    # --- Carrusel "7 cosas que tu mente hace contra ti" (fondos reutilizables 4:5) ---
    ("carrusel_fondo_01.jpg", (1080,1350),
     "minimalist dark moody background, a single warm dawn light beam breaking through deep darkness, subtle fog, " + BASE, 11),
    ("carrusel_fondo_02.jpg", (1080,1350),
     "abstract dark background, soft golden light rays piercing through shadow, depth, elegant negative space at center, " + BASE, 23),

    # --- Posts por pilar (4:5) ---
    ("post_dolor_01.jpg", (1080,1350),
     "dark introspective scene, a person silhouette with swirling chaotic thought lines around the head, muted blue-grey tones, " + BASE, 31),
    ("post_metodo_01.jpg", (1080,1350),
     "clean structured abstract composition, a glowing human brain made of soft light threads, dark background, warm amber accents, " + BASE, 47),
    ("post_autoridad_01.jpg", (1080,1350),
     "warm authentic atmosphere, soft window light on an empty wooden chair facing a sunrise, calm and personal, " + BASE, 59),
    ("post_oferta_01.jpg", (1080,1350),
     "dramatic sunrise over a calm sea, first light breaking the horizon, silhouette of a person standing tall, awakening theme, " + BASE, 71),

    # --- Stories por pilar (9:16) ---
    ("story_dolor_01.jpg", (1080,1920),
     "vertical dark moody background, anxious fog with a faint warm light at the top, roomy center for text, " + BASE, 83),
    ("story_metodo_01.jpg", (1080,1920),
     "vertical clean dark background, subtle geometric neural network lines glowing softly, space for text, " + BASE, 97),
    ("story_prueba_01.jpg", (1080,1920),
     "vertical warm hopeful background, soft golden bokeh lights, gentle gradient, space for a testimonial quote, " + BASE, 113),
    ("story_autoridad_01.jpg", (1080,1920),
     "vertical personal warm scene, soft morning light, minimalist desk with a notebook, authentic behind-the-scenes feel, " + BASE, 131),
    ("story_oferta_01.jpg", (1080,1920),
     "vertical dramatic dawn, light breaking through darkness from above, inspiring, large empty center for announcement text, " + BASE, 149),

    # --- Portada de reel (9:16) ---
    ("reel_cover_01.jpg", (1080,1920),
     "vertical cinematic hook cover, a single bright light bursting through darkness at center, bold dramatic contrast, " + BASE, 167),
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
        sz = os.path.getsize(path)
        print(f"OK  {name}  {sz} bytes")
        ok += 1
    except Exception as e:
        print(f"FALLO {name}: {str(e)[:120]}")
        fail += 1
    time.sleep(1)

print(f"\nTotal: {ok} generadas, {fail} fallidas -> {OUT}")
