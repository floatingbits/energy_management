"""Market resolution for portfolios.

The portfolio model has no market relation yet; v1 resolves every
portfolio to the configured default market. Kept behind an interface so
asset-service can own the relation without orchestration changes.
"""

from app.config import settings


class MarketResolver:

    def market_for_portfolio(self, portfolio_id: int) -> str:
        raise NotImplementedError


class DefaultMarketResolver(MarketResolver):
    """Every portfolio trades the default market ("DE-LU") for now."""

    def market_for_portfolio(self, portfolio_id: int) -> str:
        return settings.DEFAULT_MARKET
