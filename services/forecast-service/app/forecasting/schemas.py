from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict

from app.forecasting.enums import ForecastMetric


class TimeSeriesValueResponse(BaseModel):
    slot_index: int

    p05: float | None = None
    p50: float | None = None
    p95: float | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class TimeSeriesResponse(BaseModel):
    metric: ForecastMetric

    value_type_definition: str

    values: list[TimeSeriesValueResponse]

    model_config = ConfigDict(
        from_attributes=True
    )


class TimeSeriesTimeBaseResponse(BaseModel):
    id: int

    start: datetime
    resolution_seconds: int
    slots: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TimeSeriesGroupResponse(BaseModel):
    id: int

    time_series_time_base: TimeSeriesTimeBaseResponse

    time_series: list[TimeSeriesResponse]

    model_config = ConfigDict(
        from_attributes=True
    )
