from sqlalchemy.orm import Session

from app.repositories import forecast_repository


def get_forecasts(db: Session):

    return forecast_repository.get_forecasts(db)


def get_asset_forecasts(
    db: Session,
    asset_id: int
):

    return forecast_repository.get_forecasts_by_asset(
        db,
        asset_id
    )

def create_forecast_for_asset(
        asset_id: int
):
    pass