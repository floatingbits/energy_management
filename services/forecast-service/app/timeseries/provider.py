from typing import Protocol

from app.timeseries.domain import TimeRange, TimeSeriesRun


class TimeSeriesProvider(Protocol):
    """Serves one time series, queried by time range only.

    Non-temporal context (metric, market, location, the underlying data
    source) is baked into the implementation at composition time — the
    client of a provider does not need to know any data source details.

    An implementation is free to serve observed and forecast from
    different sources.
    """

    def get_observed(
        self,
        time_range: TimeRange,
    ) -> TimeSeriesRun:
        ...

    def get_forecast(
        self,
        time_range: TimeRange,
    ) -> TimeSeriesRun:
        ...
