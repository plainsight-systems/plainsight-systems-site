#!/usr/bin/env python3
"""
Generate the Open Graph social card for plainsight-systems.com.

Output:  static/images/social-card.png  (1200 x 630)

Inputs:  static/fonts/PlexSerif-Regular.woff2
         static/fonts/PlexSerif-LightItalic.woff2
         static/fonts/PlexMono-Regular.woff2

Brand tokens are mirrored from assets/css/overrides.css. If those tokens
change, update the BRAND block below to match — the social card is the
same brand surface as the site, just rendered as a raster.

Deterministic: given the same input fonts and this script, produces the
same bytes.

Dependencies (Python 3):  Pillow, fonttools, brotli
Install:  pip install Pillow fonttools brotli
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = REPO_ROOT / "static" / "fonts"
OUTPUT_PATH = REPO_ROOT / "static" / "images" / "social-card.png"

# ── Brand tokens (mirror assets/css/overrides.css) ─────────────────────────
IVORY = (250, 250, 245)   # --ivory          #fafaf5
RULE = (212, 208, 202)    # --rule           #d4d0ca
INK = (15, 15, 15)        # --ink            #0f0f0f
MUTED = (91, 89, 85)      # --muted          #5b5955
MUTED_STRONG = (59, 57, 54)  # --muted-strong #3b3936

# ── Card geometry ──────────────────────────────────────────────────────────
W, H = 1200, 630
PAD_X = 96
PAD_Y = 88

# Type sizes
SIZE_EYEBROW = 18
SIZE_WORDMARK = 96
SIZE_TAGLINE = 38
SIZE_FOOTER = 16

# Letter-spacing (px) for tracked mono — mirrors CSS letter-spacing in em.
TRACK_EYEBROW = 3   # ~0.18em at 18px
TRACK_FOOTER = 2    # ~0.06em at 16px


def woff2_to_ttf(woff2_path: Path, ttf_path: Path) -> None:
    """Convert a .woff2 to .ttf so Pillow can rasterize it.

    Pillow does not read woff2 directly. fontTools handles the decompression
    via brotli; setting flavor=None outputs an uncompressed TTF.
    """
    font = TTFont(str(woff2_path))
    font.flavor = None
    font.save(str(ttf_path))


def draw_tracked(draw: ImageDraw.ImageDraw, xy, text: str, font: ImageFont.FreeTypeFont, fill, track_px: int) -> int:
    """Draw `text` with `track_px` pixels added between glyphs. Return total width."""
    x, y = xy
    start_x = x
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), ch, font=font)
        x += (bbox[2] - bbox[0]) + track_px
    # Final track applied past last glyph; subtract it for accurate width.
    return x - start_x - track_px


def measure_tracked(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, track_px: int) -> int:
    x = 0
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        x += (bbox[2] - bbox[0]) + track_px
    return x - track_px


def main() -> int:
    if not FONT_DIR.is_dir():
        print(f"error: font directory not found: {FONT_DIR}", file=sys.stderr)
        return 1

    inputs = {
        "serif_regular": FONT_DIR / "PlexSerif-Regular.woff2",
        "serif_light_italic": FONT_DIR / "PlexSerif-LightItalic.woff2",
        "mono_regular": FONT_DIR / "PlexMono-Regular.woff2",
    }
    for name, path in inputs.items():
        if not path.is_file():
            print(f"error: missing input font {name}: {path}", file=sys.stderr)
            return 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        ttf_paths = {name: tmp_dir / f"{name}.ttf" for name in inputs}
        for name, src in inputs.items():
            woff2_to_ttf(src, ttf_paths[name])

        font_eyebrow = ImageFont.truetype(str(ttf_paths["mono_regular"]), SIZE_EYEBROW)
        font_wordmark = ImageFont.truetype(str(ttf_paths["serif_regular"]), SIZE_WORDMARK)
        font_tagline = ImageFont.truetype(str(ttf_paths["serif_light_italic"]), SIZE_TAGLINE)
        font_footer = ImageFont.truetype(str(ttf_paths["mono_regular"]), SIZE_FOOTER)

        img = Image.new("RGB", (W, H), IVORY)
        draw = ImageDraw.Draw(img)

        # ── Eyebrow (top-left): "PLAINSIGHT SYSTEMS LLC"
        eyebrow_text = "PLAINSIGHT SYSTEMS LLC"
        draw_tracked(draw, (PAD_X, PAD_Y), eyebrow_text, font_eyebrow, MUTED, TRACK_EYEBROW)

        # ── Wordmark
        wordmark_text = "Plainsight Systems"
        wm_y = 232
        draw.text((PAD_X, wm_y), wordmark_text, font=font_wordmark, fill=INK)

        # ── Hairline rule under the wordmark
        wm_bbox = draw.textbbox((PAD_X, wm_y), wordmark_text, font=font_wordmark)
        rule_y = wm_bbox[3] + 38
        rule_w = 520
        draw.line([(PAD_X, rule_y), (PAD_X + rule_w, rule_y)], fill=RULE, width=1)

        # ── Tagline (italic light)
        tagline_text = "Authority that does not depend on us."
        draw.text((PAD_X, rule_y + 30), tagline_text, font=font_tagline, fill=INK)

        # ── Footer line: domain (left), locator (right)
        foot_y = H - PAD_Y - 4
        draw.text((PAD_X, foot_y), "plainsight-systems.com", font=font_footer, fill=MUTED)

        locator = "PHOENIX, AZ \u00b7 USA"  # middle dot
        loc_w = measure_tracked(draw, locator, font_footer, TRACK_FOOTER)
        loc_x = W - PAD_X - loc_w
        draw_tracked(draw, (loc_x, foot_y), locator, font_footer, MUTED, TRACK_FOOTER)

        img.save(OUTPUT_PATH, format="PNG", optimize=True)

    print(f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}  ({W}x{H})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
