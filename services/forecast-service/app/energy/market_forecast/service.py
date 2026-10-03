from datetime import timedelta

from app.energy.market_forecast.core.domain import EnergyMarketForecast
from app.energy.market_forecast.core.forecaster import EnergyMarketForecaster
from app.forecasting.enums import ForecastMetric
from app.repositories.energy_market_forecast_repository import (
    EnergyMarketForecastRepository,
)


class EnergyMarketForecastService:

    def __init__(
        self,
        forecaster: EnergyMarketForecaster,
        repository: EnergyMarketForecastRepository,
    ):
        self.forecaster = forecaster
        self.repository = repository

    def generate(
        self,
        market: str,
        horizon: timedelta,
        resolution: timedelta | None = None,
        variable=None,
    ) -> EnergyMarketForecast:
        # CLI strings normalize to the interface's metric enum; enum
        # hash keys differ from the str value in the dispatcher dict.
        if isinstance(variable, str):
            variable = ForecastMetric(variable)
        forecast = self.forecaster.forecast(
            market=market,
            horizon=horizon,
            resolution=resolution,
            variable=variable,
        )
        self.repository.save(forecast)
        return forecast

    def get_market_forecasts(
        self,
        market: str | None = None,
        variable: str | None = None,
    ) -> list:
        return self.repository.get_forecasts(market, variable)

    def get_market_forecast(
        self,
        forecast_id: int,
    ):
        return self.repository.get_forecast(forecast_id)
