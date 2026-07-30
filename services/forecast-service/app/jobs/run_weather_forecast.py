from app.forecasting.enums import ForecastMetric
from app.infrastructure.weather import create_weather_service, create_weather_forecast_repository
from app.database import SessionLocal

from datetime import datetime, timedelta, timezone

from app.weather.open_meteo import OpenMeteoProvider
from app.services.weather_service import WeatherService
from sqlalchemy.orm import Session

from app.weather.request import WeatherForecastRequest


def run_weather_forecast_job(
    db: Session,
    weather_service: WeatherService,
    weather_repository
):

    locations = weather_service.resolve_locations(
        [
            (53.55, 10.0),
            (53.56, 10.01),
        ]
    )



    now = datetime.now(timezone.utc)

    horizon_end = now + timedelta(days=2)

    variables = [
        ForecastMetric.WIND_SPEED,
        ForecastMetric.CLOUD_COVER,
        ForecastMetric.TEMPERATURE,
    ]

    request = WeatherForecastRequest(
        start=now,
        end=horizon_end,
        locations=locations,
        variables=variables
    )

    result =  weather_service.get_forecast(
        request
    )

    weather_repository.create_weather_forecast_run(
        db,
        result
    )

def main():

    db = SessionLocal()

    service = create_weather_service()
    weather_repository = create_weather_forecast_repository()
    run_weather_forecast_job(
        db,
        service,
        weather_repository
    )


if __name__ == "__main__":
    main()