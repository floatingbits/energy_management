from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate


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