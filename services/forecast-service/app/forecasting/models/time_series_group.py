from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base


class TimeSeriesGroup(Base):

    __tablename__ = "time_series_groups"


    id = Column(
        Integer,
        primary_key=True
    )

    time_series_time_base_id = Column(
        Integer,
        ForeignKey(
            "time_series_time_bases.id"
        ),
        nullable=False
    )

    time_series = relationship(
        "TimeSeries",
        back_populates="time_series_group",
        cascade="all, delete-orphan"
    )

    time_series_time_base = relationship(
        "TimeSeriesTimeBase"
    )
