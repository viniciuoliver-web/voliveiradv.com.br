"""Gera a imagem de compartilhamento (1200x630) de uma edição.

Uso: python3 fonte/ferramentas/og.py <slug> <foto> [--x PIXELS --y PIXELS]
Lê título, número e og_subtitulo de fonte/edicoes.json e grava
docs/assets/img/<og_imagem>. A foto ocupa a metade direita (recorte 560x630).
Requer Playwright com Chromium (PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers).
"""
import base64
import io
import json
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[2]
slug, foto = sys.argv[1], sys.argv[2]
arg = lambda k, d: int(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
e = next(x for x in json.loads((RAIZ / "fonte/edicoes.json").read_text(encoding="utf-8")) if x["slug"] == slug)

im = Image.open(foto).convert("L")
if im.width > 1080:
    im = im.resize((1080, round(im.height * 1080 / im.width)), Image.LANCZOS)
x, y = arg("--x", max(0, (im.width - 560) // 2)), arg("--y", max(0, (im.height - 630) // 2))
rec = im.crop((x, y, x + 560, y + 630))
buf = io.BytesIO(); rec.save(buf, "JPEG", quality=90)
photo = base64.b64encode(buf.getvalue()).decode()
font = (RAIZ / "docs/assets/fonts/inter-var-latin.woff2").resolve().as_uri()

html = f"""<html><head><style>@font-face{{font-family:Inter;src:url("{font}") format("woff2");font-weight:100 900}}
html,body{{margin:0}}.c{{width:1200px;height:630px;display:grid;grid-template-columns:640px 560px;background:#fff;color:#111;font-family:Inter}}
.t{{padding:54px 56px;display:flex;flex-direction:column;justify-content:space-between;border-right:1px solid #ddd}}
.m{{display:flex;justify-content:space-between;font:700 15px/1 Inter;letter-spacing:.08em;text-transform:uppercase;color:#5c5c5c;padding-bottom:16px;border-bottom:1px solid #ddd}}
.m b{{color:#111;font-size:26px;letter-spacing:-.02em;text-transform:none}}
h1{{font:800 66px/1.03 Inter;letter-spacing:-2.4px;margin:0}}
p{{font:500 25px/1.35 Inter;color:#4a4a4a;margin:18px 0 0}}
.f{{font:600 17px/1 Inter;color:#5c5c5c;padding-top:16px;border-top:1px solid #ddd}}
.ph{{background:url(data:image/jpeg;base64,{photo}) center/cover}}</style></head><body>
<div class="c"><div class="t"><div class="m"><b>VMO</b><span>The Business Letter · Nº {e['numero']}</span></div>
<div><h1>{e['titulo_html']}</h1><p>{e['og_subtitulo']}</p></div>
<div class="f">voliveiradv.com.br</div></div><div class="ph"></div></div></body></html>"""

png = RAIZ / "docs/assets/img/_og.png"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(html, wait_until="load")
    pg.evaluate("document.fonts.ready")
    pg.screenshot(path=str(png))
    b.close()
Image.open(png).convert("RGB").save(RAIZ / "docs/assets/img" / e["og_imagem"], "JPEG", quality=86, optimize=True, progressive=True)
png.unlink()
print("ok:", e["og_imagem"])
