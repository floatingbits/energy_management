from sqlalchemy.orm import Session

from app.repositories import asset_repository
from app.schemas.asset import AssetCreate
from app.models.asset import Asset


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
    asset: AssetCreate
) -> Asset:

    return asset_repository.create_asset(
        db,
        asset
    )