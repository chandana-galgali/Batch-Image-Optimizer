#!/usr/bin/env python3
"""Batch Image Optimizer — dependency-light CLI for local image processing."""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parent
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
FORMATS = {"jpeg": ("JPEG", ".jpg"), "png": ("PNG", ".png"), "webp": ("WEBP", ".webp")}


@dataclass(frozen=True)
class Result:
    source: Path
    destination: Path | None
    original_bytes: int
    output_bytes: int
    error: str | None = None


def unique_path(directory: Path, stem: str, extension: str) -> Path:
    candidate = directory / f"{stem}{extension}"
    index = 1
    while candidate.exists():
        candidate = directory / f"{stem}_{index}{extension}"
        index += 1
    return candidate


def optimize_image(source: Path, output_dir: Path, max_width: int, max_height: int,
                   quality: int = 75, output_format: str = "jpeg") -> Result:
    """Resize without upscaling, respect EXIF rotation and avoid overwrites."""
    original_bytes = source.stat().st_size
    try:
        with Image.open(source) as original:
            # Normalize EXIF orientation before dimensions are calculated.
            image = ImageOps.exif_transpose(original)
            image.seek(0) if getattr(image, "n_frames", 1) > 1 else None
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            width, height = image.size
            fmt, extension = FORMATS[output_format]
            if fmt == "JPEG":
                # Alpha cannot be encoded as JPEG: composite on white instead of dropping it.
                if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
                    rgba = image.convert("RGBA")
                    background = Image.new("RGB", rgba.size, "white")
                    background.paste(rgba, mask=rgba.getchannel("A"))
                    image = background
                else:
                    image = image.convert("RGB")
            elif fmt == "PNG":
                image = image.convert("RGBA" if "A" in image.getbands() or "transparency" in image.info else "RGB")
            else:
                image = image.convert("RGBA" if "A" in image.getbands() or "transparency" in image.info else "RGB")
            output_dir.mkdir(parents=True, exist_ok=True)
            destination = unique_path(output_dir, f"{source.stem}_{width}x{height}", extension)
            options = {"optimize": True}
            if fmt != "PNG":
                options["quality"] = quality
            if fmt == "JPEG":
                options["progressive"] = True
            try:
                image.save(destination, format=fmt, **options)
            except Exception:
                destination.unlink(missing_ok=True)
                raise
            return Result(source, destination, original_bytes, destination.stat().st_size)
    except (OSError, ValueError, UnidentifiedImageError) as exc:
        return Result(source, None, original_bytes, 0, str(exc))


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def quality_int(value: str) -> int:
    number = int(value)
    if not 1 <= number <= 100:
        raise argparse.ArgumentTypeError("must be between 1 and 100")
    return number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resize and optimize images locally; no uploads.")
    parser.add_argument("--input", type=Path, default=ROOT / "images/input", help="Input folder (default: images/input)")
    parser.add_argument("--output", type=Path, default=ROOT / "images/output", help="Output folder (default: images/output)")
    parser.add_argument("--max-width", type=positive_int, default=1920)
    parser.add_argument("--max-height", type=positive_int, default=1080)
    parser.add_argument("--quality", type=quality_int, default=75)
    parser.add_argument("--format", choices=tuple(FORMATS), default="jpeg")
    args = parser.parse_args(argv)
    source_dir = args.input.expanduser().resolve()
    dest_dir = args.output.expanduser().resolve()
    if not source_dir.is_dir():
        print(f"Input folder not found: {source_dir}", file=sys.stderr)
        return 2
    if source_dir == dest_dir:
        print("Input and output folders must be different.", file=sys.stderr)
        return 2
    candidates = sorted(p for p in source_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED)
    if not candidates:
        print(f"No supported images found in {source_dir}")
        return 0
    successes, failures, before, after = 0, 0, 0, 0
    for source in candidates:
        result = optimize_image(source, dest_dir, args.max_width, args.max_height, args.quality, args.format)
        if result.error:
            failures += 1
            print(f"FAIL {source.name}: {result.error}")
        else:
            successes += 1
            before += result.original_bytes
            after += result.output_bytes
            delta = (1 - result.output_bytes / result.original_bytes) * 100 if result.original_bytes else 0
            print(f" OK  {source.name} -> {result.destination.name} ({delta:+.1f}% smaller)")
    savings = (1 - after / before) * 100 if before else 0
    print(f"\nFinished: {successes} succeeded, {failures} failed | total size change: {savings:+.1f}% smaller")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
