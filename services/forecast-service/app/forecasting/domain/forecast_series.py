from dataclasses import dataclass

from app.forecasting.enums import ForecastMetric
from .forecast_value import ForecastValue


@dataclass
class ForecastSeries:

    metric: ForecastMetric

    values: list[ForecastValue]