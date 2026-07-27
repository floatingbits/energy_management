from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ForecastRun(Base):

    __tablename__ = "forecast_runs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    horizon_start: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    horizon_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    resolution_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    model_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    asset_forecasts = relationship(
        "AssetForecast",
        back_populates="forecast_run",
        cascade="all, delete-orphan"
    )

    portfolio_forecasts = relationship(
        "PortfolioForecast",
        back_populates="forecast_run",
        cascade="all, delete-orphan"
    )

    status: Mapped[str]