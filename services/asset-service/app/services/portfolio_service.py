from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.mapper import to_response, to_response_list
from app.repositories import portfolio_repository, asset_repository

from app.schemas.portfolio import PortfolioCreate


def get_portfolios(
    db: Session
):

    return portfolio_repository.get_portfolios(db)


def get_portfolio(
    db: Session,
    portfolio_id: int
):

    return portfolio_repository.get_portfolio(
        db,
        portfolio_id
    )

def get_assets(
    db: Session,
    portfolio_id: int
):
    portfolio = portfolio_repository.get_portfolio(
        db,
        portfolio_id
    )

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    return to_response_list(asset_repository.get_assets_by_portfolio(
        db,
        portfolio_id
    ))


def create_portfolio(
    db: Session,
    portfolio: PortfolioCreate
):

    return portfolio_repository.create_portfolio(
        db,
        portfolio
    )

def add_asset(
    db: Session,
    portfolio_id: int,
    asset_id: int
):

    return portfolio_repository.add_asset(
        db,
        portfolio_id,
        asset_id
    )

def remove_asset(
    db: Session,
    portfolio_id: int,
    asset_id: int
):

    return portfolio_repository.remove_asset(
        db,
        portfolio_id,
        asset_id
    )