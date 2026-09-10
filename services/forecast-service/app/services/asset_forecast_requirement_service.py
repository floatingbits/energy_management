from app.repositories.asset_forecast_requirement_repository import AssetForecastRequirementRepository
from app.repositories.asset_forecast_repository import AssetForecastRepository
from app.asset_forecast.models.asset_forecast_requirement import (
    AssetForecastRequirement,
)
class AssetForecastRequirementService:

    def __init__(
        self,
        requirement_repository: AssetForecastRequirementRepository,
        forecast_repository: AssetForecastRepository
    ):
        self.requirement_repository = requirement_repository
        self.forecast_repository = forecast_repository

    def require(
        self,
        asset_id: int,
        revision: int,
    ) -> None:
        self.requirement_repository.require(
            asset_id=asset_id,
            revision=revision,
        )

    def get_all(self):
        return self.requirement_repository.get_all()

    def get_assets_needing_forecasts(self) -> list[int]:
        requirements = (
            self.requirement_repository.get_all()
        )

        result = []

        for requirement in requirements:
            forecast = (
                self.forecast_repository
                .get_latest_asset_forecast(
                    requirement.asset_id
                )
            )

            if (
                    forecast is None
                    or forecast.based_on_revision
                    < requirement.required_revision
            ):
                result.append(requirement.asset_id)

        return result

    def check_requirement(self,
                requirement: AssetForecastRequirement,
                weather_forecast_id: int
            ) -> bool:
        asset_forecast = self.forecast_repository.get_for_requirements(requirement.asset_id, requirement.required_revision,weather_forecast_id)
        return asset_forecast is not None


