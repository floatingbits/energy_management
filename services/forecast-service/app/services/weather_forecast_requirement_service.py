from app.forecasting.domain.forecast_policy import ForecastPolicy
from app.repositories.weather_repository import WeatherRepository
from app.services.weather_service import WeatherService
from datetime import datetime, timezone, timedelta

from app.weather.request import WeatherForecastRequest


class WeatherForecastRequirementService:
    def __init__(
        self,
        repository: WeatherRepository,
        weather_forecast_service: WeatherService,
        policy: ForecastPolicy,
    ):
        self.repository = repository
        self.weather_forecast_service = weather_forecast_service
        self.policy = policy

    def get_or_create_suitable(self, location) -> int:
        required_run = self.policy.required_run(datetime.now(timezone.utc))

        forecasts = self.repository.get_for_run(
            location=location,
            start=required_run.start,
            resolution_seconds=required_run.resolution_seconds,
            slots=required_run.slots,
        )


        if len(forecasts) > 0:
            return forecasts[0].id

        resolution = timedelta(seconds=required_run.resolution_seconds)
        request = WeatherForecastRequest(
            start=required_run.start,
            end=required_run.start + (required_run.slots * resolution),
            resolution=resolution,
            locations=[location],
            variables=[]
        )
        result = self.weather_forecast_service.get_forecast(request)
        forecast = self.repository.create_weather_forecast_run(
            result
        )

        return forecast.id