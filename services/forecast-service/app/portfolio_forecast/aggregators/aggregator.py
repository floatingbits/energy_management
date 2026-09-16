from abc import ABC, abstractmethod

from app.portfolio_forecast.domain.timeslice import (
    TimesliceValues,
    AggregatedTimeslice,
)


class PortfolioAggregator(ABC):
    """
    Strategie-Objekt für die eigentliche Aggregations-Mathematik.

    Erhält für jede Zeitscheibe die Quantil-Tripel aller Assets
    und liefert das aggregierte Quantil-Tripel der Zeitscheibe.
    """

    @abstractmethod
    def get_name(
        self,
    ) -> str:
        pass

    @abstractmethod
    def aggregate(
        self,
        timeslice_values: list[TimesliceValues],
    ) -> AggregatedTimeslice:
        pass
