from pydantic import BaseModel, ConfigDict

from app.forecasting.schemas import TimeSeriesGroupResponse

class WeatherSourceResponse(BaseModel):
    provider: str
    model: str

    model_config = ConfigDict(
        from_attributes=True
    )

class WeatherForecastResponse(BaseModel):
    id: int

    latitude: float
    longitude: float

    source: WeatherSourceResponse

    forecast: TimeSeriesGroupResponse

    model_config = ConfigDict(
        from_attributes=True
    )

