from datetime import datetime, timedelta, timezone

import pytest

from app.energy.observation.provider import EnergyObservationProvider
from app.energy.observation.provider_result import (
    ProviderLocationObservations,
    ProviderObservationResult,
    ProviderObservationSeries,
)
from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series_value import (
    TimeSeriesValue,
    from_quantiles,
)
from app.forecasting.encoding.definitions import DEFAULT_QUANTILE_DEFINITION
from app.forecasting.enums import ForecastMetric
from app.services.weather_service import WeatherService
from app.timeseries.domain import TimeRange
from app.timeseries.providers.energy import EnergyTimeSeriesProvider
from app.timeseries.providers.weather import WeatherTimeSeriesProvider
from app.weather.location import WeatherLocation
from app.weather.result import WeatherForecastResult, WeatherLocationForecast

SLOT = timedelta(hours=1)
RANGE = TimeRange(
    start=datetime(2024, 12, 4, 9, 0, tzinfo=timezone.utc),
    end=datetime(2024, 12, 4, 11, 0, tzinfo=timezone.utc),
    resolution=SLOT,
)


# ------------------------------------------------------------------
# energy


class FakeEnergyObservationProvider(EnergyObservationProvider):

    def __init__(self, observations: list[ProviderObservationSeries], location_key: str = "DE-LU"):
        self.observations = observations
        self.location_key = location_key
        self.requests = []

    def get_observations(self, request):
        self.requests.append(request)
        return ProviderObservationResult(
            provider="synthetic",
            observations=[
                ProviderLocationObservations(
                    location_key=self.location_key,
                    series=self.observations,
                )
            ],
        )


def test_energy_provider_fetches_and_aligns_series():
    provider = FakeEnergyObservationProvider([
        ProviderObservationSeries(
            variable_name="day_ahead_electricity_price",
            start=datetime(2024, 12, 4, 8, 0, tzinfo=timezone.utc),
            resolution=SLOT,
            # starts one slot before the requested range, has a gap
            values=[0.5, 1.0, None, 3.0],
        ),
    ])
    time_series_provider = EnergyTimeSeriesProvider(
        provider=provider,
        metric=ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE,
        market="DE-LU",
    )

    run = time_series_provider.get_observed(RANGE)

    assert run.base.start == RANGE.start
    assert run.base.slots == 2
    assert run.series.metric == ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE
    assert run.series.values == pytest.approx([1.0, 1.0])

    request = provider.requests[0]
    assert request.region == "DE-LU"
    assert request.start == RANGE.start
    assert request.end == RANGE.end


def test_energy_provider_forecast_not_implemented():
    time_series_provider = EnergyTimeSeriesProvider(
        provider=FakeEnergyObservationProvider([]),
        metric=ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE,
        market="DE-LU",
    )

    with pytest.raises(NotImplementedError):
        time_series_provider.get_forecast(RANGE)


def test_energy_provider_missing_series_raises():
    time_series_provider = EnergyTimeSeriesProvider(
        provider=FakeEnergyObservationProvider([]),
        metric=ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE,
        market="DE-LU",
    )

    with pytest.raises(ValueError, match="No observed series"):
        time_series_provider.get_observed(RANGE)


# ------------------------------------------------------------------
# weather


class FakeWeatherService:

    def __init__(self, values: list[float], start: datetime = RANGE.start):
        self.values = values
        self.start = start
        self.request = None

    def get_forecast(self, request):
        self.request = request
        return WeatherForecastResult(
            provider="synthetic",
            model="forecast",
            forecasts=[
                WeatherLocationForecast(
                    location=WeatherLocation(latitude=52.52, longitude=13.405),
                    run=TimeSeriesTimeBase(
                        start=self.start,
                        resolution=SLOT,
                        slots=len(self.values),
                    ),
                    series=[
                        TimeSeries(
                            metric=ForecastMetric.TEMPERATURE,
                            values=[
                                TimeSeriesValue(
                                    from_quantiles(
                                        p05=value - 1, p50=value, p95=value + 1,
                                    )
                                )
                                for value in self.values
                            ],
                            value_definition=DEFAULT_QUANTILE_DEFINITION,
                        ),
                    ],
                )
            ],
        )


def test_weather_provider_serves_median_values_for_observed_and_forecast():
    weather_service = FakeWeatherService([10.0, 11.0, 12.0])
    provider = WeatherTimeSeriesProvider(
        weather_service=weather_service,
        metric=ForecastMetric.TEMPERATURE,
        location=WeatherLocation(latitude=52.52, longitude=13.405),
    )

    observed = provider.get_observed(RANGE)
    forecast = provider.get_forecast(RANGE)

    assert observed.series.values == pytest.approx([10.0, 11.0])
    assert forecast.series.values == pytest.approx([10.0, 11.0])
    assert observed.series.metric == ForecastMetric.TEMPERATURE
    assert weather_service.request.variables == [ForecastMetric.TEMPERATURE]
    assert weather_service.request.start == RANGE.start
