from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship


from app.database import Base


class ForecastSeries(Base):

    __tablename__ = "forecast_series"


    id = Column(
        Integer,
        primary_key=True
    )


    metric = Column(
        String,
        nullable=False
    )

    forecast_id = Column(
        Integer,
        ForeignKey(
            "forecasts.id"
        ),
        nullable=False
    )

    forecast = relationship(
        "Forecast",
        back_populates="series"
    )
    values = relationship(
        "ForecastValue",
        back_populates="series",
        cascade="all, delete-orphan"
    )