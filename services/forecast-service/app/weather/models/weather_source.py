from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.database import Base


class WeatherSource(Base):

    __tablename__ = "weather_sources"


    id = Column(
        Integer,
        primary_key=True
    )


    provider = Column(
        String,
        nullable=False
    )


    model = Column(
        String,
        nullable=False
    )


    version = Column(
        String,
        nullable=True
    )