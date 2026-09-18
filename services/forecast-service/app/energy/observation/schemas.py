from pydantic import BaseModel, ConfigDict

from app.forecasting.schemas import TimeSeriesGroupResponse


class EnergyMarketObservationResponse(BaseModel):
    """
    Observation of one or more energy market variables
    (e. g. total energy consumption, day-ahead price) for a
    location_key, fetched from a source (provider).
    """

    id: int

    location_key: str

    source: str

    observation: TimeSeriesGroupResponse

    model_config = ConfigDict(
        from_attributes=True
    )
