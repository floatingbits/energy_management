"""Time period and grid matching for decision inputs and outputs.

All awkwardness about aligning foreign-forecast grids onto the decision's
delivery window lives here, so strategies receive pre-aligned values and
more sophisticated mapping (DST, oversampling, backfilling) can be
introduced later by changing only this module.
"""

from datetime import timedelta

from em_timeseries.domain import TimeSeries, TimeSeriesTimeBase, TimeSeriesValue
from em_timeseries.grid import TimeRange, TimeSeriesRun, aligned_values

from app.decisions.request import DeliveryWindow

DELIVERY_RESOLUTION_SECONDS = 3600


def delivery_grid(
    window: DeliveryWindow,
    resolution_seconds: int = DELIVERY_RESOLUTION_SECONDS,
) -> TimeRange:
    """The canonical grid of a delivery window (v1: hourly)."""
    return TimeRange(
        start=window.start,
        end=window.end,
        resolution=timedelta(seconds=resolution_seconds),
    )


def map_run_to_window(
    run: TimeSeriesRun,
    window: DeliveryWindow,
) -> list[float | None]:
    """Place a run's values on the window's grid.

    Slots not covered by the run's source grid stay None. Requires the
    source resolution to equal the window resolution.
    """
    grid = delivery_grid(window)
    try:
        return aligned_values(run, grid)
    except ValueError as error:
        # aligned_values only rejects mismatched resolution; surface the
        # window context with the failure.
        if "resolution" in str(error):
            raise ValueError(
                f"Forecast resolution {run.base.resolution} does not match "
                f"the delivery window grid of {window.start}..{window.end} "
                f"({grid.resolution}); window alignment cannot proceed"
            ) from error
        raise


def covered(run: TimeSeriesRun, window: DeliveryWindow) -> bool:
    """True if the run's native slot grid encloses the delivery window."""
    return run.base.start <= window.start and run.base.end >= window.end


def run_on_window(
    run: TimeSeriesRun,
    window: DeliveryWindow,
) -> TimeSeriesRun:
    """Rebuild a run with one value per slot of the window's grid.

    A target slot takes the value of the source slot *covering* the
    target slot's start time (step-function alignment); slots outside
    the source grid become all-None values kept aligned with the series'
    definition. Works across differing resolutions (e.g. 15-minute
    weather/price grids onto the hourly delivery grid).
    """
    grid = delivery_grid(window)
    definition = run.series.value_definition
    arity = definition.arity()
    empty = TimeSeriesValue(values=(None,) * arity)

    source_resolution = run.base.resolution.total_seconds()
    mapped = []
    for slot_index in range(grid.slots):
        target_time = grid.start + grid.resolution * slot_index
        elapsed = TimeRange.duration(
            run.base.start, target_time
        ).total_seconds()
        source_index = int(elapsed // source_resolution)
        if 0 <= source_index < len(run.series.values):
            mapped.append(run.series.values[source_index])
        else:
            mapped.append(None)

    rebuilt = [
        value if value is not None else TimeSeriesValue(values=(None,) * arity)
        for value in mapped
    ]
    return TimeSeriesRun(
        base=window_base(window),
        series=TimeSeries(
            metric=run.series.metric,
            values=rebuilt,
            value_definition=definition,
        ),
    )


def window_base(
    window: DeliveryWindow,
    resolution_seconds: int = DELIVERY_RESOLUTION_SECONDS,
) -> TimeSeriesTimeBase:
    """The persisted time base for a decision over a delivery window."""
    grid = delivery_grid(window, resolution_seconds)
    return TimeSeriesTimeBase(
        start=grid.start,
        resolution=grid.resolution,
        slots=grid.slots,
    )
