from typing import Literal

from event_contracts.base import BaseEvent


class ForecastCreatedEvent(BaseEvent):
    event_type: Literal["forecast.created"] = "forecast.created"

    asset_id: int
    forecast_count: int
