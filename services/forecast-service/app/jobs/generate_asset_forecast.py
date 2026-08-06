from app.asset_forecast.service import AssetForecastService
from app.bootstrap.asset_forecast import create_asset_forecast_service


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


def main():

    service = create_asset_forecast_service()
    job = GenerateAssetForecastJob(service)
    result = job.run(1)
    print(result)



if __name__ == "__main__":
    main()