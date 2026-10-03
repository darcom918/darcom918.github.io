"""
Creates small, fast WebP copies of the photos for phones and tablets.

The original files are never changed, renamed or moved. Copies are written to
assets/images/opt/ as <name>-480.webp and <name>-800.webp and are used through
`srcset` in the HTML, so the browser picks the right size automatically.

After replacing a photo in assets/images/ais/ (keep the same file name), run:
    python tools/optimize-images.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCES = [ROOT / "assets/images/ais", ROOT / "assets/images/banners-user"]
OUT = ROOT / "assets/images/opt"
WIDTHS = (480, 800)

OUT.mkdir(parents=True, exist_ok=True)
for folder in SOURCES:
    for src in sorted(folder.iterdir()):
        if src.suffix.lower() not in (".webp", ".jpg", ".jpeg", ".png") or src.name.startswith("logo"):
            continue
        with Image.open(src) as im:
            im = im.convert("RGB")
            for w in WIDTHS:
                if im.width <= w:
                    continue
                h = round(im.height * w / im.width)
                dst = OUT / f"{src.stem}-{w}.webp"
                im.resize((w, h), Image.LANCZOS).save(dst, "WEBP", quality=78, method=6)
                print(f"{dst.relative_to(ROOT)}  {dst.stat().st_size // 1024} KB")
