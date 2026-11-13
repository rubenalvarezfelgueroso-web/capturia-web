#!/usr/bin/env python3
"""Genera la landing de Capturia (capturia.es) en los 7 idiomas.

Uso:  python3 build/generar.py
Escribe en ../docs/: index.html (español), en/, fr/, it/, pt/, de/, ar/ y sitemap.xml.
Para cambiar textos, edita build/textos.py y vuelve a ejecutarlo.
"""
from pathlib import Path
from textos import TEXTOS

# ---------------- Configuración ----------------
DOMINIO = "https://capturia.es"
PLAY_URL = "https://play.google.com/store/apps/details?id=com.capturia.app"
# Cuando la app esté publicada en App Store, pega aquí su enlace
# (p. ej. "https://apps.apple.com/es/app/capturia/id1234567890").
# Mientras esté vacío, el botón sale como "Próximamente".
APPSTORE_URL = ""
# Cuando la app esté publicada en Google Play, pon esto a True.
# Mientras sea False, el botón de Google Play sale como "Próximamente".
PLAY_PUBLICADA = False
LEGAL = "https://rubenalvarezfelgueroso-web.github.io/Capturia-Legal/"
EMAIL = "capturiaSpain@gmail.com"
PRECIOS = {"plus_mes": "1,49 €", "plus_anio": "11,99 €", "premium_mes": "1,99 €", "premium_anio": "15,99 €"}
IDIOMAS = ["es", "en", "fr", "it", "pt", "de", "ar"]
# ------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent / "docs"

# Versión del CSS en el enlace (?v=...): cambia sola cada vez que cambia estilo.css, así el
# navegador no se queda con la versión antigua guardada en caché (GitHub Pages la guarda 10 min).
import hashlib
# Saltos de línea normalizados (11/11/2026): así la versión es la misma en Windows (CRLF) y en
# cualquier otro equipo (LF), y solo cambia si cambia de verdad el CSS.
VERSION_CSS = hashlib.md5((RAIZ / "assets" / "estilo.css").read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:8]


def url_idioma(l):
    return "/" if l == "es" else f"/{l}/"


def legal(l, seccion):
    sub = "" if l == "es" else f"{l}/"
    if seccion == "privacidad":
        return f"{LEGAL}{sub}"
    if seccion == "manual":
        return f"{LEGAL}manual/{l}.html"
    return f"{LEGAL}{seccion}/{sub}"


ICONO_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 2.8v18.4c0 .5.5.8 1 .6l15.6-9.2c.4-.3.4-.9 0-1.2L5 2.2c-.5-.2-1 .1-1 .6z"/></svg>'
ICONO_MOVIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 1h10a2 2 0 0 1 2 2v18a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2zm0 3v15h10V4H7zm5 16.2a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/></svg>'


def botones(t):
    if PLAY_PUBLICADA:
        play = (f'<a class="tienda" href="{PLAY_URL}" rel="noopener">{ICONO_PLAY}'
                f'<span><small>{t["btn_play_small"]}</small>Google Play</span></a>')
    else:
        play = (f'<span class="tienda pronto" aria-disabled="true">{ICONO_PLAY}'
                f'<span><small>{t["btn_play_soon"]}</small>Google Play</span></span>')
    if APPSTORE_URL:
        ios = (f'<a class="tienda" href="{APPSTORE_URL}" rel="noopener">{ICONO_MOVIL}'
               f'<span><small>{t["btn_ios_small"]}</small>App Store</span></a>')
    else:
        ios = (f'<span class="tienda pronto" aria-disabled="true">{ICONO_MOVIL}'
               f'<span><small>{t["btn_ios_soon"]}</small>App Store</span></span>')
    return f'<div class="tiendas">{play}{ios}</div>'


def plan(nombre, precio_html, items, destacado=False, etiqueta=""):
    lis = "".join(f"<li>{i}</li>" for i in items)
    cls = "plan destacado" if destacado else "plan"
    eti = f'<span class="etiqueta">{etiqueta}</span>' if etiqueta else ""
    return f'<article class="{cls}">{eti}<h3>{nombre}</h3><p class="precio">{precio_html}</p><ul>{lis}</ul></article>'


GALERIA_ES = [
    "Sabe cuándo van a picar: previsión con mareas, luna y las mejores horas de cada día",
    "Toda tu pesca en una sola app: capturas, sitios, equipo, compañeros y más",
    "Tu diario de pesca: cada captura con su foto, sitio, fecha y peso",
    "Descubre qué te funciona: estadísticas de tus capturas",
    "El clima y el mar de cada captura: viento, oleaje, marea y agua",
    "Dónde se pesca, sin delatar a nadie: mapa anónimo de capturas públicas",
    "Tu catálogo de especies con fotos, capturas y talla mínima",
    "¿Qué cebo funciona mejor? Cebos y señuelos con sus capturas",
]

PECES = {
    "es": ("Lubina", "Calamar", "Dorada"), "en": ("Sea bass", "Squid", "Gilthead bream"),
    "fr": ("Bar", "Calmar", "Dorade royale"), "it": ("Spigola", "Calamaro", "Orata"),
    "pt": ("Robalo", "Lula", "Dourada"), "de": ("Wolfsbarsch", "Kalmar", "Dorade"),
    "ar": ("قاروص", "حبّار", "دنيس"),
}


def pagina(l):
    t = TEXTOS[l]
    p1, p2, p3 = PECES[l]
    galeria = ""
    if l == "es":  # Las imágenes de la tienda están en español
        figs = "".join(
            f'<img src="/assets/galeria/{i:02d}.webp" alt="{a}" width="440" height="956" loading="lazy">'
            for i, a in enumerate(GALERIA_ES, 1))
        puntos = "".join(
            f'<button type="button" aria-label="Imagen {i} de {len(GALERIA_ES)}"></button>'
            for i in range(1, len(GALERIA_ES) + 1))
        galeria = f'''  <section class="galeria" aria-label="Así es Capturia">
    <h2>Así es Capturia</h2>
    <div class="carrusel-marco">
      <button class="flecha anterior" type="button" aria-label="Anterior">‹</button>
      <div class="carrusel" id="carrusel">{figs}</div>
      <button class="flecha siguiente" type="button" aria-label="Siguiente">›</button>
    </div>
    <div class="puntos" id="puntos">{puntos}</div>
  </section>
'''
    rtl = l == "ar"
    alt = "\n".join(
        f'<link rel="alternate" hreflang="{x}" href="{DOMINIO}{url_idioma(x)}">' for x in IDIOMAS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{DOMINIO}/">'
    selector = "".join(
        f'<option value="{url_idioma(x)}" data-l="{x}"{" selected" if x == l else ""}>{TEXTOS[x]["nombre"]}</option>'
        for x in IDIOMAS
    )
    feats = "".join(
        f'<article class="func"><span class="ico" aria-hidden="true">{e}</span><h3>{h}</h3><p>{p}</p></article>'
        for e, h, p in t["features"]
    )
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"])
    mes, anio, o = t["mes"], t["anio"], t["o"]
    planes = (
        plan("Free", f'<strong>{t["gratis"]}</strong>', t["plan_free"])
        + plan("Plus", f'<strong>{PRECIOS["plus_mes"]}</strong>{mes}<br><span>{o} {PRECIOS["plus_anio"]}{anio}</span>', t["plan_plus"])
        + plan("Premium", f'<strong>{PRECIOS["premium_mes"]}</strong>{mes}<br><span>{o} {PRECIOS["premium_anio"]}{anio}</span>',
               t["plan_premium"], destacado=True, etiqueta=t["popular"])
    )
    # En la página en español (raíz) se redirige una sola vez al idioma del navegador,
    # salvo que el visitante ya haya elegido idioma con el selector.
    redir = ""
    if l == "es":
        redir = """<script>
(function(){try{
  if(localStorage.getItem('capturia-idioma'))return;
  var d=['en','fr','it','pt','de','ar'],n=(navigator.language||'es').slice(0,2).toLowerCase();
  if(d.indexOf(n)>-1)location.replace('/'+n+'/');
}catch(e){}})();
</script>"""

    return f"""<!DOCTYPE html>
<html lang="{l}"{' dir="rtl"' if rtl else ''}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t["title"]}</title>
<meta name="description" content="{t["description"]}">
<link rel="canonical" href="{DOMINIO}{url_idioma(l)}">
{alt}
<meta property="og:type" content="website">
<meta property="og:title" content="{t["title"]}">
<meta property="og:description" content="{t["description"]}">
<meta property="og:url" content="{DOMINIO}{url_idioma(l)}">
<meta property="og:image" content="{DOMINIO}/assets/og.png">
<meta name="theme-color" content="#3d2b12">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<link rel="stylesheet" href="/assets/estilo.css?v={VERSION_CSS}">
{redir}
</head>
<body>

<header class="barra">
  <a class="marca" href="{url_idioma(l)}">
    <img src="/assets/logo.png" alt="" width="36" height="36" onerror="this.replaceWith(Object.assign(document.createElement('span'),{{className:'logo-emoji',textContent:'🎣'}}))">
    <span>Capturia</span>
  </a>
  <nav class="menu">
    <a href="#funciones">{t["nav_func"]}</a>
    <a href="#planes">{t["nav_planes"]}</a>
    <a href="#preguntas">{t["nav_faq"]}</a>
  </nav>
  <label class="idioma"><span class="oculto">{t["idioma"]}</span>
    <select id="idioma" aria-label="{t["idioma"]}">{selector}</select>
  </label>
</header>

<section class="hero">
  <div class="hero-in">
    <div class="hero-txt">
      <p class="tag">{t["hero_tag"]}</p>
      <h1>{t["hero_h1"]}</h1>
      <p class="lead">{t["hero_p"]}</p>
      {botones(t)}
      <p class="nota-hero">{t["hero_note"]}</p>
    </div>
    <div class="hero-movil" aria-hidden="true">
      <div class="movil">
        <img src="/assets/captura-app.webp" alt="" onerror="this.remove()">
        <div class="movil-relleno">
          <div class="mv-cab">🎣 Capturia</div>
          <div class="mv-card"><b>🐟 {p1}</b><span>2,350 kg · 58 cm</span><em>🌤 18° · 🌊 1,2 m · 9 s</em></div>
          <div class="mv-card"><b>🦑 {p2}</b><span>0,640 kg</span><em>🌙 · 🌊 0,8 m · 7 s</em></div>
          <div class="mv-card"><b>🐟 {p3}</b><span>1,120 kg · 41 cm</span><em>⛅ 16° · 🌊 1,5 m · 11 s</em></div>
          <div class="mv-nav"><i></i><i></i><i></i><i></i><i></i></div>
        </div>
      </div>
    </div>
  </div>
  <svg class="ola" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 40c120 30 240 45 360 30S600 10 720 20s240 50 360 50 240-30 360-40v60H0z"/></svg>
</section>

<main>
  <section id="funciones" class="seccion">
    <h2>{t["func_h2"]}</h2>
    <p class="sub">{t["func_p"]}</p>
    <div class="rejilla">{feats}</div>
  </section>

{galeria}
  <section class="privacidad">
    <div class="priv-in">
      <span class="ico-grande" aria-hidden="true">🔒</span>
      <div><h2>{t["priv_h2"]}</h2><p>{t["priv_p"]}</p></div>
    </div>
  </section>

  <section id="planes" class="seccion">
    <h2>{t["planes_h2"]}</h2>
    <p class="sub">{t["planes_p"]}</p>
    <div class="planes">{planes}</div>
    <p class="nota-planes">{t["planes_nota"]}</p>
  </section>

  <section id="preguntas" class="seccion estrecha">
    <h2>{t["faq_h2"]}</h2>
    <div class="faq">{faqs}</div>
  </section>

  <section class="cta">
    <h2>{t["cta_h2"]}</h2>
    <p>{t["cta_p"]}</p>
    {botones(t)}
  </section>
</main>

<footer>
  <nav class="legal">
    <a href="{legal(l, 'privacidad')}">{t["f_priv"]}</a>
    <a href="{legal(l, 'terminos')}">{t["f_term"]}</a>
    <a href="{legal(l, 'condiciones')}">{t["f_cond"]}</a>
    <a href="{legal(l, 'eliminar-cuenta')}">{t["f_borrar"]}</a>
    <a href="{legal(l, 'manual')}">{t["f_manual"]}</a>
    <a href="mailto:{EMAIL}">{t["f_contacto"]}</a>
  </nav>
  <p>{t["f_hecho"]}</p>
  <p class="copy">© 2026 Capturia</p>
</footer>

<script>
document.getElementById('idioma').addEventListener('change', function(e){{
  var o=e.target.selectedOptions[0];
  try{{localStorage.setItem('capturia-idioma', o.dataset.l);}}catch(err){{}}
  location.href=e.target.value;
}});
// Galería: puntos y flechas (solo existe en la página en español)
(function(){{
  var c=document.getElementById('carrusel'), p=document.getElementById('puntos');
  if(!c||!p)return;
  var imgs=[].slice.call(c.querySelectorAll('img')), dots=[].slice.call(p.children);
  function ir(i){{ i=Math.max(0,Math.min(imgs.length-1,i)); c.scrollTo({{left: imgs[i].offsetLeft-(c.clientWidth-imgs[i].clientWidth)/2, behavior:'smooth'}}); }}
  function actual(){{
    if(c.scrollLeft<=2)return 0;
    if(c.scrollLeft+c.clientWidth>=c.scrollWidth-2)return imgs.length-1;
    var centro=c.scrollLeft+c.clientWidth/2, mejor=0, d=1e9;
    imgs.forEach(function(im,i){{ var x=Math.abs(im.offsetLeft+im.clientWidth/2-centro); if(x<d){{d=x;mejor=i;}} }});
    return mejor;
  }}
  function pintar(){{
    var a=actual(); dots.forEach(function(b,i){{ b.classList.toggle('activo', i===a); b.setAttribute('aria-current', i===a?'true':'false'); }});
    document.querySelector('.flecha.anterior').disabled = c.scrollLeft<=2;
    document.querySelector('.flecha.siguiente').disabled = c.scrollLeft+c.clientWidth>=c.scrollWidth-2;
  }}
  dots.forEach(function(b,i){{ b.addEventListener('click', function(){{ ir(i); }}); }});
  document.querySelector('.flecha.anterior').addEventListener('click', function(){{ c.scrollBy({{left: -c.clientWidth*0.8, behavior:'smooth'}}); }});
  document.querySelector('.flecha.siguiente').addEventListener('click', function(){{ c.scrollBy({{left: c.clientWidth*0.8, behavior:'smooth'}}); }});
  var t; c.addEventListener('scroll', function(){{ clearTimeout(t); t=setTimeout(pintar,60); }}, {{passive:true}});
  window.addEventListener('resize', pintar); pintar();
}})();
</script>
</body>
</html>
"""


def main():
    for l in IDIOMAS:
        destino = RAIZ / ("index.html" if l == "es" else f"{l}/index.html")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(l), encoding="utf-8")
    urls = "".join(f"<url><loc>{DOMINIO}{url_idioma(l)}</loc></url>" for l in IDIOMAS)
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
        encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    (RAIZ / "CNAME").write_text("capturia.es\n", encoding="utf-8")
    print("Generadas", len(IDIOMAS), "páginas en", RAIZ)


if __name__ == "__main__":
    main()
