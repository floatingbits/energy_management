from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class ForecastRun:

    start: datetime

    resolution: timedelta

    slots: int

    def timestamp_for_slot(
        self,
        index: int
    ) -> datetime:

        return (
            self.start
            + self.resolution * index
        )

    @property
    def end(self) -> datetime:

        return (
            self.start
            + self.resolution * self.slots
        )