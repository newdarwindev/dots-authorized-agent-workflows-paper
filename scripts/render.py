#!/usr/bin/env python3
"""Render every slide/page and make reviewer contact sheets."""
import argparse
import shutil
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--pdf-dir", type=Path, default=ROOT / "build")
args = p.parse_args()
dest = ROOT / "docs/review"
dest.mkdir(parents=True, exist_ok=True)
for source, name in (("deck", "argument"), ("deck-evidence", "evidence"), ("deck-fleet", "fleet"), ("paper", "paper")):
    folder = ROOT / "build/render" / name
    folder.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdftoppm", "-scale-to", "1200", "-png", str(args.pdf_dir / f"{source}.pdf"), str(folder / "page")], check=True)
    images = [Image.open(path).convert("RGB") for path in sorted(folder.glob("page-*.png"))]
    width, height = 1200, max(im.height for im in images)
    canvas = Image.new("RGB", (2 * (width + 16), ((len(images) + 1) // 2) * (height + 16)), "#d8e0e7")
    for i, im in enumerate(images):
        canvas.paste(im, (8 + (i % 2) * (width + 16), 8 + (i // 2) * (height + 16)))
    canvas.save((dest / f"{name}.png") if name != "paper" else (folder / "contact.png"), optimize=True)
    if name != "paper":
        choices = Image.new("RGB", (2 * (width + 16), height + 16), "#d8e0e7")
        for i, index in enumerate((4, 6)):
            choices.paste(images[index], (8 + i * (width + 16), 8))
        choices.save(dest / f"{name}-choices.png", optimize=True)
        shutil.copy2(args.pdf_dir / f"{source}.pdf", dest / f"{name}.pdf")
print("Rendered all pages; reviewer contact sheets and three PDFs staged")
