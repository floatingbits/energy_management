from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base


class ForecastValue(Base):

    __tablename__ = "forecast_values"


    id = Column(
        Integer,
        primary_key=True
    )


    series_id = Column(
        Integer,
        ForeignKey(
            "forecast_series.id"
        ),
        nullable=False
    )


    slot_index = Column(
        Integer,
        nullable=False
    )


    p05 = Column(
        Float,
        nullable=True
    )


    p50 = Column(
        Float,
        nullable=False
    )


    p95 = Column(
        Float,
        nullable=True
    )


    value_type = Column(
        String,
        nullable=False,
        default="forecast"
    )