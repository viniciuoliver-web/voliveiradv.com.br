"""Gera o site voliveiradv.com.br (VMO — The Business Letter) em docs/.

Uso, a partir da raiz do repositório:
  python3 fonte/build.py                  # gera docs/ (o que o GitHub Pages publica)
  python3 fonte/build.py --previa SAIDA   # prévia: links terminam em index.html, sem PDF

Conteúdo:
  fonte/edicoes.json         lista das edições (metadados de SEO e capa)
  fonte/edicoes/<slug>.html  corpo de cada edição (do <figure> ao aviso final)
Imagens, fontes e PDFs ficam direto em docs/assets e docs/business-letter/pdf.
"""
import json
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "fonte"
PREVIA = "--previa" in sys.argv
OUT = Path(sys.argv[sys.argv.index("--previa") + 1]) if PREVIA else RAIZ / "docs"

BASE = "https://voliveiradv.com.br"
DOMINIO = "voliveiradv.com.br"
INSTAGRAM = "https://www.instagram.com/vinicius.deoliver/"
MARCA = "VMO Advocacia Empresarial"

EDICOES = sorted(json.loads((FONTE / "edicoes.json").read_text(encoding="utf-8")),
                 key=lambda e: (e["data"], e["numero"]), reverse=True)
ULTIMA = EDICOES[0]


def link(path: str) -> str:
    """Link relativo para diretório; na prévia aponta para o index.html."""
    if not PREVIA:
        return path or "./"
    if path in ("", "./"):
        return "index.html"
    return path + "index.html" if path.endswith("/") else path


def url_edicao(e):
    return f"{BASE}/business-letter/{e['slug']}/"


def iso(e):
    return f"{e['data']}T09:00:00-03:00"


CSS = """
/* VOICE: editorial sóbrio de banca empresarial, sem adjetivo
   IDEA: a própria newsletter impressa, agora legível na web
   PICTURE: a foto da edição, em P&B, ocupando a largura da coluna
   COLOUR and TYPE: branco e preto, cinzas de apoio; Inter variável
   LAYOUT: coluna de leitura de 720px, faixas de número com fio fino */
@font-face{font-family:"Inter";src:url("{F}/assets/fonts/inter-var-latin.woff2") format("woff2");font-weight:100 900;font-display:swap}
:root{color-scheme:light dark;--bg:light-dark(#ffffff,#0e0e0e);--ink:light-dark(#111111,#f1f1f1);--mut:light-dark(#5c5c5c,#a6a6a6);--rule:light-dark(#dcdcdc,#2c2c2c);--inv:light-dark(#111111,#f1f1f1);--invink:light-dark(#ffffff,#111111)}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 "Inter",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;font-feature-settings:"cv11","ss01";overflow-x:clip}
a{color:inherit;text-underline-offset:3px;text-decoration-thickness:1px}
a:focus-visible,summary:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
img{display:block;max-width:100%;height:auto}
.wrap{max-width:1080px;margin:0 auto;padding:0 max(5vw,18px)}
.col{max-width:720px;margin:0 auto}
.top{border-bottom:1px solid var(--rule)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:64px;flex-wrap:wrap}
.brand{display:flex;align-items:baseline;gap:12px;text-decoration:none}
.brand b{font-size:24px;font-weight:800;letter-spacing:-.02em}
.brand span{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.nav a{font-size:14px;font-weight:600;text-decoration:none;padding:12px 0;display:inline-block}
.nav a[aria-current]{text-decoration:underline}
.crumbs{font-size:13px;color:var(--mut);margin:22px 0 0}
.crumbs a{color:var(--mut)}
.kick{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin:0 0 14px}
h1,h2{text-wrap:balance;letter-spacing:-.025em;margin:0}
h1{font-size:clamp(38px,6.2vw,62px);line-height:1.03;font-weight:800}
h2{font-size:clamp(26px,3.6vw,34px);line-height:1.12;font-weight:750}
.dek{font-size:clamp(18px,2.2vw,21px);line-height:1.45;color:var(--mut);margin:18px 0 0}
.by{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:14px;color:var(--mut);margin:22px 0 0;padding:14px 0 0;border-top:1px solid var(--rule)}
.by strong{color:var(--ink);font-weight:600}
.mast{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin:34px 0 26px;padding-bottom:12px;border-bottom:1px solid var(--rule)}
figure{margin:36px 0 0}
figcaption{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin-top:10px}
.stat{display:grid;grid-template-columns:auto minmax(0,1fr);gap:8px 36px;align-items:center;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:24px 0;margin:36px 0 0}
.stat .n{font-size:clamp(40px,6vw,58px);font-weight:800;letter-spacing:-.03em;line-height:1;white-space:nowrap}
.stat p{margin:0;font-size:13px;line-height:1.5;color:var(--mut)}
.stat p b{display:block;color:var(--ink);font-size:13px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:2px}
.norma{font-size:14px;line-height:1.55;color:var(--mut);margin:14px 0 0}
section{margin:44px 0 0}
section p{margin:14px 0 0}
section ul,section ol{margin:16px 0 0;padding-left:1.25em}
section li{margin:10px 0 0;padding-left:.2em}
.duo{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;align-items:start}
.duo figcaption{grid-column:1/-1;margin-top:0}
.pull{font-size:clamp(20px,2.6vw,24px);line-height:1.35;font-weight:650;letter-spacing:-.01em;margin:28px 0 0;padding-left:18px;border-left:3px solid var(--ink)}
.cen{border-top:1px solid var(--rule);padding:22px 0;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:6px 32px;align-items:start}
.cen:last-of-type{border-bottom:1px solid var(--rule)}
.cen .l{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin:0 0 6px}
.cen .v{font-size:clamp(34px,5vw,46px);font-weight:800;letter-spacing:-.03em;line-height:1.05;white-space:nowrap;margin:0}
.cen p{margin:0;font-size:16px}
.box{background:var(--inv);color:var(--invink);padding:22px 24px;margin:28px 0 0}
.box strong{display:block;font-size:19px;font-weight:700;letter-spacing:-.01em}
.box span{display:block;font-size:15px;margin-top:4px;opacity:.85}
.notes{font-size:13px;line-height:1.55;color:var(--mut);margin:14px 0 0}
details{margin:22px 0 0;border:1px solid var(--rule)}
summary{cursor:pointer;font-size:15px;font-weight:650;padding:14px 18px;min-height:44px}
details .in{padding:0 18px 18px}
.scroll{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}
th,td{padding:9px 8px;border-bottom:1px solid var(--rule);text-align:right;white-space:nowrap}
th:first-child,td:first-child{text-align:left;white-space:normal}
thead th{font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--mut);font-weight:700}
tr.t td{font-weight:750;border-bottom:0}
.diag{border-top:2px solid var(--ink);margin:30px 0 0;padding-top:16px}
.diag b{display:block;font-size:13px;letter-spacing:.06em;text-transform:uppercase}
.diag span{display:block;font-size:15px;margin-top:4px}
.disc{font-size:13px;color:var(--mut);margin:18px 0 0}
.acts{display:flex;flex-wrap:wrap;gap:12px;margin:34px 0 0}
.btn{display:inline-flex;align-items:center;min-height:46px;padding:0 20px;font-size:15px;font-weight:650;text-decoration:none;border:1.5px solid var(--ink)}
.btn.p{background:var(--ink);color:var(--bg)}
.card{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:22px 32px;align-items:center;text-decoration:none;border-top:1px solid var(--rule);padding:26px 0}
.card:last-child{border-bottom:1px solid var(--rule)}
.card h3{font-size:clamp(24px,3.2vw,30px);line-height:1.12;letter-spacing:-.02em;margin:6px 0 0;text-wrap:balance}
.card p{margin:10px 0 0;color:var(--mut);font-size:16px}
.card .meta{display:block;line-height:1.5;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.card .go{display:inline-block;margin-top:14px;font-size:15px;font-weight:650;text-decoration:underline}
.lead{font-size:clamp(19px,2.3vw,22px);line-height:1.5;margin:18px 0 0}
.who{font-size:15px;color:var(--mut);margin:16px 0 0}
.foot{border-top:1px solid var(--rule);margin-top:72px}
.foot .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px 24px;padding-top:22px;padding-bottom:34px;font-size:13px;color:var(--mut)}
.foot a{color:var(--mut)}
@media(max-width:600px){body{font-size:16.5px}.stat,.cen,.card{grid-template-columns:minmax(0,1fr)}.brand span{display:none}th,td{padding:8px 5px;font-size:13px}}
@media print{.top,.foot,.acts,.crumbs{display:none}details{border:0}details>*{display:block}}
"""

ORG = {"@type": "Organization", "@id": f"{BASE}/#org", "name": MARCA, "url": f"{BASE}/",
       "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/img/vmo-logo.png", "width": 512, "height": 512},
       "founder": {"@id": f"{BASE}/#vinicius"}}
PERSON = {"@type": "Person", "@id": f"{BASE}/#vinicius", "name": "Vinicius de Oliveira", "jobTitle": "Advogado",
          "description": "Advogado inscrito na OAB/MG sob o nº 219.408", "worksFor": {"@id": f"{BASE}/#org"},
          "address": {"@type": "PostalAddress", "addressLocality": "Belo Horizonte", "addressRegion": "MG", "addressCountry": "BR"},
          "sameAs": [INSTAGRAM]}


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def head(title, desc, canon, depth, og_img, og_alt, og_type="website", extra_meta="", jsonld=None):
    f = ("../" * depth).rstrip("/") or "."
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Vinicius de Oliveira">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{MARCA}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/assets/img/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
{extra_meta}
<link rel="icon" href="{f}/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{f}/assets/img/apple-touch-icon.png">
<link rel="preload" href="{f}/assets/fonts/inter-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS.replace("{F}", f)}</style>
{ld}
</head>
<body>"""


def topbar(depth, current=None):
    up = "../" * depth
    cur = ' aria-current="page"' if current == "bl" else ""
    return f"""<header class="top"><div class="wrap">
<a class="brand" href="{link(up or './')}"><b>VMO</b><span>Advocacia Empresarial</span></a>
<nav class="nav" aria-label="Principal"><a href="{link(up + 'business-letter/')}"{cur}>Business Letter</a></nav>
</div></header>"""


FOOT = f"""<footer class="foot"><div class="wrap">
<span>{MARCA} · Vinicius de Oliveira · OAB/MG 219.408 · Belo Horizonte/MG</span>
<span><a href="{INSTAGRAM}" rel="me noopener">Instagram</a></span>
</div></footer>
</body>
</html>
"""


def write(rel, html):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")


def picture(depth, e, small=False):
    a = "../" * depth
    sfx = "-640" if small else ""
    w, h = (640, 360) if small else (1080, 608)
    return (f'<picture><source type="image/webp" srcset="{a}assets/img/{e["imagem"]}{sfx}.webp">'
            f'<img src="{a}assets/img/{e["imagem"]}{sfx}.jpg" width="{w}" height="{h}" alt="{esc(e["imagem_alt"])}" '
            f'loading="lazy" decoding="async"></picture>')


def og_alt(e):
    return f"{e['titulo']} — VMO The Business Letter nº {e['numero']}"


def card(depth, e, href):
    return f"""<a class="card" href="{href}">
{picture(depth, e, small=True)}
<div><span class="meta">Nº {e['numero']} · {e['mes_ano']} · {e['editoria']}</span>
<h3>{e['titulo_html']}</h3>
<p>{e['subtitulo']}</p><span class="go">Ler a edição</span></div></a>"""


def edicao(e):
    d = 2
    url = url_edicao(e)
    corpo = (FONTE / "edicoes" / f"{e['slug']}.html").read_text(encoding="utf-8").strip()
    art = {"@type": "Article", "@id": f"{url}#article", "headline": e["titulo"],
           "alternativeHeadline": e["subtitulo"], "description": e["seo_descricao"],
           "image": [f"{BASE}/assets/img/{e['og_imagem']}", f"{BASE}/assets/img/{e['imagem']}.jpg"],
           "datePublished": iso(e), "dateModified": e.get("atualizado_iso", iso(e)),
           "author": {"@id": f"{BASE}/#vinicius"}, "publisher": {"@id": f"{BASE}/#org"},
           "mainEntityOfPage": url, "url": url, "inLanguage": "pt-BR",
           "articleSection": e["secao"], "keywords": e["palavras_chave"],
           "isPartOf": {"@type": "CreativeWorkSeries", "name": "The Business Letter", "url": f"{BASE}/business-letter/"}}
    if e.get("legislacao"):
        art["mentions"] = {"@type": "Legislation", "name": e["legislacao"]["nome"], "legislationDate": e["legislacao"]["data"]}
    if e.get("pdf"):
        art["associatedMedia"] = {"@type": "MediaObject", "contentUrl": f"{BASE}/business-letter/pdf/{e['pdf']}",
                                  "encodingFormat": "application/pdf"}
    ld = {"@context": "https://schema.org", "@graph": [ORG, PERSON, art,
          {"@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{BASE}/"},
              {"@type": "ListItem", "position": 2, "name": "Business Letter", "item": f"{BASE}/business-letter/"},
              {"@type": "ListItem", "position": 3, "name": f"Nº {e['numero']} — {e['titulo']}", "item": url}]}]}
    tags = "".join(f'<meta property="article:tag" content="{esc(k)}">\n' for k in e["palavras_chave"][:4])
    extra = (f'<meta property="article:published_time" content="{iso(e)}">\n'
             f'<meta property="article:modified_time" content="{e.get("atualizado_iso", iso(e))}">\n'
             '<meta property="article:author" content="Vinicius de Oliveira">\n'
             f'<meta property="article:section" content="{esc(e["secao"])}">\n{tags}')
    pdf_btn = (f'<a class="btn p" href="../pdf/{e["pdf"]}" type="application/pdf">Baixar a edição em PDF</a>'
               if e.get("pdf") and not PREVIA else "")
    html = head(e["seo_titulo"], e["seo_descricao"], url, d, e["og_imagem"], og_alt(e), "article", extra, ld) + topbar(d, "bl") + f"""
<main class="wrap"><article class="col">
<p class="crumbs"><a href="{link('../../')}">Início</a> › <a href="{link('../')}">Business Letter</a> › Nº {e['numero']}</p>
<div class="mast"><span>The Business Letter</span><span>Nº {e['numero']} · {e['mes_ano']}</span></div>
<p class="kick">{e['editoria']}</p>
<h1>{e['titulo_html']}</h1>
<p class="dek">{e['subtitulo']}</p>
<p class="by"><span>Por <strong>Vinicius de Oliveira</strong> · OAB/MG 219.408</span><time datetime="{e['data']}">{e['data_humana']}</time><span>Leitura de {e['leitura_min']} min</span></p>

{corpo}

<div class="acts">
{pdf_btn}
<a class="btn" href="{link('../')}">Todas as edições</a>
</div>
</article></main>
""" + FOOT
    write(f"business-letter/{e['slug']}/index.html", html)


def lista():
    d = 1
    url = f"{BASE}/business-letter/"
    title = f"The Business Letter | {MARCA}"
    desc = f"Edições da newsletter da {MARCA} sobre direito aplicado à gestão de empresas: trabalho, contratos, sociedade e risco."
    ld = {"@context": "https://schema.org", "@graph": [ORG,
          {"@type": "CollectionPage", "@id": f"{url}#page", "name": "The Business Letter", "url": url,
           "description": desc, "inLanguage": "pt-BR", "publisher": {"@id": f"{BASE}/#org"},
           "hasPart": [{"@type": "Article", "headline": e["titulo"], "url": url_edicao(e), "datePublished": iso(e)} for e in EDICOES]},
          {"@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{BASE}/"},
              {"@type": "ListItem", "position": 2, "name": "Business Letter", "item": url}]}]}
    cards = "\n".join(card(d, e, link(f"{e['slug']}/")) for e in EDICOES)
    html = head(title, desc, url, d, ULTIMA["og_imagem"], og_alt(ULTIMA), jsonld=ld) + topbar(d, "bl") + f"""
<main class="wrap"><div class="col">
<p class="crumbs"><a href="{link('../')}">Início</a> › Business Letter</p>
<div class="mast"><span>VMO</span><span>Edições</span></div>
<h1>The Business Letter</h1>
<p class="dek">Direito aplicado à gestão de empresas, em edições curtas.</p>
<div style="margin-top:34px">{cards}</div>
</div></main>
""" + FOOT
    write("business-letter/index.html", html)


def inicio():
    url = f"{BASE}/"
    title = f"{MARCA} | Vinicius de Oliveira, OAB/MG 219.408"
    desc = "Advocacia empresarial preventiva e estratégica em Belo Horizonte/MG: estrutura societária, contratos, relações de trabalho e de consumo, operações digitais."
    ld = {"@context": "https://schema.org", "@graph": [ORG, PERSON,
          {"@type": "WebSite", "@id": f"{BASE}/#site", "name": MARCA, "url": url,
           "inLanguage": "pt-BR", "publisher": {"@id": f"{BASE}/#org"}}]}
    html = head(title, desc, url, 0, ULTIMA["og_imagem"], og_alt(ULTIMA), jsonld=ld) + topbar(0) + f"""
<main class="wrap"><div class="col">
<div class="mast" style="margin-top:40px"><span>Advocacia Empresarial</span><span>Belo Horizonte / MG</span></div>
<h1>{MARCA}</h1>
<p class="lead">Direito empresarial preventivo e estratégico para empresas e operações digitais: estrutura societária, contratos, relações de trabalho e de consumo.</p>
<p class="who">Vinicius de Oliveira · OAB/MG 219.408</p>
<section>
<p class="kick">The Business Letter</p>
<div>{card(0, ULTIMA, link('business-letter/' + ULTIMA['slug'] + '/'))}</div>
<div class="acts"><a class="btn" href="{link('business-letter/')}">Todas as edições</a></div>
</section>
</div></main>
""" + FOOT
    write("index.html", html)


def extras():
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    hoje = max(e.get("atualizado_iso", iso(e))[:10] for e in EDICOES)
    urls = [(f"{BASE}/", hoje), (f"{BASE}/business-letter/", hoje)]
    for e in EDICOES:
        urls.append((url_edicao(e), e.get("atualizado_iso", iso(e))[:10]))
        if e.get("pdf"):
            urls.append((f"{BASE}/business-letter/pdf/{e['pdf']}", e["data"]))
    body = "".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n')
    write("CNAME", f"{DOMINIO}\n")
    write(".nojekyll", "")
    write("404.html", f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Página não encontrada | VMO</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml"><style>{CSS.replace('{F}', '')}</style></head><body>
<header class="top"><div class="wrap"><a class="brand" href="/"><b>VMO</b><span>Advocacia Empresarial</span></a><nav class="nav"><a href="/business-letter/">Business Letter</a></nav></div></header>
<main class="wrap"><div class="col"><div class="mast" style="margin-top:40px"><span>Erro 404</span><span>VMO</span></div><h1>Página não encontrada.</h1><p class="dek">O endereço pode ter mudado. As edições estão reunidas na Business Letter.</p><div class="acts"><a class="btn p" href="/business-letter/">Ir para a Business Letter</a><a class="btn" href="/">Início</a></div></div></main></body></html>
""")


for e in EDICOES:
    assert (FONTE / "edicoes" / f"{e['slug']}.html").exists(), f"falta fonte/edicoes/{e['slug']}.html"
    edicao(e)
lista()
inicio()
if PREVIA:
    # a prévia precisa das imagens e da fonte, mas não do PDF
    for sub in ("assets/fonts", "assets/img"):
        shutil.copytree(RAIZ / "docs" / sub, OUT / sub, dirs_exist_ok=True)
else:
    extras()
print("ok:", OUT, "| edições:", ", ".join(e["slug"] for e in EDICOES))
