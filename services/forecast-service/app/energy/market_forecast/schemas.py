from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.forecasting.schemas import TimeSeriesResponse, TimeSeriesGroupResponse


class EnergyMarketForecastBasisResponse(BaseModel):
    """One input time series a forecast's model consumed."""

    id: int

    role: str

    series_name: str

    # The ORM column attribute is `metadata_` (SQLAlchemy reserves the
    # declarative name `metadata`).
    metadata: Any | None = Field(
        default=None,
        validation_alias=AliasChoices("metadata_", "metadata"),
    )

    series: TimeSeriesResponse

    model_config = ConfigDict(
        from_attributes=True,
    )


class EnergyMarketForecastResponse(BaseModel):
    """
    Forecast of an energy market variable for a market
    (e.g. "DE-LU"), produced by a source (forecaster).
    """

    id: int

    market: str

    variable: str

    source: str

    forecast: TimeSeriesGroupResponse

    basis: list[EnergyMarketForecastBasisResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )
