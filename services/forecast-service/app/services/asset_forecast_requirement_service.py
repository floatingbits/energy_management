from app.repositories.asset_forecast_requirement_repository import AssetForecastRequirementRepository


class AssetForecastRequirementService:

    def __init__(
        self,
        repository: AssetForecastRequirementRepository,
    ):
        self.repository = repository

    def require(
        self,
        asset_id: int,
        revision: int,
    ) -> None:
        self.repository.require(
            asset_id=asset_id,
            revision=revision,
        )