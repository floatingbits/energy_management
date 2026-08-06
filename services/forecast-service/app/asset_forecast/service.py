from app.asset_forecast.context.provider import AssetContextProvider
from app.asset_forecast.generators.pv_asset_forecast_generator import (
    PvAssetForecastGenerator,
)
from app.repositories.asset_forecast_repository import AssetForecastRepository
from app.services.weather_service import WeatherService
from app.weather.mappers.weather_forecast_mapper import WeatherForecastMapper


class AssetForecastService:

    def __init__(
            self,
            asset_context_provider: AssetContextProvider,
            domain_mapper: WeatherForecastMapper,
            weather_service: WeatherService,
            pv_forecast_generator: PvAssetForecastGenerator,
            asset_forecast_repository: AssetForecastRepository
    ):
        self.asset_context_provider = asset_context_provider
        self.weather_service = weather_service
        self.pv_forecast_generator = pv_forecast_generator
        self.asset_forecast_repository = asset_forecast_repository
        self.domain_mapper = domain_mapper

    def generate(
        self,
        asset_id: int
    ):
        print(asset_id)
        asset = (
            self.asset_context_provider
            .get_pv_asset_context(asset_id)
        )
        print(asset)

        db_weather = (
            self.weather_service
            .get_weather_forecasts(
                asset.latitude,
                asset.longitude,
                1
            )
        )


        domain_weather_forecast = self.domain_mapper.to_domain(db_weather[0])
        # TODO: Where will the forecast gnerated event be triggered
        series = self.pv_forecast_generator.generate(
            asset,
            domain_weather_forecast,
        )

        return self.asset_forecast_repository.save(
            asset_id=asset.asset_id,
            forecast_run=domain_weather_forecast.run,
            series=series,
        )

    def get_asset_forecast(
        self,
        asset_id: int,
    ):

        return self.asset_forecast_repository.get_latest_asset_forecast(
            asset_id
        )
