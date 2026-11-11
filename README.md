# Capturia · web (capturia.es)

Landing de Capturia en 7 idiomas (es, en, fr, it, pt, de, ar), estática, lista para GitHub Pages.

## Estructura
- `docs/` → lo que se publica con GitHub Pages (index.html = español; en/, fr/, it/, pt/, de/, ar/; CNAME; sitemap.xml; robots.txt).
- `docs/assets/` → estilo.css y las imágenes:
  - `logo.png`, `favicon.png`, `apple-touch-icon.png`: icono de la app (sacado de play-store/icono_512.png).
  - `captura-app.webp`: pantalla "Tus capturas" del móvil de la portada (recorte de app-store/capturas-es/03).
  - `og.png` (1200×630): imagen al compartir el enlace (a partir de grafico_funciones_1024x500.png).
  - `galeria/01-08.webp`: las 8 capturas de App Store; solo se muestran en la página en español.
- `build/` → generador. Los textos están en `build/textos.py`, y los precios y enlaces, arriba de `build/generar.py`.
  Tras cambiar algo: `python build/generar.py` (regenera `docs/`), commit y push.

## App Store
Cuando la app esté publicada en iOS, pega el enlace en `APPSTORE_URL` (build/generar.py) y regenera.
Mientras esté vacío, el botón sale como "Próximamente en App Store".

## Publicar
GitHub → Settings → Pages → Source: *Deploy from a branch*, rama `main`, carpeta `/docs`. Custom domain: `capturia.es`.
