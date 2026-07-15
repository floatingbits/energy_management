from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate

def get_assets(
    db: Session
) -> list[Asset]:

    return db.query(Asset).all()


def get_asset_by_id(
    db: Session,
    asset_id: int
) -> Asset | None:

    return (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )


def create_asset(
    db: Session,
    asset: AssetCreate
) -> Asset:

    db_asset = Asset(
        name=asset.name,
        asset_type=asset.asset_type,
        installed_power_kw=asset.installed_power_kw,
        latitude=asset.latitude,
        longitude=asset.longitude,
        status=asset.status
    )

    db.add(db_asset)

    db.commit()

    db.refresh(db_asset)

    return db_asset

def update_asset(
    db: Session,
    asset_id: int,
    asset: AssetUpdate
) -> Asset | None:

    db_asset = get_asset_by_id(
        db,
        asset_id
    )

    if db_asset is None:
        return None

    update_data = asset.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_asset,
            key,
            value
        )

    db.commit()

    db.refresh(db_asset)

    return db_asset

def delete_asset(
    db: Session,
    asset_id: int
) -> bool:

    db_asset = get_asset_by_id(
        db,
        asset_id
    )

    if db_asset is None:
        return False

    db.delete(db_asset)

    db.commit()

    return True