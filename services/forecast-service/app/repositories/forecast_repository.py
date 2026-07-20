# repositories/forecast_repository.py

from sqlalchemy.orm import Session

from app.models.forecast import Forecast


def get_forecasts(
    db: Session
):

    return (
        db.query(Forecast)
        .all()
    )

def get_forecast(
    id: int,
    db: Session
):

    return (
        db.query(Forecast)
        .filter(
            Forecast.id == id
        )
        .first()
    )


def get_forecasts_by_asset(
    db: Session,
    asset_id: int
):

    return (
        db.query(Forecast)
        .filter(
            Forecast.asset_id == asset_id
        )
        .all()
    )

def create_forecasts(
    db: Session,
    forecasts: list[Forecast]
):

    db.add_all(forecasts)

    db.commit()

    for forecast in forecasts:
        db.refresh(forecast)

    return forecasts