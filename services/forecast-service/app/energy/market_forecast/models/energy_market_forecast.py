from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime,
    JSON,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class EnergyMarketForecast(Base):

    __tablename__ = "energy_market_forecasts"

    id = Column(
        Integer,
        primary_key=True,
    )

    time_series_group_id = Column(
        Integer,
        ForeignKey(
            "time_series_groups.id"
        ),
        nullable=False,
    )

    market = Column(
        String,
        nullable=False,
    )

    variable = Column(
        String,
        nullable=False,
    )

    source = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    forecast = relationship(
        "TimeSeriesGroup"
    )

    # Input runs the model consumed: at series level, because the
    # basis is inherently per variable. The referenced series knows
    # its group (time base and siblings), so values and grid are
    # reachable from here. Heterogeneous context that a series alone
    # cannot express goes into the metadata JSON.
    basis = relationship(
        "EnergyMarketForecastBasis",
        order_by="EnergyMarketForecastBasis.id",
        cascade="save-update, merge",
    )


class EnergyMarketForecastBasis(Base):

    __tablename__ = "energy_market_forecast_bases"

    id = Column(
        Integer,
        primary_key=True,
    )

    energy_market_forecast_id = Column(
        Integer,
        ForeignKey(
            "energy_market_forecasts.id"
        ),
        nullable=False,
    )

    time_series_id = Column(
        Integer,
        ForeignKey(
            "time_series.id"
        ),
        nullable=False,
    )

    role = Column(
        String,
        nullable=False,
    )

    series_name = Column(
        String,
        nullable=False,
    )

    metadata_ = Column(
        "metadata",
        JSON,
        nullable=True,
    )

    series = relationship(
        "TimeSeries"
    )
