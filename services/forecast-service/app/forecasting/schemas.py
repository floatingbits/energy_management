from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict

from app.forecasting.enums import ForecastMetric


class ForecastValueResponse(BaseModel):
    slot_index: int

    p05: float | None = None
    p50: float | None = None
    p95: float | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class ForecastSeriesResponse(BaseModel):
    metric: ForecastMetric

    values: list[ForecastValueResponse]

    model_config = ConfigDict(
        from_attributes=True
    )


class ForecastRunResponse(BaseModel):
    id: int

    start: datetime
    resolution_seconds: int
    slots: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ForecastResponse(BaseModel):
    id: int

    forecast_run: ForecastRunResponse

    series: list[ForecastSeriesResponse]

    model_config = ConfigDict(
        from_attributes=True
    )