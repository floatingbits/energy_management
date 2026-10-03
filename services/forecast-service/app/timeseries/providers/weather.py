from app.forecasting.enums import ForecastMetric
from app.services.weather_service import WeatherService
from app.timeseries.domain import TimeRange, TimeSeriesRun
from app.timeseries.grid import (
    aligned_values,
    build_run,
    interpolate_missing,
)
from app.weather.location import WeatherLocation
from app.weather.request import WeatherForecastRequest


class WeatherTimeSeriesProvider:
    """Serves one weather variable as a TimeSeries, queried by time range.

    Constructed per (metric, location): location and variable are
    context the weather source needs. Both observed and forecast are
    served from the weather model's own forecast run — forecasts for
    historical dates are treated as observations of those dates.
    Quantile values are reduced to their median.
    """

    def __init__(
        self,
        weather_service: WeatherService,
        metric: ForecastMetric,
        location: WeatherLocation,
    ):
        self.weather_service = weather_service
        self.metric = metric
        self.location = location

    def get_observed(
        self,
        time_range: TimeRange,
    ) -> TimeSeriesRun:
        return self._fetch(time_range)

    def get_forecast(
        self,
        time_range: TimeRange,
    ) -> TimeSeriesRun:
        return self._fetch(time_range)

    def _fetch(
        self,
        time_range: TimeRange,
    ) -> TimeSeriesRun:
        request = WeatherForecastRequest(
            start=time_range.start,
            end=time_range.end,
            resolution=time_range.resolution,
            locations=[self.location],
            variables=[self.metric],
        )
        result = self.weather_service.get_forecast(request)
        source = self._series(result)

        medians = [
            source.quantile(value, 50)
            for value in source.values
        ]
        source_run = build_run(
            self.metric,
            TimeRange(
                start=result.forecasts[0].run.start,
                end=result.forecasts[0].run.start
                + result.forecasts[0].run.resolution * len(medians),
                resolution=result.forecasts[0].run.resolution,
            ),
            medians,
        )
        values = aligned_values(source_run, time_range)
        return build_run(
            self.metric,
            time_range,
            interpolate_missing(values),
        )

    def _series(self, result):
        for forecast in result.forecasts:
            for series in forecast.series:
                if series.metric != self.metric:
                    continue
                return series
        raise ValueError(
            f"No weather series for {self.metric} "
            f"at {self.location.latitude}/{self.location.longitude}"
        )
