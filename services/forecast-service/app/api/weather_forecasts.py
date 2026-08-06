from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.bootstrap.weather import create_weather_service
from app.weather.schemas import WeatherForecastResponse
from app.services.weather_service import WeatherService

router = APIRouter(
    prefix="/weather-forecasts",
    tags=["Weather Forecasts"]
)


@router.get(
    "/",
    response_model=list[WeatherForecastResponse]
)
def get_weather_forecasts(
    latitude: float,
    longitude: float,
    limit: Optional[int] = None,
    weather_service: WeatherService = Depends(create_weather_service)
):

    weather_locations = weather_service.resolve_locations([(latitude,longitude)])

    return weather_service.get_weather_forecasts(
        latitude=weather_locations[0].latitude,
        longitude=weather_locations[0].longitude,
        limit=limit
    )