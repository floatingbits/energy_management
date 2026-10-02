from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class SarimaxConfig:
    """Model configuration of the SARIMAX price forecaster.

    This is the only model-internal configuration the forecaster
    knows; everything about data sources (markets, locations, which
    metric serves what) lives in the factories composing the
    providers.
    """

    order: tuple = (1, 0, 1)

    seasonal_order: tuple = (1, 0, 1, 24)

    # how far back history is fetched for fitting
    history: timedelta = timedelta(days=14)

    resolution: timedelta = timedelta(hours=1)
