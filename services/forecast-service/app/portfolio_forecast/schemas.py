from pydantic import BaseModel, ConfigDict

from app.forecasting.schemas import ForecastResponse


class PortfolioForecastResponse(BaseModel):

    id: int

    portfolio_id: int

    forecast: ForecastResponse

    model_config = ConfigDict(
        from_attributes=True
    )
