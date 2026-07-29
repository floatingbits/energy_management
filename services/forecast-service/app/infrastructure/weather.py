from app.weather.adapters.default import DefaultWeatherAdapter
from app.weather.resolver import WeatherLocationResolver
from app.weather.open_meteo import OpenMeteoProvider
from app.services.weather_service import WeatherService

from app.weather.fake_provider import FakeWeatherProvider
from app.repositories import weather_repository

def create_weather_service():

    resolver = WeatherLocationResolver(
        grid_size=0.1
    )

    provider = FakeWeatherProvider()

    adapter = DefaultWeatherAdapter()

    return WeatherService(
        resolver=resolver,
        provider=provider,
        adapter=adapter
    )


def create_weather_forecast_repository():
    return weather_repository
