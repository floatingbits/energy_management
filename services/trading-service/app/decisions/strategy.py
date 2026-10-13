from abc import ABC, abstractmethod

from app.decisions.request import DayAheadSalesDecisionRequest
from app.decisions.result import DayAheadSalesDecisionResult
from app.decisions.requirements import StrategyRequirements


class DayAheadSalesStrategy(ABC):
    """Base of the day-ahead sales decision strategies.

    A strategy is a calculation over separated input factors; it must
    declare what it needs (see requirements()) and work with whatever the
    orchestrator managed to provide for exactly those requirements.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Stable identifier persisted on the decision as provenance."""

    @abstractmethod
    def requirements(self) -> StrategyRequirements:
        """The requirements the strategy needs to decide."""

    @abstractmethod
    def decide(
        self,
        request: DayAheadSalesDecisionRequest,
    ) -> DayAheadSalesDecisionResult:
        """Produce the decision's time series for the delivery window."""
