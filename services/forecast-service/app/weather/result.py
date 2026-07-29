from dataclasses import dataclass

from app.weather.location import WeatherLocation

from app.forecasting.domain.forecast_series import ForecastSeries
from app.forecasting.domain.forecast_run import ForecastRun


@dataclass
class WeatherLocationForecast:

    location: WeatherLocation

    run: ForecastRun

    series: list[ForecastSeries]


@dataclass
class WeatherForecastResult:

    provider: str

    model: str

    forecasts: list[WeatherLocationForecast]