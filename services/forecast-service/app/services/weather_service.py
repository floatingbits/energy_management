from sqlalchemy.orm import Session

from app.repositories import weather_repository
from app.weather.provider import WeatherProvider
from app.weather.resolver import WeatherLocationResolver
from app.weather.value_objects import WeatherLocation
class WeatherService:

    def __init__(
        self,
        resolver: WeatherLocationResolver,
        provider: WeatherProvider
    ):
        self.resolver = resolver
        self.provider = provider

    def resolve_locations(
            self,
            coordinates: list[tuple[float, float]]
    ) -> list[WeatherLocation]:
        return [
            self.resolver.resolve(
                lat,
                lon
            )
            for lat, lon in coordinates
        ]

    def create_forecast(
        self,
        db,
        locations,
        horizon_start,
        horizon_end,
        resolution_minutes
    ):

        result = self.provider.get_forecast(
            locations,
            horizon_start,
            horizon_end,
            resolution_minutes
        )

        return weather_repository.create_weather_forecast_run(
            db,
            result
        )