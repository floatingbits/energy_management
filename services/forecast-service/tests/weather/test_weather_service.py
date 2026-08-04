from datetime import datetime, timezone, timedelta

from app.weather.adapters.default import DefaultWeatherAdapter
from app.weather.open_meteo_mapping import OPEN_METEO_VARIABLES
from app.weather.request import WeatherForecastRequest
from app.weather.resolver import WeatherLocationResolver
from app.schemas.weather import (
    WeatherForecastPoint,
    WeatherVariableValue
)

from app.weather.result import WeatherForecastResult

from app.services.weather_service import WeatherService

from app.weather.fake_provider import FakeWeatherProvider
from app.forecasting.domain.forecast_run import ForecastRun
from app.forecasting.enums import ForecastMetric

class DummyRepository:
    def __init__(self):
        pass


def test_weather_service_calls_provider():

    resolver = WeatherLocationResolver()

    provider = FakeWeatherProvider()
    adapter = DefaultWeatherAdapter(OPEN_METEO_VARIABLES, resolver)
    repository = DummyRepository()
    service = WeatherService(
        provider,
        adapter,
        resolver,
        repository
    )


    locations = service.resolve_locations(
        [
            (53.55, 10.0)
        ]
    )

    run = ForecastRun(
        start=datetime.now(timezone.utc),
        resolution=timedelta(minutes=15),
        slots=1
    )

    result = service.get_forecast(WeatherForecastRequest(
            start=run.start,
            end=run.end,
            locations=locations,
            resolution=timedelta(minutes=15),
            variables=[
                ForecastMetric.TEMPERATURE,
                ForecastMetric.WIND_SPEED,
                ForecastMetric.CLOUD_COVER
            ]

        )
    )
    print(result)


    assert result.provider == "fake"
    assert len(result.forecasts[0].series) == 1
    # We do not want to test Fake Provider her.
    # TODO: Do sensible assertions
    # assert len(
    #     result.forecasts[0]
    #     .series[0]
    #     .values
    # ) == result.forecasts[0].run.slots