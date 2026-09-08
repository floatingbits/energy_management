from datetime import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PortfolioForecastRequirement(Base):
    __tablename__ = "portfolio_forecast_requirements"

    portfolio_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    required_revision: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )