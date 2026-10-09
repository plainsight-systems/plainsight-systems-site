#!/usr/bin/env python3
"""
Generate the Open Graph social card for plainsight-systems.com.

Output:  static/images/social-card.jpg  (1200 x 630)

Inputs:  assets/images/home-hero.png        (the night-lab art, 1774 x 887)
         static/fonts/PlexSerif-Light.woff2
         static/fonts/PlexMono-Regular.woff2

The card is the home page in miniature: the night-lab art on top, cropped
around the bench as the hero is, a thread-red seam, and the navy thesis
band underneath with the wordmark (firefly dot first, as in the nav), the
thesis in brass, and the domain.

Brand tokens are mirrored from assets/css/overrides.css. If those tokens
change, update the BRAND block below to match.

Deterministic: given the same inputs and this script, produces the same
bytes (Pillow, fixed geometry, no timestamps in the JPEG).

Dependencies (Python 3):  Pillow, fonttools, brotli
Install:  pip install Pillow fonttools brotli
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont


REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = REPO_ROOT / "static" / "fonts"
ART_PATH = REPO_ROOT / "assets" / "images" / "home-hero.png"
OUTPUT_PATH = REPO_ROOT / "static" / "images" / "social-card.jpg"

# ── Brand tokens (mirror assets/css/overrides.css) ─────────────────────────
NIGHT = (14, 21, 36)          # --night        #0e1524
NIGHT_INK = (241, 235, 220)   # --night-ink    #f1ebdc
NIGHT_MUTED = (185, 178, 162) # --night-muted  #b9b2a2
BRASS_SOFT = (233, 207, 143)  # --brass-soft   #e9cf8f
FIREFLY = (232, 196, 106)     # --firefly      #e8c46a
THREAD = (179, 38, 30)        # --thread       #b3261e

# ── Card geometry ──────────────────────────────────────────────────────────
W, H = 1200, 630
ART_H = 380            # the art band; the navy band takes the rest
ART_FOCUS_Y = 0.62     # vertical focus of the crop, as the hero's object-position
SEAM_H = 3             # the thread-red seam between art and band
PAD_X = 72

SIZE_WORDMARK = 64
SIZE_THESIS = 30
SIZE_DOMAIN = 18
TRACK_DOMAIN = 1       # px between mono glyphs

DOT = 14               # firefly dot diameter
DOT_GAP = 20           # dot to wordmark
GLOW_RADIUS = 9        # Gaussian blur radius of the dot's glow


def woff2_to_ttf(woff2_path: Path, ttf_path: Path) -> None:
    """Convert a .woff2 to .ttf so Pillow can rasterize it."""
    font = TTFont(str(woff2_path))
    font.flavor = None
    font.save(str(ttf_path))


def draw_tracked(draw: ImageDraw.ImageDraw, xy, text: str, font, fill, track_px: int) -> None:
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track_px


def measure_tracked(draw: ImageDraw.ImageDraw, text: str, font, track_px: int) -> float:
    return sum(draw.textlength(ch, font=font) for ch in text) + track_px * (len(text) - 1)


def art_band() -> Image.Image:
    """The night-lab art scaled to the card's width, cropped around the bench."""
    art = Image.open(ART_PATH).convert("RGB")
    scaled_h = round(art.height * W / art.width)
    art = art.resize((W, scaled_h), Image.LANCZOS)
    top = round((scaled_h - ART_H) * ART_FOCUS_Y)
    return art.crop((0, top, W, top + ART_H))


def firefly(img: Image.Image, cx: int, cy: int) -> None:
    """A warm dot with a soft glow, as the nav's brand dot."""
    glow = Image.new("L", img.size, 0)
    ImageDraw.Draw(glow).ellipse((cx - DOT, cy - DOT, cx + DOT, cy + DOT), fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(GLOW_RADIUS))
    img.paste(Image.new("RGB", img.size, FIREFLY), (0, 0), glow)
    r = DOT // 2
    ImageDraw.Draw(img).ellipse((cx - r, cy - r, cx + r, cy + r), fill=FIREFLY)


def main() -> int:
    inputs = {
        "serif_light": FONT_DIR / "PlexSerif-Light.woff2",
        "mono_regular": FONT_DIR / "PlexMono-Regular.woff2",
    }
    for path in [ART_PATH, *inputs.values()]:
        if not path.is_file():
            print(f"error: missing input: {path}", file=sys.stderr)
            return 1

    with tempfile.TemporaryDirectory() as tmp:
        ttf = {name: Path(tmp) / f"{name}.ttf" for name in inputs}
        for name, src in inputs.items():
            woff2_to_ttf(src, ttf[name])
        font_wordmark = ImageFont.truetype(str(ttf["serif_light"]), SIZE_WORDMARK)
        font_thesis = ImageFont.truetype(str(ttf["serif_light"]), SIZE_THESIS)
        font_domain = ImageFont.truetype(str(ttf["mono_regular"]), SIZE_DOMAIN)

        img = Image.new("RGB", (W, H), NIGHT)
        img.paste(art_band(), (0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, ART_H, W, ART_H + SEAM_H - 1), fill=THREAD)

        # The band's two lines, set from their baselines ("ls" anchor).
        band_top = ART_H + SEAM_H
        wordmark_base = band_top + 112
        thesis_base = wordmark_base + 62

        text_x = PAD_X + DOT + DOT_GAP
        wm_box = draw.textbbox((text_x, wordmark_base), "Plainsight Systems", font=font_wordmark, anchor="ls")
        firefly(img, PAD_X + DOT // 2, (wm_box[1] + wm_box[3]) // 2 + 4)
        draw = ImageDraw.Draw(img)
        draw.text((text_x, wordmark_base), "Plainsight Systems", font=font_wordmark, fill=NIGHT_INK, anchor="ls")
        draw.text((text_x, thesis_base), "Builds things to understand them.", font=font_thesis, fill=BRASS_SOFT, anchor="ls")

        domain = "plainsight-systems.com"
        dom_w = measure_tracked(draw, domain, font_domain, TRACK_DOMAIN)
        dom_x = W - PAD_X - dom_w
        bbox = draw.textbbox((0, 0), domain, font=font_domain, anchor="ls")
        draw_tracked(draw, (dom_x, thesis_base + bbox[1]), domain, font_domain, NIGHT_MUTED, TRACK_DOMAIN)

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        img.save(OUTPUT_PATH, format="JPEG", quality=88, optimize=True, subsampling=0)

    print(f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}  ({W}x{H})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
