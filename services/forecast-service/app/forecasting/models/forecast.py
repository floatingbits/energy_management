from datetime import timezone, datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base


class Forecast(Base):

    __tablename__ = "forecasts"


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

    series = relationship(
        "ForecastSeries",
        back_populates="forecast",
        cascade="all, delete-orphan"
    )

    forecast_run = relationship(
        "ForecastRun"
    )