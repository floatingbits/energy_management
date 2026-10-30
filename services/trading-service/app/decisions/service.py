"""Orchestration of day-ahead sales decisions.

The service fulfils exactly the requirements the chosen strategy
declares, via one provider per requirement, then hands the request to
the strategy and persists its result."""

from datetime import datetime, timezone
from dataclasses import replace

from app.decisions.alignment import run_on_window
from app.decisions.models import DayAheadSalesDecision
from app.decisions.providers.production_forecast import ProductionForecastProvider
from app.decisions.providers.price_forecast import PriceForecastProvider
from app.decisions.providers.storage_context import StorageContextProvider
from app.decisions.providers.grid_constraints import GridConstraintsProvider
from app.decisions.repositories.day_ahead_sales_decision_repository import (
    DayAheadSalesDecisionRepository,
)
from app.decisions.request import (
    DayAheadSalesDecisionRequest,
    DeliveryWindow,
    PriceForecastInput,
    ProductionForecastInput,
)
from app.decisions.requirements import Requirement
from app.decisions.strategy import DayAheadSalesStrategy


class DayAheadSalesDecisionService:

    def __init__(
        self,
        production_forecast_provider: ProductionForecastProvider,
        price_forecast_provider: PriceForecastProvider,
        storage_context_provider: StorageContextProvider,
        grid_constraints_provider: GridConstraintsProvider,
        strategy: DayAheadSalesStrategy,
        repository: DayAheadSalesDecisionRepository,
        market_resolver,
        delivery_day_tz: str,
    ):
        self.production_forecast_provider = production_forecast_provider
        self.price_forecast_provider = price_forecast_provider
        self.storage_context_provider = storage_context_provider
        self.grid_constraints_provider = grid_constraints_provider
        self.strategy = strategy
        self.repository = repository
        self.market_resolver = market_resolver
        self.delivery_day_tz = delivery_day_tz

    def decide_for_portfolio(
        self,
        portfolio_id: int,
        now: datetime | None = None,
    ) -> DayAheadSalesDecision:
        """Produce one decision (no overwriting/regeneration rules yet:
        every call yields a new decision)."""

        window = DeliveryWindow.next_delivery_day(
            from_ts=now or datetime.now(timezone.utc),
            tz_name=self.delivery_day_tz,
        )
        market = self.market_resolver.market_for_portfolio(portfolio_id)

        provider_for = self._provider_for()
        request = DayAheadSalesDecisionRequest(
            portfolio_id=portfolio_id,
            delivery_window=window,
            market=market,
        )

        for requirement in self.strategy.requirements():
            provider = provider_for[requirement]
            provided = provider.get(
                portfolio_id=portfolio_id,
                market=market,
                window=window,
            )
            if provided is None:
                # Provider answered "unavailable"; the strategy sees the
                # field unset and decides how to cope (or fail).
                continue
            provided = self._align_to_window(requirement, provided, window)
            setattr(request, self._field_for(requirement), provided)

        result = self.strategy.decide(request)

        return self.repository.save(
            request=request,
            result=result,
            strategy_name=self.strategy.name,
        )

    def _provider_for(self) -> dict[Requirement, object]:
        return {
            Requirement.PRODUCTION_FORECAST: self.production_forecast_provider,
            Requirement.PRICE_FORECAST: self.price_forecast_provider,
            Requirement.STORAGE_CONTEXT: self.storage_context_provider,
            Requirement.GRID_CONSTRAINTS: self.grid_constraints_provider,
        }

    @staticmethod
    def _field_for(requirement: Requirement) -> str:
        return (
            "production_forecast"
            if requirement is Requirement.PRODUCTION_FORECAST
            else "price_forecast"
            if requirement is Requirement.PRICE_FORECAST
            else "storage_context"
            if requirement is Requirement.STORAGE_CONTEXT
            else "grid_constraints"
        )

    @staticmethod
    def _align_to_window(requirement: Requirement, provided, window):
        """Place forecast requirements on the delivery window's grid.

        The mapping home-ground (see the alignment module); other
        requirement types pass through unchanged.
        """
        if requirement not in (Requirement.PRODUCTION_FORECAST, Requirement.PRICE_FORECAST):
            return provided
        if provided.run is None:
            return provided
        return replace(provided, run=run_on_window(provided.run, window))
