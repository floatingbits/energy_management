from dataclasses import dataclass


@dataclass(frozen=True)
class TimesliceValues:
    """
    Asset-Quantile innerhalb eines einzelnen Zeitscheibenslots
    eines aggregierten Asset-Forecasts.
    """

    asset_id: int
    p05: float
    p50: float
    p95: float


@dataclass(frozen=True)
class AggregatedTimeslice:
    """
    Aggregiertes Quantile-Tripel für eine einzelne
    Zeitscheibe eines Portfolio-Forecasts.
    """

    p05: float
    p50: float
    p95: float
