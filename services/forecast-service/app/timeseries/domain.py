from dataclasses import dataclass
from datetime import datetime, timedelta

from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase


@dataclass(frozen=True)
class TimeRange:
    """A regular slot grid defined by start, end and resolution."""

    start: datetime

    end: datetime

    resolution: timedelta

    @property
    def slots(self) -> int:
        seconds = self.resolution.total_seconds()
        return int((self.end - self.start).total_seconds() // seconds)


@dataclass(frozen=True)
class TimeSeriesRun:
    """A time series together with the time base its values are aligned to."""

    base: TimeSeriesTimeBase

    series: TimeSeries
