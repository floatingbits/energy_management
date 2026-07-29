from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Observation:

    timestamp: datetime

    value: float

    original: bool = True


from dataclasses import dataclass

from app.weather.variables import WeatherVariable


@dataclass
class TimeSeries:
    variable: WeatherVariable
    observations: list[Observation]