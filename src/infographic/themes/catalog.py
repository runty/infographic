import random
from dataclasses import dataclass


@dataclass
class Theme:
    name: str
    slug: str
    description: str
    style_prompt: str
    color_hints: str


THEMES: dict[str, Theme] = {}


def _register(theme: Theme) -> None:
    THEMES[theme.slug] = theme


def get_theme(slug: str) -> Theme:
    if slug not in THEMES:
        raise ValueError(f"Unknown theme '{slug}'. Available: {', '.join(THEMES.keys())}")
    theme = THEMES[slug]
    # Dynamic style for headline theme — randomize Lego vs Pixar each call
    if slug == "headline" and hasattr(theme, "_style_fn"):
        return Theme(
            name=theme.name, slug=theme.slug, description=theme.description,
            style_prompt=theme._style_fn(),
            color_hints=theme.color_hints,
        )
    return theme


def list_themes() -> list[Theme]:
    return list(THEMES.values())


# --- Theme Definitions ---

_register(Theme(
    name="Scenic Landscape",
    slug="scenic_landscape",
    description="Studio Ghibli anime landscape with dreamy atmosphere",
    style_prompt=(
        "Rendered in the LUSH, PAINTERLY style of Studio Ghibli / Hayao Miyazaki anime — soft "
        "watercolor-like cel shading with warm, saturated colors. INVENT A NEW LANDSCAPE SCENE "
        "each time — vary between: rolling green hills with a village, coastal cliffs over a "
        "sparkling ocean, a misty bamboo forest with a hidden shrine, a sunflower field stretching "
        "to the horizon, a snowy alpine lake reflecting mountains, a cherry blossom park overlooking "
        "a city, a terraced rice paddy valley, a desert canyon with red rock formations, a lavender "
        "field in Provence, a Scottish highland with a castle ruin. Each generation should be a "
        "COMPLETELY DIFFERENT landscape — surprise the viewer every time. "
        "Text content is woven INTO the landscape on LARGE, CLOSE-UP objects in the FOREGROUND — "
        "wooden signposts, stone markers, carved rocks, painted fences, hanging banners — so text "
        "is LARGE and easily readable. Place these text-bearing objects close to the viewer in the "
        "near foreground, with the vast landscape stretching into the beautiful distance behind them. "
        "Headlines in a warm handwritten Japanese-poster font with LARGE LEGIBLE lettering. "
        "Quotes flow across the sky or are carved into prominent foreground features. "
        "Proverbs on a mossy stone wall or wooden gate in the immediate foreground. "
        "Tiny Ghibli details everywhere — butterflies, small animals, laundry on a line, "
        "windblown grass. Use rounded, soft ANIME typography — handwritten brush-style fonts for "
        "quotes and clean rounded sans-serif for headlines. "
        "The feeling of Howl's Moving Castle, My Neighbor Totoro, and Kiki's Delivery Service. "
        "Warm, nostalgic, impossibly beautiful — you want to step into this world."
    ),
    color_hints="Works best with 7+ colors. In BW, the soft gradients create lovely tonal variation.",
))

_register(Theme(
    name="Daily Briefing",
    slug="daily_briefing",
    description="Lo-fi anime study desk with coffee and morning light",
    style_prompt=(
        "Rendered in COZY LO-FI BEATS anime aesthetic — soft flat colors, warm lighting, gentle "
        "purple and amber tones. The scene is viewed from a slightly elevated angle at a charming "
        "anime-style desk positioned right by a LARGE floor-to-ceiling window that takes up at least "
        "HALF the image. Through the window: a DETAILED, VIBRANT anime cityscape — a random mix of "
        "rooftops, neon signs, water towers, bridges, train tracks, cherry blossom trees, power lines, "
        "distant skyscrapers, and winding streets. The city should be richly detailed and different "
        "every time — sometimes a Tokyo-like dense urban scene, sometimes a European rooftop vista, "
        "sometimes a coastal city with a harbor visible, sometimes a rainy neon-lit night scene. "
        "The cityscape is the BACKDROP STAR of the image, not just a blurred afterthought. "
        "On the desk: a steaming cup of coffee with visible steam wisps animated-style, a folded "
        "newspaper with headlines visible in clean sans-serif type, an open notebook with handwritten "
        "notes (the quotes rendered in a casual handwriting font), sticky notes with proverbs in "
        "brush script, a small potted succulent, scattered pens, and a phone showing the date. "
        "A small fluffy BLACK AND WHITE HAVANESE PUPPY is curled up sleeping on the desk or on a "
        "cushion nearby — adorable, with distinctive silky black and white fur, floppy ears, and a "
        "little black nose. Headphones rest on a stack of books. "
        "The art style is DISTINCTLY lo-fi anime: soft cel shading, slightly desaturated warm palette "
        "(dusty pink, lavender, warm cream, soft teal), visible but gentle outlines, and that "
        "signature lo-fi CHILL atmosphere. Typography uses clean rounded sans-serif fonts for "
        "headlines (like Quicksand or Nunito), casual handwriting for quotes, and a cute monospace "
        "for the date. Rain dots on the window. The whole image radiates calm productivity — "
        "the visual equivalent of 'lofi hip hop radio - beats to relax/study to'."
    ),
    color_hints="Excellent in BW and BWR. The flat anime shading preserves well with limited colors.",
))

_register(Theme(
    name="Retro Comic",
    slug="retro_comic",
    description="Explosive vintage comic book with action panels",
    style_prompt=(
        "A FULL comic book page in authentic 1960s Marvel/DC style — bold black ink outlines, "
        "vibrant Ben-Day halftone dot patterns in primary red, blue, and yellow, heavy crosshatching. "
        "The page is divided into dynamic TILTED panels at dramatic angles showing an action scene: "
        "a superhero reading a newspaper mid-flight, a villain's lair with screens showing headlines, "
        "a city skyline with news ticker scrolling across buildings. Text content appears in SPEECH "
        "BUBBLES, THOUGHT CLOUDS, dramatic CAPTION BOXES with yellow backgrounds, and bold "
        "onomatopoeia (POW! ZAP! NEWS!) bursting out of panels. Headlines are screamed by a "
        "newspaper boy character. Quotes appear in a wise old mentor's speech bubble. The date "
        "is stamped in the corner like a comic issue number: 'ISSUE #408 — APRIL 2026'. "
        "ALL typography in BOLD BLOCKY COMIC BOOK LETTERING — uppercase, slightly uneven, hand-"
        "lettered feel. Captions in italic narration boxes. Sound effects in explosive display fonts. "
        "Weathered newsprint paper texture, slight yellowing, ink bleed at edges. MAXIMUM ENERGY."
    ),
    color_hints="Works in BWR with red accents. BW mode enhances the classic comic feel.",
))

_register(Theme(
    name="Technical Blueprint",
    slug="technical_blueprint",
    description="Engineering blueprint of a fantastical machine",
    style_prompt=(
        "A gorgeous LARGE-FORMAT engineering blueprint. Rich Prussian blue background with precise "
        "white and cyan technical line work. INVENT A NEW FANTASTICAL MACHINE each time — vary "
        "between: a submersible exploration vessel, a flying clockwork airship, a steam-powered "
        "analytical engine, a space elevator cross-section, a mechanical dragon automaton, a "
        "perpetual motion machine, a time-travel device, a giant walking castle mechanism, a "
        "terraforming engine, a deep-sea mining platform. DIFFERENT invention every time. "
        "The machine's components are labeled with the actual content: headlines appear as component "
        "specifications in technical callout boxes with leader lines pointing to machine parts, "
        "quotes etched onto brass nameplates, proverbs written in the chief engineer's annotation "
        "handwriting in the margins. The date in the formal title block in the lower-right corner. "
        "ALL typography in MONOSPACE TECHNICAL DRAFTING FONTS — like Courier, OCR-A, or DIN 1451 "
        "Engschrift. Labels in precise uppercase engineering lettering. Handwritten annotations in "
        "a scratchy technical hand. Title block text in condensed sans-serif. "
        "Include crosshatch shading, dimension lines, section cut views, exploded assembly diagrams. "
        "Compass rose in one corner. Blueprint paper with fold creases and worn edges."
    ),
    color_hints="Naturally works in 2-3 colors. BW inverts to white-on-dark beautifully.",
))

_register(Theme(
    name="Vintage Poster",
    slug="vintage_poster",
    description="Bold 1930s Art Deco travel poster",
    style_prompt=(
        "A STUNNING 1930s Art Deco travel poster in the style of A.M. Cassandre or the WPA national "
        "parks series. Bold geometric shapes, dramatic forced perspective, and a LIMITED palette of "
        "4-5 flat colors: deep navy, burnt orange, cream, forest green, and metallic gold. A grand "
        "architectural scene — a towering Art Deco skyscraper, a streamlined locomotive, or a "
        "majestic bridge — dominates the composition with powerful diagonal lines converging to a "
        "vanishing point. ALL typography in TALL, ULTRA-CONDENSED ART DECO DISPLAY TYPEFACES — "
        "like Broadway, Bifur, Peignot, or Futura Display. Headlines stacked vertically along the "
        "architecture in geometric letterforms. Quotes on marquee signs in condensed gothic. "
        "The date rendered as 'APRIL 8, 2026' in metallic gold lettering across a banner in an "
        "ornamental frame. Proverbs carved into the building's cornerstone in chiseled Roman capitals. "
        "ZERO gradients — only flat color blocks with sharp edges. Subtle linen paper texture. "
        "Museum-quality lithograph print worth framing."
    ),
    color_hints="Designed for limited palettes. Excellent in 7-color and even BWR mode.",
))

_register(Theme(
    name="Cozy Cafe",
    slug="cozy_cafe",
    description="Lo-fi anime cafe with rain and warm lights",
    style_prompt=(
        "Rendered in DREAMY LO-FI ANIME aesthetic with soft flat anime cel-shading. "
        "INVENT A NEW COZY SCENE each time — vary between: a corner cafe with rain-streaked windows, "
        "a bookshop nook with floor-to-ceiling shelves, a rooftop garden terrace at golden hour, "
        "a train compartment window seat with passing countryside, a cozy bedroom with fairy lights "
        "and a window seat, a vintage record shop with listening station, a greenhouse studio full "
        "of plants, a houseboat cabin gently rocking on a canal. DIFFERENT setting every time. "
        "The scene always includes: a steaming drink, scattered newspaper clippings or papers with "
        "headlines in a rounded sans-serif font, something handwritten with quotes in elegant cursive, "
        "a chalkboard or sign with proverbs in chalk-style font, and a cute daily calendar or phone "
        "showing the date. A small fluffy BLACK AND WHITE HAVANESE PUPPY sleeps somewhere in the "
        "scene — adorable, with silky black and white fur and floppy ears. "
        "Color palette: dusty rose, warm amber, soft lavender, cream, sage green, muted teal. "
        "Gentle anime outlines, soft shadows, visible brush texture. Typography is rounded and "
        "friendly — Quicksand, Comfortaa, or similar soft sans-serif fonts. "
        "The visual equivalent of 'lofi hip hop radio - beats to relax/study to'. "
        "Peaceful, intimate, healing."
    ),
    color_hints="Works well in 7+ colors. In BW, the anime style creates clean tonal contrast.",
))

_register(Theme(
    name="Space Mission",
    slug="space_mission",
    description="Deep space command center with holographic displays",
    style_prompt=(
        "INVENT A NEW SCI-FI SCENE each time — vary between: the bridge of a starship approaching "
        "a ringed planet, a lunar outpost overlooking Earth from the Moon's surface, a space station "
        "observation deck watching a comet pass, the cockpit of a fighter during a nebula flythrough, "
        "a Mars colony command center with red desert outside, a deep space relay station orbiting "
        "a black hole, a generation ship's greenhouse dome with stars visible overhead, a mining "
        "platform in an asteroid field. DIFFERENT cosmic setting every time. "
        "The scene always includes: holographic floating displays showing headlines, glowing data "
        "readouts, a viewport or window showing the spectacular space environment, and instrument "
        "panels with text integrated as readouts and logs. "
        "Quotes materialize as translucent holograms. Proverbs etched into hull plating in alien-"
        "looking script alongside their translations. The date on the ship's chronometer. "
        "ALL typography in FUTURISTIC TECH FONTS — Eurostile Extended, Orbitron, Rajdhani, or "
        "Bank Gothic. Data readouts in monospace (Fira Code, JetBrains Mono). Holographic text "
        "has a thin glowing outline. HUD overlays use condensed all-caps with tracking. "
        "Dark atmosphere with dramatic neon lighting — cyan, amber, magenta accents. "
        "Cinematic sci-fi like Blade Runner meets The Expanse. Every surface gleams with purpose."
    ),
    color_hints="Excellent in BW with the dark background. 7-color adds dramatic glow effects.",
))

_register(Theme(
    name="Japanese Ink",
    slug="japanese_ink",
    description="Serene sumi-e ink wash painting with mountains and mist",
    style_prompt=(
        "A MASTERFUL traditional Japanese sumi-e ink wash painting spanning the entire image. "
        "INVENT A NEW INK WASH SCENE each time — vary between: misty mountains with a stone bridge "
        "over a koi pond, a windswept coastal cliff with crashing waves and a lone pine, a bamboo "
        "grove with a hidden temple path, a snow-covered village with smoke rising from thatched roofs, "
        "a waterfall cascading into a rocky gorge with a meditation pavilion, cranes flying over "
        "a moonlit lake, a cherry blossom grove beside a quiet stream, an ancient torii gate on a "
        "misty hillside. DIFFERENT composition every time. "
        "ALL text rendered in TRADITIONAL EAST ASIAN CALLIGRAPHIC BRUSHWORK — headlines flow "
        "vertically down hanging scroll banners in semi-cursive kaisho or gyosho style, quotes "
        "written on a stone lantern's base in elegant running script, proverbs in dramatic grass "
        "script (sosho) cascading like a waterfall. English text in a refined thin serif like "
        "Garamond or Minion, echoing the elegance of the brushwork. "
        "The date is rendered as a red seal stamp (hanko) pressed into the corner. "
        "Generous negative space — the empty areas are as important as the painted ones. "
        "Ink gradations from deep black to barely-there pale gray. Off-white washi paper texture "
        "with visible fibers. One single RED accent: the hanko seal. Contemplative, meditative, "
        "profoundly beautiful."
    ),
    color_hints="Perfect for BW mode. The ink wash style is naturally monochromatic. BWR adds the red seal accent.",
))

_register(Theme(
    name="Library Study",
    slug="library_study",
    description="Candlelit ancient library with illuminated manuscripts",
    style_prompt=(
        "The interior of a MAGNIFICENT candlelit medieval library — floor-to-ceiling oak shelves "
        "stuffed with leather-bound volumes, a massive carved desk in the center, warm golden "
        "candlelight flickering from ornate brass candelabras casting dramatic shadows. On the desk: "
        "an open illuminated manuscript with decorated borders in gold leaf, lapis blue, and "
        "vermillion red — the manuscript pages contain the actual headlines rendered in beautiful "
        "MEDIEVAL BLACKLETTER CALLIGRAPHY (Textura or Fraktur) with ornate illuminated drop capitals "
        "in gold and cobalt. Quotes written in an elegant COPPERPLATE SCRIPT on rolled parchment "
        "scrolls tied with wax-sealed ribbons. Proverbs carved into the wooden desk frame in "
        "ROMAN CAPITALIS (chiseled Roman square capitals). The date on a brass library clock in a "
        "classic ENGRAVED SERIF typeface. A globe, an astrolabe, a raven perched on books. "
        "Dust motes float in shafts of light from a rose window. Rich palette: mahogany, gold, "
        "deep red, hunter green, midnight blue. Atmospheric, reverent, magical — like stepping "
        "into Hogwarts' restricted section."
    ),
    color_hints="Works in 7+ colors for full warmth. BW mode creates a beautiful engraving effect.",
))

_register(Theme(
    name="Steampunk Workshop",
    slug="steampunk_workshop",
    description="Miyazaki anime steampunk workshop with flying machines",
    style_prompt=(
        "Rendered in STUDIO GHIBLI / HAYAO MIYAZAKI anime style with soft anime cel-shading and "
        "rich warm colors. INVENT A NEW STEAMPUNK SETTING each time — vary between: a flying airship "
        "workshop above the clouds, a clocktower interior with massive gears and pendulums, a "
        "locomotive engine room barreling through mountains, a submarine command deck with portholes "
        "showing deep sea, an observatory dome with a giant brass telescope, a printing press factory "
        "with mechanical typesetting, a Victorian greenhouse lab full of strange inventions, a "
        "dirigible bridge navigating through storm clouds. DIFFERENT workshop every time. "
        "A young anime inventor character is always present, tinkering at a workbench. A small "
        "robot assistant helps. Cheerful chaos of brass gears, bubbling flasks, steam pipes. "
        "Headlines are EMBOSSED on rotating brass cylinders in an ornate VICTORIAN DISPLAY TYPEFACE "
        "(like Playfair Display or Didot with decorative swashes). Quotes glow inside amber vacuum "
        "tubes in a warm COPPERPLATE ITALIC. Proverbs engraved on brass plaques in bold "
        "INDUSTRIAL SLAB-SERIF lettering (like Rockwell or Clarendon). The date on a magnificent "
        "mechanical calendar with interlocking wheels. Sparrows nest in the rafters. "
        "Color palette: warm brass gold, sky blue, copper green patina, rich wood brown, cream. "
        "Miyazaki's signature blend of whimsy, wonder, and warmth."
    ),
    color_hints="Works in 7+ colors for the brass warmth. BW creates dramatic industrial contrast.",
))

_register(Theme(
    name="Ocean Depths",
    slug="ocean_depths",
    description="Ghibli anime underwater world with glowing sea life",
    style_prompt=(
        "Rendered in a MAGICAL STUDIO GHIBLI / PONYO anime underwater style — a dreamlike deep-sea "
        "world with soft anime cel-shading and luminous colors. INVENT A NEW UNDERWATER SCENE each "
        "time — vary between: a sunken ancient temple overgrown with coral, a vast kelp forest with "
        "shafts of light, an underwater volcanic vent garden with strange creatures, a shipwreck "
        "graveyard with treasure, a crystal cave with bioluminescent pools, a coral reef city built "
        "by sea creatures, a deep ocean trench with alien-like life forms, a frozen underwater "
        "cavern beneath polar ice with ethereal blue light. DIFFERENT undersea world every time. "
        "The scene always includes: glowing jellyfish or sea creatures, marine life (whales, fish, "
        "seahorses, octopi), god-rays filtering from above, and marine snow drifting. "
        "Headlines appear as BIOLUMINESCENT text on sea creatures in a clean rounded ANIME TITLE "
        "FONT (like M PLUS Rounded or Kosugi Maru). Quotes float upward in translucent bubbles in "
        "an elegant THIN SANS-SERIF (like Raleway Light). Proverbs carved into underwater stone in "
        "WEATHERED ROMAN CAPITALS. The date etched into a giant clam shell in a playful HANDWRITTEN "
        "font. Color palette: deep midnight blue, electric cyan, soft purple, warm coral orange, "
        "bioluminescent green. Every creature glows with gentle anime magic. "
        "The wonder of Ponyo's underwater world meets the mystery of the deep."
    ),
    color_hints="7-color mode captures the bioluminescence. BW creates a dramatic deep-sea silhouette effect.",
))


# --- Headline Theme (dynamic style selection) ---

_HEADLINE_LEGO = (
    "Rendered as a PHOTOREALISTIC 3D CGI RENDER of LEGO bricks and minifigures — NOT drawn, NOT "
    "illustrated, NOT cartoon, NOT flat. This MUST look like a REAL PHOTOGRAPH of actual Lego pieces "
    "on a table, or like a frame from The Lego Movie with full 3D ray-traced rendering. Every brick "
    "must have REALISTIC plastic material — glossy sheen, subtle reflections, fingerprint smudges, "
    "visible injection mold seams on studs, sharp geometric edges. Characters are Lego minifigures "
    "with yellow skin, C-shaped hands, and blocky hair pieces. The environment is constructed "
    "entirely from Lego bricks, plates, and specialty pieces with visible studs, brick seams, and "
    "realistic plastic surface texture. Lighting is cinematic with soft shadows, ambient occlusion "
    "between bricks, depth of field blur, and slight tilt-shift to sell the miniature scale. "
    "CRITICAL: Read the headlines and identify the SINGLE BIGGEST, most dramatic story. Build the "
    "ENTIRE SCENE around depicting THAT story using Lego minifigs acting it out — politicians as "
    "minifigs at a Lego podium, tech stories as minifig engineers building a Lego computer, "
    "sports stories as minifig athletes on a Lego field, conflict stories as minifig soldiers "
    "with Lego vehicles. The scene should be IMMEDIATELY RECOGNIZABLE as that news story. "
    "MAKE THE SCENE BUSY AND PACKED WITH DETAIL. The main story dominates the center, but the "
    "edges and fringes of the image should be TEEMING with secondary Lego vignettes inspired by "
    "OTHER headlines — a tiny Lego newsroom in one corner with minifig anchors, a Lego stock "
    "ticker scrolling across a building, minifig protesters with tiny signs, a Lego construction "
    "crew building something related to a tech headline, a Lego courtroom drama playing out in "
    "the background, a miniature Lego sports stadium visible behind buildings, Lego delivery "
    "trucks with newspaper bundles, a Lego hot dog cart where minifigs read tiny newspapers. "
    "Every corner and background area should reward closer inspection with another headline-inspired "
    "micro-scene. Think of it like a Lego WHERE'S WALDO — dense, chaotic, delightful. "
    "Headlines appear on LEGO newspaper pieces, Lego TV screens, Lego billboards, Lego store "
    "signs, printed Lego tiles, sandwich board signs carried by minifigs, banners towed by Lego "
    "planes, scrolling text on Lego buses, and graffiti on Lego walls. Quotes appear on a Lego "
    "scroll held by a wise wizard minifigure. Proverbs on a Lego temple wall. The date on a "
    "Lego calendar brick. "
    "ALL typography in BOLD, CHUNKY, PLAYFUL block letters — like the Lego logo font or similar "
    "rounded bold sans-serif. Text on printed Lego tiles. Everything is fun, colorful, tactile. "
    "Bright primary colors: red, blue, yellow, green Lego bricks. Slight motion blur on moving "
    "pieces. The joyful, irreverent energy of The Lego Movie. EVERYTHING IS AWESOME."
)

_HEADLINE_PIXAR = (
    "Rendered as a FULL 3D CGI RENDER in the style of PIXAR ANIMATION STUDIOS — NOT 2D, NOT flat, "
    "NOT hand-drawn. This MUST look like a screenshot from a Pixar movie: PHOTOREALISTIC 3D "
    "computer-generated characters and environments with smooth plastic-like 3D surfaces, realistic "
    "3D lighting with global illumination, ray-traced reflections, ambient occlusion, depth of field "
    "blur, and volumetric fog/atmosphere. Characters are 3D MODELED with smooth rounded geometry, "
    "big glossy eyes with realistic light reflections in them, soft subsurface scattering on skin, "
    "individually rendered 3D hair strands, and exaggerated but fully THREE-DIMENSIONAL proportions. "
    "The rendering quality should be INDISTINGUISHABLE from an actual frame of Toy Story, The "
    "Incredibles, Up, Inside Out, or Soul. Think Renderman-quality 3D CGI. "
    "CRITICAL: Read the headlines and identify the SINGLE BIGGEST, most dramatic story. Build the "
    "ENTIRE 3D SCENE around depicting THAT story with Pixar-style 3D animated characters acting "
    "it out — politicians as stylized 3D caricature characters at a grand podium, tech stories as "
    "cute 3D robot characters in a futuristic lab, sports stories as 3D athlete characters on a "
    "field, world events as a dramatic 3D panoramic scene with expressive characters reacting. "
    "The scene should be IMMEDIATELY RECOGNIZABLE as that news story, rendered in full 3D CGI. "
    "The remaining headlines appear on 3D newspaper props held by characters, 3D TV screens in the "
    "background, 3D billboards in the scene. Quotes on a 3D journal or letter prop. Proverbs "
    "carved into a 3D stone monument. The date on a 3D calendar or clock prop. "
    "ALL typography in warm, ROUNDED, FRIENDLY fonts — like Pixar title cards. Headlines in bold "
    "rounded sans-serif (like Baloo or Fredoka), quotes in elegant hand-lettered script. "
    "Rich, saturated Pixar color palette with warm cinematic 3D lighting. MUST look 3D, not flat."
)


def _headline_style() -> str:
    return random.choice([_HEADLINE_LEGO, _HEADLINE_PIXAR])


_headline_theme = Theme(
    name="Headline",
    slug="headline",
    description="Top news story depicted in Lego Movie or Pixar animation style (random)",
    style_prompt="",  # filled dynamically via _style_fn
    color_hints="Works with any color setting. BW creates dramatic contrast in both styles.",
)
_headline_theme._style_fn = _headline_style  # type: ignore[attr-defined]
_register(_headline_theme)

_register(Theme(
    name="Headline (Lego)",
    slug="headline-lego",
    description="Top news story depicted in Lego Movie minifig style",
    style_prompt=_HEADLINE_LEGO,
    color_hints="Works with any color setting. BW creates dramatic contrast.",
))

_register(Theme(
    name="Headline (Pixar)",
    slug="headline-pixar",
    description="Top news story depicted in Pixar 3D CGI animation style",
    style_prompt=_HEADLINE_PIXAR,
    color_hints="Works with any color setting. BW creates dramatic contrast.",
))
