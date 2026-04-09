import json
import random
from importlib import resources

from infographic.sources import register
from infographic.sources.base import DataSource, SourceResult

DATA_FILE = resources.files("infographic") / "data" / "quotes.json"


@register("quotes")
class QuotesSource(DataSource):
    name = "quotes"
    description = "Wise quotes from foreign languages with English translations"

    def collect(self, config: dict) -> SourceResult:
        count = config.get("count", 1)
        quotes = self._load_quotes()
        selected = random.sample(quotes, min(count, len(quotes)))

        items = []
        for q in selected:
            items.append({
                "original": q["text"],
                "language": q["language"],
                "translation": q["translation"],
                "attribution": q["attribution"],
            })

        return SourceResult(
            source_name=self.name,
            title="Words of Wisdom",
            items=items,
        )

    def is_available(self) -> bool:
        return DATA_FILE.is_file()

    def _load_quotes(self) -> list[dict]:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
