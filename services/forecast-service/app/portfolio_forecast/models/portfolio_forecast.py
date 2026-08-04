from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String
)

from app.database import Base
from sqlalchemy.orm import relationship

class PortfolioForecast(Base):

    __tablename__ = "portfolio_forecasts"


    id = Column(
        Integer,
        primary_key=True
    )


    forecast_id = Column(
        Integer,
        ForeignKey(
            "forecast_runs.id"
        ),
        nullable=False
    )


    portfolio_id = Column(
        Integer,
        nullable=False
    )


    aggregation_model = Column(
        String,
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    forecast = relationship(
        "Forecast"
    )