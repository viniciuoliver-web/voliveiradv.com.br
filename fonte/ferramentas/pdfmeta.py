"""Copia o PDF de uma edição para o site com título, autor e idioma corretos.

Uso: python3 fonte/ferramentas/pdfmeta.py <pdf-original> <slug>
O conteúdo do PDF não é alterado; só os metadados (o Google usa o título).
"""
import json
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject

RAIZ = Path(__file__).resolve().parents[2]
src, slug = sys.argv[1], sys.argv[2]
e = next(x for x in json.loads((RAIZ / "fonte/edicoes.json").read_text(encoding="utf-8")) if x["slug"] == slug)
dst = RAIZ / "docs/business-letter/pdf" / e["pdf"]
dst.parent.mkdir(parents=True, exist_ok=True)
w = PdfWriter(clone_from=PdfReader(src))
w.add_metadata({
    "/Title": f"{e['titulo']} — VMO The Business Letter nº {e['numero']}",
    "/Author": "Vinicius de Oliveira — VMO Advocacia Empresarial (OAB/MG 219.408)",
    "/Subject": e["seo_descricao"],
    "/Keywords": ", ".join(e["palavras_chave"]),
    "/Creator": "VMO Advocacia Empresarial",
    "/Producer": "VMO Advocacia Empresarial",
})
w._root_object[NameObject("/Lang")] = TextStringObject("pt-BR")
w.write(dst)
print("ok:", dst)
