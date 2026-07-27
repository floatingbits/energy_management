from app.infrastructure.weather import create_weather_service
from app.database import SessionLocal

from datetime import datetime, timedelta, timezone

from app.weather.open_meteo import OpenMeteoProvider
from app.services.weather_service import WeatherService
from sqlalchemy.orm import Session


def run_weather_forecast_job(
    db: Session,
    weather_service: WeatherService
):

    locations = weather_service.resolve_locations(
        [
            (53.55, 10.0),
            (53.56, 10.01),
        ]
    )



    now = datetime.now(timezone.utc)

    horizon_end = now + timedelta(days=2)


    return weather_service.create_forecast(
        db=db,
        locations=locations,
        horizon_start=now,
        horizon_end=horizon_end,
        resolution_minutes=60
    )

def main():

    db = SessionLocal()

    service = create_weather_service()

    run_weather_forecast_job(
        db,
        service
    )


if __name__ == "__main__":
    main()