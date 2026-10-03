# plainsight-systems.com

Static site for the Plainsight Systems LLC holding-company web presence. Deployed to Cloudflare Workers on push to `main`.

---

## Stack

- **Hugo** 0.154.2 extended
- **Theme:** [hugo-theme-operator](https://github.com/plainsight-lab/hugo-theme-operator) — git submodule
- **Deploy:** Cloudflare Workers via `wrangler.toml`
- **CI/CD:** GitHub Actions (`.github/workflows/deploy.yaml`) on push to `main`

Brand tokens (ink-on-ivory, Fraunces + DM Mono, institutional register) live in `assets/css/overrides.css` and are loaded after the theme stylesheet.

---

## Local development

```bash
# Initialise submodules (first clone only)
git submodule update --init --recursive

# Install Hugo (extended) — https://gohugo.io/installation/
brew install hugo

# Serve locally
hugo server -D
```

The site is available at `http://localhost:1313`.

For a local Cloudflare Workers preview:

```bash
hugo --minify
npx wrangler dev --port 8787
```

---

## Deployment

Push to `main` triggers automatic deployment via GitHub Actions.

**Required GitHub Secrets:**

| Secret                   | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `CLOUDFLARE_API_TOKEN`   | Cloudflare API token with Workers Scripts edit permission     |
| `CLOUDFLARE_ACCOUNT_ID`  | Your Cloudflare account ID                                    |

---

## Structure

```
plainsight-systems-site/
├── assets/
│   └── css/overrides.css            # Brand tokens (ink on ivory)
├── content/                         # Markdown content
│   ├── _index.md                    # Homepage frontmatter
│   ├── portfolio/_index.md
│   ├── licensing/_index.md
│   ├── about/_index.md
│   ├── contact/_index.md
│   ├── privacy/_index.md
│   ├── terms/_index.md
│   └── security/_index.md
├── layouts/                         # Theme overrides
│   ├── _default/
│   │   ├── baseof.html
│   │   ├── single.html
│   │   └── list.html
│   ├── partials/
│   │   ├── head.html
│   │   ├── header.html
│   │   └── footer.html
│   └── index.html                   # Homepage template
├── papers/                          # Research paper sources (see papers/README.md)
├── scripts/build-paper.sh           # paper.md → content/research/<slug>/ (page + PDF)
├── static/
│   ├── _headers                     # Cloudflare response headers
│   ├── .well-known/security.txt     # RFC 9116 security contact
│   └── fonts/                       # Fraunces + DM Mono woff2
├── themes/
│   └── hugo-theme-operator/         # git submodule
├── hugo.yaml                        # Hugo configuration
├── wrangler.toml                    # Cloudflare Workers configuration
└── .github/workflows/deploy.yaml    # CI/CD
```

---

## Licensing

Split license, Apache 2.0 for code and CC BY 4.0 for written content; see `LICENSE`.

- Site code (layouts, templates, styles, scripts, configuration): Apache 2.0, `LICENSE-CODE`.
- Written content (pages, research papers and their PDFs): CC BY 4.0, `LICENSE-CONTENT`.
- Brand assets ("Plainsight Systems", the wordmark and logomarks): all rights reserved, excluded from both.
- Third-party fonts, KaTeX and the theme keep their own licenses: `NOTICE`.
