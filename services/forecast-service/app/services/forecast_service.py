from sqlalchemy.orm import Session
from app.services import forecast_generator
from app.repositories import forecast_repository

from event_contracts.forecast_events import ForecastCreatedEvent
from app.messaging.publisher import EventPublisher

def get_forecast(id: int, db: Session):

    return forecast_repository.get_forecast(id, db)

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
    db: Session,
    asset_id: int,
    publisher: EventPublisher
):

    forecasts = (
        forecast_generator.generate_forecasts(
            asset_id
        )
    )

    event = ForecastCreatedEvent(
        asset_id = asset_id,
        forecast_count=len(forecasts)
    )




    forecasts = (
        forecast_repository.create_forecasts(
            db,
            forecasts
        )
    )
    publisher.publish(event)
    return forecasts