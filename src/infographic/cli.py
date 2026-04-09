import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from infographic.config import AppConfig, load_config
from infographic.pipeline import run_pipeline
from infographic.themes import list_themes

# Import source modules so they register themselves
import infographic.sources.rss  # noqa: F401
import infographic.sources.quotes  # noqa: F401
import infographic.sources.proverbs  # noqa: F401
import infographic.sources.paperboy  # noqa: F401
import infographic.sources.calendar_source  # noqa: F401
from infographic.sources import SOURCES

app = typer.Typer(
    name="infographic",
    help="Generate AI-powered infographics for e-ink devices.",
    no_args_is_help=True,
)
console = Console()

VALID_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4",
    "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
]
VALID_RESOLUTIONS = ["512", "1K", "2K", "4K"]
VALID_PALETTES = ["bw", "bwr", "7color", "16color"]


def _compute_dimensions(width: int, height: int, aspect_ratio: str | None) -> tuple[int, int]:
    if aspect_ratio:
        parts = aspect_ratio.split(":")
        w_ratio, h_ratio = int(parts[0]), int(parts[1])
        # Derive height from width + ratio
        height = int(width * h_ratio / w_ratio)
    return width, height


@app.command()
def generate(
    width: Annotated[int, typer.Option("--width", "-w", help="Image width in pixels")] = 1024,
    height: Annotated[int, typer.Option("--height", "-h", help="Image height in pixels")] = 768,
    aspect_ratio: Annotated[Optional[str], typer.Option(
        "--aspect-ratio", "-a", help=f"Aspect ratio ({', '.join(VALID_RATIOS)}). Overrides height."
    )] = None,
    theme: Annotated[str, typer.Option("--theme", "-t", help="Visual theme")] = "daily_briefing",
    colors: Annotated[int, typer.Option("--colors", "-c", help="Max colors (0=no limit)")] = 0,
    palette: Annotated[Optional[str], typer.Option(
        "--palette", "-p", help=f"E-ink palette ({', '.join(VALID_PALETTES)})"
    )] = None,
    output: Annotated[Optional[Path], typer.Option("--output", "-o", help="Output file path")] = None,
    config_file: Annotated[Optional[Path], typer.Option("--config", help="Path to config.toml")] = None,
    sources: Annotated[Optional[list[str]], typer.Option(
        "--sources", "-s", help="Enable specific sources (can repeat)"
    )] = None,
    rss_count: Annotated[int, typer.Option("--rss-count", help="Stories per RSS feed")] = 5,
    resolution: Annotated[str, typer.Option("--resolution", "-r", help=f"Image resolution ({', '.join(VALID_RESOLUTIONS)})")] = "1K",
    dark_mode: Annotated[bool, typer.Option("--dark-mode", "-d", help="Generate dark background image")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print prompt without generating")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Verbose logging")] = False,
):
    """Generate an infographic from configured data sources."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    # Validate inputs
    if width <= 0 or height <= 0:
        console.print("[red]Width and height must be positive integers[/red]")
        raise typer.Exit(1)
    if aspect_ratio and aspect_ratio not in VALID_RATIOS:
        console.print(f"[red]Invalid aspect ratio '{aspect_ratio}'. Valid: {', '.join(VALID_RATIOS)}[/red]")
        raise typer.Exit(1)
    if resolution not in VALID_RESOLUTIONS:
        console.print(f"[red]Invalid resolution '{resolution}'. Valid: {', '.join(VALID_RESOLUTIONS)}[/red]")
        raise typer.Exit(1)
    if palette and palette not in VALID_PALETTES:
        console.print(f"[red]Invalid palette '{palette}'. Valid: {', '.join(VALID_PALETTES)}[/red]")
        raise typer.Exit(1)

    # Load config
    config = load_config(config_file)

    # Override RSS count if specified
    config.sources.rss.count = rss_count

    # Compute dimensions
    final_width, final_height = _compute_dimensions(width, height, aspect_ratio)

    # Default output path
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = Path(f"infographic_{timestamp}.png")

    # Use aspect ratio for the API, or derive from dimensions
    api_ratio = aspect_ratio or _nearest_ratio(final_width, final_height)

    console.print(f"[bold]Generating infographic[/bold]")
    console.print(f"  Theme: {theme}")
    console.print(f"  Size: {final_width}x{final_height} ({api_ratio})")
    console.print(f"  Resolution: {resolution}")
    if dark_mode:
        console.print(f"  Mode: dark")
    else:
        _h = datetime.now().hour
        _tod = (
            "dawn" if 5 <= _h < 8 else
            "morning" if 8 <= _h < 12 else
            "afternoon" if 12 <= _h < 15 else
            "golden hour" if 15 <= _h < 18 else
            "sunset/evening (auto-dark)" if 18 <= _h < 21 else
            "night (auto-dark)"
        )
        console.print(f"  Sundial: {_tod}")
    if palette:
        console.print(f"  Palette: {palette}")
    elif colors > 0:
        console.print(f"  Colors: {colors}")
    console.print(f"  Output: {output}")
    console.print()

    try:
        result = run_pipeline(
            config=config,
            width=final_width,
            height=final_height,
            aspect_ratio=api_ratio,
            theme_slug=theme,
            palette=palette,
            colors=colors,
            output=output,
            dark_mode=dark_mode,
            sources_filter=sources,
            dry_run=dry_run,
            resolution=resolution,
        )
        if result:
            console.print(f"[green]Infographic saved to {result}[/green]")
        elif dry_run:
            console.print("[yellow]Dry run complete — no image generated.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


def _nearest_ratio(width: int, height: int) -> str:
    """Find the nearest supported aspect ratio for the given dimensions."""
    target = width / height
    best = "16:9"
    best_diff = float("inf")
    for ratio_str in VALID_RATIOS:
        w, h = ratio_str.split(":")
        ratio = int(w) / int(h)
        diff = abs(ratio - target)
        if diff < best_diff:
            best_diff = diff
            best = ratio_str
    return best


@app.command()
def themes():
    """List available visual themes."""
    table = Table(title="Available Themes")
    table.add_column("Slug", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Description")
    table.add_column("E-ink Notes", style="dim")

    for t in list_themes():
        table.add_row(t.slug, t.name, t.description, t.color_hints)

    console.print(table)


@app.command(name="sources")
def list_sources_cmd():
    """List available data sources."""
    table = Table(title="Available Data Sources")
    table.add_column("Name", style="cyan")
    table.add_column("Description")

    for name, cls in SOURCES.items():
        table.add_row(name, cls.description)

    console.print(table)


if __name__ == "__main__":
    app()
