from dataclasses import dataclass


@dataclass(frozen=True)
class TimesliceValues:
    """
    Asset-Quantile innerhalb eines einzelnen Zeitscheibenslots
    eines aggregierten Asset-Forecasts.

    Quantile-Stufen sind Prozentwerte (z. B. 5, 50, 95) und hängen
    nicht mehr an festen p05/p50/p95-Attributen.
    """

    asset_id: int
    quantiles: dict[float, float]


@dataclass(frozen=True)
class AggregatedTimeslice:
    """
    Aggregiertes Quantile für eine einzelne
    Zeitscheibe eines Portfolio-Forecasts.
    """

    quantiles: dict[float, float]
