from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base


class TimeSeriesValue(Base):

    __tablename__ = "time_series_values"


    id = Column(
        Integer,
        primary_key=True
    )


    time_series_id = Column(
        Integer,
        ForeignKey(
            "time_series.id"
        ),
        nullable=False
    )


    slot_index = Column(
        Integer,
        nullable=False
    )


    payload = Column(
        String,
        nullable=False
    )


    value_type = Column(
        String,
        nullable=False,
        default="forecast"
    )

    time_series = relationship(
        "TimeSeries",
        back_populates="values"
    )
