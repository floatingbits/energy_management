from dataclasses import dataclass

from app.forecasting.domain.time_series import TimeSeries
from app.forecasting.domain.time_series_time_base import TimeSeriesTimeBase


@dataclass(frozen=True)
class EnergyObservation:

    location_key: str

    provider: str

    run: TimeSeriesTimeBase

    time_series: list[TimeSeries]
