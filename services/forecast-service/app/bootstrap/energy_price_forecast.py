from datetime import timedelta

from app.bootstrap.energy_observation import create_smard_provider
from app.bootstrap.weather import create_weather_service
from app.database import SessionLocal
from app.energy.price_forecast.core.market_forecaster import (
    MarketPriceForecaster,
)
from app.energy.price_forecast.service import (
    EnergyPriceForecastService,
)
from app.energy.price_forecast.sarimax.config import SarimaxConfig
from app.energy.price_forecast.sarimax.forecaster import (
    SarimaxPriceForecaster,
)
from app.forecasting.enums import ForecastMetric
from app.repositories.energy_price_forecast_repository import (
    EnergyPriceForecastRepository,
)
from app.timeseries.providers.energy import EnergyTimeSeriesProvider
from app.timeseries.providers.weather import WeatherTimeSeriesProvider
from app.weather.location import WeatherLocation

# Composition: which markets get forecasters, and what each market
# needs — endogenous metric and the exogenous variables' locations.
MARKET_LOCATIONS: dict[str, WeatherLocation] = {
    "DE-LU": WeatherLocation(latitude=52.52, longitude=13.405),
    "DE": WeatherLocation(latitude=52.52, longitude=13.405),
}

EXOGENOUS_VARIABLES: list[ForecastMetric] = [
    ForecastMetric.TEMPERATURE,
]


def create_energy_time_series_provider(
    metric: ForecastMetric,
    market: str,
):
    return EnergyTimeSeriesProvider(
        provider=create_smard_provider(),
        metric=metric,
        market=market,
    )


def create_weather_time_series_provider(
    metric: ForecastMetric,
    location: WeatherLocation,
):
    return WeatherTimeSeriesProvider(
        weather_service=create_weather_service(),
        metric=metric,
        location=location,
    )


def create_market_price_forecaster(market: str):
    """Compose the market-bound data providers and the SARIMAX model
    wrapper for one market."""
    sarimax_config = SarimaxConfig()

    exogenous_providers = {
        variable: create_weather_time_series_provider(
            metric=variable,
            location=MARKET_LOCATIONS[market],
        )
        for variable in EXOGENOUS_VARIABLES
    }

    return SarimaxPriceForecaster(
        market=market,
        price_provider=create_energy_time_series_provider(
            metric=ForecastMetric.DAY_AHEAD_ELECTRICITY_PRICE,
            market=market,
        ),
        exogenous_providers=exogenous_providers,
        config=sarimax_config,
    )


def create_price_forecaster() -> MarketPriceForecaster:
    return MarketPriceForecaster(
        forecasters={
            market: create_market_price_forecaster(market)
            for market in MARKET_LOCATIONS
        }
    )


def create_energy_price_forecast_repository():
    return EnergyPriceForecastRepository(
        SessionLocal(),
    )


def create_energy_price_forecast_service():
    return EnergyPriceForecastService(
        forecaster=create_price_forecaster(),
        repository=create_energy_price_forecast_repository(),
    )
