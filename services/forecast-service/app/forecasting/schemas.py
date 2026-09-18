import json

from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator

from app.forecasting.enums import ForecastMetric


class TimeSeriesValueResponse(BaseModel):
    """
    Ein Wert innerhalb einer Serie, bestehend aus dem Slot-Index und
    dem Payload als Zahlenarray — geordnet nach der Definition
    der Serie (siehe value_type_definition am TimeSeriesResponse).
    """

    slot_index: int

    values: list[float | None]

    @model_validator(mode="before")
    @classmethod
    def _values_from_payload(cls, data):
        """Accept a TimeSeriesValue model (from_attributes mode). The
        stored payload is a JSON array, definition-agnostic: the
        semantics are documented by the series' value_type_definition."""
        if (
            hasattr(data, "slot_index")
            and hasattr(data, "payload")
            and not hasattr(data, "values")
        ):
            return {
                "slot_index": data.slot_index,
                "values": json.loads(data.payload),
            }

        return data

    model_config = ConfigDict(
        from_attributes=True
    )


class TimeSeriesResponse(BaseModel):
    """
    Eine Serie mit ihrer Wert-Definition (z. B.
    {"type": "quantile", "quantiles": [5, 50, 95]}). Das
    values-Array je Wert ist bezüglich dieser Definition geordnet.
    """

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
