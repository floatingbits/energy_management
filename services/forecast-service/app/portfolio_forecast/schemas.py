from pydantic import BaseModel, ConfigDict

from app.forecasting.schemas import TimeSeriesGroupResponse


class PortfolioTimeSeriesGroupResponse(BaseModel):

    id: int

    portfolio_id: int

    forecast: TimeSeriesGroupResponse

    model_config = ConfigDict(
        from_attributes=True
    )
