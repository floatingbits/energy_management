from sqlalchemy.orm import Session


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
            resolver: WeatherLocationResolver
    ):
        self.provider = provider
        self.adapter = adapter
        self.resolver = resolver

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
