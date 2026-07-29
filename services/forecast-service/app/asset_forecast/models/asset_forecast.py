from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String
)

from app.database import Base
from sqlalchemy.orm import relationship

class AssetForecast(Base):

    __tablename__ = "asset_forecasts"


    id = Column(
        Integer,
        primary_key=True
    )


    forecast_run_id = Column(
        Integer,
        ForeignKey(
            "forecast_runs.id"
        ),
        nullable=False
    )


    asset_id = Column(
        Integer,
        nullable=False
    )


    model = Column(
        String,
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    forecast_run = relationship(
        "ForecastRun"
    )
