from dataclasses import dataclass
from app.forecasting.enums import ForecastValueType



@dataclass(frozen=True)
class ForecastValue:

    p50: float

    p05: float | None = None

    p95: float | None = None

    value_type: ForecastValueType = (
        ForecastValueType.FORECAST
    )