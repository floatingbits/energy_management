from pydantic import BaseModel, ConfigDict
from app.forecasting.schemas import ForecastResponse

class AssetForecastResponse(BaseModel):

    id: int

    asset_id: int

    forecast: ForecastResponse

    model_config = ConfigDict(
        from_attributes=True
    )