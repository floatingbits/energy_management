from dataclasses import dataclass

from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase
from app.forecasting.domain.time_series import TimeSeries

@dataclass
class TimeSeriesGroup:
    time_series_time_base: TimeSeriesTimeBase
    time_series: list[TimeSeries]
