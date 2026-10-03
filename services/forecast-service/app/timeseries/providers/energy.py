from app.energy.observation.provider import EnergyObservationProvider
from app.energy.observation.request import EnergyObservationRequest
from app.forecasting.enums import ForecastMetric
from app.timeseries.domain import TimeRange, TimeSeriesRun
from app.timeseries.grid import (
    aligned_values,
    build_run,
    interpolate_missing,
)


class EnergyTimeSeriesProvider:
    """Serves an energy market variable as a TimeSeries.

    Constructed per (metric, market): the market and the variable are
    context the data source needs. Observations come from an
    EnergyObservationProvider; a forecast source is not implemented
    for energy variables yet — forecasts "after having been forecast"
    will back get_forecast later.
    """

    def __init__(
        self,
        provider: EnergyObservationProvider,
        metric: ForecastMetric,
        market: str,
    ):
        self.provider = provider
        self.metric = metric
        self.market = market

    def get_observed(
        self,
        time_range: TimeRange,
    ) -> TimeSeriesRun:
        request = EnergyObservationRequest(
            variables=[self.metric],
            region=self.market,
            resolution=time_range.resolution,
            start=time_range.start,
            end=time_range.end,
        )
        result = self.provider.get_observations(request)
        source = self._series(result)

        source_run = build_run(
            self.metric,
            TimeRange(
                start=source.start,
                end=source.start + source.resolution * len(source.values),
                resolution=source.resolution,
            ),
            source.values,
        )
        values = aligned_values(source_run, time_range)
        return self._run(time_range, values)

    def get_forecast(
        self,
        time_range: TimeRange,
    ) -> TimeSeriesRun:
        raise NotImplementedError(
            "No forecast source implemented for energy market variables yet"
        )

    def _series(self, result):
        for location in result.observations:
            if location.location_key != self.market:
                continue
            for series in location.series:
                if series.variable_name == str(self.metric):
                    return series
        raise ValueError(
            f"No observed series for {self.metric} "
            f"in market {self.market}"
        )

    def _run(self, time_range: TimeRange, values: list[float | None]) -> TimeSeriesRun:
        return build_run(self.metric, time_range, interpolate_missing(values))
