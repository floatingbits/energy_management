from dataclasses import dataclass
from app.forecasting.enums import ForecastValueType
from app.forecasting.encoding.definitions import DEFAULT_QUANTILE_DEFINITION, ValueDefinition


@dataclass(frozen=True)
class TimeSeriesValue:
    """A raw slot value. Its entries are ordered per the series' value
    definition (see app.forecasting.encoding); alone it carries no meaning."""

    values: tuple[float | None, ...]

    value_type: ForecastValueType = (
        ForecastValueType.FORECAST
    )

    @classmethod
    def deterministic(cls, value: float) -> "TimeSeriesValue":
        """Median-style entry for a default-quantile series (only p50 set)."""
        return cls(
            from_quantiles(p05=None, p50=value, p95=None),
        )

    @classmethod
    def probabilistic(
            cls,
            p05: float,
            p50: float,
            p95: float,
    ) -> "TimeSeriesValue":
        return cls(
            from_quantiles(p05=p05, p50=p50, p95=p95),
        )


def from_quantiles(p05: float | None, p50: float | None, p95: float | None,
                   definition: ValueDefinition = DEFAULT_QUANTILE_DEFINITION) -> tuple[float | None, ...]:
    """Pack a (p05, p50, p95) triple into a payload tuple in definition order."""
    if definition != DEFAULT_QUANTILE_DEFINITION:
        raise ValueError(
            "Building (p05, p50, p95) triplets is only supported for the "
            "default quantile definition"
        )
    return (p05, p50, p95)
