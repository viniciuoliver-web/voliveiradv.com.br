"""Prepara a foto de capa de uma edição.

Uso: python3 fonte/ferramentas/imagem.py <foto> <nome-base> [--topo PIXELS]
Gera docs/assets/img/<nome-base>.jpg/.webp (1080 de largura, 16:9) e a
miniatura <nome-base>-640.jpg/.webp, em tons de cinza, como no PDF.
--topo escolhe a altura (em pixels da foto) onde começa o recorte 16:9.
"""
import sys
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
foto, nome = sys.argv[1], sys.argv[2]
topo = int(sys.argv[sys.argv.index("--topo") + 1]) if "--topo" in sys.argv else None
out = RAIZ / "docs" / "assets" / "img"
out.mkdir(parents=True, exist_ok=True)

im = Image.open(foto).convert("L")
if im.width > 1080:
    im = im.resize((1080, round(im.height * 1080 / im.width)), Image.LANCZOS)
w, h = im.size
ch = round(w * 9 / 16)
t = (h - ch) // 2 if topo is None else max(0, min(topo, h - ch))
capa = im.crop((0, t, w, t + ch))
capa.save(out / f"{nome}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
capa.save(out / f"{nome}.webp", "WEBP", quality=80, method=6)
mini = capa.resize((640, 360), Image.LANCZOS)
mini.save(out / f"{nome}-640.jpg", "JPEG", quality=80, optimize=True, progressive=True)
mini.save(out / f"{nome}-640.webp", "WEBP", quality=78, method=6)
print("ok:", capa.size, "recorte a partir de", t)
