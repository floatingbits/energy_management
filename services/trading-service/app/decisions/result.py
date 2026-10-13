from dataclasses import dataclass

from em_timeseries.domain import TimeSeriesValue
from em_timeseries.encoding import ValueDefinition


@dataclass
class DayAheadSalesDecisionResult:
    """The strategy's output for one delivery window.

    The TimeSeries structure allows n series; v1 features exactly one
    (the planned sell volumes for the window's delivery slots).
    """

    metric: str

    value_definition: ValueDefinition

    values: list[TimeSeriesValue]

    # Provenance: the production-forecast quantile level the plan settled
    # on, when applicable (None when obtained otherwise).
    quantile_level: float | None = None

    notes: str | None = None
