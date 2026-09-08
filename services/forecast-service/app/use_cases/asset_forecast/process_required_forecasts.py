from app.asset_forecast.service import AssetForecastService


class ProcessRequiredForecasts:

    def __init__(
        self,
        requirement_service,
        asset_forecast_service,
    ):
        self.requirement_service = requirement_service
        self.asset_forecast_service = asset_forecast_service

    def process(self) -> None:
        asset_ids = (
            self.requirement_service
            .get_assets_needing_forecasts()
        )
        print("Generating forecast for asset_ids", asset_ids)
        for asset_id in asset_ids:
            self.asset_forecast_service.generate(
                asset_id
            )