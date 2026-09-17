from fastapi import APIRouter, Depends, HTTPException

from app.bootstrap.portfolio_forecast import (
    create_portfolio_forecast_service,
)
from app.portfolio_forecast.schemas import PortfolioTimeSeriesGroupResponse


router = APIRouter(
    prefix="/portfolio-forecasts",
    tags=["Portfolio Forecasts"],
)


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioTimeSeriesGroupResponse,
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
            detail="TimeSeriesGroup not found",
        )

    return forecast
