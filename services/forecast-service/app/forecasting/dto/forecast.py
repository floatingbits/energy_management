from dataclasses import dataclass

from app.forecasting.domain.forecast_run import ForecastRun
from app.forecasting.domain.forecast_series import ForecastSeries

@dataclass
class ForecastResult:
    run: ForecastRun
    series: list[ForecastSeries]