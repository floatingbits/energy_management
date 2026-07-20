from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.forecast import ForecastResponse
from app.services import forecast_service


router = APIRouter(
    prefix="/forecasts",
    tags=["Forecasts"]
)


@router.get(
    "/",
    response_model=list[ForecastResponse]
)
def get_forecasts(
    db: Session = Depends(get_db)
):

    return forecast_service.get_forecasts(db)

@router.get(
    "/{id}",
    response_model=ForecastResponse
)
def get_forecast(
        id: int,
    db: Session = Depends(get_db)
):

    return forecast_service.get_forecast(id, db)


@router.get(
    "/asset/{asset_id}",
    response_model=list[ForecastResponse]
)
def get_asset_forecasts(
    asset_id: int,
    db: Session = Depends(get_db)
):

    return forecast_service.get_asset_forecasts(
        db,
        asset_id
    )