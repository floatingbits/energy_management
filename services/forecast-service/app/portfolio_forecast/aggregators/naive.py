from app.portfolio_forecast.aggregators.aggregator import (
    PortfolioAggregator,
)
from app.portfolio_forecast.domain.timeslice import (
    TimesliceValues,
    AggregatedTimeslice,
)


class NaivePortfolioAggregator(PortfolioAggregator):
    """
    Naive Aggregation: Quantil-weise Summation über alle Assets.

    Unterstellte Kausal-Korrelation zwischen den Assets — die
    Aggregate tendieren damit bewusst stärker zu den Randquantilen
    als in der Realität zu erwarten wäre. Soll später durch eine
    probabilistische Aggregation ersetzt werden.
    """

    def get_name(
        self,
    ) -> str:
        return "naive"

    def aggregate(
        self,
        timeslice_values: list[TimesliceValues],
    ) -> AggregatedTimeslice:

        if not timeslice_values:
            raise ValueError(
                "No asset timeslices to aggregate."
            )

        return AggregatedTimeslice(
            p05=sum(value.p05 for value in timeslice_values),
            p50=sum(value.p50 for value in timeslice_values),
            p95=sum(value.p95 for value in timeslice_values),
        )
