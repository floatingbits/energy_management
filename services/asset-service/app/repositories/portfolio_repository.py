from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate
from app.repositories.asset_repository import get_asset_by_id

def get_portfolios(
    db: Session
) -> list[Portfolio]:

    return db.query(Portfolio).all()


def get_portfolio(
    db: Session,
    portfolio_id: int
) -> Portfolio | None:

    return (
        db.query(Portfolio)
        .filter(
            Portfolio.id == portfolio_id
        )
        .first()
    )


def create_portfolio(
    db: Session,
    portfolio: PortfolioCreate
) -> Portfolio:

    db_portfolio = Portfolio(
        name=portfolio.name,
        description=portfolio.description
    )

    db.add(db_portfolio)

    db.commit()

    db.refresh(db_portfolio)

    return db_portfolio

def add_asset(
    db: Session,
        portfolio_id: int,
        asset_id: int
):
    portfolio = get_portfolio(db, portfolio_id)


    if portfolio is None:
        raise ValueError(
            "Portfolio not found"
        )

    asset = get_asset_by_id(db, asset_id)


    if asset is None:
        raise ValueError(
            "Asset not found"
        )

    if asset in portfolio.assets:
        return portfolio

    portfolio.assets.append(asset)

    db.commit()

    db.refresh(portfolio)

    return portfolio

def remove_asset(
    db,
    portfolio_id: int,
        asset_id: int
):
    portfolio = get_portfolio(
        db,
        portfolio_id
    )
    if portfolio is None:
        raise ValueError(
            "Portfolio not found"
        )

    asset = get_asset_by_id(
        db,
        asset_id
    )
    if asset is None:
        raise ValueError(
            "Asset not found"
        )

    portfolio.assets.remove(asset)

    db.commit()