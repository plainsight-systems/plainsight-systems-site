#!/usr/bin/env bash
#
# Builds a research paper's web page and PDF from one markdown source.
#
#   scripts/build-paper.sh <slug>            web page + PDF into content/
#   scripts/build-paper.sh <slug> --arxiv    arXiv source bundle into build/
#
# Source (edit these):          papers/<slug>/paper.md
#                               papers/<slug>/refs.bib      optional
#                               papers/<slug>/<any other files, e.g. figures/>
#
# Output (generated, never edit): content/research/<slug>/index.md
#                                 content/research/<slug>/<slug>.pdf
#                                 content/research/<slug>/<copied figures>
#
# pandoc resolves citations once for both outputs. The web body is written
# as markdown that Hugo's Goldmark parses (pipe tables, raw-HTML divs, no
# pandoc-only syntax); math stays as \( \) and \[ \] for the site's KaTeX
# hook. Dollar signs are never math in either output.
#
# The output directory is replaced wholesale, so nothing stale survives a
# rebuild. Any failure (wrong pandoc version, unresolved citation, LaTeX
# error, missing font) stops the build before the output is touched.
#
# Cross-references (@fig:x, @tbl:x, @eq:x, @sec:x) are resolved by
# pandoc-crossref for both outputs, with shared settings in
# scripts/paper/crossref.yaml.
#
# Requires: pandoc 3.12 and pandoc-crossref 0.3.25 built against it (both
# pinned), xelatex with TeX Live's IBM Plex fonts, rsvg-convert for SVG
# figures.

set -euo pipefail

PANDOC_VERSION="3.12"
CROSSREF_VERSION="0.3.25"

die() { echo "build-paper: $*" >&2; exit 1; }

usage="usage: scripts/build-paper.sh <slug> [--arxiv]"
[[ $# -ge 1 && $# -le 2 ]] || die "$usage"
slug="$1"
mode="site"
if [[ $# -eq 2 ]]; then
  [[ "$2" == "--arxiv" ]] || die "$usage"
  mode="arxiv"
fi
[[ "$slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "slug must be lowercase words joined by hyphens, got '$slug'"

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$root/papers/$slug"
out="$root/content/research/$slug"
filter="$root/scripts/paper/pdf-metadata.lua"
header="$root/scripts/paper/pdf-header.tex"
xref="$root/scripts/paper/crossref.yaml"
xrefweb="$root/scripts/paper/crossref-web.yaml"
webfilter="$root/scripts/paper/web-body.lua"
shift="$root/scripts/paper/shift-headings.lua"
arxivfig="$root/scripts/paper/arxiv-figures.lua"

[[ -f "$src/paper.md" ]] || die "no source at papers/$slug/paper.md"

# ── Toolchain ──────────────────────────────────────────────────
command -v pandoc >/dev/null || die "pandoc not found (need $PANDOC_VERSION)"
have="$(pandoc --version | head -1 | awk '{print $2}')"
[[ "$have" == "$PANDOC_VERSION" ]] \
  || die "pandoc $PANDOC_VERSION required for reproducible output, found $have"
command -v pandoc-crossref >/dev/null || die "pandoc-crossref not found (need $CROSSREF_VERSION)"
xr="$(pandoc-crossref --version)"
[[ "$xr" == "pandoc-crossref v$CROSSREF_VERSION "* ]] \
  || die "pandoc-crossref $CROSSREF_VERSION required, found: $xr"
[[ "$xr" == *"built with Pandoc v$PANDOC_VERSION,"* ]] \
  || die "pandoc-crossref must be built with pandoc $PANDOC_VERSION, found: $xr"
command -v xelatex >/dev/null || die "xelatex not found (install TeX Live)"
for face in IBMPlexSerif-Regular IBMPlexSerif-Italic IBMPlexSerif-Bold IBMPlexSerif-BoldItalic \
            IBMPlexMono-Regular IBMPlexMono-Italic IBMPlexMono-Bold IBMPlexMono-BoldItalic; do
  kpsewhich "$face.otf" >/dev/null || die "TeX Live font $face.otf not found (tlmgr install plex)"
done
if grep -q '\.svg)' "$src/paper.md"; then
  command -v rsvg-convert >/dev/null || die "rsvg-convert not found; needed for SVG figures (brew install librsvg)"
fi

# ── Front matter ───────────────────────────────────────────────
# The YAML block between the first two '---' lines is copied verbatim into
# index.md; Hugo validates it (layouts/partials/paper/validate.html).
front="$(awk 'NR==1 && $0!="---"{exit 1} NR>1 && $0=="---"{exit} NR>1{print}' "$src/paper.md")" \
  || die "paper.md must start with a '---' front matter block"
[[ -n "$front" ]] || die "paper.md front matter is empty"
if grep -qE '^pdf:' <<<"$front"; then
  die "remove 'pdf:' from paper.md; the build sets it to $slug.pdf"
fi

# Reproducible PDF timestamps: the paper's own date (lastmod if present).
# awk, not grep: a missing key must yield an empty string, not a pipefail exit.
fm_value() { awk -v k="$1" '$1 == k":" {gsub(/"/, "", $2); print $2; exit}' <<<"$front"; }
stamp="$(fm_value lastmod)"
[[ -n "$stamp" ]] || stamp="$(fm_value date)"
[[ "$stamp" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || die "front matter date must be YYYY-MM-DD, got '$stamp'"
if date -u -j -f '%Y-%m-%d %H:%M:%S' "$stamp 00:00:00" +%s >/dev/null 2>&1; then
  epoch="$(date -u -j -f '%Y-%m-%d %H:%M:%S' "$stamp 00:00:00" +%s)"   # BSD date (macOS)
else
  epoch="$(date -u -d "$stamp 00:00:00" +%s)"                           # GNU date
fi

# Canonical web address for the PDF's title block, from the site config.
base_url="$(awk '$1 == "baseURL:" {print $2; exit}' "$root/hugo.yaml" | tr -d '"' | sed 's#/*$##')"
[[ "$base_url" =~ ^https:// ]] || die "could not read an https baseURL from hugo.yaml"

# ── pandoc options ─────────────────────────────────────────────
reader='markdown-tex_math_dollars+tex_math_single_backslash'
writer='markdown-tex_math_dollars+tex_math_single_backslash'
writer+='-fenced_divs-native_divs-bracketed_spans-native_spans'
writer+='-link_attributes-raw_attribute-fenced_code_attributes-implicit_figures'
writer+='-simple_tables-multiline_tables-grid_tables+pipe_tables-smart'

cite=()
if [[ -f "$src/refs.bib" ]]; then
  cite=(--citeproc --bibliography="$src/refs.bib" --metadata=link-citations:true)
elif grep -qE '\[@[A-Za-z0-9_:-]+' "$src/paper.md"; then
  die "paper.md cites sources but papers/$slug/refs.bib does not exist"
fi

# LaTeX options shared by the site PDF and the arXiv source, so the two
# cannot drift apart.
plex=(Extension=.otf UprightFont=*-Regular ItalicFont=*-Italic BoldFont=*-Bold BoldItalicFont=*-BoldItalic)
latexopts=(
  --from="$reader"
  --number-sections --lua-filter="$shift"
  --filter=pandoc-crossref --metadata-file="$xref"
  --lua-filter="$filter"
  ${cite[@]+"${cite[@]}"} --fail-if-warnings
  --include-in-header="$header"
  --metadata=paper-url:"$base_url/research/$slug/"
  --resource-path="$src"
  --variable=mainfont:IBMPlexSerif --variable=monofont:IBMPlexMono
  --variable=fontsize:11pt
  --variable=geometry:margin=1.1in
  --variable=linestretch:1.15
  --variable=colorlinks:true
  --variable=linkcolor:black --variable=citecolor:black --variable=urlcolor:black
  --variable=lang:en-US
)
for o in "${plex[@]}"; do
  latexopts+=(--variable=mainfontoptions:"$o" --variable=monofontoptions:"$o")
done

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# ── arXiv source bundle ────────────────────────────────────────
# arXiv compiles source itself and rejects PDFs produced from TeX. The
# bundle is <slug>.tex (citations already resolved by citeproc, so no .bib
# or .bbl is needed) plus figures, with SVGs converted to PDF. It is
# compiled here exactly once as arXiv would (two xelatex passes, no
# network, no files outside the bundle) before it is zipped.
if [[ "$mode" == "arxiv" ]]; then
  bundle="$work/arxiv"
  mkdir -p "$bundle"
  while IFS= read -r -d '' f; do
    mkdir -p "$bundle/$(dirname "$f")"
    case "$f" in
      *.svg) SOURCE_DATE_EPOCH="$epoch" rsvg-convert --format=pdf --output="$bundle/${f%.svg}.pdf" "$src/$f" ;;
      *)     cp "$src/$f" "$bundle/$f" ;;
    esac
  done < <(cd "$src" && find . -type f ! -name 'paper.md' ! -name 'refs.bib' ! -name '.DS_Store' -print0)

  pandoc "$src/paper.md" "${latexopts[@]}" --lua-filter="$arxivfig" \
    --standalone --to=latex --output="$bundle/$slug.tex"

  for pass in 1 2; do
    if ! (cd "$bundle" && SOURCE_DATE_EPOCH="$epoch" FORCE_SOURCE_DATE=1 \
          xelatex -interaction=nonstopmode -halt-on-error -no-shell-escape "$slug.tex" >"$work/xelatex.log" 2>&1); then
      tail -25 "$work/xelatex.log" >&2
      die "the arXiv bundle does not compile with xelatex (pass $pass)"
    fi
  done
  if grep -q "There were undefined references" "$bundle/$slug.log"; then
    die "the arXiv bundle has undefined references"
  fi
  rm -f "$bundle/$slug".{aux,log,out,toc,pdf}

  # Reproducible zip: fixed timestamps (the paper's date, UTC), sorted entries.
  mkdir -p "$root/build/arxiv"
  zipfile="$root/build/arxiv/$slug-arxiv.zip"
  rm -f "$zipfile"
  (cd "$bundle" \
    && find . -type f -exec env TZ=UTC touch -t "${stamp//-/}0000" {} + \
    && find . -type f | LC_ALL=C sort | TZ=UTC zip -X -q "$zipfile" -@)

  echo "build-paper: wrote build/arxiv/$slug-arxiv.zip ($(cd "$bundle" && find . -type f | wc -l | tr -d ' ') files)"
  echo "  Upload it as a TeX submission and choose the XeLaTeX processor (TeX Live 2025)."
  exit 0
fi

# ── Web body ───────────────────────────────────────────────────
# Papers use ## for top-level sections (the page title is the h1), so
# headings are shifted up one level (shift-headings.lua) for crossref and
# LaTeX section numbering; web-body.lua shifts them back for Hugo.
# Filter order matters: crossref first (its @fig:x refs look like
# citations), then the web reshaping, then citeproc.
pandoc "$src/paper.md" \
  --from="$reader" --to="$writer" --wrap=preserve \
  --lua-filter="$shift" \
  --filter=pandoc-crossref --metadata-file="$xref" --metadata-file="$xrefweb" \
  --metadata=equationNumberTeX:'\tag' \
  --lua-filter="$webfilter" \
  ${cite[@]+"${cite[@]}"} --fail-if-warnings \
  --output="$work/body.md"

{
  echo "---"
  echo "# GENERATED by scripts/build-paper.sh from papers/$slug/paper.md."
  echo "# Do not edit; change the source and rebuild."
  printf '%s\n' "$front"
  echo "pdf: $slug.pdf"
  echo "---"
  echo
  cat "$work/body.md"
} > "$work/index.md"

# ── PDF ────────────────────────────────────────────────────────
# The PDF's /ID would otherwise depend on pandoc's random temp path. Set it
# from a hash of every input, so identical inputs give a byte-identical PDF
# and any change to the inputs changes the ID.
pdf_id="$(
  { echo "pandoc $PANDOC_VERSION crossref $CROSSREF_VERSION"
    cat "$0" "$filter" "$header" "$xref" "$xrefweb" "$webfilter" "$shift"
    (cd "$src" && find . -type f ! -name '.DS_Store' | LC_ALL=C sort | while IFS= read -r f; do
       echo "$f"; cat "$f"; done)
  } | shasum -a 256 | cut -c1-32
)"
printf '\\AtBeginDocument{\\special{pdf:trailerid [<%s><%s>]}}\n' "$pdf_id" "$pdf_id" > "$work/pdf-id.tex"

SOURCE_DATE_EPOCH="$epoch" FORCE_SOURCE_DATE=1 \
pandoc "$src/paper.md" "${latexopts[@]}" \
  --include-in-header="$work/pdf-id.tex" \
  --pdf-engine=xelatex \
  --output="$work/$slug.pdf"

# ── Install ────────────────────────────────────────────────────
# Copy every source file except the markdown and bibliography (figures and
# other assets keep their relative paths), then replace the output.
mkdir -p "$work/bundle"
(cd "$src" && find . -type f ! -name 'paper.md' ! -name 'refs.bib' ! -name '.DS_Store' -print0 \
  | while IFS= read -r -d '' f; do mkdir -p "$work/bundle/$(dirname "$f")"; cp "$f" "$work/bundle/$f"; done)
mv "$work/index.md" "$work/$slug.pdf" "$work/bundle/"

rm -rf "$out"
mkdir -p "$(dirname "$out")"
mv "$work/bundle" "$out"

echo "build-paper: wrote content/research/$slug/ (index.md, $slug.pdf$(cd "$out" && find . -type f ! -name index.md ! -name "$slug.pdf" | wc -l | awk '$1>0{printf ", %d other file(s)", $1}'))"
