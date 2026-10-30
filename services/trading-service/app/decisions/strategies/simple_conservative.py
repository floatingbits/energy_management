"""The conservative baseline day-ahead sales strategy.

Deliberately minimal: it sells the pessimistic (p05) production of the
portfolio for every slot of the delivery day, regardless of price. The
concrete calculation is meant to grow by hand; plumbing (alignment,
persistence, provenance) is already in place.
"""

from em_timeseries.domain import TimeSeriesValue
from em_timeseries.encoding import ScalarDefinition, QuantileDefinition

from app.decisions.request import DayAheadSalesDecisionRequest
from app.decisions.requirements import Requirement, StrategyRequirements
from app.decisions.result import DayAheadSalesDecisionResult
from app.decisions.strategy import DayAheadSalesStrategy

# The pessimistic level the sell plan settles on.
SELL_QUANTILE_LEVEL = 5.0

SELL_PLAN_METRIC = "day_ahead_sell_plan"

COVERAGE_NOTE = (
    "Slots not covered by the production forecast cannot be planned."
)


class SimpleConservativeDayAheadSalesStrategy(DayAheadSalesStrategy):
    """Sell p05 of the production forecast for every delivery slot."""

    @property
    def name(self) -> str:
        return "simple_conservative"

    def requirements(self) -> StrategyRequirements:
        # Price forecast is declared although v1 ignores it: the
        # conservative baseline is price-agnostic today, and the
        # requirement exercises the plumbing until the real calculation
        # (you write it by hand) uses the price.
        return StrategyRequirements.of(
            Requirement.PRODUCTION_FORECAST,
            Requirement.PRICE_FORECAST,
        )

    def decide(
        self,
        request: DayAheadSalesDecisionRequest,
    ) -> DayAheadSalesDecisionResult:
        production = request.production_forecast
        if production is None or production.run is None:
            raise ValueError(
                "Strategy requires a production forecast; none provided"
            )

        run = production.run
        if not isinstance(run.series.value_definition, QuantileDefinition):
            raise ValueError(
                "Conservative strategy expects a quantile-defined "
                "production forecast"
            )

        values = []
        for value in run.series.values:
            level = run.series.quantile(value, SELL_QUANTILE_LEVEL)
            if level is None:
                raise ValueError(COVERAGE_NOTE)
            # A decision series is scalar-defined; its payload is one number.
            values.append(TimeSeriesValue(values=(level,)))

        return DayAheadSalesDecisionResult(
            metric=SELL_PLAN_METRIC,
            value_definition=ScalarDefinition(),
            values=values,
            quantile_level=SELL_QUANTILE_LEVEL,
            notes="Sells p05 of the production forecast per hour.",
        )
