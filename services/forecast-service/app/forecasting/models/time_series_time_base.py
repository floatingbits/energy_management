from datetime import timezone, datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime
)
from sqlalchemy.orm import relationship

from app.database import Base


class TimeSeriesTimeBase(Base):

    __tablename__ = "time_series_time_bases"


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
