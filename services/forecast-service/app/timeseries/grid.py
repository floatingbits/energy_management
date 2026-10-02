import numpy as np
import pandas as pd

from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.encoding.definitions import ScalarDefinition
from app.timeseries.domain import TimeRange, TimeSeriesRun


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
        (source.base.start - target.start).total_seconds()
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
    series = pd.Series(values, dtype="float64")
    if not series.notna().any():
        raise ValueError(
            "Series has no usable (non-missing) observations"
        )
    interpolated = series.interpolate(limit_direction="both")
    return [float(value) for value in interpolated]
