from enum import StrEnum


class Requirement(StrEnum):
    """A data requirement a decision strategy can declare.

    The orchestrator fulfils every required requirement via its matching
    provider; a provider may answer "unavailable" (None), in which case
    the strategy receives its request with that field unset.
    """

    PRICE_FORECAST = "price_forecast"
    PRODUCTION_FORECAST = "production_forecast"
    STORAGE_CONTEXT = "storage_context"
    GRID_CONSTRAINTS = "grid_constraints"


class StrategyRequirements:
    """The named requirements a strategy declares it needs.

    Wraps an immutable set of Requirement members instead of fixed
    booleans, so new requirements join without changing this class.
    """

    def __init__(self, required=()):
        self._required = frozenset(required)

    @classmethod
    def of(cls, *requirements: Requirement) -> "StrategyRequirements":
        return cls(requirements)

    @classmethod
    def none(cls) -> "StrategyRequirements":
        return cls(())

    @property
    def required(self) -> frozenset[Requirement]:
        return self._required

    def includes(self, requirement: Requirement) -> bool:
        return requirement in self._required

    def __iter__(self):
        return iter(self._required)

    def __bool__(self) -> bool:
        return bool(self._required)

    def __repr__(self) -> str:
        return (
            f"StrategyRequirements({sorted(r.name for r in self._required)})"
        )
