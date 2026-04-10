import io
import logging

from google import genai
from google.genai import types
from PIL import Image

logger = logging.getLogger(__name__)


def generate_image(
    client: genai.Client,
    model: str,
    prompt: str,
    aspect_ratio: str = "16:9",
    image_size: str = "1K",
) -> Image.Image:
    logger.info(f"Generating image with model={model}, ratio={aspect_ratio}, size={image_size}")

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=image_size,
            ),
        ),
    )

    usage = response.usage_metadata
    if usage:
        logger.info(
            f"Image gen tokens — in: {usage.prompt_token_count}, "
            f"out: {usage.candidates_token_count}, "
            f"total: {usage.total_token_count}"
        )

    for part in response.parts:
        if part.inline_data is not None:
            # Convert google.genai Image to PIL Image
            image_bytes = part.inline_data.data
            pil_image = Image.open(io.BytesIO(image_bytes))
            logger.info(f"Generated image: {pil_image.size[0]}x{pil_image.size[1]}")
            return pil_image

    raise RuntimeError(
        "Nano Banana 2 returned no image. This may be due to content policy "
        "restrictions or API overload. Try adjusting the prompt or retrying."
    )
