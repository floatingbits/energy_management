from datetime import datetime

from app.weather.resolver import WeatherLocationResolver
from app.schemas.weather import (
    WeatherForecastResult,
    WeatherForecastPoint,
    WeatherVariableValue
)

from app.services.weather_service import WeatherService

from app.weather.fake_provider import FakeWeatherProvider


def test_weather_service_calls_provider():

    resolver = WeatherLocationResolver()

    provider = FakeWeatherProvider()

    service = WeatherService(
        resolver,
        provider
    )


    locations = service.resolve_locations(
        [
            (53.55, 10.0)
        ]
    )


    result = provider.get_forecast(
        locations,
        datetime.now(),
        datetime.now(),
        60
    )


    assert result.provider == "fake"
    assert len(result.forecasts) == 1