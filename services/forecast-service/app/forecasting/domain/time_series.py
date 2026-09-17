from dataclasses import dataclass

from app.forecasting.enums import ForecastMetric
from app.forecasting.domain.time_series_value import TimeSeriesValue


@dataclass
class TimeSeries:

    metric: ForecastMetric

    values: list[TimeSeriesValue]