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

## Writing across project sites

Project sites own their articles. This site combines their published metadata
with local papers and optional curated links in Research and the homepage's
Latest list. The article text stays on the originating site.

Register a project's complete RSS feed with `feed` and `writing_name` in its
existing `data/featured_repos.yaml` entry. Serenity publishes
`https://serenity.plainsight-systems.com/writing/index.xml`; Cradle publishes
`https://cradle.plainsight-systems.com/lessons/index.xml`; Dolittle publishes
`https://dolittle.plainsight-systems.com/writing/index.xml`. Feeds contain published
articles only, with title, description, date, project URL and canonical GUID.
They must contain the complete archive, without a recent-item limit.

To refresh locally:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/refresh-writing.py
hugo --minify
```

`data/project_writing.json` is a generated starting snapshot, so a fresh checkout
can build without fetching feeds. Do not maintain article entries in it by hand.
CI restores its last successful snapshot, fetches the registered feeds, builds,
and deploys daily at 07:17 UTC (00:17 Arizona), and on pushes to main or a manual
workflow run. PRs test and build with the checked-in snapshot without deploying.
A successful feed replaces that project's entries, including corrections and
removals. A failed feed retains its previous entries and prints a warning; a new
source without a saved snapshot fails explicitly. The cache is saved after a
successful deployment. GitHub's cache can be evicted; the checked-in snapshot
remains the fallback if that happens during a feed outage.

Reading links and canonical URLs belong to the project sites. Legacy off-site
RSS GUIDs fall back to the project article URL, including in saved snapshots.
For a curated syndicated copy, set `canonical_url` to the project article URL
so it does not duplicate the original. `data/writing.yaml` is optional curation
for standalone posts and writing without a feed; new project articles need no
entry there.

For initial setup before a feed is deployed, generate its production output in
the project repository, then pass `--feed-file URL=/absolute/path/index.xml` to
the refresh script. This option seeds metadata from the real production feed,
not from private planning files. Deploy the project feeds before deploying the
hub. No cross-repository credentials or browser-side feed requests are required.

Verification: `.venv/bin/python -m unittest discover -s tests -v` covers RSS
parsing, outage recovery, changes/removals, future dates and duplicate editions,
and renders both article lists through Hugo.

GitHub disables public scheduled workflows after 60 days without repository
activity. A separate scheduled job keeps this workflow enabled using GitHub's
workflow-enable API and its short-lived repository token. Only that job has
`actions: write`; the build/deploy job keeps `contents: read`, and PRs cannot run
the keepalive job. This follows the API-based approach documented by
[gh-workflow-keepalive](https://github.com/liskin/gh-workflow-keepalive), without
adding an external action or dummy commits. GitHub may delay scheduled runs;
the manual trigger is available for immediate publication.

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
