from datetime import timezone, datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime
)
from sqlalchemy.orm import relationship

from app.database import Base


class ForecastRun(Base):

    __tablename__ = "forecast_runs"


    id = Column(
        Integer,
        primary_key=True
    )


    start = Column(
        DateTime(timezone=True),
        nullable=False
    )


    resolution_seconds = Column(
        Integer,
        nullable=False
    )


    slots = Column(
        Integer,
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    series = relationship(
        "ForecastSeries",
        back_populates="forecast_run",
        cascade="all, delete-orphan"
    )