import json
from abc import ABC, abstractmethod


DEFAULT_QUANTILES = (5.0, 50.0, 95.0)


class ValueDefinition(ABC):

    @abstractmethod
    def serialize(self) -> str:
        """JSON representation stored in the series' value_type_definition."""

    @abstractmethod
    def arity(self) -> int:
        """Number of entries in a payload aligned with this definition."""


class ScalarDefinition(ValueDefinition):

    def serialize(self) -> str:
        return json.dumps({"type": "scalar"})

    def arity(self) -> int:
        return 1

    def __eq__(self, other):
        return isinstance(other, ScalarDefinition)

    def __hash__(self):
        return hash("scalar")


class QuantileDefinition(ValueDefinition):

    def __init__(self, quantiles: tuple[float, ...] | list[float]):
        # Levels are percents (e.g. 5 for 5%), sorted ascending.
        self.quantiles = tuple(sorted(float(q) for q in quantiles))

    def serialize(self) -> str:
        # Serialize whole-number percents as integers so the column value stays
        # byte-compatible with previously persisted definitions: [5, 50, 95]
        levels = [int(q) if q == int(q) else q for q in self.quantiles]
        return json.dumps({"type": "quantile", "quantiles": levels})

    def arity(self) -> int:
        return len(self.quantiles)

    def index(self, level: float) -> int:
        return self.quantiles.index(float(level))

    def has(self, level: float) -> bool:
        return float(level) in self.quantiles

    def __eq__(self, other):
        return isinstance(other, QuantileDefinition) and other.quantiles == self.quantiles

    def __hash__(self):
        return hash(("quantile", self.quantiles))


DEFAULT_QUANTILE_DEFINITION = QuantileDefinition(DEFAULT_QUANTILES)


def definition_from_payload(payload: str) -> ValueDefinition:
    """Factory: build the definition encoded in a value_type_definition string."""
    data = json.loads(payload)
    value_type = data.get("type")
    if value_type == "scalar":
        return ScalarDefinition()
    if value_type == "quantile":
        return QuantileDefinition(data["quantiles"])
    raise ValueError(f"Unknown value type definition: {payload!r}")
