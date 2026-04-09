import logging
import os

import httpx

from infographic.sources import register
from infographic.sources.base import DataSource, SourceResult

logger = logging.getLogger(__name__)

NEWSAPI_BASE = "https://newsapi.org/v2/top-headlines"


@register("paperboy")
class PaperboySource(DataSource):
    name = "paperboy"
    description = "World headlines from NewsAPI.org (top headlines by country)"

    def collect(self, config: dict) -> SourceResult:
        api_key = os.environ.get("NEWSAPI_KEY", "") or config.get("api_key", "")
        if not api_key:
            logger.warning("No NewsAPI key. Set NEWSAPI_KEY env var or add api_key to [sources.paperboy]")
            return SourceResult(source_name=self.name, title="World Headlines", items=[])

        countries = config.get("countries", ["us", "gb", "fr", "de", "jp"])
        count = config.get("count", 3)
        items = []

        for country in countries:
            try:
                headlines = self._fetch_headlines(api_key, country, count)
                items.extend(headlines)
            except Exception as e:
                logger.warning(f"Failed to fetch headlines for country '{country}': {e}")

        return SourceResult(
            source_name=self.name,
            title="World Headlines",
            items=items,
        )

    def is_available(self) -> bool:
        return bool(os.environ.get("NEWSAPI_KEY", ""))

    def _fetch_headlines(
        self, api_key: str, country: str, count: int
    ) -> list[dict[str, str]]:
        resp = httpx.get(
            NEWSAPI_BASE,
            params={
                "country": country,
                "pageSize": count,
                "apiKey": api_key,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "ok":
            logger.warning(f"NewsAPI error for {country}: {data.get('message', 'unknown')}")
            return []

        headlines = []
        for article in data.get("articles", []):
            headline = article.get("title", "")
            if not headline or headline == "[Removed]":
                continue
            headlines.append({
                "country": country.upper(),
                "source": article.get("source", {}).get("name", "Unknown"),
                "headline": headline,
                "description": (article.get("description") or "")[:200],
            })

        return headlines
