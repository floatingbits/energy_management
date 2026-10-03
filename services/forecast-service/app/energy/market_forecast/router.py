from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.energy.market_forecast.schemas import (
    EnergyMarketForecastResponse,
)
from app.repositories.energy_market_forecast_repository import (
    EnergyMarketForecastRepository,
)

router = APIRouter(
    prefix="/energy-market-forecasts",
    tags=["Energy Market Forecasts"],
)


@router.get(
    "/",
    response_model=list[EnergyMarketForecastResponse],
)
def get_energy_market_forecasts(
    market: str | None = None,
    variable: str | None = None,
    db: Session = Depends(get_db),
):

    repository = EnergyMarketForecastRepository(db)

    return repository.get_forecasts(market, variable)


@router.get(
    "/{forecast_id}",
    response_model=EnergyMarketForecastResponse,
)
def get_energy_market_forecast(
    forecast_id: int,
    db: Session = Depends(get_db),
):

    repository = EnergyMarketForecastRepository(db)

    forecast = repository.get_forecast(forecast_id)

    if forecast is None:
        raise HTTPException(
            status_code=404,
            detail="Energy Market Forecast not found",
        )

    return forecast
