from datetime import timedelta

from app.bootstrap.asset_forecast import create_asset_client
from app.bootstrap.weather import create_weather_service, create_weather_forecast_repository
from app.forecasting.domain.forecast_policy import ForecastPolicy
from app.services.asset_service import AssetService
from app.services.weather_forecast_requirement_service import WeatherForecastRequirementService


def create_asset_service():
    return AssetService(
        create_asset_client(),
        create_weather_service()
    )

def create_weather_forecast_requirement_service():
    policy = ForecastPolicy(horizon=timedelta(days=2), quantization=timedelta(hours=1))
    return WeatherForecastRequirementService(
        repository=create_weather_forecast_repository(),
        weather_forecast_service=create_weather_service(),
        policy=policy
    )