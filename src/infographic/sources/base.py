from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class SourceResult:
    source_name: str
    title: str
    items: list[dict[str, str]]
    metadata: dict[str, str] = field(default_factory=dict)

    # Keys that should never be sent to the image prompt
    _SKIP_KEYS = {"link", "url", "summary", "description"}

    def to_text(self) -> str:
        lines = [f"## {self.title}"]
        for item in self.items:
            parts = []
            for key, value in item.items():
                # Skip URLs and long text that the image model can't render
                if key in self._SKIP_KEYS:
                    continue
                if not value or not value.strip():
                    continue
                parts.append(f"{key}: {value}")
            if parts:
                lines.append(" | ".join(parts))
        return "\n".join(lines)


class DataSource(ABC):
    name: str
    description: str

    @abstractmethod
    def collect(self, config: dict) -> SourceResult:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...
