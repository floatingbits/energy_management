from abc import ABC, abstractmethod

from app.weather.location import WeatherLocation
from app.weather.provider_result import ProviderForecastResult
from app.weather.request import WeatherForecastRequest
from app.weather.result import WeatherLocationForecast
from app.forecasting.domain.forecast_run import ForecastRun
from app.forecasting.domain.metric import ForecastMetric


class WeatherProvider(ABC):

    @abstractmethod
    def get_forecast(
        self,
        request: WeatherForecastRequest
    ) -> ProviderForecastResult:
        raise NotImplementedError