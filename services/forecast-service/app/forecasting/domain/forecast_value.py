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

    @property
    def is_probabilistic(self) -> bool:
        return self.p05 is not None and self.p95 is not None

    @classmethod
    def deterministic(cls, value: float) -> "ForecastValue":
        return cls(
            p05=None,
            p50=value,
            p95=None,
        )

    @classmethod
    def probabilistic(
            cls,
            p05: float,
            p50: float,
            p95: float,
    ) -> "ForecastValue":
        # hack
        if p05 > p50:
            p05, p50 = p50,p05
        if p50 > p95:
            p95, p50 = p50,p95

        return cls(
            p05=p05,
            p50=p50,
            p95=p95,
        )