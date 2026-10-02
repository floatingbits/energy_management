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
# Relevant Wind locations roughly taken from:
# https://www.disy.net/fileadmin/Bilder-Dokumente/01_Produkte/02_Cadenza/9_Showroom/Datenstory/2023/1-Windenergie-Windkraftanlagen-Deutschland-Punkte-Heatmap_.jpg
# Relevant Solar power locations roughly derived from:
# https://www.gfk-solar.de/solar-karte-deutschland/
# https://solarfarmmap.com/

VARIABLE_LOCATIONS_DE: dict[str, list[WeatherLocation]] = {
        ForecastMetric.WIND_SPEED: [
            WeatherLocation(latitude=53.73, longitude=6.64), # Roughly Borkum (Bc of Borkum Off-Shore Cluster)
            WeatherLocation(latitude=54.66, longitude=8.88), # Schleswig Holstein
            WeatherLocation(latitude=53.24, longitude=14.21), # Northeast
            WeatherLocation(latitude=52.63, longitude=6.95), # West
            WeatherLocation(latitude=51.76, longitude=10.31), # Harz
            WeatherLocation(latitude=50.11, longitude=7.89), # Rhineland-Palatinat
        ],
        ForecastMetric.GLOBAL_SOLAR_IRRADIANCE: [
            WeatherLocation(latitude=48.84, longitude=11.55), # Center of bavaria (most installed power)
            WeatherLocation(latitude=52.5, longitude=13.33), # Berlin + Brandenburg (High density)
            WeatherLocation(latitude=52.63, longitude=6.95), # West
            WeatherLocation(latitude=49.37, longitude=8.88), # South west
        ]
    }
MARKET_LOCATIONS: dict[str, dict[str, list[WeatherLocation]]] = {
    "DE-LU": VARIABLE_LOCATIONS_DE,
    "DE": VARIABLE_LOCATIONS_DE,
}

EXOGENOUS_VARIABLES: list[ForecastMetric] = [
    ForecastMetric.WIND_SPEED,
    ForecastMetric.GLOBAL_SOLAR_IRRADIANCE,
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
        (variable + "-" + str(i)): create_weather_time_series_provider(
            metric=variable,
            location=location
        )
        for variable in EXOGENOUS_VARIABLES
            for i,location in enumerate(MARKET_LOCATIONS[market][str(variable)])


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
