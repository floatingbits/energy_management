from dataclasses import dataclass

from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase


@dataclass(frozen=True)
class EnergyPriceForecast:
    """A price forecast for an energy market.

    market is a plain string (e.g. "DE-LU"). Prices are stored as
    scalar values: every returned series carries a ScalarDefinition,
    so each TimeSeriesValue holds exactly one price.
    """

    market: str

    provider: str

    run: TimeSeriesTimeBase

    time_series: list[TimeSeries]
