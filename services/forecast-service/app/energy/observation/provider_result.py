from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class ProviderObservationSeries:

    variable_name: str

    start: datetime

    resolution: timedelta

    # scalar values; None marks missing quotations
    values: list[float | None]


@dataclass(frozen=True)
class ProviderLocationObservations:

    location_key: str

    series: list[ProviderObservationSeries]


@dataclass(frozen=True)
class ProviderObservationResult:

    provider: str

    observations: list[ProviderLocationObservations]
