from sqlalchemy import select
from sqlalchemy.orm import Session

from app.asset_forecast.models.asset_forecast_requirement import (
    AssetForecastRequirement,
)


class AssetForecastRequirementRepository:

    def __init__(self, db):
        self.db = db

    def require(
        self,
        asset_id: int,
        revision: int,
    ) -> None:
        requirement = self.db.get(
            AssetForecastRequirement,
            asset_id,
        )

        if requirement is None:
            requirement = AssetForecastRequirement(
                asset_id=asset_id,
                required_revision=revision,
            )
            self.db.add(requirement)

        else:
            requirement.required_revision = max(
                requirement.required_revision,
                revision,
            )

        self.db.commit()

    def get_all(self):
        return self.db.query(
            AssetForecastRequirement
        ).all()