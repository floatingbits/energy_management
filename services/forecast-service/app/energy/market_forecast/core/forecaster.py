from abc import ABC, abstractmethod
from datetime import timedelta

from app.energy.market_forecast.core.domain import EnergyMarketForecast
from app.forecasting.enums import ForecastMetric

# The variable a market forecaster predicts when a request does not
# name one. Another model forecaster per variable may be composed in
# the bootstrap as soon as a second variable needs a forecast.
DEFAULT_VARIABLE = ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE


class EnergyMarketForecaster(ABC):
    """The central interface for producing energy market forecasts."""

    @abstractmethod
    def forecast(
        self,
        market: str,
        horizon: timedelta,
        resolution: timedelta | None = None,
        variable: ForecastMetric = DEFAULT_VARIABLE,
    ) -> EnergyMarketForecast:
        """Forecast a variable for a market.

        resolution=None lets the forecaster fall back to the model's
        default resolution.
        """
        raise NotImplementedError
