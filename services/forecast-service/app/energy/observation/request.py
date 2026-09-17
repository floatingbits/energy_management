from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from app.forecasting.enums import ForecastMetric


@dataclass(frozen=True)
class EnergyObservationRequest:

    variables: list[ForecastMetric]

    resolution: timedelta = timedelta(minutes=15)

    region: str = "DE"

    # start of the observation window; None fetches the latest available series
    start: datetime | None = None
