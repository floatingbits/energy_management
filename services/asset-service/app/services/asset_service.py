from sqlalchemy.orm import Session

from app.mapper import to_response, to_response_list, create_asset_model
from app.repositories import asset_repository
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate
from event_contracts.asset_events import AssetCreatedEvent, AssetUpdatedEvent
from app.messaging.publisher import EventPublisher

def get_assets(
    db: Session
) -> list[Asset]:

    assets = asset_repository.get_assets(db)
    return to_response_list(assets)



def get_asset(
    db: Session,
    asset_id: int
) -> Asset | None:

    asset =  asset_repository.get_asset_by_id(
        db,
        asset_id
    )
    return to_response(asset)


def create_asset(
    db: Session,
    asset: AssetCreate,
    publisher: EventPublisher
) -> Asset:

    db_asset = create_asset_model(
        asset
    )

    asset_repository.save_asset(db,db_asset)
    event = AssetCreatedEvent(
        asset_id=db_asset.id,
        asset_type=db_asset.asset_type
    )

    publisher.publish(event)

    return to_response(db_asset)

def update_asset(
    db: Session,
    asset_id: int,
    asset: AssetUpdate,
    publisher: EventPublisher
) -> Asset | None:

    db_asset = asset_repository.update_asset(
        db,
        asset_id,
        asset
    )
    if db_asset:
        event = AssetUpdatedEvent(
            asset_id=db_asset.id,
            revision=db_asset.revision,
            changed_fields=[]
        )

        publisher.publish(event)

    return to_response(db_asset)

def delete_asset(
    db: Session,
    asset_id: int
) -> bool:

    return asset_repository.delete_asset(
        db,
        asset_id
    )