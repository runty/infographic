import json
import random
from importlib import resources

from infographic.sources import register
from infographic.sources.base import DataSource, SourceResult

DATA_FILE = resources.files("infographic") / "data" / "proverbs.json"


@register("proverbs")
class ProverbsSource(DataSource):
    name = "proverbs"
    description = "Chinese proverbs with pinyin and English translation"

    def collect(self, config: dict) -> SourceResult:
        count = config.get("count", 1)
        proverbs = self._load_proverbs()
        selected = random.sample(proverbs, min(count, len(proverbs)))

        items = []
        for p in selected:
            items.append({
                "chinese": p["chinese"],
                "pinyin": p["pinyin"],
                "translation": p["translation"],
                "source": p["source"],
            })

        return SourceResult(
            source_name=self.name,
            title="Chinese Proverb",
            items=items,
        )

    def is_available(self) -> bool:
        return DATA_FILE.is_file()

    def _load_proverbs(self) -> list[dict]:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
