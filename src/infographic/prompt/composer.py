import logging
from datetime import datetime

from google import genai

from infographic.sources.base import SourceResult
from infographic.themes.catalog import Theme

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are an expert infographic designer and visual artist. Given data items and a visual theme, \
compose a single detailed text-to-image prompt that describes a stunning, creative infographic.

SCENE VARIANCE — CRITICAL:
- Every generation MUST create a UNIQUE, FRESH scene. NEVER repeat the same composition twice.
- The theme describes a STYLE and MOOD, not a fixed scene. Invent a NEW specific scene each time \
that fits the theme's style. For example, a "Scenic Landscape" theme could be: a coastal cliff \
at sunset, a misty bamboo forest, a sunflower field with distant windmills, a snowy alpine lake, \
a cherry blossom park overlooking a city, a desert canyon at golden hour — each time DIFFERENT.
- Vary the specific setting, camera angle, weather, season, lighting, and composition.
- The theme's art style, font choices, and text integration rules stay consistent — but the \
SCENE ITSELF should surprise and delight every time.

CRITICAL DESIGN PHILOSOPHY:
- Do NOT use generic section headers like "Top Stories", "Daily Briefing", "Words of Wisdom", \
"Chinese Proverb", "World Headlines", or any category labels.
- Instead, ARTFULLY and CREATIVELY integrate all content directly into the visual design.
- Headlines, quotes, proverbs, and dates should flow naturally into the composition as part of \
the artwork itself — woven into the theme's visual language.
- Think of this as a beautiful poster or art print that happens to contain information, NOT a \
newspaper layout with labeled boxes.
- Each piece of content should be placed with artistic intent: a proverb might be rendered as \
brushwork calligraphy flowing along a mountain ridge; headlines might appear as fragments on \
torn paper, etched into stone, projected on screens, written in stars, etc.
- The date can be subtle — embossed, watermarked, or integrated into a decorative element.

THEME IS EVERYTHING:
- The visual theme must DOMINATE the entire image. It is not a subtle accent — it defines \
every pixel: the background, the textures, the typography, the borders, the atmosphere, the lighting.
- If the theme is "Space Mission", the image should look like a mission control screen with \
glowing HUD elements, star fields, and data readouts — not a white page with rocket clip art.
- If the theme is "Japanese Ink", the entire image should be a sumi-e painting with ink wash \
mountains, bamboo, and calligraphic text — not text boxes on a white background with a bamboo border.
- Push the theme to its extreme. Make it unmistakable. A viewer should instantly recognize \
the theme from a thumbnail.

TYPOGRAPHY MUST MATCH THE THEME:
- The font style for ALL text in the image MUST match the visual theme. This is NON-NEGOTIABLE.
- The theme description specifies exact font styles — follow them precisely.
- NEVER use generic default fonts. NEVER use plain Arial or Times New Roman unless the theme \
specifically calls for it.
- Every piece of text should look like it BELONGS in the theme's world:
  * A steampunk theme needs Victorian industrial letterpress fonts
  * A comic theme needs bold hand-lettered comic book fonts
  * A Japanese ink theme needs calligraphic brushwork
  * A space theme needs futuristic tech/HUD fonts
  * A lo-fi anime theme needs rounded, soft, friendly fonts
- If the theme specifies a font style, REPEAT that font style instruction prominently in your \
prompt for every text element.

TEXT LEGIBILITY — CRITICAL:
- ALL text MUST be LARGE ENOUGH TO READ at a glance. This is the #1 priority after theme.
- Text elements must be in the FOREGROUND or on CLOSE-UP objects, NEVER on tiny distant signs \
or far-away surfaces where they shrink to illegible sizes.
- The MINIMUM text size for any element should be what you'd comfortably read on a poster from \
3 feet away. If text would be too small to read, make the object it's on BIGGER and CLOSER.
- Headlines should be BOLD and PROMINENT — the largest text in the image.
- Quotes and proverbs should be medium-large — clearly readable without squinting.
- Even the smallest text (date, attributions, source names) must still be legible.
- NEVER put important text on small or distant objects. Bring them to the foreground.

TEXT RENDERING RULES:
- ONLY include HEADLINES (short titles) and SHORT TEXT (quotes, proverbs, dates).
- NEVER include URLs, links, web addresses, or "https://..." in the prompt.
- NEVER include long descriptions, summaries, or paragraphs — the image model CANNOT render \
these legibly and they will come out garbled.
- Keep each text item to ONE SHORT LINE wherever possible. If a headline is very long, \
truncate it to the most important words.
- For each text element, specify EXACTLY how it should appear: the font style, size relative \
to other elements (large, medium, small), color, and physical treatment (carved, printed, \
glowing, handwritten, etc.)

Your prompt MUST specify:
- A FULLY IMMERSIVE scene in the theme's world where content is organically embedded
- The EXACT FONT STYLE for each text element, matching the theme
- Visual hierarchy through size, weight, position, and artistic treatment — not through headers
- How each piece of text physically manifests within the theme's world
- Rich atmospheric details: lighting, texture, depth, mood
- Color scheme and palette that reinforces the theme

RULES:
- Output ONLY the image generation prompt. No explanations, no preamble.
- Include the headline text and quote/proverb text verbatim — but NEVER include URLs or long \
descriptions.
- NEVER include category labels or section headers. The content speaks for itself.
- Keep the prompt under 2000 words.
"""


def compose_prompt(
    client: genai.Client,
    model: str,
    results: list[SourceResult],
    theme: Theme,
    aspect_ratio: str,
    color_constraint: str | None = None,
    dark_mode: bool = False,
) -> str:
    # Build the data section
    data_sections = []
    for result in results:
        data_sections.append(result.to_text())

    data_text = "\n\n".join(data_sections)

    user_message = f"""DATA TO INCLUDE IN THE INFOGRAPHIC:

{data_text}

VISUAL THEME: {theme.name}
{theme.style_prompt}

TARGET ASPECT RATIO: {aspect_ratio}
"""

    # Sundial mode: when dark_mode is not explicitly set, match the time of day
    use_dark = dark_mode
    if not dark_mode:
        hour = datetime.now().hour
        if 5 <= hour < 8:
            user_message += (
                "\nTIME OF DAY — EARLY MORNING / DAWN: The scene takes place at dawn. Soft golden-pink "
                "light is just breaking over the horizon. Long shadows, cool blue undertones giving way "
                "to warm amber. Dew on surfaces. The world is waking up — quiet, fresh, gentle. "
                "If the scene has a window or outdoor view, show a sunrise sky in peach, coral, and "
                "pale lavender. Interior scenes have soft, diffused early light.\n"
            )
        elif 8 <= hour < 12:
            user_message += (
                "\nTIME OF DAY — MORNING: The scene is bathed in bright, cheerful morning light. "
                "Warm white sunlight streams in at an angle. Crisp shadows, vibrant colors, the "
                "energy of a fresh day. Blue skies if outdoor or visible through windows. "
                "Everything feels awake and optimistic.\n"
            )
        elif 12 <= hour < 15:
            user_message += (
                "\nTIME OF DAY — MIDDAY / AFTERNOON: Bright, direct overhead sunlight. High contrast, "
                "short shadows. Vivid, saturated colors. If outdoors, a clear or partly cloudy sky. "
                "The scene feels warm and fully lit — peak daylight energy.\n"
            )
        elif 15 <= hour < 18:
            user_message += (
                "\nTIME OF DAY — LATE AFTERNOON / GOLDEN HOUR: Rich, warm golden light pouring in "
                "from a low angle. Long dramatic shadows. Everything glows amber and honey-gold. "
                "The light is cinematic and beautiful — the 'magic hour' photographers love. "
                "Warm tones dominate: gold, orange, soft red, warm brown.\n"
            )
        elif 18 <= hour < 21:
            use_dark = True
            user_message += (
                "\nTIME OF DAY — SUNSET / EVENING: The scene takes place at sunset or dusk. The sky "
                "is ablaze with deep orange, magenta, and purple gradients fading to dark blue. "
                "City lights and neon signs are flickering on. Interior scenes are lit by warm "
                "artificial light — lamps, candles, screens. The mood is reflective and winding down.\n"
            )
        else:  # 21-5
            use_dark = True
            user_message += (
                "\nTIME OF DAY — NIGHT: The scene takes place at night. Deep dark sky with stars "
                "or city glow. Artificial lighting only — warm lamp light, neon signs, screen glow, "
                "moonlight, streetlights. Rich contrast between pools of light and deep shadows. "
                "The mood is contemplative, quiet, intimate. If a cityscape is visible, it sparkles "
                "with thousands of lit windows and colorful signs.\n"
            )

    if use_dark:
        user_message += (
            "\nDARK MODE: The overall image MUST have a predominantly DARK background — deep blacks, "
            "dark grays, dark navy, or dark theme-appropriate colors. All text must be LIGHT-colored "
            "(white, cream, light gray, or bright accent colors) for high contrast against the dark "
            "background. The image should look comfortable on a dark desktop or dark-themed device. "
            "Avoid large bright or white areas. Embrace shadows, night scenes, low-key lighting, "
            "and moody atmospherics. If the theme is naturally light (e.g., a cafe scene), shift it "
            "to a nighttime or evening version.\n"
        )

    if color_constraint:
        user_message += f"\nCOLOR CONSTRAINT: {color_constraint}\n{theme.color_hints}\n"

    logger.info(f"Composing prompt with model={model}")
    response = client.models.generate_content(
        model=model,
        contents=[SYSTEM_PROMPT + "\n\n" + user_message],
    )

    prompt = response.text
    if not prompt:
        raise RuntimeError("Gemini returned empty prompt composition")

    logger.debug(f"Composed prompt ({len(prompt)} chars)")
    return prompt
