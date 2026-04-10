import logging
from datetime import datetime

from infographic.sources import register
from infographic.sources.base import DataSource, SourceResult

logger = logging.getLogger(__name__)



@register("calendar")
class CalendarSource(DataSource):
    name = "calendar"
    description = "Today's date, day of week, and calendar information"

    def collect(self, config: dict) -> SourceResult:
        now = datetime.now()
        items = []

        if config.get("show_day_info", True):
            items.append({
                "date": now.strftime("%A, %B %d, %Y"),
                "day_of_year": f"Day {now.timetuple().tm_yday} of {now.year}",
                "week": f"Week {now.isocalendar()[1]}",
            })

        # Read .ics file if configured
        ics_file = config.get("ics_file", "")
        if ics_file:
            try:
                events = self._parse_ics(ics_file, now)
                for event in events:
                    items.append(event)
            except Exception as e:
                logger.warning(f"Failed to parse ICS file '{ics_file}': {e}")

        return SourceResult(
            source_name=self.name,
            title="Today",
            items=items,
            metadata={"date": now.isoformat()},
        )

    def is_available(self) -> bool:
        return True

    def _parse_ics(self, path: str, now: datetime) -> list[dict[str, str]]:
        events = []
        today_str = now.strftime("%Y%m%d")

        with open(path, encoding="utf-8") as f:
            content = f.read()

        in_event = False
        event: dict[str, str] = {}
        for line in content.splitlines():
            line = line.strip()
            if line == "BEGIN:VEVENT":
                in_event = True
                event = {}
            elif line == "END:VEVENT":
                in_event = False
                # Check if event is today
                dtstart = event.get("dtstart", "")
                if dtstart.startswith(today_str):
                    events.append({
                        "event": event.get("summary", "Untitled"),
                        "time": dtstart,
                    })
            elif in_event and ":" in line:
                key, _, value = line.partition(":")
                # Handle properties with parameters like DTSTART;VALUE=DATE:20260408
                key = key.split(";")[0].lower()
                event[key] = value

        return events
