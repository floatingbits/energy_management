from app.weather.provider import WeatherProvider
from app.weather.location import WeatherLocation
from app.weather.request import WeatherForecastRequest

from app.weather.result import (
    WeatherForecastResult,
    WeatherLocationForecast
)


from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_value import ForecastValue
from app.forecasting.domain.metric import ForecastMetric
from app.forecasting.domain.forecast_run import ForecastRun

class OpenMeteoProvider(WeatherProvider):

    def get_forecast(
            self,
            request: WeatherForecastRequest
    ) -> WeatherForecastResult:

        raise NotImplementedError