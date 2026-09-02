from app.forecasting.enums import ForecastMetric
from app.bootstrap.weather import create_weather_service, create_weather_forecast_repository
from app.database import SessionLocal
from app.asset_forecast.clients.asset_client import AssetClient

from datetime import datetime, timedelta, timezone

from app.repositories.weather_repository import WeatherRepository
from app.weather.open_meteo import OpenMeteoProvider
from app.services.weather_service import WeatherService
from sqlalchemy.orm import Session

from app.weather.request import WeatherForecastRequest
from app.bootstrap.asset_forecast import create_asset_client

def run_weather_forecast_job(
    weather_service: WeatherService,
    weather_repository: WeatherRepository,
    asset_client: AssetClient
):
    assets = asset_client.get_assets()

    asset_coords = []
    for asset in assets:
        asset_coords.append((asset['latitude'], asset['longitude']))

    locations = weather_service.resolve_locations(
        asset_coords
    )



    now = datetime.now(timezone.utc)

    horizon_end = now + timedelta(days=2)

    variables = [
        ForecastMetric.WIND_SPEED,
        ForecastMetric.CLOUD_COVER,
        ForecastMetric.TEMPERATURE,
        ForecastMetric.GLOBAL_SOLAR_IRRADIANCE,
        ForecastMetric.DIRECT_NORMAL_IRRADIANCE,
        ForecastMetric.DIFFUSE_IRRADIANCE
    ]

    request = WeatherForecastRequest(
        start=now,
        end=horizon_end,
        resolution=timedelta(minutes=15),
        locations=locations,
        variables=variables
    )

    result =  weather_service.get_forecast(
        request
    )

    weather_repository.create_weather_forecast_run(
        result
    )

def main():

    service = create_weather_service()
    weather_repository = create_weather_forecast_repository()
    asset_client = create_asset_client()
    run_weather_forecast_job(
        service,
        weather_repository,
        asset_client
    )


if __name__ == "__main__":
    main()