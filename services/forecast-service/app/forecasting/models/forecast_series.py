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

    forecast_run_id = Column(
        Integer,
        ForeignKey(
            "forecast_runs.id"
        ),
        nullable=False
    )

    forecast_run = relationship(
        "ForecastRun",
        back_populates="series"
    )