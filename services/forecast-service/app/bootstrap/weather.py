from app.database import SessionLocal
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
    repository = create_weather_forecast_repository()
    return WeatherService(
        resolver=resolver,
        provider=provider,
        adapter=adapter,
        repository=repository
    )


def create_weather_forecast_repository():
    db_session = SessionLocal()
    return weather_repository.WeatherRepository(db_session)
