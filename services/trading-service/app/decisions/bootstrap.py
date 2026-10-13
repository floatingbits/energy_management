"""Wiring for the day-ahead sales decision feature (mirror of
forecast-service's bootstrap)."""

from em_timeseries.grid import TimeSeriesRun  # noqa: F401  (typing aid)

from app.config import settings
from app.database import SessionLocal
from app.decisions.alignment import DELIVERY_RESOLUTION_SECONDS  # noqa: F401  (public re-export)
from app.decisions.market import DefaultMarketResolver
from app.decisions.providers.forecast_client import ForecastServiceClient
from app.decisions.providers.portfolios import PortfolioClient
from app.decisions.providers.production_forecast import (
    ForecastServiceProductionForecastProvider,
)
from app.decisions.providers.price_forecast import (
    ForecastServicePriceForecastProvider,
)
from app.decisions.providers.storage_context import (
    StorageContextUnavailableProvider,
)
from app.decisions.providers.grid_constraints import (
    GridConstraintsUnavailableProvider,
)
from app.decisions.repositories.day_ahead_sales_decision_repository import (
    DayAheadSalesDecisionRepository,
)
from app.decisions.service import DayAheadSalesDecisionService
from app.decisions.strategies.simple_conservative import (
    SimpleConservativeDayAheadSalesStrategy,
)


def create_forecast_client():
    return ForecastServiceClient(
        base_url=settings.FORECAST_API_URL,
    )


def create_portfolio_client():
    return PortfolioClient(
        base_url=settings.ASSET_API_URL,
    )


def create_portfolio_forecast_provider():
    return ForecastServiceProductionForecastProvider(
        client=create_forecast_client(),
    )


def create_price_forecast_provider():
    return ForecastServicePriceForecastProvider(
        client=create_forecast_client(),
    )


def create_day_ahead_sales_decision_service():
    return DayAheadSalesDecisionService(
        production_forecast_provider=create_portfolio_forecast_provider(),
        price_forecast_provider=create_price_forecast_provider(),
        storage_context_provider=StorageContextUnavailableProvider(),
        grid_constraints_provider=GridConstraintsUnavailableProvider(),
        strategy=SimpleConservativeDayAheadSalesStrategy(),
        repository=DayAheadSalesDecisionRepository(SessionLocal()),
        market_resolver=DefaultMarketResolver(),
        delivery_day_tz=settings.DELIVERY_DAY_TZ,
    )
