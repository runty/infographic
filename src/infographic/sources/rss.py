import logging

import feedparser
import httpx

from infographic.sources import register
from infographic.sources.base import DataSource, SourceResult

logger = logging.getLogger(__name__)


@register("rss")
class RssSource(DataSource):
    name = "rss"
    description = "Top stories from RSS feeds"

    def collect(self, config: dict) -> SourceResult:
        feeds = config.get("feeds", [])
        count = config.get("count", 5)
        items = []

        for feed_cfg in feeds:
            feed_name = feed_cfg.get("name", feed_cfg.get("url", "Unknown"))
            url = feed_cfg.get("url", "")
            if not url:
                continue

            try:
                resp = httpx.get(url, timeout=15, follow_redirects=True)
                parsed = feedparser.parse(resp.text)
                for entry in parsed.entries[:count]:
                    items.append({
                        "source": feed_name,
                        "headline": entry.get("title", ""),
                        "summary": (entry.get("summary", "") or "")[:200],
                        "link": entry.get("link", ""),
                    })
            except Exception as e:
                logger.warning(f"Failed to fetch RSS feed '{feed_name}': {e}")

        return SourceResult(
            source_name=self.name,
            title="Top Stories",
            items=items,
        )

    def is_available(self) -> bool:
        return True
