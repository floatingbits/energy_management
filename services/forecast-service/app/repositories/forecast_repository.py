# repositories/forecast_repository.py

from sqlalchemy.orm import Session

from app.forecasting.models import TimeSeriesGroup


def get_forecasts(
    db: Session
):

    return (
        db.query(TimeSeriesGroup)
        .all()
    )

def get_forecast(
    id: int,
    db: Session
):

    return (
        db.query(TimeSeriesGroup)
        .filter(
            TimeSeriesGroup.id == id
        )
        .first()
    )


def get_forecasts_by_asset(
    db: Session,
    asset_id: int
):

    return (
        db.query(TimeSeriesGroup)
        .filter(
            TimeSeriesGroup.asset_id == asset_id
        )
        .all()
    )

def create_forecasts(
    db: Session,
    forecasts: list[TimeSeriesGroup]
):

    db.add_all(forecasts)

    db.commit()

    for forecast in forecasts:
        db.refresh(forecast)

    return forecasts