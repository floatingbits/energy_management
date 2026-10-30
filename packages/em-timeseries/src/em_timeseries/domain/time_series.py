from dataclasses import dataclass

from em_timeseries.domain.time_series_value import TimeSeriesValue
from em_timeseries.encoding.definitions import (
    DEFAULT_QUANTILE_DEFINITION,
    QuantileDefinition,
    ScalarDefinition,
    ValueDefinition,
)
from em_timeseries.encoding.serializers import QuantileParser, ScalarParser, parser_for


@dataclass
class TimeSeries:
    """A series of raw slot values.

    The metric is an opaque string here: may be a service-side enum (e.g.
    ForecastMetric), which are StrEnums and therefore strings.
    """

    metric: str

    values: list[TimeSeriesValue]

    value_definition: ValueDefinition = DEFAULT_QUANTILE_DEFINITION

    def quantile(self, value: TimeSeriesValue, level: float) -> float | None:
        """Quantile lookup on this series' definition (level is a percent, e.g. 50)."""
        return self.quantile_parser().quantile(value, level)

    def scalar(self, value: TimeSeriesValue) -> float:
        return self.scalar_parser().scalar(value)

    def is_probabilistic(self, value: TimeSeriesValue) -> bool:
        """True if a quantile series provides more than the median for a row."""
        parser = parser_for(self.value_definition)
        if not isinstance(parser, QuantileParser):
            return False
        definition = self.value_definition
        if definition.has(50):
            median = definition.index(50)
            return any(
                v is not None for i, v in enumerate(value.values) if i != median
            )
        return any(v is not None for v in value.values)

    def quantile_parser(self) -> QuantileParser:
        parser = parser_for(self.value_definition)
        if not isinstance(parser, QuantileParser):
            raise ValueError(f"Series {self.metric} is not quantile-defined")
        return parser

    def scalar_parser(self) -> ScalarParser:
        parser = parser_for(self.value_definition)
        if not isinstance(parser, ScalarParser):
            raise ValueError(f"Series {self.metric} is not scalar-defined")
        return parser
