from app.database import SessionLocal
from app.repositories.asset_forecast_requirement_repository import AssetForecastRequirementRepository
from app.repositories.asset_forecast_repository import AssetForecastRepository
from app.services.asset_forecast_requirement_service import AssetForecastRequirementService


def create_asset_forecast_requirement_service():
    db_session = SessionLocal()
    requirements_repository = AssetForecastRequirementRepository(db_session)
    forecast_repository =  AssetForecastRepository(db_session)
    return AssetForecastRequirementService(requirements_repository,forecast_repository)