from datetime import timedelta

from app.energy.price_forecast.core.domain import EnergyPriceForecast
from app.energy.price_forecast.core.forecaster import PriceForecaster
from app.repositories.energy_price_forecast_repository import (
    EnergyPriceForecastRepository,
)


class EnergyPriceForecastService:

    def __init__(
        self,
        forecaster: PriceForecaster,
        repository: EnergyPriceForecastRepository,
    ):
        self.forecaster = forecaster
        self.repository = repository

    def generate(
        self,
        market: str,
        horizon: timedelta,
        resolution: timedelta | None = None,
    ) -> EnergyPriceForecast:
        forecast = self.forecaster.forecast(
            market=market,
            horizon=horizon,
            resolution=resolution,
        )
        self.repository.save(forecast)
        return forecast

    def get_price_forecasts(
        self,
        market: str | None = None,
    ) -> list:
        return self.repository.get_forecasts(market)

    def get_price_forecast(
        self,
        forecast_id: int,
    ):
        return self.repository.get_forecast(forecast_id)
