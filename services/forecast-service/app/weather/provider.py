from abc import ABC, abstractmethod

from app.weather.value_objects import WeatherLocation

from app.schemas.weather import WeatherForecastResult


class WeatherProvider(ABC):

    @abstractmethod
    def get_forecast(
        self,
        locations: list[WeatherLocation],
        horizon_start,
        horizon_end,
        resolution_minutes: int,
    ) -> WeatherForecastResult:
        raise NotImplementedError