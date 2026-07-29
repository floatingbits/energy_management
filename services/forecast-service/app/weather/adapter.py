from abc import ABC, abstractmethod

from app.weather.provider_result import ProviderForecastResult
from app.weather.request import WeatherForecastRequest
from app.weather.result import WeatherForecastResult


class WeatherAdapter(ABC):

    @abstractmethod
    def adapt(
        self,
        provider_result: ProviderForecastResult,
        request: WeatherForecastRequest
    ) -> WeatherForecastResult:
        raise NotImplementedError