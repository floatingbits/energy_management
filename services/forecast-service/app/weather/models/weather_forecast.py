from datetime import datetime,timezone

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Float
)

from app.database import Base
from sqlalchemy.orm import relationship

from app.forecasting.models import Forecast
class WeatherForecast(Base):

    __tablename__ = "weather_forecasts"


    id = Column(
        Integer,
        primary_key=True
    )


    forecast_id = Column(
        Integer,
        ForeignKey(
            "forecasts.id"
        ),
        nullable=False
    )


    source_id = Column(
        Integer,
        ForeignKey(
            "weather_sources.id"
        ),
        nullable=False
    )


    latitude = Column(
        Float,
        nullable=False
    )


    longitude = Column(
        Float,
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    forecast = relationship(
        "Forecast"
    )

    source = relationship(
        "WeatherSource"
    )