from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherLocation:
    latitude: float
    longitude: float