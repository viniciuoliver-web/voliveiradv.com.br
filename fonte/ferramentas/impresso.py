"""Gera o PDF impresso de uma edição enviada como texto (sem PDF do dono).

Uso: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 fonte/ferramentas/impresso.py NN
Lê fonte/impressos/blNN.html (A4, uma .pg por página, imagens de docs/assets/img)
e grava fonte/originais/blNN-original.pdf. Depois, siga com pdfmeta.py.
Avisa se o conteúdo de alguma página encosta no rodapé.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[2]
nn = sys.argv[1]
src = RAIZ / "fonte" / "impressos" / f"bl{nn}.html"
dst = RAIZ / "fonte" / "originais" / f"bl{nn}-original.pdf"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 794, "height": 1123})
    pg.goto(src.as_uri(), wait_until="networkidle")
    pg.evaluate("document.fonts.ready")
    folgas = pg.evaluate("""() => [...document.querySelectorAll('.pg')].map(p => {
        const w = p.querySelector('.wrap'), f = p.querySelector('.ft');
        const fim = Math.max(...[...w.children].map(c => c.getBoundingClientRect().bottom));
        return Math.round(f.getBoundingClientRect().top - fim);
    })""")
    pg.pdf(path=str(dst), format="A4", print_background=True, prefer_css_page_size=True,
           margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
    b.close()
for i, f in enumerate(folgas, 1):
    print(f"página {i}: folga até o rodapé = {f}px" + ("  <-- ESTOURO" if f < 8 else ""))
print("ok:", dst)
