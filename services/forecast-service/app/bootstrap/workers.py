from app.bootstrap.asset_forecast import (
    create_asset_forecast_service,
)
from app.bootstrap.services import (
    create_asset_service, create_weather_forecast_requirement_service,
)
from app.bootstrap.forecast_requirements import (
    create_asset_forecast_requirement_service,
)
from app.bootstrap.weather import create_weather_service

from app.use_cases.asset_forecast.process_required_forecasts import (
    ProcessRequiredForecasts
)

from app.workers.asset_forecast_worker import (
    AssetForecastWorker,
)


def create_asset_forecast_worker():

    use_case = ProcessRequiredForecasts(
        requirement_service=
            create_asset_forecast_requirement_service(),
        asset_service=create_asset_service(),
        asset_forecast_service=
            create_asset_forecast_service(),
        weather_forecast_requirement_service=create_weather_forecast_requirement_service()
    )

    return AssetForecastWorker(use_case)