from app.database import SessionLocal
from app.repositories.asset_forecast_requirement_repository import AssetForecastRequirementRepository
from app.services.asset_forecast_requirement_service import AssetForecastRequirementService


def create_asset_forecast_requirement_service():
    db_session = SessionLocal()
    return AssetForecastRequirementService(AssetForecastRequirementRepository(db_session))