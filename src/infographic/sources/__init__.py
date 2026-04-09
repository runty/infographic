from infographic.sources.base import DataSource, SourceResult

SOURCES: dict[str, type[DataSource]] = {}


def register(name: str):
    def decorator(cls: type[DataSource]) -> type[DataSource]:
        SOURCES[name] = cls
        return cls
    return decorator


def get_source(name: str) -> DataSource:
    return SOURCES[name]()


def list_sources() -> list[str]:
    return list(SOURCES.keys())
