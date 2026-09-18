from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class EnergyMarketObservation(Base):

    __tablename__ = "energy_market_observations"

    id = Column(
        Integer,
        primary_key=True,
    )

    time_series_group_id = Column(
        Integer,
        ForeignKey(
            "time_series_groups.id"
        ),
        nullable=False,
    )

    location_key = Column(
        String,
        nullable=False,
    )

    source = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    observation = relationship(
        "TimeSeriesGroup"
    )
