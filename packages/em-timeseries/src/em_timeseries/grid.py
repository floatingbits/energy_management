from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from em_timeseries.domain.time_series import TimeSeries
from em_timeseries.domain.time_series_time_base import TimeSeriesTimeBase
from em_timeseries.encoding.definitions import ScalarDefinition


@dataclass(frozen=True)
class TimeRange:
    """A regular slot grid defined by start, end and resolution."""

    start: datetime

    end: datetime

    resolution: timedelta

    @staticmethod
    def duration(start: datetime, end: datetime) -> timedelta:
        """Elapsed time between two (possibly aware) datetimes.

        Aware datetimes are normalized to UTC first: their plain
        subtraction can return the naive difference on some
        zoneinfo/DST combinations.
        """
        if start.tzinfo is not None and end.tzinfo is not None:
            return end.astimezone(timezone.utc) - start.astimezone(timezone.utc)
        return end - start

    @property
    def slots(self) -> int:
        seconds = self.resolution.total_seconds()
        return int(
            TimeRange.duration(self.start, self.end).total_seconds() // seconds
        )


@dataclass(frozen=True)
class TimeSeriesRun:
    """A time series together with the time base its values are aligned to."""

    base: TimeSeriesTimeBase

    series: TimeSeries


def build_run(
    metric,
    time_range: TimeRange,
    values: list[float | None],
) -> TimeSeriesRun:
    """Build a run whose values sit exactly on the time_range grid."""
    return TimeSeriesRun(
        base=TimeSeriesTimeBase(
            start=time_range.start,
            resolution=time_range.resolution,
            slots=time_range.slots,
        ),
        series=TimeSeries(
            metric=metric,
            values=values,
            value_definition=ScalarDefinition(),
        ),
    )


def aligned_values(
    source: TimeSeriesRun,
    target: TimeRange,
) -> list[float | None]:
    """Place a run's values on the target grid.

    Corrects for the source starting before/after target.start; slots
    without a value stay None. Values on non-target grids
    (base.resolution != target.resolution) are not supported.
    """
    if source.base.resolution != target.resolution:
        raise ValueError(
            "Source resolution does not match the requested resolution"
        )
    offset = int(
        TimeRange.duration(
            target.start, source.base.start
        ).total_seconds()
        // target.resolution.total_seconds()
    )
    values = [None] * target.slots
    for i, value in enumerate(source.series.values):
        slot = offset + i
        if 0 <= slot < target.slots:
            values[slot] = value
    return values


def interpolate_missing(values: list[float | None]) -> list[float]:
    """Interpolate missing scalar observations from their neighbours.

    Raises when no usable observation is available at all.
    """
    # pandas is imported lazily to keep this dependency-light package
    # importable without it.
    import pandas as pd

    series = pd.Series(values, dtype="float64")
    if not series.notna().any():
        raise ValueError(
            "Series has no usable (non-missing) observations"
        )
    interpolated = series.interpolate(limit_direction="both")
    return [float(value) for value in interpolated]
