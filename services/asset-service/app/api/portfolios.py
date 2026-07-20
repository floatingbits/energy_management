from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
    PortfolioAssetResponse
)

from app.schemas.asset import AssetResponse

from app.services import portfolio_service


router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"]
)


@router.get(
    "/",
    response_model=list[PortfolioResponse]
)
def get_portfolios(
    db: Session = Depends(get_db)
):

    return portfolio_service.get_portfolios(db)



@router.get(
    "/{portfolio_id}",
    response_model=PortfolioResponse
)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):

    portfolio = portfolio_service.get_portfolio(
        db,
        portfolio_id
    )

    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    return portfolio



@router.post(
    "/",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED
)
def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db)
):

    return portfolio_service.create_portfolio(
        db,
        portfolio
    )


@router.get(
    "/{portfolio_id}/assets",
    response_model=list[AssetResponse]
)
def get_portfolio_assets(
    portfolio_id: int,
    db: Session = Depends(get_db)
):

    return portfolio_service.get_assets(
        db,
        portfolio_id
    )


@router.post(
    "/{portfolio_id}/assets/{asset_id}",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED
)
def add_asset_to_portfolio(
    portfolio_id: int,
    asset_id: int,
    db: Session = Depends(get_db)
):
    try:
        return portfolio_service.add_asset(
            db,
            portfolio_id,
            asset_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )



@router.delete(
    "/{portfolio_id}/assets/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_asset_from_portfolio(
    portfolio_id: int,
    asset_id: int,
    db: Session = Depends(get_db)
):

    portfolio_service.remove_asset(
        db,
        portfolio_id,
        asset_id
    )