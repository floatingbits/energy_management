from pydantic import BaseModel, ConfigDict

from app.forecasting.schemas import TimeSeriesGroupResponse


class EnergyPriceForecastResponse(BaseModel):
    """
    Forecast of energy market prices for a market
    (e.g. "DE-LU"), produced by a source (forecaster).
    """

    id: int

    market: str

    source: str

    forecast: TimeSeriesGroupResponse

    model_config = ConfigDict(
        from_attributes=True
    )
