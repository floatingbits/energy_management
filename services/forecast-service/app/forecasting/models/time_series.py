from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship


from app.database import Base
from app.forecasting.encoding.definitions import DEFAULT_QUANTILE_DEFINITION


class TimeSeries(Base):

    __tablename__ = "time_series"


    id = Column(
        Integer,
        primary_key=True
    )


    metric = Column(
        String,
        nullable=False
    )

    value_type_definition = Column(
        String,
        nullable=False,
        default=DEFAULT_QUANTILE_DEFINITION.serialize,
    )

    time_series_group_id = Column(
        Integer,
        ForeignKey(
            "time_series_groups.id"
        ),
        nullable=False
    )

    time_series_group = relationship(
        "TimeSeriesGroup",
        back_populates="time_series"
    )
    values = relationship(
        "TimeSeriesValue",
        back_populates="time_series",
        cascade="all, delete-orphan"
    )
