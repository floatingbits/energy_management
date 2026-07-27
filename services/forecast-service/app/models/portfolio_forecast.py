from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PortfolioForecast(Base):

    __tablename__ = "portfolio_forecasts"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    forecast_run_id: Mapped[int] = mapped_column(
        ForeignKey("forecast_runs.id"),
        nullable=False
    )

    portfolio_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    period_start: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    period_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    prediction_p05: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    prediction_p50: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    prediction_p95: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    forecast_run = relationship(
        "ForecastRun",
        back_populates="portfolio_forecasts"
    )