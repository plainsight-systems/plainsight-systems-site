# Research papers

Each paper's source lives here. The web page and the PDF are generated
from it into `content/research/<slug>/`, which is build output: never
edit it by hand.

```
papers/<slug>/
  paper.md      front matter + body
  refs.bib      optional bibliography
  figures/      any other files, copied to the page bundle as-is
```

Build after every change, then commit the source and the output together:

```bash
scripts/build-paper.sh <slug>
```

The build needs pandoc 3.12 and pandoc-crossref 0.3.25 built against it
(both pinned for reproducible output; `brew install pandoc-crossref`
installs the pair), TeX Live with its IBM Plex fonts (`tlmgr install
plex`), and `rsvg-convert` for SVG figures. Identical inputs give a
byte-identical PDF.

## Front matter

```yaml
title: "Title"
subtitle: "Optional subtitle"
date: 2026-10-03          # first publication, YYYY-MM-DD
lastmod: 2026-11-01       # optional, last revision
version: "0.1"
status: working-paper     # working-paper | preprint | published
draft: true               # until it should publish
authors:
  - given: Andrew P
    family: Hunter
    orcid: 0009-0005-7613-8019
    affiliation: Plainsight Systems
abstract: |
  Markdown. Math allowed.
keywords: [one, two]
doi: ""                   # optional, bare DOI once minted
citekey: ""               # optional BibTeX key for the Cite block
```

Do not set `pdf:`; the build sets it to `<slug>.pdf`.

## Writing

- **Sections:** `##` for top-level sections, `###` below; never `#`
  (the page title is the h1). Sections are numbered (1, 2, 2.1) on the
  web and in the PDF. Unnumbered: `## References {-}`.
- **Math:** `\( ... \)` inline, `\[ ... \]` display. Dollar signs are
  always literal, on the web and in the PDF. Label a display equation to
  number it: `\[ ... \]{#eq:kl}`.
- **Figures:** an image in its own paragraph is a figure, captioned by its
  alt text, and must be labelled:
  `![Caption text.](figures/plot.svg){#fig:plot}`. Inline images are
  rejected.
- **Tables:** caption on the line after the table:
  `: Caption text. {#tbl:results}`.
- **Cross-references:** `@fig:plot`, `@tbl:results`, `@eq:kl`,
  `@sec:method` (label a section with `## Method {#sec:method}`). They
  render as linked "Figure 1", "Table 1", "Eq. (1)", "Section 3".
- **Citations:** `[@key]` with entries in `refs.bib`. Put the reference
  list where it belongs with:

  ```
  ## References {-}

  ::: {#refs}
  :::
  ```

- **No LaTeX-only constructs** (TikZ, algorithm environments, custom
  macros): the web page cannot render them. Draw diagrams as SVG and
  write algorithms as code blocks.

## arXiv

```bash
scripts/build-paper.sh <slug> --arxiv
```

writes `build/arxiv/<slug>-arxiv.zip` (not committed): `<slug>.tex` with
citations already resolved, plus figures, SVGs converted to PDF. The
build compiles the bundle on its own with two xelatex passes before
zipping it, so a bundle that would fail on arXiv fails here first.

To submit: upload the zip as a TeX submission and choose the **XeLaTeX**
processor (TeX Live 2025). arXiv advises against writing its 00README
file by hand. A first submission to a category needs an endorsement from
an established arXiv author in that category.

## What fails the build

The script stops before touching the output on: a pandoc or
pandoc-crossref version other than the pinned ones, a missing font, an
unresolved citation or cross-reference, an unlabelled figure, a `#`
heading, a LaTeX or KaTeX error, a malformed date or unknown status, or
`pdf:` in the source.
Hugo then fails on any missing required front matter field, a missing
figure, or an inline image in a paper.
