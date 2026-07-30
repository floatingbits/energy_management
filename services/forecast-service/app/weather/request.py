from dataclasses import dataclass
from datetime import datetime

from app.weather.location import WeatherLocation
from app.forecasting.enums import ForecastMetric


@dataclass(frozen=True)
class WeatherForecastRequest:

    start: datetime

    end: datetime

    locations: list[WeatherLocation]

    variables: list[ForecastMetric]