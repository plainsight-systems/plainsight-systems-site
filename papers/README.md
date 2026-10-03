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

The build needs pandoc 3.8.3 (pinned for reproducible output), TeX Live
with its IBM Plex fonts (`tlmgr install plex`), and `rsvg-convert` for
SVG figures. Identical inputs give a byte-identical PDF.

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

- **Math:** `\( ... \)` inline, `\[ ... \]` display. Dollar signs are
  always literal, on the web and in the PDF.
- **Figures:** an image in its own paragraph is a numbered figure,
  captioned by its alt text: `![Caption text.](figures/plot.svg)`.
  Inline images are rejected.
- **Citations:** `[@key]` with entries in `refs.bib`. Put the reference
  list where it belongs with:

  ```
  ## References

  ::: {#refs}
  :::
  ```

- **No LaTeX-only constructs** (TikZ, algorithm environments, custom
  macros): the web page cannot render them. Draw diagrams as SVG and
  write algorithms as code blocks.

## What fails the build

The script stops before touching the output on: a pandoc version other
than the pinned one, a missing font, an unresolved citation, a LaTeX or
KaTeX error, a malformed date or unknown status, or `pdf:` in the source.
Hugo then fails on any missing required front matter field, a missing
figure, or an inline image in a paper.
