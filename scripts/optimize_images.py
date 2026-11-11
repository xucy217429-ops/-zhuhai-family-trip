from pathlib import Path
from PIL import Image, ImageOps

SOURCE_DIR = Path("assets/source")
OUTPUT_DIR = Path("public/assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Keep source JPEGs in the repository; only optimized WebP files are published.
for source in sorted(SOURCE_DIR.glob("*.jpg")):
    image = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    stem = source.stem
    for target_width in (480, 1200):
        width = min(target_width, image.width)
        height = round(image.height * width / image.width)
        resized = image if width == image.width else image.resize((width, height), Image.Resampling.LANCZOS)
        output = OUTPUT_DIR / f"{stem}-{target_width}.webp"
        resized.save(output, "WEBP", quality=76, method=6)
        print(f"{output}: {output.stat().st_size:,} bytes")
