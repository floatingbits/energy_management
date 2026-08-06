from http.client import HTTPException

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.asset_forecast.schemas import AssetForecastResponse
from app.database import get_db
from app.bootstrap.asset_forecast import (
    create_asset_forecast_service,
)

router = APIRouter(
    prefix="/asset-forecasts",
    tags=["Asset Forecasts"],
)


@router.post(
    "/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def generate_asset_forecast(
    asset_id: int,
    service = Depends(create_asset_forecast_service),
):

    service.generate(
        asset_id=asset_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.get(
    "/{asset_id}",
    response_model=AssetForecastResponse,
)
def get_asset_forecast(
    asset_id: int,
    service= Depends(create_asset_forecast_service),
):

    forecast = (
        service.get_asset_forecast(
            asset_id,
        )
    )

    if forecast is None:
        raise HTTPException(
            status_code=404,
            detail="Forecast not found",
        )

    return forecast