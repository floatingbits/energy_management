from dataclasses import dataclass
from datetime import datetime, timedelta

from app.weather.location import WeatherLocation
from app.forecasting.enums import ForecastMetric


@dataclass(frozen=True)
class WeatherForecastRequest:

    start: datetime

    end: datetime

    resolution: timedelta

    locations: list[WeatherLocation]

    variables: list[ForecastMetric]