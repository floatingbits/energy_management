from app.asset_forecast.service import (
    AssetForecastService,
)

from app.asset_forecast.generators.pv_asset_forecast_generator import (
    PvAssetForecastGenerator,
)

from app.asset_forecast.calculators.pv_forecast_calculator import (
    PvForecastCalculator,
)

from app.asset_forecast.calculators.pv_power_calculator import (
    PvPowerCalculator,
)

from app.asset_forecast.calculators.plane_of_array_calculator import (
    PlaneOfArrayCalculator,
)

from app.asset_forecast.calculators.solar_geometry_calculator import (
    SolarGeometryCalculator,
)

from app.asset_forecast.context.api_provider import (
    ApiAssetContextProvider,
)

from app.asset_forecast.clients.asset_client import (
    AssetClient,
)

from app.bootstrap.weather import (
    create_weather_service,
)
from app.database import SessionLocal
from app.repositories.asset_forecast_repository import AssetForecastRepository
from app.weather.mappers.weather_forecast_mapper import WeatherForecastMapper


def create_asset_forecast_service():
    db_session = SessionLocal()

    asset_client = AssetClient(
        base_url="http://asset-service:8000/api/v1"
    )

    asset_context_provider = (
        ApiAssetContextProvider(
            asset_client
        )
    )


    calculator = PvForecastCalculator(
        solar_geometry_calculator=(
            SolarGeometryCalculator()
        ),
        plane_of_array_calculator=(
            PlaneOfArrayCalculator()
        ),
        pv_power_calculator=(
            PvPowerCalculator()
        ),
    )


    generator = (
        PvAssetForecastGenerator(
            calculator
        )
    )

    repository = AssetForecastRepository(db_session)


    return AssetForecastService(
        asset_context_provider=(
            asset_context_provider
        ),
        domain_mapper=WeatherForecastMapper(),
        weather_service=(
            create_weather_service()
        ),
        pv_forecast_generator=generator,
        asset_forecast_repository=repository
    )