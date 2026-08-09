from app.asset_forecast.clients.asset_client import AssetClient
from app.asset_forecast.service import AssetForecastService
from app.bootstrap.asset_forecast import create_asset_forecast_service, create_asset_client


class GenerateAssetForecastJob:

    def __init__(
        self,
        service: AssetForecastService,
    ):
        self.service = service

    def run(
        self,
        asset_id: int,
    ):

        return self.service.generate(
            asset_id=asset_id,
        )

class GenerateAllAssetForecastsJob:

    def __init__(
        self,
        asset_client: AssetClient,
        service: AssetForecastService
    ):
        self.asset_client = asset_client
        self.service = service

    def run(self):
        assets = self.asset_client.get_assets()

        job = GenerateAssetForecastJob(self.service)
        for asset in assets:
            result = job.run(asset['id'])

def main():

    service = create_asset_forecast_service()
    client = create_asset_client()
    job = GenerateAllAssetForecastsJob(client,service)

    job.run()




if __name__ == "__main__":
    main()