from datetime import timedelta

from app.energy.market_forecast.core.domain import EnergyMarketForecast
from app.energy.market_forecast.core.forecaster import (
    DEFAULT_VARIABLE,
    EnergyMarketForecaster,
)
from app.forecasting.enums import ForecastMetric


class MarketForecastDispatcher(EnergyMarketForecaster):
    """Dispatches forecast requests to composed market-variable forecasters.

    Since an EnergyMarketForecaster's data providers are bound to
    their non-temporal context (market, location) at composition
    time, one forecaster exists per configured market and variable;
    this dispatcher keeps the public interface market- and
    variable-independent.
    """

    def __init__(
        self,
        forecasters: dict[tuple[str, ForecastMetric], EnergyMarketForecaster],
    ):
        self.forecasters = forecasters

    def forecast(
        self,
        market: str,
        horizon: timedelta,
        resolution: timedelta | None = None,
        variable: ForecastMetric = DEFAULT_VARIABLE,
    ) -> EnergyMarketForecast:
        key = (market, variable)
        if key not in self.forecasters:
            raise ValueError(
                f"No forecaster configured for market {market} and "
                f"variable {variable}, configured: "
                f"{[self._describe(key) for key in self.forecasters]}"
            )
        return self.forecasters[key].forecast(
            market=market,
            horizon=horizon,
            resolution=resolution,
            variable=variable,
        )

    @staticmethod
    def _describe(key: tuple[str, ForecastMetric]) -> str:
        market, variable = key
        return f"{market}/{variable}"
