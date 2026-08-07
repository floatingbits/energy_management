from typing import Optional

from app.repositories.weather_repository import WeatherRepository
from app.weather.adapter import WeatherAdapter
from app.weather.provider import WeatherProvider
from app.weather.request import WeatherForecastRequest
from app.weather.resolver import WeatherLocationResolver
from app.weather.location import WeatherLocation
from app.weather.result import WeatherForecastResult



class WeatherService:

    def __init__(
            self,
            provider: WeatherProvider,
            adapter: WeatherAdapter,
            resolver: WeatherLocationResolver,
            repository: WeatherRepository
    ):
        self.provider = provider
        self.adapter = adapter
        self.resolver = resolver
        self.repository = repository

    def get_weather_forecasts(
            self,
            latitude: float,
            longitude: float,
            limit: Optional[int] = None
    ):


        return self.repository.get_forecasts_for_location(
            latitude=latitude,
            longitude=longitude,
            limit=limit
        )

    def get_forecast(
            self,
            request: WeatherForecastRequest
    ) -> WeatherForecastResult:
        provider_result = (
            self.provider.get_forecast(
                request
            )
        )

        return self.adapter.adapt(
            provider_result,
            request
        )

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
