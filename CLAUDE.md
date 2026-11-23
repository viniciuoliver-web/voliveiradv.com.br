# voliveiradv.com.br — VMO · The Business Letter

Site da VMO Advocacia Empresarial (Vinicius de Oliveira, OAB/MG 219.408, Belo Horizonte/MG).
O GitHub Pages publica a pasta `docs/` da branch `main` no domínio `voliveiradv.com.br`.
Tudo em `docs/` é público. Os arquivos de origem ficam em `fonte/`.

## Marca e padrão visual
- A marca é **VMO** (decisão do dono). O domínio usa "voliveiradv", mas o nome exibido é sempre VMO Advocacia Empresarial.
- Fundo branco, texto preto, tons de cinza. Fonte Inter (auto-hospedada em `docs/assets/fonts`). Nada de serifa nem de fundo bege.
- Fotos em preto e branco. Nenhuma imagem com marca de terceiros visível.
- O CSS está em `fonte/build.py` (constante `CSS`). Mudou o CSS, regenere todas as páginas.

## Regras de conteúdo
- Revisão dupla: refaça as contas e confira toda afirmação jurídica em fonte oficial e atual (lei, emenda, súmula) antes de publicar.
- Nada de nota interna, marcador ou instrução entre colchetes no texto publicado.
- Conteúdo informativo, compatível com o Provimento 205/2021 da OAB: sem promessa de resultado e sem chamada agressiva para contratação.
- O texto da edição vem do PDF que o dono envia. Acréscimos (base normativa, memória de cálculo) precisam estar corretos e ser informados a ele.

## Publicar uma nova edição
A partir da raiz do repositório:
1. Guarde o PDF e a foto em `fonte/originais/` (`blNN-original.pdf`, `blNN-foto.jpg`). Fotos de dentro do PDF: `pdfimages -all <pdf> /tmp/x`.
2. Acrescente a edição em `fonte/edicoes.json` (copie o formato da edição 01; `slug` = `NN-assunto-em-poucas-palavras`).
   `seo_titulo` com até 60 caracteres, `seo_descricao` entre 120 e 160.
3. Escreva o corpo em `fonte/edicoes/<slug>.html`, do `<figure>` até o aviso final, usando as classes que já existem
   (`stat`, `norma`, `pull`, `cen`, `box`, `notes`, `details`, `diag`, `disc`). Imagens com `../../assets/img/...`.
4. Gere a capa: `python3 fonte/ferramentas/imagem.py fonte/originais/blNN-foto.jpg blNN-capa [--topo PIXELS]`
5. Gere a imagem de compartilhamento: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 fonte/ferramentas/og.py <slug> fonte/originais/blNN-foto.jpg`
6. Copie o PDF com metadados: `python3 fonte/ferramentas/pdfmeta.py fonte/originais/blNN-original.pdf <slug>`
7. Gere o site: `python3 fonte/build.py` (refaz início, lista, edições, sitemap e robots).
8. Confira: sirva `docs/` (`python3 -m http.server -d docs`), tire prints em 1280px e 390px, veja se não há rolagem lateral,
   links quebrados ou JSON-LD inválido.
9. Faça o commit na `main` e o push. O Pages publica em cerca de um minuto.

Edição enviada só como texto (sem PDF do dono), como a nº 02: monte a versão impressa em `fonte/impressos/blNN.html`
(copie `bl02.html`; A4, Inter em TTF de `fonte/impressos/fontes/`, imagens de `docs/assets/img/`) e gere
`fonte/originais/blNN-original.pdf` com `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 fonte/ferramentas/impresso.py NN`
(o script avisa se alguma página estoura). Depois siga do passo 6. O texto do dono vai em `fonte/originais/blNN-texto.md`.

Prévia sem publicar: `python3 fonte/build.py --previa /tmp/previa` (links com index.html, sem PDF).
