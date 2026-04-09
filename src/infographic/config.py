import os
import tomllib
from pathlib import Path
from pydantic import BaseModel, Field


class RssFeedConfig(BaseModel):
    name: str
    url: str


class RssSourceConfig(BaseModel):
    enabled: bool = True
    count: int = 5
    feeds: list[RssFeedConfig] = Field(default_factory=lambda: [
        RssFeedConfig(name="Hacker News", url="https://news.ycombinator.com/rss"),
        RssFeedConfig(name="Ars Technica", url="https://feeds.arstechnica.com/arstechnica/index"),
        RssFeedConfig(name="Financial Times", url="https://www.ft.com/rss/home"),
    ])


class QuotesSourceConfig(BaseModel):
    enabled: bool = True
    count: int = 1


class ProverbsSourceConfig(BaseModel):
    enabled: bool = True
    count: int = 1


class PaperboySourceConfig(BaseModel):
    enabled: bool = True
    api_key: str = ""  # or set NEWSAPI_KEY env var
    countries: list[str] = Field(default_factory=lambda: ["us", "gb", "fr", "de", "jp"])
    count: int = 3  # headlines per country


class CalendarSourceConfig(BaseModel):
    enabled: bool = True
    show_day_info: bool = True
    ics_file: str = ""


class SourcesConfig(BaseModel):
    rss: RssSourceConfig = Field(default_factory=RssSourceConfig)
    quotes: QuotesSourceConfig = Field(default_factory=QuotesSourceConfig)
    proverbs: ProverbsSourceConfig = Field(default_factory=ProverbsSourceConfig)
    paperboy: PaperboySourceConfig = Field(default_factory=PaperboySourceConfig)
    calendar: CalendarSourceConfig = Field(default_factory=CalendarSourceConfig)


class ApiConfig(BaseModel):
    google_api_key: str = ""
    composer_model: str = "gemini-2.5-flash"
    generator_model: str = "gemini-3.1-flash-image-preview"
    image_size: str = "1K"


class EinkPalettes(BaseModel):
    bw: list[str] = ["#000000", "#FFFFFF"]
    bwr: list[str] = ["#000000", "#FFFFFF", "#FF0000"]
    sevcolor: list[str] = [
        "#000000", "#FFFFFF", "#FF0000", "#00FF00",
        "#0000FF", "#FFFF00", "#FF8000",
    ]
    sixteencolor: list[str] = [
        "#000000", "#FFFFFF", "#FF0000", "#00FF00",
        "#0000FF", "#FFFF00", "#FF8000", "#800080",
        "#00FFFF", "#FF00FF", "#808080", "#C0C0C0",
        "#800000", "#008000", "#000080", "#808000",
    ]


PALETTE_MAP = {
    "bw": "bw",
    "bwr": "bwr",
    "7color": "sevcolor",
    "16color": "sixteencolor",
}


class EinkConfig(BaseModel):
    default_palette: str = ""
    dither: bool = True
    dither_method: str = "floyd-steinberg"
    palettes: EinkPalettes = Field(default_factory=EinkPalettes)


class GeneralConfig(BaseModel):
    output_dir: str = "."
    default_theme: str = "none"
    default_width: int = 1024
    default_height: int = 768
    default_colors: int = 0


class AppConfig(BaseModel):
    general: GeneralConfig = Field(default_factory=GeneralConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    sources: SourcesConfig = Field(default_factory=SourcesConfig)
    eink: EinkConfig = Field(default_factory=EinkConfig)


def load_config(config_path: Path | None = None) -> AppConfig:
    if config_path and config_path.exists():
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        return AppConfig(**data)
    # Try default locations
    for candidate in [Path("config.toml"), Path("config.default.toml")]:
        if candidate.exists():
            with open(candidate, "rb") as f:
                data = tomllib.load(f)
            return AppConfig(**data)
    return AppConfig()


def get_api_key(config: AppConfig) -> str:
    key = os.environ.get("GOOGLE_API_KEY", "") or config.api.google_api_key
    if not key:
        raise ValueError(
            "No API key found. Set GOOGLE_API_KEY env var or add it to config.toml"
        )
    return key


def get_palette_colors(config: AppConfig, palette_name: str) -> list[tuple[int, int, int]]:
    field_name = PALETTE_MAP.get(palette_name, palette_name)
    hex_colors = getattr(config.eink.palettes, field_name, None)
    if hex_colors is None:
        raise ValueError(f"Unknown palette: {palette_name}")
    colors = []
    for h in hex_colors:
        h = h.lstrip("#")
        colors.append((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    return colors
