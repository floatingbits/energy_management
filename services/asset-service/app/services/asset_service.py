from sqlalchemy.orm import Session

from app.repositories import asset_repository
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate
from app.events.asset_events import AssetCreatedEvent
from app.messaging.publisher import EventPublisher

def get_assets(
    db: Session
) -> list[Asset]:

    return asset_repository.get_assets(db)


def get_asset(
    db: Session,
    asset_id: int
) -> Asset | None:

    return asset_repository.get_asset_by_id(
        db,
        asset_id
    )


def create_asset(
    db: Session,
    asset: AssetCreate,
    publisher: EventPublisher
) -> Asset:

    db_asset = asset_repository.create_asset(
        db,
        asset
    )

    event = AssetCreatedEvent(
        asset_id=db_asset.id,
        asset_type=db_asset.asset_type
    )

    publisher.publish(event)

    return db_asset

def update_asset(
    db: Session,
    asset_id: int,
    asset: AssetUpdate
) -> Asset | None:

    return asset_repository.update_asset(
        db,
        asset_id,
        asset
    )

def delete_asset(
    db: Session,
    asset_id: int
) -> bool:

    return asset_repository.delete_asset(
        db,
        asset_id
    )