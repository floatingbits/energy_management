from dataclasses import dataclass

from app.weather.location import WeatherLocation

from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase


@dataclass
class WeatherLocationForecast:

    location: WeatherLocation

    run: TimeSeriesTimeBase

    series: list[TimeSeries]


@dataclass
class WeatherForecastResult:

    provider: str

    model: str

    forecasts: list[WeatherLocationForecast]