from app.weather.resolver import WeatherLocationResolver
from app.weather.open_meteo import OpenMeteoProvider
from app.services.weather_service import WeatherService

from app.weather.fake_provider import FakeWeatherProvider


def create_weather_service():

    resolver = WeatherLocationResolver(
        grid_size=0.1
    )

    provider = FakeWeatherProvider()


    return WeatherService(
        resolver=resolver,
        provider=provider
    )