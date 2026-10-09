#!/usr/bin/env python3
"""
Generate the site's favicons and app icons from the GitHub org avatar, so
the browser tab, the home-screen icon and the org share one mark.

Input:   static/images/org-avatar.jpg  (1024 x 1024: brass lens, firefly,
         red thread on navy)

Output:  static/favicon.ico           16, 32, 48   tight crop
         static/favicon-32.png        32           tight crop
         static/apple-touch-icon.png  180          full art
         static/icon-192.png          192          full art
         static/icon-512.png          512          full art

The tight crop frames the lens so its ring fills the tile and still reads
at 16 px; the large icons keep the full art and its margin, which survives
a platform's rounded-corner mask.

Deterministic: given the same input and this script, produces the same
bytes (Pillow, LANCZOS resampling, no timestamps in PNG or ICO).

Dependencies (Python 3):  Pillow
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "static" / "images" / "org-avatar.jpg"
STATIC = REPO_ROOT / "static"

SOURCE_SIZE = (1024, 1024)
# Box around the lens and the top of its handle, in source pixels.
TIGHT_BOX = (150, 80, 890, 820)


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: missing input: {SOURCE}", file=sys.stderr)
        return 1
    src = Image.open(SOURCE).convert("RGB")
    if src.size != SOURCE_SIZE:
        print(f"error: {SOURCE.name} is {src.size}, expected {SOURCE_SIZE}", file=sys.stderr)
        return 1

    tight = src.crop(TIGHT_BOX)

    tight.resize((48, 48), Image.LANCZOS).save(
        STATIC / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)]
    )
    tight.resize((32, 32), Image.LANCZOS).save(STATIC / "favicon-32.png", optimize=True)
    for name, size in (("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
        src.resize((size, size), Image.LANCZOS).save(STATIC / name, optimize=True)

    print("wrote favicon.ico, favicon-32.png, apple-touch-icon.png, icon-192.png, icon-512.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
