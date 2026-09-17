from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.forecasting.encoding import parse_quantiles


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

    @property
    def p05(self):
        return parse_quantiles(self.payload)[0]

    @property
    def p50(self):
        return parse_quantiles(self.payload)[1]

    @property
    def p95(self):
        return parse_quantiles(self.payload)[2]
