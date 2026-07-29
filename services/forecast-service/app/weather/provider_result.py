from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class ProviderForecastValue:

    variable: str

    values: list[float]

@dataclass
class ProviderSeries:

    variable_name: str

    start: datetime

    resolution: timedelta

    values: list[float]

@dataclass(frozen=True)
class ProviderLocationForecast:

    latitude: float

    longitude: float

    series: list[ProviderSeries]


@dataclass(frozen=True)
class ProviderForecastResult:

    provider: str

    model: str

    forecasts: list[ProviderLocationForecast]