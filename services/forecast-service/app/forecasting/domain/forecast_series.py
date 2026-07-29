from dataclasses import dataclass

from .metric import ForecastMetric
from .forecast_value import ForecastValue


@dataclass
class ForecastSeries:

    metric: ForecastMetric

    values: list[ForecastValue]