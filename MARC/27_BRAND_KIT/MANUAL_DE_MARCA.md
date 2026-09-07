# 🎨 MANUAL DE MARCA — DESPIERTA (Marc Souza)
> Brand Kit v1 · 31/8/2026 · Creado por el agente. Todo verificado en archivos reales.
> Ubicación: `MARC/27_BRAND_KIT/`

## 1. CONCEPTO
**El amanecer mental.** Despertar = pasar de la oscuridad del piloto automático a la luz de dirigir tu propia mente. Todo el kit gira en un único símbolo: **el sol asomando sobre el horizonte** — no un sol completo (eso sería "ya llegaste"), sino **en el momento de salir** (estás despertando, en proceso).

## 2. LOGO
| Archivo | Uso |
|---|---|
| `logo_dark_512/192.png` | Fondo oscuro: perfil IG, cabeceras, app |
| `logo_light_512/192.png` | Fondo claro: documentos impresos, e-book |
| `favicon.png` | Web |
| Significado | Semicírculo ámbar asomando sobre línea de horizonte con 5 rayos de luz |

**Reglas:** margen de seguridad = 25% del ancho del logo alrededor. Nunca deformar, nunca sobre fondos con patrón cargado. El wordmark es tipográfico: **D E S P I E R T A** espaciado (ver §4).

## 3. PALETA (la misma de landing + app + reels — ya coherente)
| Color | HEX | Uso |
|---|---|---|
| **Negro noche** | `#0e0e11` | Fondo principal |
| **Gris profundo** | `#1e1e26` | Tarjetas, bloques |
| **Ámbar despertar** | `#e8a54b` | Acento: CTAs, números, subrayados, sol |
| **Ámbar profundo** | `#b97a2c` | Hover, sombras del acento |
| **Crema** | `#ece7dd` | Texto principal sobre oscuro |
| **Gris cálido** | `#a49c8d` | Texto secundario |

**Regla 70/20/10:** 70% negro/gris, 20% crema, 10% ámbar. El ámbar ES el despertar — si se gasta en todo, deja de señalar.

## 4. TIPOGRAFÍA
| Papel | Fuente | Uso |
|---|---|---|
| Titulares | **Georgia / serif** (bold) | Hooks, frases, títulos de slide |
| Cuerpo | **Segoe UI / system sans** | Párrafos, captions, app |
| Wordmark | Georgia bold, tracking amplio: `D E S P I E R T A` | Marca en imágenes |

Justificación: serif = autoridad de +10 años; sans = cercanía práctica. Evita Inter/Roboto como identidad (comodidad, no marca).

## 5. VOZ Y TONO
- **Directo, sin humo.** Frases cortas. Una idea por frase.
- Segunda persona: "tu mente", "tus miedos" — nunca "la gente".
- Valida primero, enseña después: "No es debilidad. Es un programa."
- Prohibido: promesas médicas, "cura", "garantizado", jerga esotérica sin traducir.
- Cierre de todo contenido: CTA a "DESPIERTA" por WhatsApp.

## 6. PLANTILLAS (en `PLANTILLAS/`, todas 1080px verificadas)
| Plantilla | Formato | Contenido fijo |
|---|---|---|
| `POST_1_portada_ejemplo.jpg` | 1080×1350 (4:5) | Marca arriba + título serif + subtítulo + CTA + barra ámbar |
| `CARRUSEL_1_portada_ejemplo.jpg` | 1080×1350 | Igual, título más corto (slides internos = fondo limpio + 1 idea) |
| `STORY_1_ejemplo.jpg` | 1080×1920 (9:16) | Marca arriba-centro, título al 40% superior, sub, safe-area inferior |
| `QUOTE_1_ejemplo.jpg` | 1080×1080 (1:1) | Solo frase centrada + wordmark abajo |

**Patrón de composición (SIEMPRE):** título en la mitad superior (el feed de IG solo muestra la superior en el grid), CTA antes del último 15% inferior, nada de texto pegado a bordes.

## 7. APLICACIONES YA EN LÍNEA (coherencia verificada)
- Landing despierta-marc.netlify.app → misma paleta/tipos ✅
- App despierta-app.netlify.app (incl. CALMA y watch) ✅
- Reels de testimonios + historias diarias del protocolo clon → misma estética ✅

## 8. QUÉ FALTA (requiere humano)
1. **Foto de perfil de Marc** (una marca de mentor sin cara no engancha — móvil, buena luz, 15 min).
2. Aprobar el logo (si Marc tiene símbolo propio/parecido, se integra en v2).
3. Versión EN del kit (solo si el mercado lo pide).

## 9. CLONACIÓN / USO
Aurora = espejo con verde (`AURORA/` paleta propia en su landing). Cualquier pieza nueva (posts, reels, stories) parte de estas plantillas o del script `_gen_historia_diaria.py` — nunca de cero.
