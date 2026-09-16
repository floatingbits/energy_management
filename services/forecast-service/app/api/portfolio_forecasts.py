from fastapi import APIRouter, Depends, HTTPException

from app.bootstrap.portfolio_forecast import (
    create_portfolio_forecast_service,
)
from app.portfolio_forecast.schemas import PortfolioForecastResponse


router = APIRouter(
    prefix="/portfolio-forecasts",
    tags=["Portfolio Forecasts"],
)


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioForecastResponse,
)
def get_portfolio_forecast(
    portfolio_id: int,
    service=Depends(create_portfolio_forecast_service),
):

    forecast = (
        service.get_portfolio_forecast(
            portfolio_id,
        )
    )

    if forecast is None:
        raise HTTPException(
            status_code=404,
            detail="Forecast not found",
        )

    return forecast
