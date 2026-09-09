from dataclasses import replace
from typing import Optional

from app.repositories.weather_repository import WeatherRepository
from app.weather.adapter import WeatherAdapter
from app.weather.provider import WeatherProvider
from app.weather.request import WeatherForecastRequest
from app.weather.resolver import WeatherLocationResolver
from app.weather.location import WeatherLocation
from app.weather.result import WeatherForecastResult
from app.weather.uncertainty.estimator import WeatherUncertaintyEstimator


class WeatherService:

    def __init__(
            self,
            provider: WeatherProvider,
            adapter: WeatherAdapter,
            resolver: WeatherLocationResolver,
            repository: WeatherRepository,
            uncertainty_estimator: WeatherUncertaintyEstimator
    ):
        self.provider = provider
        self.adapter = adapter
        self.resolver = resolver
        self.repository = repository
        self.uncertainty_estimator = uncertainty_estimator

    def get_weather_forecasts(
            self,
            latitude: float,
            longitude: float,
            limit: Optional[int] = None
    ):

        location = self.resolver.resolve(latitude, longitude)
        print(location)
        return self.repository.get_forecasts_for_location(
            latitude=location.latitude,
            longitude=location.longitude,
            limit=limit
        )

    def get_weather_forecast(
            self,
            weather_forecast_id: int
    ):
        return self.repository.get_forecast_by_id(
            weather_forecast_id
        )

    def get_forecast(
            self,
            request: WeatherForecastRequest
    ) -> WeatherForecastResult:
        # Merge requested variables with those needed by uncertainty estimation
        new_request = replace(
            request,
            variables=list(set(self.uncertainty_estimator.needs_variables())|set(request.variables))
        )
        provider_result = (
            self.provider.get_forecast(
                new_request
            )
        )

        normalized_result = self.adapter.adapt(
            provider_result,
            new_request
        )

        probabilistic_result = self.uncertainty_estimator.apply(normalized_result)
        return probabilistic_result

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


