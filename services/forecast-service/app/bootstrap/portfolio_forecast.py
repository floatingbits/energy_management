from app.database import SessionLocal
from app.portfolio_forecast.aggregators.naive import (
    NaivePortfolioAggregator,
)
from app.portfolio_forecast.clients.portfolio_client import (
    PortfolioClient,
)
from app.portfolio_forecast.service import (
    PortfolioForecastService,
)
from app.repositories.asset_forecast_repository import (
    AssetForecastRepository,
)
from app.repositories.portfolio_forecast_repository import (
    PortfolioForecastRepository,
)


def create_portfolio_client():
    return PortfolioClient(
        base_url="http://asset-service:8000/api/v1"
    )


def create_portfolio_aggregator():
    # Austauschpunkt für die Aggregations-Strategie
    # (z.B. "naive" -> probabilistische Aggregation).
    return NaivePortfolioAggregator()


def create_portfolio_forecast_service():
    db_session = SessionLocal()

    return PortfolioForecastService(
        portfolio_client=create_portfolio_client(),
        portfolio_forecast_repository=(
            PortfolioForecastRepository(db_session)
        ),
        asset_forecast_repository=(
            AssetForecastRepository(db_session)
        ),
        aggregator=create_portfolio_aggregator(),
    )
