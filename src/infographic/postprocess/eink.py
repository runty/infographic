import logging

from PIL import Image

logger = logging.getLogger(__name__)


def reduce_to_palette(
    img: Image.Image,
    palette_colors: list[tuple[int, int, int]],
    dither: bool = True,
) -> Image.Image:
    num_colors = len(palette_colors)
    logger.info(f"Reducing to {num_colors}-color palette, dither={dither}")

    # Special case: 2-color black and white
    if num_colors == 2 and palette_colors == [(0, 0, 0), (255, 255, 255)]:
        gray = img.convert("L")
        if dither:
            return gray.convert("1", dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
        else:
            return gray.point(lambda x: 255 if x > 128 else 0).convert("RGB")

    # Build a palette image for quantization
    palette_img = Image.new("P", (1, 1))
    flat_palette = []
    for r, g, b in palette_colors:
        flat_palette.extend([r, g, b])
    # Pad to 256 entries (768 bytes total)
    flat_palette.extend([0] * (768 - len(flat_palette)))
    palette_img.putpalette(flat_palette)

    # Quantize to the exact palette
    dither_mode = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    quantized = img.convert("RGB").quantize(
        colors=num_colors,
        palette=palette_img,
        dither=dither_mode,
    )

    return quantized.convert("RGB")


def resize_image(
    img: Image.Image,
    width: int,
    height: int,
) -> Image.Image:
    if img.size == (width, height):
        return img
    logger.info(f"Resizing from {img.size[0]}x{img.size[1]} to {width}x{height}")
    return img.resize((width, height), Image.Resampling.LANCZOS)
