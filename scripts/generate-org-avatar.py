#!/usr/bin/env python3
"""
Generate the GitHub organisation avatar for Plainsight Systems LLC.

Output: static/images/org-avatar.png  (1024 x 1024)

Same brand register as the OG social card — ink on ivory, IBM Plex
Serif wordmark stacked over two lines, IBM Plex Mono mono eyebrow,
hairline rule. Designed to remain legible at GitHub's small avatar
sizes (40x40 in repo listings, 80x80 in member listings).

Deterministic: given the same input fonts and this script, produces
the same bytes.

Dependencies (Python 3): Pillow, fonttools, brotli.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = REPO_ROOT / "static" / "fonts"
OUTPUT_PATH = REPO_ROOT / "static" / "images" / "org-avatar.png"

# Brand tokens (mirror assets/css/overrides.css)
IVORY = (250, 250, 245)
RULE = (212, 208, 202)
INK = (15, 15, 15)
MUTED = (91, 89, 85)

# Geometry
SIZE = 1024
PAD_TOP = 140

SIZE_EYEBROW = 30
SIZE_WORDMARK = 172
TRACK_EYEBROW = 5
LINE_GAP = 24


def woff2_to_ttf(woff2_path: Path, ttf_path: Path) -> None:
    font = TTFont(str(woff2_path))
    font.flavor = None
    font.save(str(ttf_path))


def draw_tracked(draw, xy, text, font, fill, track_px):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), ch, font=font)
        x += (bbox[2] - bbox[0]) + track_px


def measure_tracked(draw, text, font, track_px):
    x = 0
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        x += (bbox[2] - bbox[0]) + track_px
    return x - track_px


def main() -> int:
    inputs = {
        "serif_regular": FONT_DIR / "PlexSerif-Regular.woff2",
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

        img = Image.new("RGB", (SIZE, SIZE), IVORY)
        draw = ImageDraw.Draw(img)

        # Eyebrow — top center, mono uppercase, tracked
        eyebrow = "PLAINSIGHT SYSTEMS LLC"
        eyebrow_w = measure_tracked(draw, eyebrow, font_eyebrow, TRACK_EYEBROW)
        draw_tracked(
            draw,
            ((SIZE - eyebrow_w) // 2, PAD_TOP),
            eyebrow,
            font_eyebrow,
            MUTED,
            TRACK_EYEBROW,
        )

        # Wordmark — two lines, centered, generous space below the eyebrow
        line1 = "Plainsight"
        line2 = "Systems"
        bbox1 = draw.textbbox((0, 0), line1, font=font_wordmark)
        bbox2 = draw.textbbox((0, 0), line2, font=font_wordmark)
        line_h = bbox1[3] - bbox1[1]
        line1_w = bbox1[2] - bbox1[0]
        line2_w = bbox2[2] - bbox2[0]

        block_h = line_h * 2 + LINE_GAP
        block_top = (SIZE - block_h) // 2 + 36  # nudge below geometric center

        draw.text(((SIZE - line1_w) // 2, block_top), line1, font=font_wordmark, fill=INK)
        draw.text(
            ((SIZE - line2_w) // 2, block_top + line_h + LINE_GAP),
            line2,
            font=font_wordmark,
            fill=INK,
        )

        # Hairline rule — short, centered, near the bottom
        rule_y = SIZE - PAD_TOP - 8
        rule_w = 220
        rule_x = (SIZE - rule_w) // 2
        draw.line(
            [(rule_x, rule_y), (rule_x + rule_w, rule_y)],
            fill=RULE,
            width=1,
        )

        img.save(OUTPUT_PATH, format="PNG", optimize=True)

    print(f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}  ({SIZE}x{SIZE})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
