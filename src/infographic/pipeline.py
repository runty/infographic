import logging
from pathlib import Path

from google import genai

from infographic.config import AppConfig, get_api_key, get_palette_colors, PALETTE_MAP
from infographic.generator.nano_banana import generate_image
from infographic.postprocess.eink import reduce_to_palette, resize_image
from infographic.prompt.composer import compose_prompt
from infographic.sources import SOURCES
from infographic.sources.base import SourceResult
from infographic.themes import get_theme

logger = logging.getLogger(__name__)


def _source_config_dict(config: AppConfig, name: str) -> dict:
    source_cfg = getattr(config.sources, name, None)
    if source_cfg is None:
        return {}
    return source_cfg.model_dump()


def run_pipeline(
    config: AppConfig,
    *,
    width: int,
    height: int,
    aspect_ratio: str,
    theme_slug: str,
    palette: str | None,
    colors: int,
    output: Path,
    sources_filter: list[str] | None,
    dark_mode: bool,
    dry_run: bool,
    resolution: str,
) -> Path | None:
    # 1. Collect data from enabled sources
    results: list[SourceResult] = []
    for name, source_cls in SOURCES.items():
        # Skip if filtered out
        if sources_filter and name not in sources_filter:
            continue
        # Skip if disabled in config
        source_cfg = _source_config_dict(config, name)
        if not source_cfg.get("enabled", True):
            continue

        source = source_cls()
        try:
            result = source.collect(source_cfg)
            if result.items:
                results.append(result)
                logger.info(f"Source '{name}': collected {len(result.items)} items")
            else:
                logger.info(f"Source '{name}': no items")
        except Exception as e:
            logger.warning(f"Source '{name}' failed: {e}")

    if not results:
        raise RuntimeError("No data collected from any source. Cannot generate infographic.")

    # 2. Determine color constraint text
    color_constraint = None
    if palette:
        field = PALETTE_MAP.get(palette, palette)
        color_constraint = f"Use ONLY these colors: {palette} palette ({getattr(config.eink.palettes, field, [])})"
    elif colors > 0:
        color_constraint = f"Use at most {colors} distinct colors."

    # 3. Compose image prompt via Gemini
    theme = get_theme(theme_slug)
    api_key = get_api_key(config)
    client = genai.Client(api_key=api_key)

    image_prompt = compose_prompt(
        client=client,
        model=config.api.composer_model,
        results=results,
        theme=theme,
        aspect_ratio=aspect_ratio,
        color_constraint=color_constraint,
        dark_mode=dark_mode,
    )

    if dry_run:
        print("=== COMPOSED IMAGE PROMPT ===")
        print(image_prompt)
        print("=== END PROMPT ===")
        return None

    # 4. Generate image via Nano Banana 2
    raw_image = generate_image(
        client=client,
        model=config.api.generator_model,
        prompt=image_prompt,
        aspect_ratio=aspect_ratio,
        image_size=resolution,
    )

    # 5. Post-process: resize
    raw_image = resize_image(raw_image, width, height)

    # 6. Post-process: color reduction for e-ink
    if palette:
        palette_colors = get_palette_colors(config, palette)
        raw_image = reduce_to_palette(
            raw_image,
            palette_colors,
            dither=config.eink.dither,
        )
    elif colors > 0:
        # Generic quantization to N colors
        raw_image = raw_image.quantize(colors=colors).convert("RGB")

    # 7. Save
    output.parent.mkdir(parents=True, exist_ok=True)
    raw_image.save(str(output))
    logger.info(f"Saved infographic to {output}")
    return output
