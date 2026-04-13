# Infographic Generator

A CLI tool that generates beautiful, themed AI infographics from live data sources. Uses Google's Gemini API for intelligent prompt composition and Nano Banana 2 (Gemini 3.1 Flash Image) for image generation.

Built for desktop wallpapers, e-ink displays, and digital signage.

## Features

- **14 Visual Themes** with unique art styles and scene variance (every generation is different)
- **5 Data Sources**: RSS feeds, world headlines (NewsAPI), foreign language quotes, Chinese proverbs, calendar
- **Sundial Mode**: Automatically adjusts lighting to match time of day (dawn, morning, golden hour, night)
- **Dark Mode**: Force dark backgrounds, or auto-dark after sunset via sundial
- **E-ink Support**: Color-limited palettes (BW, BWR, 7-color, 16-color) with Floyd-Steinberg dithering
- **Wallpaper Rotation**: Auto-generation 3x/day (6am, 12pm, 6pm) with last 10 wallpapers kept, auto-dark at 6pm

## Themes

| Theme | Style |
|---|---|
| `scenic_landscape` | Studio Ghibli anime landscape (varied scenes each run) |
| `daily_briefing` | Lo-fi beats anime study desk with cityscape |
| `retro_comic` | 1960s Marvel/DC comic book panels |
| `technical_blueprint` | Engineering blueprint of fantastical machines |
| `vintage_poster` | 1930s Art Deco travel poster |
| `cozy_cafe` | Lo-fi anime cozy interiors (varied scenes) |
| `space_mission` | Sci-fi spacecraft bridge (varied cosmic settings) |
| `japanese_ink` | Traditional sumi-e ink wash painting |
| `library_study` | Candlelit medieval library with illuminated manuscripts |
| `steampunk_workshop` | Miyazaki anime steampunk inventor's workshop |
| `ocean_depths` | Ghibli anime bioluminescent underwater world |
| `headline` | Top news story as Lego Movie or Pixar 3D (random 50/50) |
| `headline-lego` | Top news story in photorealistic 3D Lego Movie style |
| `headline-pixar` | Top news story in Pixar 3D CGI animation style |

## Installation

Requires Python 3.12+.

```bash
git clone https://github.com/runty/infographic.git
cd infographic
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configuration

### API Keys

You need two API keys:

1. **Google Gemini API** (for prompt composition + image generation): [Get one at Google AI Studio](https://aistudio.google.com)
2. **NewsAPI.org** (for world headlines): [Get one at newsapi.org](https://newsapi.org/register) (free tier: 100 requests/day)

Set them as environment variables:

```bash
export GOOGLE_API_KEY="your-gemini-key"
export NEWSAPI_KEY="your-newsapi-key"
```

Or create a `.env` file in the project root:

```
GOOGLE_API_KEY=your-gemini-key
NEWSAPI_KEY=your-newsapi-key
```

### Config File

Copy `config.default.toml` to `config.toml` to customize RSS feeds, headline countries, proverb count, e-ink palettes, and more.

## Usage

```bash
# Generate with a theme
infographic generate --theme daily_briefing --aspect-ratio 16:9 --resolution 1K -o output.png

# 4K wallpaper
infographic generate --theme scenic_landscape --aspect-ratio 16:9 --resolution 4K --width 3840 --height 2160 -o wallpaper.png

# Dark mode
infographic generate --theme space_mission --dark-mode -o dark.png

# E-ink black & white
infographic generate --theme japanese_ink --palette bw --aspect-ratio 4:3 -o eink.png

# E-ink 3-color (black, white, red)
infographic generate --theme retro_comic --palette bwr -o eink_color.png

# Preview the prompt without generating
infographic generate --theme ocean_depths --dry-run

# Only use specific data sources
infographic generate --theme cozy_cafe --sources rss --sources quotes

# List all themes
infographic themes

# List all data sources
infographic sources
```

### CLI Options

| Option | Default | Description |
|---|---|---|
| `--theme`, `-t` | `daily_briefing` | Visual theme |
| `--width`, `-w` | `1024` | Image width in pixels |
| `--height`, `-h` | `768` | Image height in pixels |
| `--aspect-ratio`, `-a` | auto | Aspect ratio (e.g., `16:9`, `4:3`). Overrides height |
| `--resolution`, `-r` | `1K` | Nano Banana resolution: `512`, `1K`, `2K`, `4K` |
| `--dark-mode`, `-d` | off | Force dark background |
| `--palette`, `-p` | none | E-ink palette: `bw`, `bwr`, `7color`, `16color` |
| `--colors`, `-c` | `0` | Max colors (0 = unlimited) |
| `--output`, `-o` | auto-timestamped | Output file path |
| `--sources`, `-s` | all | Enable specific sources (repeatable) |
| `--rss-count` | `5` | Headlines per RSS feed |
| `--config` | auto | Path to config.toml |
| `--dry-run` | off | Print composed prompt, skip image generation |
| `--verbose`, `-v` | off | Debug logging |

## Sundial Mode

When `--dark-mode` is not set, the tool automatically adjusts lighting based on your local time:

| Time | Mood | Auto-dark? |
|---|---|---|
| 5am - 8am | Dawn / sunrise | No |
| 8am - 12pm | Bright morning | No |
| 12pm - 3pm | Midday / afternoon | No |
| 3pm - 6pm | Golden hour | No |
| 6pm - 9pm | Sunset / evening | Yes |
| 9pm - 5am | Night | Yes |

## Wallpaper Rotation

Auto-generate a new infographic wallpaper 3x/day (6am, 12pm, 6pm). The 6pm run automatically uses dark mode. Targets a specific monitor by display name (default: `X EQUIP`), so it survives monitor reordering. Keeps the last 10 wallpapers (`wallpaper_1.png` through `wallpaper_10.png`) so you can browse recent ones.

Image generation includes automatic retry (up to 3 attempts) in case the model's content policy blocks a headline scene.

To change the target display, edit `DISPLAY_NAME` in `wallpaper_rotate.sh`.

### Setup

1. Create a `.env` file with your API keys (see above)
2. Copy the plist to LaunchAgents:

```bash
cp com.infographic.wallpaper.plist ~/Library/LaunchAgents/
```

3. Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.infographic.wallpaper.plist
```

### Force a one-time refresh

```bash
bash wallpaper_rotate.sh
```

Or add to your PATH:

```bash
mkdir -p ~/bin
ln -s /path/to/infographic/wallpaper_rotate.sh ~/bin/wallpaper
```

Then just run `wallpaper`.

### Stop / restart

```bash
# Stop
launchctl unload ~/Library/LaunchAgents/com.infographic.wallpaper.plist

# Start
launchctl load ~/Library/LaunchAgents/com.infographic.wallpaper.plist
```

### Check logs

```bash
tail -f wallpaper_rotate.log
```

## Architecture

The tool uses a two-stage AI pipeline:

1. **Data Collection**: RSS feeds (feedparser), NewsAPI headlines, bundled quotes/proverbs, calendar
2. **Prompt Composition**: Gemini 2.5 Flash composes a detailed text-to-image prompt from collected data + theme style + sundial/dark mode
3. **Image Generation**: Nano Banana 2 (Gemini 3.1 Flash Image Preview) renders the infographic
4. **Post-processing**: Resize + optional palette quantization with dithering for e-ink

## Data Sources

| Source | Description | Config |
|---|---|---|
| `rss` | Top stories from RSS feeds | Configurable feed URLs and count |
| `paperboy` | World headlines via NewsAPI.org | Configurable countries (default: US, GB, FR, DE, JP) |
| `quotes` | Foreign language quotes with English translations | 146 quotes in 20+ languages (Latin, French, Japanese, Arabic, etc.) |
| `proverbs` | Chinese proverbs with pinyin and translation | 79 proverbs from Confucius, Laozi, Sun Tzu, Mencius, etc. |
| `calendar` | Today's date, day of year, week number | Optional .ics file support |

## License

MIT
