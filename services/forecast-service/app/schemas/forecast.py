from datetime import datetime

from pydantic import BaseModel


class ForecastResponse(BaseModel):

    id: int
    asset_id: int
    forecast_time: datetime
    predicted_power_kw: float


    model_config = {
        "from_attributes": True
    }