from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.asset import (
    AssetCreate,
    AssetResponse,
    AssetUpdate
)
from app.services import asset_service
from app.messaging.publisher import EventPublisher
from app.infrastructure.messaging import get_event_publisher


router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.get(
    "/",
    response_model=list[AssetResponse]
)
def get_assets(
    db: Session = Depends(get_db)
):
    return asset_service.get_assets(db)


@router.get(
    "/{asset_id}",
    response_model=AssetResponse
)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    asset = asset_service.get_asset(
        db,
        asset_id
    )

    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    return asset


@router.post(
    "/",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED
)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    publisher: EventPublisher = Depends(get_event_publisher)
):
    return asset_service.create_asset(
        db,
        asset,
        publisher
    )


@router.put(
    "/{asset_id}",
    response_model=AssetResponse
)
def update_asset(
    asset_id: int,
    asset: AssetUpdate,
    db: Session = Depends(get_db)
):
    updated_asset = asset_service.update_asset(
        db,
        asset_id,
        asset
    )

    if updated_asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    return updated_asset


@router.delete(
    "/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    deleted = asset_service.delete_asset(
        db,
        asset_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )