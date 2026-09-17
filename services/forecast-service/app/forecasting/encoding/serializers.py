import json

from app.forecasting.encoding.definitions import (
    QuantileDefinition,
    ScalarDefinition,
    ValueDefinition,
)
from app.forecasting.domain.time_series_value import TimeSeriesValue


def serialize_values(
    values: tuple[float | None, ...] | list[float | None],
    definition: ValueDefinition,
) -> str:
    """Serialize a value tuple into a JSON array payload, ordered/padded per
    the definition (missing entries become null)."""
    if len(values) != definition.arity():
        raise ValueError(
            f"Value tuple has {len(values)} entries, "
            f"definition expects {definition.arity()}"
        )
    return json.dumps(list(values))


def deserialize(payload: str, definition: ValueDefinition) -> tuple[float | None, ...]:
    """Parse a JSON array payload into a value tuple aligned with the definition."""
    data = json.loads(payload)
    if len(data) != definition.arity():
        raise ValueError(
            f"Payload has {len(data)} entries, "
            f"definition expects {definition.arity()}"
        )
    return tuple(data)


def serialize(value: "TimeSeriesValue", definition: ValueDefinition) -> str:
    """Serialize a domain value's tuple into its JSON payload."""
    return serialize_values(value.values, definition)


class QuantileParser:
    """Parser/serializer for quantile-defined payloads.

    Knows the quantile levels of one series; makes a raw payload meaningful.
    """

    def __init__(self, definition: QuantileDefinition):
        self.definition = definition

    def parse(self, payload: str) -> TimeSeriesValue:
        return TimeSeriesValue(values=deserialize(payload, self.definition))

    def serialize(self, value: TimeSeriesValue) -> str:
        return serialize_values(value.values, self.definition)

    @property
    def levels(self) -> tuple[float, ...]:
        return self.definition.quantiles

    def quantile(self, value: TimeSeriesValue, level: float) -> float | None:
        """The value at quantile `level` (percent, e.g. 50), None if absent."""
        if level not in self.definition.quantiles:
            raise ValueError(
                f"Quantile level {level} not in definition {self.definition.quantiles}"
            )
        return value.values[self.definition.quantiles.index(level)]


class ScalarParser:
    """Parser/serializer for scalar-defined payloads (non-parametric)."""

    def __init__(self, definition: ScalarDefinition):
        self.definition = definition

    def parse(self, payload: str) -> TimeSeriesValue:
        return TimeSeriesValue(values=deserialize(payload, self.definition))

    def serialize(self, value: TimeSeriesValue) -> str:
        return serialize_values(value.values, self.definition)

    def scalar(self, value: TimeSeriesValue) -> float:
        return value.values[0]


def parser_for(definition: ValueDefinition):
    if isinstance(definition, QuantileDefinition):
        return QuantileParser(definition)
    if isinstance(definition, ScalarDefinition):
        return ScalarParser(definition)
    raise ValueError(f"No parser for definition {definition!r}")
