# KaTeX stylesheet and fonts

Self-hosted assets for math that Hugo renders at build time with
`transform.ToMath` (see `layouts/_markup/render-passthrough.html`).

- **Version:** KaTeX 0.16.21, the version embedded in Hugo 0.154.2
  (the version pinned in CI). Hugo 0.166.0 moved to KaTeX 0.18.4; if
  Hugo is upgraded past that, these files must be replaced to match.
- **Source:** `npm pack katex@0.16.21`
  (sha1 `8f63c659e931b210139691f2cc7bb35166b792a3`, matches the registry).
- **Contents:** `dist/katex.min.css` and the 20 `dist/fonts/*.woff2`.
- **Modification:** the woff and ttf fallback `url()` entries were
  removed from `katex.min.css`, so it references only the woff2 files
  shipped here. All supported browsers load woff2.
- **License:** MIT, see `LICENSE`.
