from datetime import timedelta

from app.energy.price_forecast.core.domain import EnergyPriceForecast
from app.energy.price_forecast.core.forecaster import PriceForecaster


class MarketPriceForecaster(PriceForecaster):
    """Dispatches forecast requests to market-bound forecasters.

    Since a PriceForecaster's data providers are bound to their
    non-temporal context (market, location) at composition time, one
    forecaster exists per configured market; this dispatcher keeps the
    public interface market-independent.
    """

    def __init__(self, forecasters: dict[str, PriceForecaster]):
        self.forecasters = forecasters

    def forecast(
        self,
        market: str,
        horizon: timedelta,
        resolution: timedelta | None = None,
    ) -> EnergyPriceForecast:
        if market not in self.forecasters:
            raise ValueError(
                f"No forecaster configured for market {market}, "
                f"configured: {list(self.forecasters)}"
            )
        return self.forecasters[market].forecast(
            market=market,
            horizon=horizon,
            resolution=resolution,
        )
