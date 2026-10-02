from abc import ABC, abstractmethod
from datetime import timedelta

from app.energy.price_forecast.core.domain import EnergyPriceForecast


class PriceForecaster(ABC):
    """The central interface for producing energy price forecasts."""

    @abstractmethod
    def forecast(
        self,
        market: str,
        horizon: timedelta,
        resolution: timedelta | None = None,
    ) -> EnergyPriceForecast:
        """Forecast prices for a market.

        resolution=None lets the forecaster fall back to the model's
        default resolution.
        """
        raise NotImplementedError
