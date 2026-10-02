from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.energy.price_forecast.schemas import (
    EnergyPriceForecastResponse,
)
from app.repositories.energy_price_forecast_repository import (
    EnergyPriceForecastRepository,
)

router = APIRouter(
    prefix="/energy-price-forecasts",
    tags=["Energy Price Forecasts"],
)


@router.get(
    "/",
    response_model=list[EnergyPriceForecastResponse],
)
def get_energy_price_forecasts(
    market: str | None = None,
    db: Session = Depends(get_db),
):

    repository = EnergyPriceForecastRepository(db)

    return repository.get_forecasts(market)


@router.get(
    "/{forecast_id}",
    response_model=EnergyPriceForecastResponse,
)
def get_energy_price_forecast(
    forecast_id: int,
    db: Session = Depends(get_db),
):

    repository = EnergyPriceForecastRepository(db)

    forecast = repository.get_forecast(forecast_id)

    if forecast is None:
        raise HTTPException(
            status_code=404,
            detail="Energy Price Forecast not found",
        )

    return forecast
