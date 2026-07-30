from app.weather.adapters.default import DefaultWeatherAdapter
from app.weather.open_meteo_mapping import OPEN_METEO_VARIABLES

from app.weather.resolver import WeatherLocationResolver
from app.weather.open_meteo import OpenMeteoProvider
from app.services.weather_service import WeatherService


from app.repositories import weather_repository

def create_location_resolver():
    return WeatherLocationResolver(
        grid_size=0.1
    )

def create_weather_service():

    resolver = create_location_resolver()

    provider = OpenMeteoProvider()

    adapter = DefaultWeatherAdapter(OPEN_METEO_VARIABLES, resolver)

    return WeatherService(
        resolver=resolver,
        provider=provider,
        adapter=adapter
    )


def create_weather_forecast_repository():
    return weather_repository
