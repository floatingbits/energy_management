from pydantic import BaseModel, ConfigDict
from app.forecasting.schemas import TimeSeriesGroupResponse

class AssetTimeSeriesGroupResponse(BaseModel):

    id: int

    asset_id: int

    forecast: TimeSeriesGroupResponse

    model_config = ConfigDict(
        from_attributes=True
    )